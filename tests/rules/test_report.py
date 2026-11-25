"""Counting results over a whole translation file (rules/report.py, rules/cli.py)."""

import json

from rules import cli, report

NEVER_FORCE = {"status": "ok", "reason": "", "left_out": "",
               "clauses": [{"type": "never", "where": {"cmd": ["force_push"]}}]}
MUST_FORCE = {"status": "ok", "reason": "", "left_out": "",
              "clauses": [{"type": "must_do", "where": {"cmd": ["force_push"]}}]}
FORCE_GROUP = {"status": "ok", "reason": "", "left_out": "",  # same meaning as NEVER_FORCE
               "clauses": [{"type": "never", "where": {"cmd": ["force_push", "force_push"]}}]}
UNCLEAR = {"status": "unclear", "word": "write", "reason": ""}

RULES = [
    {"folder": "f1", "id": "R1", "file": "a.md", "rule": "Never force push.",
     "runs": [NEVER_FORCE, FORCE_GROUP, NEVER_FORCE]},
    {"folder": "f1", "id": "R2", "file": "b.md", "rule": "Always force push.",
     "runs": [MUST_FORCE, MUST_FORCE, NEVER_FORCE]},
    {"folder": "f1", "id": "R3", "file": "c.md", "rule": "Write the notes.",
     "runs": [UNCLEAR, UNCLEAR, UNCLEAR]},
    {"folder": "f2", "id": "R1", "file": "a.md", "rule": "Always force push.",
     "runs": [MUST_FORCE, MUST_FORCE, MUST_FORCE]},
]


def test_pairs_only_within_a_folder_and_unclear_rules_are_listed():
    res = report.check_all(RULES, run=0)
    assert res["counts"] == {"clash": 1}           # R1 vs R2 in f1; f2's rule is alone
    assert res["rule_status"] == {"ok": 3, "unclear": 1}
    assert [x["id"] for x in res["excluded"]] == ["R3"]


def test_agreement_counts():
    res = report.agreement_all(RULES)
    assert res["rules"] == 4 and res["same_status"] == 4
    assert res["all_ok"] == 3 and res["same_meaning"] == 2   # R2 changed meaning in run 3
    assert res["rows"][2]["same_meaning"] is None            # unclear: meaning not compared


def test_estimate_counts_calls_with_retries():
    est = report.estimate(RULES, runs=3, prompt_words=1000, retry_rate=0.0)
    assert est["calls"] == 12 and est["input_tokens"] > 12 * 1000


def test_cli_check_and_agreement_write_files(tmp_path):
    t = tmp_path / "t.json"
    t.write_text(json.dumps({"rules": RULES}))
    cli.main(["check", "--translations", str(t), "--out", str(tmp_path / "c.json"), "--run", "1"])
    cli.main(["agreement", "--translations", str(t), "--out", str(tmp_path / "a.json")])
    assert json.loads((tmp_path / "c.json").read_text())["counts"] == {"clash": 1}
    assert json.loads((tmp_path / "a.json").read_text())["same_meaning"] == 2


def test_load_rules(tmp_path):
    f = tmp_path / "rules.json"
    f.write_text(json.dumps({"folders": [{"repo": "o__r", "rules": [
        {"id": "R1", "file": "x.md", "quote": "q", "rule": "Never rebase."}]}]}))
    assert report.load_rules(f) == [{"folder": "o__r", "id": "R1", "file": "x.md",
                                     "rule": "Never rebase."}]
