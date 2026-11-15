"""Score a system's flagged pairs against human pair labels; append one row to data/results.jsonl.

A "conflict" is a pair labelled contradiction or override. Two views are reported:
  conflict  system says contradiction/override  vs  human says contradiction/override
  issue     system flags anything but duplicate vs  human records anything but duplicate
            (human "other", "stale", "tension" count here)
plus duplicate (both say duplicate).

Usage:
  uv run python checker/score.py --name dev_judge --pred data/runs/dev_judge/judge.json \
      --labels data/open_coding/agent_a.json
"""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFLICT = {"contradiction", "override"}


def pairs(rows, folder_key):
    return {(r[folder_key], frozenset((r["a"], r["b"]))): r["label"] for r in rows
            if r.get("a") and r.get("b") and r.get("label") not in (None, "none", "invalid")}


def prf(pred, gold):
    tp = len(pred & gold)
    p = tp / len(pred) if pred else 0.0
    r = tp / len(gold) if gold else 0.0
    f = 2 * p * r / (p + r) if p + r else 0.0
    return {"tp": tp, "flagged": len(pred), "labelled": len(gold), "precision": round(p, 3), "recall": round(r, 3), "f1": round(f, 3)}


def score(pred_path, labels_path):
    pred = pairs(json.loads((ROOT / pred_path).read_text()), "folder")
    gold = {}
    for f in json.loads((ROOT / labels_path).read_text())["folders"]:
        gold.update(pairs([{**r, "folder": f["repo"]} for r in f["relations"]], "folder"))
    view = lambda d, keep: {k for k, v in d.items() if keep(v)}
    return {"conflict": prf(view(pred, lambda v: v in CONFLICT), view(gold, lambda v: v in CONFLICT)),
            "issue": prf(view(pred, lambda v: v != "duplicate"), view(gold, lambda v: v != "duplicate")),
            "duplicate": prf(view(pred, lambda v: v == "duplicate"), view(gold, lambda v: v == "duplicate"))}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--pred", required=True)
    ap.add_argument("--labels", required=True)
    ap.add_argument("--no-log", action="store_true")
    args = ap.parse_args()
    row = {"name": args.name, "pred": args.pred, "labels": args.labels, **score(args.pred, args.labels)}
    for k in ("conflict", "issue", "duplicate"):
        print(f"{args.name:14} {k:9} {row[k]}")
    if not args.no_log:
        with (ROOT / "data" / "results.jsonl").open("a") as fh:
            fh.write(json.dumps(row) + "\n")
