"""Score translations against the frozen hand-labelled set
(data/runs/survey_rules/label_set/frozen_2026-11-22.json).

Per rule and run:
- status right: same status as the label (ok / not_in_scope / unclear);
- rule right: Z3 says the translation means the same as the label (agreement.same_meaning);
- requirements: label clauses matched one-to-one to equivalent translation clauses (each
  pair compared alone with same_meaning); `extra` counts translation clauses that match no
  label clause (something added, or a part the label leaves out translated anyway);
- a rule with no translation record counts as wrong, never skipped.
Also, for each rule, the vote over runs (agreement.vote) is scored the same way; an unstable
vote (no majority) counts as wrong in `vote_rule_right` and is also counted on its own.
"""

from rules.agreement import same_meaning, vote


def as_translation(label):
    if label["status"] != "ok":
        return {"status": label["status"], "reason": "", "word": label.get("word", "")}
    return {"status": "ok", "reason": "", "left_out": "",
            "clauses": [{k: v for k, v in c.items() if k != "req"} for c in label["clauses"]]}


def one_clause(c):
    return {"status": "ok", "reason": "", "left_out": "", "clauses": [c]}


def match_one_to_one(want, have):
    """Largest one-to-one matching of label clauses to equivalent translation clauses."""
    edges = [[j for j, h in enumerate(have) if same_meaning(one_clause(w), one_clause(h))]
             for w in want]
    match = {}  # translation clause -> label clause

    def augment(i, seen):
        for j in edges[i]:
            if j not in seen:
                seen.add(j)
                if j not in match or augment(match[j], seen):
                    match[j] = i
                    return True
        return False

    return sum(augment(i, set()) for i in range(len(want)))


def score_one(label, t):
    if t is None:
        return {"status_right": False, "rule_right": False, "req_found": 0,
                "req_total": len(label.get("clauses", [])) if label["status"] == "ok" else 0,
                "extra": 0, "missing": True}
    lt = as_translation(label)
    want = lt.get("clauses", [])
    have = t.get("clauses", []) if t.get("status") == "ok" else []
    found = match_one_to_one(want, have)
    return {"status_right": t.get("status") == label["status"], "rule_right": same_meaning(lt, t),
            "req_found": found, "req_total": len(want), "extra": len(have) - found}


def score(labels, translated, runs=3):
    """labels: frozen rules; translated: records with `runs` (cli translate output)."""
    by = {(r["folder"], r["id"]): r for r in translated}
    rows = []
    for lab in labels:
        rec = by.get((lab["folder"], lab["id"]))
        ts = rec["runs"] if rec else [None] * runs
        winner, sizes = vote([t for t in ts if t is not None]) if rec else (None, [])
        rows.append({"folder": lab["folder"], "id": lab["id"], "ambiguous": lab.get("ambiguous", False),
                     "runs": [score_one(lab, t) for t in ts], "vote_sizes": sizes,
                     "vote": score_one(lab, winner) if winner else None,
                     "statuses": [t.get("status") if t else "missing" for t in ts],
                     "retried": [bool(t and (t.get("retried") or t.get("retried_steps"))) for t in ts]})
    return rows


def summary(rows):
    def mean(xs):
        xs = list(xs)
        return round(sum(xs) / len(xs), 3) if xs else None
    flat = [x for r in rows for x in r["runs"]]
    return {
        "rules": len(rows), "runs_per_rule": len(rows[0]["runs"]) if rows else 0,
        "status_right": mean(x["status_right"] for x in flat),
        "rule_right": mean(x["rule_right"] for x in flat),
        "req_found": sum(x["req_found"] for x in flat), "req_total": sum(x["req_total"] for x in flat),
        "extra_clauses": sum(x["extra"] for x in flat),
        "missing": sum(bool(x.get("missing")) for x in flat),
        "bad_output": sum(s == "invalid_output" for r in rows for s in r["statuses"]),
        "retried_runs": sum(x for r in rows for x in r["retried"]),
        "vote_unstable": sum(r["vote"] is None for r in rows),
        "vote_rule_right": mean(bool(r["vote"] and r["vote"]["rule_right"]) for r in rows),
        "rule_right_clear": mean(x["rule_right"] for r in rows if not r["ambiguous"] for x in r["runs"]),
        "rule_right_ambiguous": mean(x["rule_right"] for r in rows if r["ambiguous"] for x in r["runs"]),
    }
