"""Stage 2, pair judge: the LLM reads two rules together and labels the pair.

One call per pair (prompts/general/judge_pair.md). Each rule is shown with its file name, its verbatim
quote, and its restatement. With --candidates only the pairs proposed by stage 1 are judged;
without it every pair of a folder is judged (the all-pairs baseline).

Usage:
  uv run python pipeline/general/judge_pair.py --run dev --rules data/dev/rules.json \
      [--candidates data/runs/dev/filter.json]
Output: data/runs/<run>/judge.json (every judged pair with its label), judge_summary.json
"""

import argparse
import asyncio
import json
from collections import Counter
from itertools import combinations
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # shared LLM client: pipeline/llm.py

from llm import LLM

ROOT = Path(__file__).resolve().parents[2]
PROMPT = (ROOT / "prompts" / "general" / "judge_pair.md").read_text()
LABELS = ("duplicate", "contradiction", "override", "stale", "tension", "none")


def show(tag, r):
    return f"RULE {tag} (file `{r['file']}`)\n- quote: {r['quote']}\n- rule: {r['rule']}"


async def run(llm, rules_path, out_dir, candidates=None, swap=False):
    """candidates: path of a filter.json, or None for all pairs. swap: show the rules in reverse order."""
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    folders = json.loads((ROOT / rules_path).read_text())["folders"]
    keep = None
    if candidates:
        keep = {(r["folder"], frozenset((r["a"], r["b"]))) for r in json.loads((ROOT / candidates).read_text())}
    total = len(keep) if keep is not None else sum(len(f["rules"]) * (len(f["rules"]) - 1) // 2 for f in folders)
    for f in folders:
        name = f.get("repo") or f["folder"]
        for a, b in combinations(f["rules"], 2):
            if keep is not None and (name, frozenset((a["id"], b["id"]))) not in keep:
                continue
            first, second = (b, a) if swap else (a, b)
            out = await llm.chat_json([{"role": "system", "content": PROMPT},
                                       {"role": "user", "content": show("A", first) + "\n\n" + show("B", second)}])
            label = out.get("label") if isinstance(out, dict) and out.get("label") in LABELS else "invalid"
            results.append({"folder": name, "a": a["id"], "b": b["id"], "label": label,
                            "explanation": out.get("explanation") if isinstance(out, dict) else None})
            if len(results) % 25 == 0:
                print(f"judge [{len(results)}/{total}] {dict(Counter(r['label'] for r in results))}", flush=True)
                (out_dir / "judge.json").write_text(json.dumps(results, indent=1, ensure_ascii=False))
    (out_dir / "judge.json").write_text(json.dumps(results, indent=1, ensure_ascii=False))
    summary = {"model": llm.model, "pairs": len(results), "swap": swap, "candidates": candidates,
               "labels": dict(Counter(r["label"] for r in results)), "usage": dict(llm.usage)}
    (out_dir / "judge_summary.json").write_text(json.dumps(summary, indent=1))
    print(f"judge: {summary['pairs']} pairs {summary['labels']}", flush=True)
    return results


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--rules", required=True)
    ap.add_argument("--candidates", help="a filter.json: only pairs listed there are judged")
    ap.add_argument("--swap", action="store_true", help="show the two rules in reverse order (order-sensitivity test)")
    args = ap.parse_args()
    asyncio.run(run(LLM(), args.rules, ROOT / "data" / "runs" / args.run, args.candidates, args.swap))
