"""Two-step translation with a fake LLM, and voting (rules/translate.py, rules/agreement.py)."""

import asyncio

from rules.agreement import vote
from rules.translate import load, translate_rule_two_step
from test_template import blank
from test_translate import FakeLLM

RULE = "Before any commit, verify no .env files, API keys, or secrets are staged."
S1 = {"status": "ok", "reason": "", "requirements": [
    {"id": "q1", "quote": "Before any commit, verify", "keep": "translate", "why": ""},
    {"id": "q2", "quote": "no .env files, API keys, or secrets are staged", "keep": "translate", "why": ""}]}


def clause(req, type_, where, needs=None):
    return {"req": req, "type": type_, "where": {**blank(), **where},
            "needs": {**blank(), **(needs or {})}, "when_unmodeled": ""}


CHECK = clause("q1", "only_if", {"cmd": ["commit"]}, {"secrets_checked": "true"})
NO_SECRET = clause("q2", "never", {"cmd": ["commit"], "has_secret": "true"})


def step2(*clauses, left_out=()):
    return {"status": "ok", "word": "", "reason": "", "clauses": list(clauses), "left_out": list(left_out)}


def run(answers):
    llm = FakeLLM(answers)
    out = asyncio.run(translate_rule_two_step(llm, load()[1], "security.md", RULE, run=1))
    return out, llm


def test_both_requirements_translated():
    out, llm = run([S1, step2(CHECK, NO_SECRET)])
    assert out["status"] == "ok" and len(out["clauses"]) == 2 and len(llm.calls) == 2
    assert out["trace"]["clause_req"] == ["q1", "q2"]
    assert llm.calls[0]["tool"]["function"]["name"] == "list_requirements"
    assert "REQUIREMENTS" in llm.calls[1]["messages"][1]["content"]


def test_dropped_requirement_is_sent_back_and_fixed():
    out, llm = run([S1, step2(CHECK), step2(CHECK, NO_SECRET)])
    assert out["status"] == "ok" and out["retried_steps"] == ["step2"]
    assert "q2" in llm.calls[2]["messages"][-1]["content"]


def test_dropped_twice_gives_invalid_output():
    out, _ = run([S1, step2(CHECK), step2(CHECK)])
    assert out["status"] == "invalid_output" and out["step"] == 2


def test_step1_bad_quote_is_retried():
    bad = {**S1, "requirements": [{**S1["requirements"][0], "quote": "check first"}, S1["requirements"][1]]}
    out, llm = run([bad, S1, step2(CHECK, NO_SECRET)])
    assert out["status"] == "ok" and out["retried_steps"] == ["step1"]


def test_not_in_scope_skips_step2():
    s1 = {"status": "not_in_scope", "reason": "style", "requirements": [
        {"id": "q1", "quote": "Before any commit", "keep": "outside_vocabulary", "why": "x"}]}
    out, llm = run([s1])
    assert out["status"] == "not_in_scope" and len(llm.calls) == 1


def test_everything_left_out_as_unclear_gives_unclear():
    out, _ = run([S1, step2(left_out=[{"req": "q1", "reason": "unclear_word", "word": "verify"},
                                      {"req": "q2", "reason": "outside_vocabulary", "word": ""}])])
    assert out["status"] == "unclear" and out["word"] == "verify"


def test_vote():
    a = {"status": "ok", "reason": "", "left_out": "", "clauses": [{"type": "never", "where": {"cmd": ["push"]}}]}
    a2 = {"status": "ok", "reason": "", "left_out": "", "clauses": [{"type": "never", "where": {"cmd": ["push_branch", "push_delete", "force_push"]}}]}
    b = {"status": "ok", "reason": "", "left_out": "", "clauses": [{"type": "never", "where": {"cmd": ["commit"]}}]}
    c = {"status": "not_in_scope", "reason": ""}
    bad = {"status": "invalid_output", "errors": ["x"]}
    assert vote([a, b, a2]) == (a, [2, 1])
    assert vote([a, b, c])[0] is None
    assert vote([bad, bad, a]) == (None, [1])  # failed runs never form a majority
