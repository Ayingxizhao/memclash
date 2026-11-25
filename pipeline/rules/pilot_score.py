"""Score the pilot against the planted rules (docs/review/experiment_design.md, run A).

  uv run python pipeline/rules/pilot_score.py --translations data/runs/rules/pilot/translations_run1.json --run 1

Planted clashes in scope: R1 vs X1/X2 and R3 vs X7/X8 expect `clash`, R6 vs X13/X14 expect
`exception`. Paraphrases R1/X3, R3/X9, R6/X15 expect: both ok, same meaning, `compatible`.
All expected pairs (each planted rule vs every real rule it should clash with, not only its
host) are in data/inject/dev_pilot_expected.json, written after run 1. Every other flagged
pair is listed for a hand check.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rules.agreement import same_meaning  # noqa: E402
from rules.pair import check_pair  # noqa: E402
from rules.report import check_all  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
EXPECTED = {"opposite": "clash", "narrower": "clash", "permission": "exception"}
CONFLICT = ("clash", "exception", "state_conflict")


def score_all_expected(rules, expected, run):
    """Each planted rule against every real rule it should clash with, in its own copy."""
    by = {(r["folder"], r["id"]): r["runs"][run] for r in rules}
    out = []
    for x in expected:
        folder = next(f for (f, i) in by if i == x["planted"])
        a, b = by[(folder, x["real"])], by[(folder, x["planted"])]
        verdict, _ = check_pair(a, b)
        out.append({**x, "got": verdict, "found": verdict == x["verdict"],
                    "found_any": verdict in CONFLICT, "found_possible": verdict == "possible_clash",
                    "status": [a["status"], b["status"]]})
    return out


def score(rules, inject, run, expected=()):
    by = {(r["folder"], r["id"]): r["runs"][run] for r in rules}
    planted, paraphrases, keys = [], [], set()
    for x in inject:
        if x["pattern"] not in EXPECTED or x["host"] not in ("R1", "R3", "R6"):
            continue
        folder = next(f for (f, i) in by if i == x["id"])
        a, b = by[(folder, x["host"])], by[(folder, x["id"])]
        verdict, _ = check_pair(a, b)
        keys.add((folder, *sorted([x["host"], x["id"]])))
        row = {"host": x["host"], "planted": x["id"], "kind": x["kind"], "verdict": verdict,
               "status": [a["status"], b["status"]]}
        if x["kind"] == "paraphrase":
            row["same_meaning"] = a["status"] == b["status"] == "ok" and same_meaning(a, b)
            row["correct"] = row["same_meaning"] and verdict == "compatible"
            paraphrases.append(row)
        else:
            row["found"] = verdict == EXPECTED[x["pattern"]]
            planted.append(row)
    for x in expected:  # pairs expected to clash are not "other" flags
        for (f, i) in by:
            if i == x["planted"]:
                keys.add((f, *sorted([x["real"], x["planted"]])))
    res = check_all(rules, run)
    # the real rules repeat in all three copies: list each flagged real pair once
    other, seen = [], set()
    for p in res["pairs"]:
        if p["verdict"] in ("clash", "exception", "state_conflict", "possible_clash", "invalid") and \
                (p["folder"], *sorted([p["a"], p["b"]])) not in keys:
            k = tuple(sorted([p["rule_a"], p["rule_b"]]))
            if k not in seen:
                seen.add(k)
                other.append(p)
    return {"planted_found": sum(r["found"] for r in planted), "planted": planted,
            "paraphrases_correct": sum(r["correct"] for r in paraphrases),
            "paraphrases": paraphrases, "other_flagged": other}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--translations", required=True)
    ap.add_argument("--run", type=int, default=1)
    ap.add_argument("--vote", action="store_true",
                    help="score the majority meaning over all runs (no majority: rule unstable)")
    ap.add_argument("--inject", default=str(ROOT / "data" / "inject" / "dev_pilot.json"))
    ap.add_argument("--expected", default=str(ROOT / "data" / "inject" / "dev_pilot_expected.json"))
    a = ap.parse_args()
    rules = json.loads(Path(a.translations).read_text())["rules"]
    if a.vote:
        from rules.agreement import vote
        rules = [{**r, "runs": [vote(r["runs"])[0] or {"status": "unstable", "reason": "no majority"}]}
                 for r in rules]
        a.run = 1
    expected = json.loads(Path(a.expected).read_text())["expected"]
    out = score(rules, json.loads(Path(a.inject).read_text()), a.run - 1, expected)
    out["all_expected"] = score_all_expected(rules, expected, a.run - 1)
    t = Path(a.translations)
    tag = "vote" if a.vote else f"run{a.run}"
    t.with_name(f"score_{t.stem}_{tag}.json").write_text(json.dumps(out, indent=1))
    print(f"planted clashes found: {out['planted_found']} of {len(out['planted'])}")
    for r in out["planted"]:
        print(f"  {r['host']} vs {r['planted']} ({r['kind']}): {r['verdict']} {r['status']}")
    print(f"paraphrases correct: {out['paraphrases_correct']} of {len(out['paraphrases'])}")
    for r in out["paraphrases"]:
        print(f"  {r['host']} vs {r['planted']}: {r['verdict']}, same meaning {r['same_meaning']} {r['status']}")
    ex = out["all_expected"]
    print(f"all expected pairs found: exact verdict {sum(r['found'] for r in ex)}, any conflict verdict "
          f"{sum(r['found_any'] for r in ex)}, plus possible_clash {sum(r['found_possible'] for r in ex)}"
          f" — of {len(ex)} ({sum(1 for r in ex if r.get('limit'))} out of reach by design)")
    for r in ex:
        if not r["found"]:
            print(f"  missed {r['real']} vs {r['planted']}: got {r['got']} {r['status']}"
                  f"{' [by design: ' + r['limit'][:50] + ']' if r.get('limit') else ''}")
    print(f"other flagged pairs (unique): {len(out['other_flagged'])}")
    for p in out["other_flagged"]:
        print(f"  {p['verdict']}: {p['a']} {p['rule_a'][:60]} || {p['b']} {p['rule_b'][:60]}")
