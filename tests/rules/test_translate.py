"""Translation step with a fake LLM: no API calls (rules/translate.py)."""

import asyncio
import json
import re

from rules.translate import errors, load, translate_all, translate_rule

GOOD = {"status": "ok", "reason": "x", "left_out": "",
        "clauses": [{"type": "never", "where": {"cmd": ["force_push"]}}]}
BAD_NAME = {"status": "ok", "reason": "x", "left_out": "",
            "clauses": [{"type": "never", "where": {"cmd": ["erase"]}}]}
BAD_VOCAB = {"status": "ok", "reason": "x", "left_out": "",  # passes the schema, not the vocabulary
             "clauses": [{"type": "never", "where": {"cmd": ["delete"], "path_except": ["a/"]}}]}


class FakeLLM:
    def __init__(self, answers):
        self.answers, self.calls = list(answers), []

    async def chat_json(self, messages, temperature=0.0, run=0, tool=None):
        self.calls.append({"messages": messages, "temperature": temperature, "run": run,
                           "tool": tool})
        return self.answers.pop(0)


def run(llm, rule="Never force push.", file="git.md", **kw):
    prompt, validator = load()
    return asyncio.run(translate_rule(llm, prompt, validator, file, rule, **{"use_tool": False, **kw}))


def test_every_example_in_the_prompt_fits_the_format():
    prompt, validator = load()
    examples = [json.loads(line) for line in prompt.splitlines() if line.startswith('{"status"')]
    assert len(examples) == 3
    assert all(errors(x, validator) == [] for x in examples)


def test_good_answer_is_kept():
    llm = FakeLLM([GOOD])
    assert run(llm) == GOOD and len(llm.calls) == 1


def test_bad_answer_is_sent_back_once_with_the_error():
    llm = FakeLLM([BAD_NAME, GOOD])
    out = run(llm)
    assert out["status"] == "ok" and out["retried"]
    feedback = llm.calls[1]["messages"][-1]["content"]
    assert "erase" in feedback


def test_two_bad_answers_give_invalid_output():
    llm = FakeLLM([BAD_NAME, BAD_VOCAB])
    out = run(llm)
    assert out["status"] == "invalid_output" and "path_except without path" in out["errors"][0]


def test_vocabulary_errors_beyond_the_schema_are_caught():
    _, validator = load()
    assert errors(BAD_VOCAB, validator) == ["path_except without path"]


def test_the_llm_sees_only_the_rule_and_its_file():
    llm = FakeLLM([GOOD])
    run(llm, rule="Never force push.", file="git.md")
    user = llm.calls[0]["messages"][1]["content"]
    assert user == "FILE: git.md RULE: Never force push."
    assert len(llm.calls[0]["messages"]) == 2


def test_three_runs_are_separate_calls_with_default_sampling():
    llm = FakeLLM([GOOD] * 6)
    rules = [{"folder": "f", "id": "R1", "file": "a.md", "rule": "Never force push."},
             {"folder": "f", "id": "R2", "file": "b.md", "rule": "Never rebase."}]
    out = asyncio.run(translate_all(llm, rules, runs=3, use_tool=False))
    assert [len(r["runs"]) for r in out] == [3, 3]
    assert sorted(c["run"] for c in llm.calls) == [1, 1, 2, 2, 3, 3]
    assert all(c["temperature"] is None for c in llm.calls)
    assert re.search("R2", json.dumps(out))


def test_a_rule_repeated_across_folders_is_translated_once_per_run():
    llm = FakeLLM([GOOD] * 2)
    rules = [{"folder": f, "id": "R1", "file": "a.md", "rule": "Never force push."}
             for f in ("copy1", "copy2", "copy3")]
    out = asyncio.run(translate_all(llm, rules, runs=2, use_tool=False))
    assert len(llm.calls) == 2 and all(len(r["runs"]) == 2 for r in out)


def test_tool_mode_sends_the_template_and_converts_the_answer():
    from test_template import blank
    args = {"status": "ok", "word": "", "reason": "", "left_out": "",
            "clauses": [{"type": "never", "where": {**blank(), "cmd": ["force_push"]},
                         "needs": blank(), "when_unmodeled": ""}]}
    llm = FakeLLM([args])
    out = run(llm, use_tool=True)
    assert llm.calls[0]["tool"]["function"]["name"] == "record_translation"
    assert out["clauses"] == [{"type": "never", "where": {"cmd": ["force_push"]}}]
    assert out["template_errors"] == []
