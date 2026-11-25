"""The translation template: a tool `record_translation` whose inputs are a fixed form. The LLM
answers by calling the tool, with DeepSeek's strict mode (beta) switched on, which is meant
to reject any answer that does not fit the form (but see the pilot note below).

Strict mode needs every field present (no optional fields) and supports no "at least one
item" or "if ... then" rules. So every field is always filled, with a blank meaning "the rule
does not say": [] for lists, "" for text, "unstated" for yes/no, -1 for numbers.
`to_translation` removes the blanks and returns the normal format
(prompts/rules/translate.schema.json), which is then checked as before (translate.errors).

Found in the pilot: the server does NOT fully enforce the template (10 of 34 answers left
fields out or wrote yes/no as true/false instead of "true"/"false"). Both have one possible
meaning, so a missing field counts as blank and a real true/false is accepted;
`template_errors` reports how far an answer was from the template, so this can be counted.
"""

from jsonschema import Draft202012Validator

from rules.vocab import BOOLS, CMDS, GROUPS, TASKS

TOOL_NAME = "record_translation"
ACTIONS = CMDS + list(GROUPS)
TYPES = ["never", "only_if", "must_do", "may_do", "must_hold", "never_hold"]
LISTS = ["path", "dest_path", "path_except", "in_repo", "running", "after_path"]
TEXTS = ["branch", "after_branch"]
NUMBERS = ["min_files", "max_files"]
TASK_PATTERN = "^$|^(" + "|".join(TASKS) + ")$|^other:.+$"


def obj(props):
    return {"type": "object", "properties": props, "required": list(props),
            "additionalProperties": False}


def facts_schema():
    p = {"cmd": {"type": "array", "items": {"type": "string", "enum": ACTIONS}},
         "after": {"type": "array", "items": {"type": "string", "enum": ACTIONS}}}
    p.update({k: {"type": "array", "items": {"type": "string"}} for k in LISTS})
    p.update({k: {"type": "string"} for k in TEXTS})
    p["kind"] = {"type": "string", "enum": ["", "file", "dir"]}
    p["task"] = {"type": "string", "pattern": TASK_PATTERN}
    p["after_task"] = {"type": "string", "pattern": TASK_PATTERN}
    p["after_ok"] = {"type": "string", "enum": ["unstated", "true", "false"]}
    p["suite"] = {"type": "string", "enum": ["", "all"]}
    p.update({k: {"type": "string", "enum": ["unstated", "true", "false"]} for k in BOOLS})
    p.update({k: {"type": "integer", "minimum": -1} for k in NUMBERS})
    return obj(p)


def tool():
    clause = obj({"type": {"type": "string", "enum": TYPES},
                  "where": facts_schema(), "needs": facts_schema(),
                  "when_unmodeled": {"type": "string"}})
    params = obj({"status": {"type": "string", "enum": ["ok", "not_in_scope", "unclear"]},
                  "word": {"type": "string"},
                  "reason": {"type": "string"},
                  "clauses": {"type": "array", "items": clause},
                  "left_out": {"type": "string"}})
    return {"type": "function", "function": {
        "name": TOOL_NAME, "strict": True, "parameters": params,
        "description": "Record the translation of one rule. Fill every field; leave a field "
                       "blank ([] / \"\" / \"unstated\" / -1) when the rule does not state it."}}


def filled(facts):
    """Only the fields the LLM filled in, in the normal format."""
    out = {}
    for k, v in facts.items():
        if k in BOOLS or k == "after_ok":
            if isinstance(v, bool):
                out[k] = v
            elif v in ("true", "false"):
                out[k] = v == "true"
            elif v != "unstated":
                raise ValueError(f"{k} must be true, false or unstated, not {v!r}")
        elif k in NUMBERS:
            if isinstance(v, int) and v >= 0:
                out[k] = v
        elif v not in ("", [], None):
            out[k] = v
    return out


def template_errors(args):
    """How the answer differs from the template (the server should have prevented these)."""
    v = Draft202012Validator(tool()["function"]["parameters"])
    return sorted({e.message for e in v.iter_errors(args)})


def to_translation(args):
    """A missing field counts as blank (see module note). Anything else wrong is left for
    translate.errors to reject."""
    status = args.get("status")
    reason = args.get("reason", "")
    if status == "not_in_scope":
        return {"status": status, "reason": reason}
    if status == "unclear":
        return {"status": status, "word": args.get("word", ""), "reason": reason}
    clauses = []
    for c in args.get("clauses", []):
        n = {"type": c.get("type"), "where": filled(c.get("where", {}))}
        needs = filled(c.get("needs", {}))
        if c.get("type") == "only_if" or needs:  # needs on another type is an error, caught later
            n["needs"] = needs
        if c.get("when_unmodeled"):
            n["when_unmodeled"] = c["when_unmodeled"]
        clauses.append(n)
    return {"status": status, "reason": reason, "clauses": clauses,
            "left_out": args.get("left_out", "")}


# ---------------------------------------------------------------- two-step mode (ADR 0008 plan)

REQ_TOOL = "list_requirements"
KEEP = ["translate", "vague", "outside_vocabulary"]
LEFT_OUT_REASONS = ["vague", "outside_vocabulary", "unclear_word"]


def requirements_tool():
    """Step 1: split the rule into requirements, each with an exact quote."""
    item = obj({"id": {"type": "string"}, "quote": {"type": "string"},
                "applies_when": {"type": "string"},
                "keep": {"type": "string", "enum": KEEP}, "why": {"type": "string"}})
    params = obj({"status": {"type": "string", "enum": ["ok", "not_in_scope"]},
                  "reason": {"type": "string"},
                  "requirements": {"type": "array", "items": item}})
    return {"type": "function", "function": {
        "name": REQ_TOOL, "strict": True, "parameters": params,
        "description": "Record the single requirements of one rule, each with an exact quote."}}


def tool_step2():
    """Step 2: the translation template, with `req` on each clause and `left_out` as a list."""
    t = tool()
    p = t["function"]["parameters"]
    clause = p["properties"]["clauses"]["items"]
    clause["properties"] = {"req": {"type": "string"}, "scope_encoded": {"type": "boolean"},
                            **clause["properties"]}
    clause["required"] = list(clause["properties"])
    p["properties"]["left_out"] = {"type": "array", "items": obj({
        "req": {"type": "string"}, "reason": {"type": "string", "enum": LEFT_OUT_REASONS},
        "word": {"type": "string"}})}
    return t


def to_translation_step2(args):
    """(translation in the normal format, trace). The trace keeps which requirement each clause
    translates and why the others were left out; the coverage check reads it."""
    clauses_args = args.get("clauses", []) or []
    left = [x for x in (args.get("left_out", []) or []) if isinstance(x, dict)]
    trace = {"clause_req": [c.get("req", "") for c in clauses_args], "left_out": left,
             "scope_encoded": [c.get("scope_encoded") is True for c in clauses_args]}
    base = to_translation({**args, "status": "ok", "left_out": "", "clauses": clauses_args})
    clauses = base["clauses"]
    if clauses:
        status = "ok"
    elif any(x.get("reason") == "unclear_word" for x in left):
        status = "unclear"
    else:
        status = "not_in_scope"
    left_text = "; ".join(f"{x.get('req')}: {x.get('reason')}" + (f" ({x['word']})" if x.get("word") else "")
                          for x in left)
    reason = args.get("reason", "")
    if status == "ok":
        t = {"status": "ok", "reason": reason, "clauses": clauses, "left_out": left_text}
    elif status == "unclear":
        word = next(x.get("word", "") for x in left if x.get("reason") == "unclear_word")
        t = {"status": "unclear", "word": word or "?", "reason": reason or left_text}
    else:
        t = {"status": "not_in_scope", "reason": reason or ("nothing left: " + left_text)}
    return t, trace
