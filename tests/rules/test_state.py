"""Repository state: must / must not be in the repo (rules/state.py, through pair.check_pair)."""

import pytest

from rules.pair import check_pair


def ok(*clauses):
    return {"status": "ok", "reason": "", "clauses": list(clauses), "left_out": ""}


def must_hold(paths, except_=(), **extra):
    w = {"in_repo": paths, **({"path_except": list(except_)} if except_ else {})}
    return {"type": "must_hold", "where": w, **extra}


def never_hold(paths, except_=(), **extra):
    w = {"in_repo": paths, **({"path_except": list(except_)} if except_ else {})}
    return {"type": "never_hold", "where": w, **extra}


CASES = {
    "vendor/cmake stays committed vs keep vendor/ out of the repo":
        (ok(must_hold(["vendor/cmake/"])), ok(never_hold(["vendor/"])), "state_conflict"),
    "the exception is written in the same rule as path_except":
        (ok(must_hold(["vendor/cmake/"])), ok(never_hold(["vendor/"], ["vendor/cmake/"])),
         "compatible"),
    "different folders":
        (ok(must_hold(["docs/"])), ok(never_hold(["dist/"])), "compatible"),
    "bare name matches at any depth":
        (ok(must_hold(["config/.env.example"])), ok(never_hold([".env*"])), "state_conflict"),
    "never_hold under an unknown condition cannot conflict":
        (ok(must_hold(["build/"])), ok(never_hold(["build/"], when_unmodeled="on release branches")),
         "compatible"),
    "one rule demanding opposite states for the same path":
        (ok(must_hold(["a/"]), never_hold(["a/x"])), ok(never_hold(["b/"])), "invalid"),
    "one rule with its own exception is fine":
        (ok(never_hold(["third_party/"], ["third_party/patches/"]), must_hold(["third_party/patches/"])),
         ok(never_hold(["dist/"])), "compatible"),
    "an action clash is reported before a state conflict":
        (ok(must_hold(["vendor/cmake/"]), {"type": "must_do", "where": {"cmd": ["force_push"]}}),
         ok(never_hold(["vendor/"]), {"type": "never", "where": {"cmd": ["force_push"]}}), "clash"),
    "unknown field in a state clause":
        (ok({"type": "must_hold", "where": {"in_repo": ["a/"], "cmd": ["commit"]}}),
         ok(never_hold(["b/"])), "invalid"),
}


@pytest.mark.parametrize("name", CASES)
def test_state(name):
    a, b, want = CASES[name]
    assert check_pair(a, b)[0] == want
    assert check_pair(b, a)[0] == want


def test_witness_path_is_in_both_targets():
    _, detail = check_pair(ok(must_hold(["vendor/cmake/"])), ok(never_hold(["vendor/"])))
    assert detail["path"].startswith("vendor/cmake")
