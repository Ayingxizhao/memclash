"""Whole-folder LLM judge: one call per folder. The model sees every rule and lists the related pairs.

With --repeats N the call is made N times per folder. Repeat 0 keeps the file order; repeat
i > 0 shuffles the rule order with seed i, so repeats differ and are reproducible. Every
relation carries its repeat number; the candidate set of k repeats is the union of repeats < k.

Usage:
  uv run python checker/judge_folder.py --run dev_folder --rules data/dev/rules.json [--repeats 5]
Output: data/runs/<run>/judge.json (same shape as checker/judge.py, flagged pairs only)
"""

import argparse
import asyncio
import json
import random
from collections import Counter
from pathlib import Path

from llm import LLM

ROOT = Path(__file__).resolve().parents[1]
PROMPT = (ROOT / "prompts" / "judge_folder.md").read_text()
LABELS = ("duplicate", "contradiction", "override", "stale", "tension")


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--rules", required=True)
    ap.add_argument("--repeats", type=int, default=1)
    args = ap.parse_args()
    out_dir = ROOT / "data" / "runs" / args.run
    out_dir.mkdir(parents=True, exist_ok=True)
    llm, results = LLM(), []
    for f in json.loads((ROOT / args.rules).read_text())["folders"]:
        name, ids = f.get("repo") or f["folder"], {r["id"] for r in f["rules"]}
        for rep in range(args.repeats):
            rules = list(f["rules"])
            if rep:
                random.Random(rep).shuffle(rules)
            listing = "\n".join(f"{r['id']} (file `{r['file']}`): {r['rule']}\n    quote: {r['quote']}" for r in rules)
            out = await llm.chat_json([{"role": "system", "content": PROMPT}, {"role": "user", "content": listing}])
            kept = 0
            for rel in (out.get("relations") or []) if isinstance(out, dict) else []:
                ok = isinstance(rel, dict) and rel.get("a") in ids and rel.get("b") in ids and rel["a"] != rel["b"] and rel.get("label") in LABELS
                if ok:
                    kept += 1
                    results.append({"folder": name, "a": rel["a"], "b": rel["b"], "label": rel["label"],
                                    "repeat": rep, "explanation": rel.get("explanation")})
            print(f"{name} [repeat {rep}]: {len(f['rules'])} rules -> {kept} relations", flush=True)
        (out_dir / "judge.json").write_text(json.dumps(results, indent=1, ensure_ascii=False))
    summary = {"run": args.run, "model": llm.model, "repeats": args.repeats, "labels": dict(Counter(r["label"] for r in results)), "usage": llm.usage}
    (out_dir / "judge_summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    asyncio.run(main())
