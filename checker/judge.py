"""LLM-judge baseline: DeepSeek reads two rules together and labels the pair directly.

No schema, no solver. One call per unordered pair within a folder (prompts/judge_pair.md).
Each rule is shown with its file name, its verbatim quote, and its restatement.

Usage:
  uv run python checker/judge.py --run dev_judge --rules data/dev/rules.json [--candidates <folder judge.json>]
Output: data/runs/<run>/judge.json (every pair with its label), judge_summary.json
"""

import argparse
import asyncio
import json
from collections import Counter
from itertools import combinations
from pathlib import Path

from llm import LLM

ROOT = Path(__file__).resolve().parents[1]
PROMPT = (ROOT / "prompts" / "judge_pair.md").read_text()
LABELS = ("duplicate", "contradiction", "override", "stale", "tension", "none")


def show(tag, r):
    return f"RULE {tag} (file `{r['file']}`)\n- quote: {r['quote']}\n- rule: {r['rule']}"


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--rules", required=True)
    ap.add_argument("--candidates", help="a folder-judge judge.json: only pairs listed there are judged")
    ap.add_argument("--swap", action="store_true", help="show the two rules in reverse order (order-sensitivity test)")
    args = ap.parse_args()
    out_dir = ROOT / "data" / "runs" / args.run
    out_dir.mkdir(parents=True, exist_ok=True)
    llm, results = LLM(), []
    folders = json.loads((ROOT / args.rules).read_text())["folders"]
    keep = None
    if args.candidates:
        keep = {(r["folder"], frozenset((r["a"], r["b"]))) for r in json.loads((ROOT / args.candidates).read_text())}
    total = len(keep) if keep is not None else sum(len(f["rules"]) * (len(f["rules"]) - 1) // 2 for f in folders)
    for f in folders:
        name = f.get("repo") or f["folder"]
        for a, b in combinations(f["rules"], 2):
            if keep is not None and (name, frozenset((a["id"], b["id"]))) not in keep:
                continue
            first, second = (b, a) if args.swap else (a, b)
            msg = [{"role": "system", "content": PROMPT},
                   {"role": "user", "content": show("A", first) + "\n\n" + show("B", second)}]
            out = await llm.chat_json(msg)
            label = out.get("label") if isinstance(out, dict) and out.get("label") in LABELS else "invalid"
            results.append({"folder": name, "a": a["id"], "b": b["id"], "label": label,
                            "explanation": out.get("explanation") if isinstance(out, dict) else None})
            if len(results) % 25 == 0:
                print(f"[{len(results)}/{total}] {dict(Counter(r['label'] for r in results))}", flush=True)
                (out_dir / "judge.json").write_text(json.dumps(results, indent=1, ensure_ascii=False))
    (out_dir / "judge.json").write_text(json.dumps(results, indent=1, ensure_ascii=False))
    summary = {"run": args.run, "model": llm.model, "pairs": len(results), "swap": args.swap,
               "labels": dict(Counter(r["label"] for r in results)), "usage": llm.usage}
    (out_dir / "judge_summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    asyncio.run(main())
