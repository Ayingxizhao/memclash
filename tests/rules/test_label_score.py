"""Scoring against labels (rules/label_score.py)."""

from rules.label_score import score, summary

LABEL = {"folder": "f", "id": "R1", "status": "ok", "ambiguous": False,
         "clauses": [{"req": "q1", "type": "only_if", "where": {"cmd": ["commit"]}, "needs": {"secrets_checked": True}},
                     {"req": "q2", "type": "never", "where": {"cmd": ["commit"], "has_secret": True}}]}
FULL = {"status": "ok", "reason": "", "left_out": "", "clauses": [
    {"type": "never", "where": {"cmd": ["commit"], "has_secret": True}},
    {"type": "only_if", "where": {"cmd": ["commit"]}, "needs": {"secrets_checked": True}}]}
HALF = {"status": "ok", "reason": "", "left_out": "", "clauses": [
    {"type": "only_if", "where": {"cmd": ["commit"]}, "needs": {"secrets_checked": True}}]}


def test_full_and_half_translations():
    rows = score([LABEL], [{"folder": "f", "id": "R1", "runs": [FULL, HALF, FULL]}])
    r = rows[0]
    assert [x["rule_right"] for x in r["runs"]] == [True, False, True]
    assert [x["req_found"] for x in r["runs"]] == [2, 1, 2]
    assert r["vote"]["rule_right"] and r["vote_sizes"] == [2, 1]
    s = summary(rows)
    assert s["req_found"] == 5 and s["req_total"] == 6 and s["vote_unstable"] == 0
    assert s["extra_clauses"] == 0


def test_matching_is_one_to_one_and_extras_count():
    dup = {"status": "ok", "reason": "", "left_out": "", "clauses": [
        {"type": "only_if", "where": {"cmd": ["commit"]}, "needs": {"secrets_checked": True}},
        {"type": "never", "where": {"cmd": ["push"]}}]}
    two_same = dict(LABEL, clauses=[LABEL["clauses"][0], LABEL["clauses"][0]])
    r = score([two_same], [{"folder": "f", "id": "R1", "runs": [dup]}])[0]["runs"][0]
    assert r["req_found"] == 1 and r["extra"] == 1


def test_missing_record_counts_as_wrong():
    rows = score([LABEL], [], runs=3)
    s = summary(rows)
    assert s["missing"] == 3 and s["rule_right"] == 0 and s["vote_rule_right"] == 0


def test_status_only_labels():
    lab = {"folder": "f", "id": "R2", "status": "not_in_scope", "ambiguous": True}
    rows = score([lab], [{"folder": "f", "id": "R2", "runs": [{"status": "not_in_scope", "reason": "x"}]}])
    assert rows[0]["runs"][0]["status_right"] and rows[0]["runs"][0]["rule_right"]
