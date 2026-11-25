"""Score the boundary stress test (docs/review/boundary_prereg.md).
  PYTHONPATH=pipeline uv run python -m rules.boundary_score
"""

import json
import random
import re
from pathlib import Path

D = Path(__file__).resolve().parents[2] / "data" / "runs" / "natural"
J = D / "boundary_judge"


def parse(path):
    t = path.read_text()
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", t, re.S)
    return json.loads(m.group(1) if m else t[t.index("{"):t.rindex("}") + 1])["actions"]


def arms():
    out = {"Z3": json.load(open(J / "Z3.json"))["results"]}
    if (J / "deepseek.json").exists():
        out["deepseek"] = json.load(open(J / "deepseek.json"))["results"]
    for run in (1, 2, 3):
        fs = sorted((J / "codex" / f"run{run}").glob("*.md"))
        if len(fs) == 3:
            out[f"codex{run}"] = [x for f in fs for x in parse(f)]
    return out


def prf(got, gold, ids):
    tp = sum(got[i][0] and bool(gold[i]) for i in ids)
    fp = sum(got[i][0] and not gold[i] for i in ids)
    fn = sum((not got[i][0]) and bool(gold[i]) for i in ids)
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return p, r, (2 * p * r / (p + r) if p + r else 0.0)


def main():
    L = json.load(open(D / "boundary_labels_final.json"))
    gold = {x["id"]: set(x["breaks"]) for x in L["labels"]}
    key = json.load(open(D / "boundary_actions_key.json"))
    ids = sorted(gold)
    A = {}
    for arm, res in arms().items():
        m = {r["action"]: (not r.get("allowed", True), set(r.get("rule_ids") or [])) for r in res}
        A[arm] = {i: m.get(i, (False, set())) for i in ids}
    table = {}
    for arm, got in A.items():
        p, r, f = prf(got, gold, ids)
        exact = sum((got[i][1] if got[i][0] else set()) == gold[i] for i in ids) / len(ids)
        cats = {}
        for c in sorted({key[i]["category"] for i in ids}):
            ci = [i for i in ids if key[i]["category"] == c]
            cats[c] = round(sum(got[i][0] == bool(gold[i]) for i in ci) / len(ci), 3)
        table[arm] = {"P": round(p, 3), "R": round(r, 3), "F1": round(f, 3), "exact_set": round(exact, 3),
                      "acc_by_category": cats}
    # rule-clustered bootstrap of Z3 F1 minus the best LLM run's F1
    llm = [a for a in A if a != "Z3"]
    best = max(llm, key=lambda a: table[a]["F1"]) if llm else None
    if best:
        rules = sorted({key[i]["rule_id"] + key[i]["aid"].split("-")[0] for i in ids})
        by = {r: [i for i in ids if key[i]["rule_id"] + key[i]["aid"].split("-")[0] == r] for r in rules}
        rng, diffs = random.Random(2520), []
        for _ in range(2000):
            s = [i for r in (rng.choice(rules) for _ in rules) for i in by[r]]
            diffs.append(prf(A["Z3"], gold, s)[2] - prf(A[best], gold, s)[2])
        diffs.sort()
        table["_bootstrap"] = {"vs": best, "diff_F1": round(table["Z3"]["F1"] - table[best]["F1"], 3),
                               "ci95": [round(diffs[49], 3), round(diffs[1949], 3)]}
    json.dump({"n": len(ids), "ambiguous": L["ambiguous"], "table": table}, open(J / "scores.json", "w"), indent=1)
    for a, v in table.items():
        print(a, v)


if __name__ == "__main__":
    main()
