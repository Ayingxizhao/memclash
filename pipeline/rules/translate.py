"""Translate rules with the LLM (prompts/rules/translate.md), one rule at a time.

The LLM sees only the rule and the name of its file, never the folder's other rules
(ADR 0008), so other rules cannot change how a rule is read. Every answer is checked against
prompts/rules/translate.schema.json and against the vocabulary (an unknown name, or
path_except without path, is an error). A bad answer is sent back once with the error; if the
second answer is also bad, the rule is marked `invalid_output` and counted, never guessed.

Repeated runs (to measure agreement) use the model's default sampling and a run label, so
each run is a separate call.
"""

import asyncio
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from rules.model import Event, action_clauses
from rules.state import state_clauses, target
from rules.coverage import apply_scopes, coverage_errors, step1_errors, uncovered_words
from rules.template import (requirements_tool, template_errors, to_translation, to_translation_step2,
                            tool, tool_step2)

ROOT = Path(__file__).resolve().parents[2]
PROMPT = ROOT / "prompts" / "rules" / "translate.md"
PROMPT_REQ = ROOT / "prompts" / "rules" / "requirements.md"
PROMPT_STEP2 = ROOT / "prompts" / "rules" / "translate_step2.md"
SCHEMA = ROOT / "prompts" / "rules" / "translate.schema.json"
STATUS_BRANCH = {"not_in_scope": 0, "unclear": 1, "ok": 2}  # order of oneOf in the schema


def load():
    return PROMPT.read_text(), Draft202012Validator(json.loads(SCHEMA.read_text()))


def errors(answer, validator):
    """Why an answer does not fit the format and the vocabulary ([] if it fits)."""
    errs = []
    for e in validator.iter_errors(answer):
        # "not valid under any of the given schemas" says nothing: report the errors of the
        # branch that matches the answer's status instead
        if e.validator == "oneOf" and e.context:
            branch = [x for x in e.context if x.relative_schema_path[0] == STATUS_BRANCH.get(
                answer.get("status") if isinstance(answer, dict) else None, -1)]
            errs += [f"{'/'.join(map(str, x.absolute_path)) or 'answer'}: {x.message}"
                     for x in branch if x.validator != "const"] or [e.message]
        else:
            errs.append(f"{'/'.join(map(str, e.path)) or 'answer'}: {e.message}")
    if errs or answer.get("status") != "ok":
        return errs
    try:
        for c in action_clauses(answer["clauses"]):
            Event("v").match(c["where"])
            Event("v").match(c.get("needs", {}))
        for c in state_clauses(answer["clauses"]):
            target(c)
    except ValueError as err:
        errs.append(str(err))
    return errs


def user_message(file, rule):
    return f"FILE: {file} RULE: {rule}"


async def ask(llm, messages, temperature, run, use_tool):
    """(answer in the normal format, how far the raw answer was from the template). With
    use_tool, the model fills the template tool and the blanks are removed; a value that
    cannot be read becomes an error the retry reports."""
    if not use_tool:
        return await llm.chat_json(messages, temperature=temperature, run=run), []
    raw = await llm.chat_json(messages, temperature=temperature, run=run, tool=tool())
    try:
        return to_translation(raw), template_errors(raw)
    except (ValueError, TypeError, AttributeError) as err:
        return {"status": "unreadable", "error": str(err)}, template_errors(raw)


async def translate_rule(llm, prompt, validator, file, rule, run=0, temperature=None,
                         use_tool=True):
    messages = [{"role": "system", "content": prompt},
                {"role": "user", "content": user_message(file, rule)}]
    answer, off = await ask(llm, messages, temperature, run, use_tool)
    errs = errors(answer, validator)
    if not errs:
        return {**answer, "template_errors": off} if use_tool else answer
    retry = messages + [{"role": "assistant", "content": json.dumps(answer)},
                        {"role": "user", "content": "Your answer does not fit the format: "
                         + "; ".join(errs[:5]) + ". Answer again, corrected."}]
    second, off2 = await ask(llm, retry, temperature, run, use_tool)
    errs2 = errors(second, validator)
    if not errs2:
        return {**second, "retried": True, **({"template_errors": off2} if use_tool else {})}
    return {"status": "invalid_output", "errors": errs2, "answer": second}


async def ask_tool(llm, messages, temperature, run, t):
    """Raw tool arguments, or {} if the answer could not be read."""
    try:
        return await llm.chat_json(messages, temperature=temperature, run=run, tool=t)
    except (ValueError, TypeError, KeyError) as err:
        return {"_error": str(err)}


def feedback(messages, answer, errs):
    return messages + [{"role": "assistant", "content": json.dumps(answer)},
                       {"role": "user", "content": "Your answer does not fit: " + "; ".join(errs[:6])
                        + ". Answer again, corrected."}]


async def translate_rule_two_step(llm, validator, file, rule, run=0, temperature=None):
    """Step 1 lists the requirements (exact quotes); step 2 translates each; code refuses an
    answer that drops a requirement silently. Each step may be retried once with the exact
    error; a second failure gives `invalid_output` (with the step)."""
    user = user_message(file, rule)
    m1 = [{"role": "system", "content": PROMPT_REQ.read_text()}, {"role": "user", "content": user}]
    s1 = await ask_tool(llm, m1, temperature, run, requirements_tool())
    e1 = step1_errors(rule, s1)
    retried = []
    if e1:
        retried.append("step1")
        s1 = await ask_tool(llm, feedback(m1, s1, e1), temperature, run, requirements_tool())
        e1 = step1_errors(rule, s1)
        if e1:
            return {"status": "invalid_output", "step": 1, "errors": e1, "answer": s1}
    reqs = s1["requirements"]
    extra = {"requirements": reqs, "uncovered_words": uncovered_words(rule, s1), "retried_steps": retried}
    if s1["status"] == "not_in_scope":
        return {"status": "not_in_scope", "reason": s1.get("reason", ""), **extra}
    m2 = [{"role": "system", "content": PROMPT.read_text() + "\n\n" + PROMPT_STEP2.read_text()},
          {"role": "user", "content": user + "\nREQUIREMENTS: " + json.dumps(reqs, ensure_ascii=False)}]

    async def step2(messages):
        raw = await ask_tool(llm, messages, temperature, run, tool_step2())
        try:
            t, trace = to_translation_step2(raw)
        except (ValueError, TypeError, AttributeError) as err:
            return raw, None, None, [f"could not read the answer: {err}"]
        return raw, t, trace, errors(t, validator) + coverage_errors(s1, trace)

    raw, t, trace, e2 = await step2(m2)
    if e2:
        retried.append("step2")
        raw, t, trace, e2 = await step2(feedback(m2, raw, e2))
        if e2:
            return {"status": "invalid_output", "step": 2, "errors": e2, "answer": raw, **extra}
    if t.get("status") == "ok":
        t = apply_scopes(t, s1, trace)
    return {**t, **extra, "trace": trace, "template_errors": template_errors_step2(raw)}


def template_errors_step2(raw):
    from jsonschema import Draft202012Validator
    v = Draft202012Validator(tool_step2()["function"]["parameters"])
    return sorted({e.message for e in v.iter_errors(raw)})


async def translate_all(llm, rules, runs=3, temperature=None, use_tool=True, mode="one_step"):
    """rules: [{"folder", "id", "file", "rule"}]. Returns the same records with
    `runs`: one translation per run. A rule that appears in several folders with the same
    file name and text is translated once per run and shared."""
    prompt, validator = load()
    keys = sorted({(r.get("file", ""), r["rule"]) for r in rules})
    jobs = [(k, run) for k in keys for run in range(1, runs + 1)]
    if mode == "two_step":
        coros = (translate_rule_two_step(llm, validator, f, rule, run=run, temperature=temperature)
                 for (f, rule), run in jobs)
    else:
        coros = (translate_rule(llm, prompt, validator, f, rule, run=run, temperature=temperature,
                                use_tool=use_tool) for (f, rule), run in jobs)
    done = await asyncio.gather(*coros)
    got = dict(zip(jobs, done))
    return [{**r, "runs": [got[((r.get("file", ""), r["rule"]), k)] for k in range(1, runs + 1)]}
            for r in rules]
