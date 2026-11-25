"""Hand-written cases for rules.enforce (never the experiment's test actions)."""

from rules.enforce import check, judge

F = {"has_secret": False, "user_confirmed": False, "files_shown": False, "secrets_checked": False,
     "admin_bypass": False, "in_worktree": False, "user_asked": False, "tests_passed": False}


def ev(cmd, branch="dev", path=None, task=None, flags=None, running=(), prior=(), kind=None):
    return {"cmd": cmd, "branch": branch, "path": path, "dest_path": None, "kind": kind,
            "task": task, "flags": {**F, **(flags or {})}, "running": list(running),
            "prior": list(prior)}


def ok(*clauses):
    return {"status": "ok", "clauses": list(clauses), "left_out": ""}


NO_PUSH_MAIN = ok({"type": "never", "where": {"cmd": ["push"], "branch": "main"}})
DEL_DAT = ok({"type": "only_if", "where": {"cmd": ["delete"], "path": ["*.dat"], "kind": "file"},
              "needs": {"user_confirmed": True}})
RESTART = ok({"type": "only_if", "where": {"cmd": ["run"], "task": "restart", "after": ["run"],
                                           "after_task": "build"}, "needs": {"user_confirmed": True}})
NO_PARALLEL = ok({"type": "never", "where": {"cmd": ["run"], "task": "test", "running": ["test"]}})
BUILD_FIRST = ok({"type": "only_if", "where": {"cmd": ["commit"]},
                  "needs": {"after": ["run"], "after_task": "build", "after_ok": True}})


def test_never_branch():
    assert check(ev("push_branch", "main"), NO_PUSH_MAIN) == [0]
    assert check(ev("force_push", "main"), NO_PUSH_MAIN) == [0]      # group "push"
    assert check(ev("push_branch", "main-old"), NO_PUSH_MAIN) == []
    assert check(ev("commit", "main"), NO_PUSH_MAIN) == []


def test_only_if_flag_and_path_depth():
    assert check(ev("delete", path="a/b/x.dat", kind="file"), DEL_DAT) == [0]   # any depth
    assert check(ev("delete", path="x.dat", kind="file", flags={"user_confirmed": True}), DEL_DAT) == []
    assert check(ev("delete", path="x.txt", kind="file"), DEL_DAT) == []
    assert check(ev("edit", path="x.dat", kind="file"), DEL_DAT) == []


def test_earlier_step():
    build = {"cmd": "run", "task": "build", "branch": "dev", "path": None, "ok": True}
    assert check(ev("run", task="restart", prior=[build]), RESTART) == [0]
    assert check(ev("run", task="restart", prior=[build], flags={"user_confirmed": True}), RESTART) == []
    assert check(ev("run", task="restart"), RESTART) == []                   # no build before
    tests = {"cmd": "run", "task": "test", "branch": "dev", "path": None, "ok": True}
    assert check(ev("run", task="restart", prior=[build, tests]), RESTART) == []  # newest run is test


def test_after_ok():
    good = {"cmd": "run", "task": "build", "branch": "dev", "path": None, "ok": True}
    bad = {**good, "ok": False}
    assert check(ev("commit", path="a.py", prior=[good]), BUILD_FIRST) == []
    assert check(ev("commit", path="a.py", prior=[bad]), BUILD_FIRST) == [0]
    assert check(ev("commit", path="a.py"), BUILD_FIRST) == [0]


def test_running():
    assert check(ev("run", task="test", running=["test"]), NO_PARALLEL) == [0]
    assert check(ev("run", task="test", running=["Test"]), NO_PARALLEL) == [0]  # name clean-up
    assert check(ev("run", task="lint", running=["test"]), NO_PARALLEL) == []
    assert check(ev("run", task="test"), NO_PARALLEL) == []


def test_unknown_condition_never_blocks():
    t = ok({"type": "never", "where": {"cmd": ["commit"]}, "when_unmodeled": "the change is docs"})
    assert check(ev("commit", path="docs/a.md"), t) == []


def test_skipped_and_failed_translations():
    assert check(ev("commit"), ok({"type": "must_do", "where": {"cmd": ["commit"]}})) == []
    assert check(ev("commit"), {"status": "not_in_scope", "clauses": None}) == []
    assert check(ev("commit"), None) == []
    r = judge(ev("commit"), {"R1": ok({"type": "never", "where": {"cmd": ["nonsense"]}})})
    assert r["allowed"] and r["errors"]


def test_judge_names_rules():
    r = judge(ev("push_branch", "main"), {"R1": NO_PUSH_MAIN, "R2": DEL_DAT})
    assert r == {"allowed": False, "rule_ids": ["R1"], "clauses": {"R1": [0]}, "errors": []}


def test_string_path_and_dot_slash():
    t = ok({"type": "never", "where": {"cmd": "edit", "path": ".env"}})
    assert check(ev("edit", path=".env"), t) == [0]
    assert check(ev("edit", path="./.env"), t) == [0]
    assert check(ev("edit", path="a/.env"), t) == [0]
    assert check(ev("edit", path="e"), t) == []          # not letter by letter
    assert check(ev("edit", path=".env.example"), t) == []
