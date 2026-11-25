"""Groups of three rules that clash only together (rules/group.py), plus controls."""

import pytest

from rules.group import check_group, group_only


def ok(*clauses):
    return {"status": "ok", "reason": "", "clauses": list(clauses), "left_out": ""}


def never(**where):
    return {"type": "never", "where": where}


def must(**where):
    return {"type": "must_do", "where": where}


def may(**where):
    return {"type": "may_do", "where": where}


def only_if(where, needs):
    return {"type": "only_if", "where": where, "needs": needs}


PUSH_END = ok(must(cmd=["push_branch"]))
PUSH_AFTER_TESTS = ok(only_if({"cmd": ["push"]}, {"after": ["run"], "after_task": "test", "after_ok": True}))
NO_TESTS = ok(never(cmd=["run"], task="test"))

CASES = {
    # chain: the push needs a passing test run earlier, and running tests is forbidden
    "always push / push only after tests pass / never run tests":
        ([PUSH_END, PUSH_AFTER_TESTS, NO_TESTS], "group_clash"),
    # chain with a condition: when the user has not asked, tests may not run, so no push
    "always push / push only after tests pass / run tests only when asked":
        ([PUSH_END, PUSH_AFTER_TESTS, ok(only_if({"cmd": ["run"], "task": "test"}, {"user_asked": True}))],
         "group_clash"),
    # a permission blocked by two rules together
    "may push / push only after tests pass / never run tests":
        ([ok(may(cmd=["push_branch"])), PUSH_AFTER_TESTS, NO_TESTS], "group_exception"),

    # --- controls ---
    "always push / push only after tests pass / tests allowed":
        ([PUSH_END, PUSH_AFTER_TESTS, ok(never(cmd=["run"], task="deploy"))], "compatible"),
    "a pair already clashes inside the group":
        ([ok(must(cmd=["force_push"])), ok(never(cmd=["force_push"])), NO_TESTS], "pair_clash"),
    "never push main / never push others / no obligation to push":
        ([ok(never(cmd=["push_branch"], branch="main")), ok(never(cmd=["push_branch"], branch="!main")),
          NO_TESTS], "compatible"),
}


@pytest.mark.parametrize("name", CASES)
def test_group(name):
    rules, want = CASES[name]
    assert group_only(rules)[0] == want


def test_chain_is_invisible_to_pairs():
    # each pair of the chain is fine on its own
    assert check_group([PUSH_END, PUSH_AFTER_TESTS])[0] == "compatible"
    assert check_group([PUSH_END, NO_TESTS])[0] == "compatible"
    assert check_group([PUSH_AFTER_TESTS, NO_TESTS])[0] == "compatible"


def test_skips_unclear():
    assert check_group([PUSH_END, {"status": "unclear"}, NO_TESTS])[0] == "skipped"


def test_scan_keeps_only_if_rules():
    # regression: rules with only only_if clauses take part in group clashes (chain links)
    from rules.group import relevant
    assert relevant(PUSH_AFTER_TESTS)
