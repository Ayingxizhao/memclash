"""Pairs of rules with known answers (rules/pair.py). Rules are written by hand in the
translation format; the first group are the user's example clashes from the survey."""

import pytest

from rules.pair import check_pair


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


CASES = {
    # --- the user's examples (ADR 0008 discussion, Codex round 5) ---
    "force push vs never force push":
        (ok(must(cmd=["force_push"])), ok(never(cmd=["force_push"])), "clash"),
    "may delete merged branches when asked vs never delete branches":
        (ok(may(cmd=["any_branch_delete"], after=["merge"], user_asked=True)),
         ok(never(cmd=["any_branch_delete"])), "exception"),
    "never push without an ask vs the final step pushes to main":  # missed by git_check.py
        (ok(only_if({"cmd": ["push"]}, {"user_asked": True})),
         ok(must(cmd=["push_branch"], branch="main")), "clash"),
    "delete map data (no path) vs never delete server-world.dat without permission":
        # not expressible: which files are map data is unknown, so the clash is missed
        (ok({"type": "must_do", "where": {"cmd": ["delete"]}, "when_unmodeled": "map or player data"}),
         ok(only_if({"cmd": ["delete"], "path": ["server-world.dat"]}, {"user_confirmed": True})),
         "compatible"),
    "create an object folder vs no subfolders in game/objects":
        (ok(must(cmd=["create"], path=["game/objects/*/"], kind="dir")),
         ok(never(cmd=["create"], path=["game/objects/**"], kind="dir")), "clash"),
    "never commit vendor/ (unclear) vs vendor/cmake stays committed":
        ({"status": "unclear", "word": "never commit", "reason": ""},
         ok({"type": "must_hold", "where": {"in_repo": ["vendor/cmake/"]}}), "skipped"),
    "run tests only when asked vs always run all tests after a commit":
        (ok(only_if({"cmd": ["run"], "task": "test"}, {"user_asked": True})),
         ok(must(cmd=["run"], task="test", suite="all", after=["commit"])), "clash"),

    # --- compatible pairs: nothing forces a clash ---
    "never force push vs must push main":
        (ok(never(cmd=["force_push"])), ok(must(cmd=["push_branch"], branch="main")), "compatible"),
    "push only with approval vs must push (agent can ask)":
        (ok(only_if({"cmd": ["push"]}, {"user_confirmed": True})), ok(must(cmd=["push_branch"])),
         "compatible"),
    "never delete a.txt vs must delete b.txt":
        (ok(never(cmd=["delete"], path=["a.txt"])), ok(must(cmd=["delete"], path=["b.txt"])),
         "compatible"),
    "never delete vs must move (move is not delete)":
        (ok(never(cmd=["delete"], path=["data/"])), ok(must(cmd=["move"], path=["data/x.db"])),
         "compatible"),
    "deploy only when asked vs must run tests (other task)":
        (ok(only_if({"cmd": ["run"], "task": "deploy"}, {"user_asked": True})),
         ok(must(cmd=["run"], task="test")), "compatible"),
    "never run tests vs push only after tests (agent can skip the push)":
        (ok(never(cmd=["run"], task="test")),
         ok(only_if({"cmd": ["push"]}, {"after": ["run"]})), "compatible"),
    "never delete while the server runs vs must delete":
        # the world decides whether the server runs; in the case it does, both cannot hold
        (ok(never(cmd=["delete"], path=["saves/"], running=["the game server"])),
         ok(must(cmd=["delete"], path=["saves/world.db"])), "clash"),
    "two never rules can always both be kept":
        (ok(never(cmd=["delete"], running=["game server"])),
         ok(never(cmd=["delete"], path=["x"])), "compatible"),

    "a step the agent can take first is not a clash":  # found by the old case L235/L237
        (ok(only_if({"cmd": ["branch_create"]}, {"after": ["checkout"]})),
         ok(must(cmd=["branch_create"], branch="feat/*")), "compatible"),
    "a rule that applies after an earlier action is tested in that case":
        (ok(never(cmd=["push"], after=["rebase"])), ok(must(cmd=["push_branch"])), "clash"),

    # --- conditions on both sides ---
    "commit only in a worktree vs commit only outside one":
        (ok(only_if({"cmd": ["commit"]}, {"in_worktree": True})),
         ok(only_if({"cmd": ["commit"]}, {"in_worktree": False})), "clash"),
    "may commit vs commit only after tests passed (world fact)":
        (ok(may(cmd=["commit"])), ok(only_if({"cmd": ["commit"]}, {"tests_passed": True})),
         "exception"),

    # --- broken or skipped input ---
    "a rule that contradicts itself":
        (ok(never(cmd=["push"]), must(cmd=["push_branch"])), ok(never(cmd=["fetch"])), "invalid"),
    "unknown action":
        (ok(never(cmd=["erase"])), ok(must(cmd=["push_branch"])), "invalid"),
    "not in scope":
        ({"status": "not_in_scope", "reason": "style"}, ok(must(cmd=["commit"])), "skipped"),
}


@pytest.mark.parametrize("name", CASES)
def test_pair(name):
    a, b, want = CASES[name]
    assert check_pair(a, b)[0] == want
    assert check_pair(b, a)[0] == want  # order of the two rules never matters


def unmod(type_, text, **where):
    return {"type": type_, "where": where, "when_unmodeled": text}


POSSIBLE = {
    "the real force-push pair: clashes only if both conditions hold":
        (ok(unmod("never", "to fix version state", cmd=["force_push"], branch="main")),
         ok(unmod("must_do", "the main branch has been reset", cmd=["force_push"], branch="main")),
         {"to fix version state", "the main branch has been reset"}),
    "a condition on the never side only":
        (ok(unmod("never", "during a hotfix", cmd=["push"])), ok(must(cmd=["push_branch"])),
         {"during a hotfix"}),
}


@pytest.mark.parametrize("name", POSSIBLE)
def test_possible_clash(name):
    a, b, conds = POSSIBLE[name]
    for x, y in ((a, b), (b, a)):
        verdict, d = check_pair(x, y)
        assert verdict == "possible_clash" and set(d["conditions"]) == conds


def test_minimal_conditions_only():
    a = ok(unmod("never", "during a hotfix", cmd=["push"]), unmod("never", "on fridays", cmd=["rebase"]))
    verdict, d = check_pair(a, ok(must(cmd=["push_branch"])))
    assert verdict == "possible_clash" and d["conditions"] == ["during a hotfix"]


def test_unrelated_condition_stays_compatible():
    a = ok(unmod("never", "during a hotfix", cmd=["push"]))
    assert check_pair(a, ok(never(cmd=["commit"])))[0] == "compatible"


V21 = {
    "after a successful build vs commit without building":
        (ok(only_if({"cmd": ["commit"]}, {"after": ["run"], "after_task": "build", "after_ok": True})),
         ok(must(cmd=["commit"], after=["run"], after_task="test")), "clash"),
    "commit only after a successful build vs commit after a successful build":
        (ok(only_if({"cmd": ["commit"]}, {"after": ["run"], "after_task": "build", "after_ok": True})),
         ok(must(cmd=["commit"], after=["run"], after_task="build", after_ok=True)), "compatible"),
    "after editing X run plutil vs never run plutil after editing X":
        (ok(must(cmd=["run"], task="other:plutil", after=["edit"], after_path=["proj/x.pbxproj"])),
         ok(never(cmd=["run"], task="other:plutil", after=["edit"], after_path=["proj/*.pbxproj"])), "clash"),
    "after editing X vs after editing Y: different files, no clash":
        (ok(must(cmd=["run"], task="lint", after=["edit"], after_path=["a.md"])),
         ok(never(cmd=["run"], task="lint", after=["edit"], after_path=["b.md"])), "compatible"),
}


@pytest.mark.parametrize("name", V21)
def test_earlier_step_details(name):
    a, b, want = V21[name]
    assert check_pair(a, b)[0] == want
    assert check_pair(b, a)[0] == want


def test_earlier_details_belong_to_the_same_step():
    # "after editing a.md" must not be met by an edit of b.md plus some other action on a.md
    from rules.model import Event, constraints
    from rules.patterns import is_sat
    e = Event("t")
    rule = [never(cmd=["run"], after=["edit"], after_path=["a.md"])]
    # an earlier edit of b.md and an earlier delete of a.md: the never does not apply
    assert is_sat(e.wellformed(), e.match({"cmd": ["run"]}), e.prior["edit"], e.prior["delete"],
                  e.match({"after": ["edit"], "after_path": ["b.md"]}),
                  e.match({"after": ["delete"], "after_path": ["a.md"]}), *constraints(e, rule))


def test_after_task_needs_run():
    import pytest as _p
    from rules.model import Event
    with _p.raises(ValueError):
        Event("t").match({"after": ["edit"], "after_task": "build"})
