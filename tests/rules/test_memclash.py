"""memclash gate and clash check on hand-written translations in a temporary git repo."""

import json
import subprocess
from pathlib import Path

import pytest

from rules import memclash


def ok(*clauses):
    return {"status": "ok", "clauses": list(clauses), "left_out": ""}


RULES = [
    ("R1", "Never read the user's .env file.", ok({"type": "never", "where": {"cmd": "read", "path": ".env"}})),
    ("R2", "Only run tests when the user explicitly asks.",
     ok({"type": "only_if", "where": {"cmd": "run", "task": "test"}, "needs": {"user_asked": True}})),
    ("R3", "Never force-push to main.", ok({"type": "never", "where": {"cmd": ["force_push"], "branch": "main"}})),
    ("R4", "Always run the tests before you commit.",  # must_do: not usable by the gate
     ok({"type": "must_do", "where": {"cmd": "commit"}})),
]


@pytest.fixture
def repo(tmp_path):
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=tmp_path, check=True)
    (tmp_path / ".memclash").mkdir()
    rules = [{"id": i, "rule": en, "translation": tr, "gate": memclash.gate_usable(tr)} for i, en, tr in RULES]
    (tmp_path / ".memclash" / "rules.json").write_text(json.dumps({"rules": rules}))
    return str(tmp_path)


def gate(repo, tool, **inp):
    return memclash.gate(repo, {"tool": tool, "input": inp})


def test_gate_usable():
    assert [memclash.gate_usable(tr) for _, _, tr in RULES] == [True, True, True, False]
    mixed = ok({"type": "never", "where": {"cmd": ["commit"], "branch": "main"}}, {"type": "must_do", "where": {"cmd": ["branch_create"]}})
    assert memclash.gate_clauses(mixed) == mixed["clauses"][:1]


def test_read_env_blocked_by_read_tool_and_bash(repo):
    assert gate(repo, "read", path=".env")["breaks"] == ["R1"]
    assert gate(repo, "bash", command="cat .env | grep KEY")["breaks"] == ["R1"]
    assert not gate(repo, "read", path=".env.example")["block"]


def test_tests_blocked_with_rule_text(repo):
    for cmd in ("./gradlew :rd-protocol:test --offline -q", "npm test", "uv run pytest -q", "python -m pytest"):
        r = gate(repo, "bash", command=cmd)
        assert r["breaks"] == ["R2"], cmd
        assert "Only run tests when the user explicitly asks." in r["reason"]
    assert not gate(repo, "bash", command="./gradlew build")["block"]


def test_git_force_push_main_only(repo):
    assert gate(repo, "bash", command="git push --force origin main")["breaks"] == ["R3"]
    assert not gate(repo, "bash", command="git push origin main")["block"]
    assert not gate(repo, "bash", command="git push -f origin feature")["block"]


def test_branch_switch_inside_one_command(repo):
    evs = memclash.events({"tool": "bash", "input": {"command": "git checkout -b fix/x && git commit -am fix"}}, repo)
    assert [(e["cmd"], e["branch"]) for e in evs] == [("branch_create", "fix/x"), ("commit", "fix/x")]


def test_event_mapping(repo):
    evs = memclash.events({"tool": "bash", "input": {"command": "git add src/a.py && mv a.txt b.txt; rm -f c.log"}}, repo)
    assert [e["cmd"] for e in evs] == ["stage", "move", "delete"]
    assert evs[1]["dest_path"] == "b.txt"
    assert memclash.events({"tool": "bash", "input": {"command": "echo hi > notes.md"}}, repo)[0] == \
        {"cmd": "create", "path": "notes.md", "branch": "main"}


def test_clash_pair(repo):
    p = f"{repo}/.memclash/rules.json"
    rules = json.load(open(p))["rules"]
    rules.append({"id": "R5", "rule": "Always force-push to main after a rebase.",
                  "translation": ok({"type": "must_do", "where": {"cmd": ["force_push"], "branch": "main"}}),
                  "gate": False})
    json.dump({"rules": rules}, open(p, "w"))
    found = memclash.clash(repo)["clashes"]
    assert [c["rules"] for c in found if c["verdict"] == "clash"] == [["R3", "R5"]]


def test_no_rules_file_allows_everything(tmp_path):
    assert not memclash.gate(str(tmp_path), {"tool": "read", "input": {"path": ".env"}})["block"]


def test_tests_passed_comes_from_the_session(repo):
    p = f"{repo}/.memclash/rules.json"
    rules = json.load(open(p))["rules"]
    tr = ok({"type": "only_if", "where": {"cmd": ["push"]}, "needs": {"tests_passed": True}})
    rules.append({"id": "R6", "rule": "Only push after the tests have passed.", "translation": tr, "gate": True})
    json.dump({"rules": rules}, open(p, "w"))
    push = {"tool": "bash", "input": {"command": "git push origin fix/x"}}
    run = lambda ok_: {"cmd": "run", "task": "test", "branch": "fix/x", "ok": ok_}
    assert memclash.gate(repo, {**push, "prior": []})["breaks"] == ["R6"]
    assert memclash.gate(repo, {**push, "prior": [run(False)]})["breaks"] == ["R6"]
    assert not memclash.gate(repo, {**push, "prior": [run(True)]})["block"]


def test_user_asked_flag_from_the_host(repo):
    call = {"tool": "bash", "input": {"command": "npm test"}}
    assert memclash.gate(repo, call)["breaks"] == ["R2"]
    assert not memclash.gate(repo, {**call, "flags": {"user_asked": True}})["block"]


def test_earlier_steps_in_the_same_command_count(repo):
    p = f"{repo}/.memclash/rules.json"
    rules = json.load(open(p))["rules"]
    tr = ok({"type": "only_if", "where": {"cmd": ["commit"]}, "needs": {"after": ["run"], "after_task": "lint", "after_ok": True}})
    rules.append({"id": "R7", "rule": "Only commit after the linter has run successfully.", "translation": tr, "gate": True})
    json.dump({"rules": rules}, open(p, "w"))
    assert memclash.gate(repo, {"tool": "bash", "input": {"command": "git commit -am x"}})["breaks"] == ["R7"]
    assert not memclash.gate(repo, {"tool": "bash", "input": {"command": "npm run lint && git commit -am x"}})["block"]


def test_check_reports_only_clashes_the_change_adds(repo, monkeypatch, tmp_path):
    (tmp_path / "MEMORY.md").write_text("- Never force-push to main.\n")
    new = ok({"type": "must_do", "where": {"cmd": ["force_push"], "branch": "main"}})
    old = RULES[2][2]

    async def fake_compile(where, only=None):  # stands in for the LLM extract + translate
        rules = [{"id": "R1", "rule": "Never force-push to main.", "quote": "Never force-push to main.", "translation": old},
                 {"id": "R2", "rule": "Always force-push to main after a rebase.",
                  "quote": "Always force-push to main after a rebase.", "translation": new}]
        Path(where, ".memclash").mkdir(exist_ok=True)
        Path(where, ".memclash", "rules.json").write_text(json.dumps({"rules": rules}))
    monkeypatch.setattr(memclash, "_compile", fake_compile)
    nxt = tmp_path / "next.md"
    nxt.write_text("- Never force-push to main.\n- Always force-push to main after a rebase.\n")
    r = memclash.check(repo, "MEMORY.md", str(nxt))
    assert r["new_rules"] == ["Always force-push to main after a rebase."]
    assert [c["verdict"] for c in r["clashes"]] == ["clash"]


def test_star_branch_means_any_branch():
    tr = memclash.any_branch(ok({"type": "only_if", "where": {"cmd": ["push"], "branch": "*"}, "needs": {"tests_passed": True}}))
    assert tr["clauses"][0]["where"] == {"cmd": ["push"]}


def test_check_reports_a_replaced_rule(repo, monkeypatch, tmp_path):
    p = f"{repo}/.memclash/rules.json"
    rules = json.load(open(p))["rules"]
    rules.append({"id": "R5", "rule": "Never commit directly to main.", "quote": "Never commit directly to main.",
                  "translation": ok({"type": "never", "where": {"cmd": ["commit"], "branch": "main"}}), "gate": True})
    json.dump({"rules": rules}, open(p, "w"))
    (tmp_path / "MEMORY.md").write_text("- Never commit directly to main.\n")
    swap = {"id": "R1", "rule": "Commit small fixes directly to main.", "quote": "Commit small fixes directly to main.",
            "translation": ok({"type": "may_do", "where": {"cmd": ["commit"], "branch": "main"}})}

    async def fake_compile(where, only=None):
        Path(where, ".memclash").mkdir(exist_ok=True)
        Path(where, ".memclash", "rules.json").write_text(json.dumps({"rules": [swap]}))
    monkeypatch.setattr(memclash, "_compile", fake_compile)
    nxt = tmp_path / "next.md"
    nxt.write_text("- Commit small fixes directly to main.\n")
    r = memclash.check(repo, "MEMORY.md", str(nxt))
    assert r["clashes"] == []
    assert [(x["removed"], x["new"]) for x in r["replaced"]] == [("Never commit directly to main.", "Commit small fixes directly to main.")]
