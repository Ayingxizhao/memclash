"""The strict template tool (rules/template.py)."""

from rules.template import TASK_PATTERN, to_translation, tool
from rules.translate import errors, load
import re


def blank():
    f = tool()["function"]["parameters"]["properties"]["clauses"]["items"]["properties"]["where"]
    out = {}
    for k, s in f["properties"].items():
        out[k] = {"array": [], "integer": -1}.get(s["type"], "unstated" if "unstated" in s.get("enum", []) else "")
    return out


def walk(schema):
    yield schema
    for v in schema.get("properties", {}).values():
        yield from walk(v)
    if "items" in schema:
        yield from walk(schema["items"])


def test_tool_fits_strict_mode_rules():
    t = tool()["function"]
    assert t["strict"] is True
    for s in walk(t["parameters"]):
        if s.get("type") == "object":  # strict: every field required, nothing extra
            assert set(s["required"]) == set(s["properties"]) and s["additionalProperties"] is False
        for banned in ("minItems", "maxItems", "minLength", "maxLength", "oneOf", "if", "allOf"):
            assert banned not in s


def test_blank_fields_are_removed():
    where = {**blank(), "cmd": ["push"], "branch": "main"}
    needs = {**blank(), "user_confirmed": "true", "tests_passed": "true"}
    args = {"status": "ok", "word": "", "reason": "r", "left_out": "",
            "clauses": [{"type": "only_if", "where": where, "needs": needs, "when_unmodeled": ""}]}
    t = to_translation(args)
    assert t["clauses"] == [{"type": "only_if", "where": {"cmd": ["push"], "branch": "main"},
                             "needs": {"user_confirmed": True, "tests_passed": True}}]
    assert errors(t, load()[1]) == []


def test_not_in_scope_and_unclear():
    base = {"word": "", "reason": "r", "left_out": "", "clauses": []}
    assert to_translation({**base, "status": "not_in_scope"}) == {"status": "not_in_scope", "reason": "r"}
    assert to_translation({**base, "status": "unclear", "word": "add"}) == \
        {"status": "unclear", "word": "add", "reason": "r"}


def test_needs_on_a_never_clause_is_kept_so_the_check_rejects_it():
    args = {"status": "ok", "word": "", "reason": "", "left_out": "",
            "clauses": [{"type": "never", "where": {**blank(), "cmd": ["push"]},
                         "needs": {**blank(), "user_asked": "true"}, "when_unmodeled": ""}]}
    assert errors(to_translation(args), load()[1]) != []


def test_task_pattern():
    assert re.fullmatch(TASK_PATTERN, "") and re.fullmatch(TASK_PATTERN, "deploy")
    assert re.fullmatch(TASK_PATTERN, "other:seed db") and not re.fullmatch(TASK_PATTERN, "pytest")


def test_retry_message_names_the_real_problem():
    bad = {"status": "ok", "reason": "", "left_out": "", "clauses": [{"type": "never", "cmd": ["push"]}]}
    msg = " ".join(errors(bad, load()[1]))
    assert "where" in msg and "any of the given schemas" not in msg


def test_real_true_false_and_missing_fields_are_read_as_meant():
    # seen in the pilot: the server let these through
    args = {"status": "ok", "reason": "", "left_out": "", "word": "",
            "clauses": [{"type": "only_if", "where": {"cmd": ["push"]},
                         "needs": {"user_confirmed": True, "files_shown": False},
                         "when_unmodeled": ""}]}
    t = to_translation(args)
    assert t["clauses"][0]["needs"] == {"user_confirmed": True, "files_shown": False}
    assert errors(t, load()[1]) == []
    from rules.template import template_errors
    assert template_errors(args)  # still reported as off-template
