"""One action and one rule as Z3 formulas (rules/vocab.py, rules/model.py)."""

import pytest
from rules.model import Event, constraints, prepared
from rules.patterns import is_sat
from rules.vocab import expand, norm_name, task_name


def allowed(action, clauses):
    """Can `action` (fields as in a translation) happen without breaking `clauses`?"""
    e = Event("t")
    return is_sat(e.wellformed(), e.match(action), *constraints(e, prepared(clauses, "t")))


NEVER_DELETE_WORLD = [{"type": "never", "where": {"cmd": ["delete"], "path": ["server-world.dat"]}}]


def test_never_delete_blocks_delete_at_any_depth():
    assert not allowed({"cmd": ["delete"], "path": ["world/server-world.dat"]}, NEVER_DELETE_WORLD)


def test_never_delete_does_not_block_move():
    assert allowed({"cmd": ["move"], "path": ["world/server-world.dat"]}, NEVER_DELETE_WORLD)


def test_push_group_covers_force_push():
    assert expand(["push"]) == ["force_push", "push_branch", "push_delete"]
    never_push = [{"type": "never", "where": {"cmd": ["push"]}}]
    assert not allowed({"cmd": ["force_push"]}, never_push)


def test_only_if_needs():
    rule = [{"type": "only_if", "where": {"cmd": ["run"], "task": "deploy"},
             "needs": {"user_asked": True}}]
    assert not allowed({"cmd": ["run"], "task": "deploy", "user_asked": False}, rule)
    assert allowed({"cmd": ["run"], "task": "deploy", "user_asked": True}, rule)
    assert allowed({"cmd": ["run"], "task": "test", "user_asked": False}, rule)  # other task


def test_path_except():
    rule = [{"type": "never", "where": {"cmd": ["edit"], "path": ["vendor/"],
                                        "path_except": ["vendor/cmake/"]}}]
    assert not allowed({"cmd": ["edit"], "path": ["vendor/a.c"]}, rule)
    assert allowed({"cmd": ["edit"], "path": ["vendor/cmake/x.txt"]}, rule)


def test_kind_dir():
    rule = [{"type": "never", "where": {"cmd": ["create"], "path": ["src/handlers/**"], "kind": "dir"}}]
    assert not allowed({"cmd": ["create"], "path": ["src/handlers/a"], "kind": "dir"}, rule)
    assert allowed({"cmd": ["create"], "path": ["src/handlers/a.ts"], "kind": "file"}, rule)


def test_running_names_match_after_cleanup():
    assert norm_name("The  Game Server") == "game server"
    rule = [{"type": "never", "where": {"cmd": ["delete"], "running": ["the game server"]}}]
    assert not allowed({"cmd": ["delete"], "running": ["Game server"]}, rule)
    assert allowed({"cmd": ["delete"], "running": ["dev server"]}, rule)


def test_tasks():
    assert task_name("deploy") == "deploy"
    assert task_name("other:Seed  DB") == "other:seed db"
    with pytest.raises(ValueError):
        task_name("pytest")


def test_after_means_some_earlier_point():
    rule = [{"type": "only_if", "where": {"cmd": ["branch_create"]}, "needs": {"after": ["fetch"]}}]
    # fetch and checkout both happened earlier: still counts as "after fetch"
    assert allowed({"cmd": ["branch_create"], "after": ["fetch"]}, rule)
    e = Event("t")
    assert is_sat(e.wellformed(), e.match({"cmd": ["branch_create"]}), e.prior["fetch"],
                  e.prior["checkout"], *constraints(e, rule))


def test_when_unmodeled_only_applies_under_its_own_fact():
    rule = [{"type": "never", "where": {"cmd": ["push"]}, "when_unmodeled": "during a hotfix"}]
    assert allowed({"cmd": ["push_branch"]}, rule)  # the solver can pick "not a hotfix"


@pytest.mark.parametrize("where", [{"cmd": ["erase"]}, {"colour": True},
                                   {"cmd": ["run"], "task": "pytest"}, {"kind": "symlink"},
                                   {"path_except": ["a/"]}, {"user_asked": "yes"}])
def test_unknown_names_raise(where):
    with pytest.raises(ValueError):
        Event("t").match(where)
