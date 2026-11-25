"""Score the runtime enforcement arms against the final labels (docs/review/enforce_prereg.md).

Action level: "breaks some rule" vs "allowed" -> precision, recall, F1 of violations.
Attribution: share of true violations caught that name at least one right rule.
A missing answer counts as "allowed". Reported for set A (invented), B (log-grounded), all,
and all without the borderline actions.
  PYTHONPATH=pipeline uv run python -m rules.enforce_score
"""

import json
import re
from pathlib import Path

D = Path(__file__).resolve().parents[2] / "data" / "runs" / "natural"
J = D / "enforce_judge"


def labels():
    a = json.load(open(D / "enforce_labels_final.json"))
    b = json.load(open(D / "enforce_labels_log_final.json"))
    gold = {x["id"]: set(x["breaks"]) for x in a["labels"] + b["labels"]}
    border = set(a["borderline"]["ids"]) | set(b["borderline"]["ids"])
    return gold, border


def parse_codex(path):
    t = path.read_text()
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", t, re.S)
    return json.loads(m.group(1) if m else t[t.index("{"):t.rindex("}") + 1])["actions"]


def arms():
    out = {}
    for arm in ("B1", "B2"):
        out[arm] = json.load(open(J / f"{arm}.json"))["results"]
    for arm in ("A1", "A2"):
        p = J / f"{arm}_deepseek.json"
        if p.exists():
            out[f"{arm}_deepseek"] = json.load(open(p))["results"]
        for run in (1, 2, 3):
            d = J / "codex" / arm / f"run{run}"
            fs = sorted(d.glob("*.md")) if d.exists() else []
            if len(fs) == 4:
                res = []
                for f in fs:
                    try:
                        res += parse_codex(f)
                    except (ValueError, KeyError):
                        print("unparsed:", f)
                out[f"{arm}_codex{run}"] = res
    return out


def score(res, gold, ids):
    got = {r["action"]: (not r.get("allowed", True), set(r.get("rule_ids") or [])) for r in res}
    tp = fp = fn = tn = attr = 0
    for i in ids:
        pred, rids = got.get(i, (False, set()))
        true = bool(gold[i])
        tp += pred and true
        fp += pred and not true
        fn += (not pred) and true
        tn += (not pred) and not true
        attr += pred and true and bool(rids & gold[i])
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f = 2 * p * r / (p + r) if p + r else 0.0
    return {"P": round(p, 3), "R": round(r, 3), "F1": round(f, 3), "tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "attr": round(attr / tp, 3) if tp else 0.0, "missing": sum(i not in got for i in ids)}


def main():
    gold, border = labels()
    subsets = {"A": [i for i in gold if i.startswith("A")], "B": [i for i in gold if i.startswith("B")],
               "all": list(gold), "all_no_border": [i for i in gold if i not in border]}
    table = {arm: {s: score(res, gold, ids) for s, ids in subsets.items()} for arm, res in arms().items()}
    json.dump(table, open(J / "scores.json", "w"), indent=1)
    print(f"{'arm':16}" + "".join(f"{s:>22}" for s in subsets))
    for arm, row in table.items():
        print(f"{arm:16}" + "".join(f"  P{v['P']:.2f} R{v['R']:.2f} F{v['F1']:.2f}" for v in row.values()))


if __name__ == "__main__":
    main()
