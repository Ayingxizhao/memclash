"""Stage 1, filter: one LLM call per folder proposes the pairs worth reading.

The model sees every rule of the folder and lists the related pairs (prompts/general/filter_folder.md).
A single call is unstable, so the call is repeated: repeat 0 keeps the file order, repeat i > 0
shuffles the rule order with seed i. The candidate set is the union over the repeats. Every
relation carries its repeat number.

Usage:
  uv run python pipeline/general/filter_folder.py --run dev --rules data/dev/rules.json [--repeats 4]
Output: data/runs/<run>/filter.json (proposed pairs with label and repeat), filter_summary.json
"""

import argparse
import asyncio
import json
import random
from collections import Counter
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # shared LLM client: pipeline/llm.py

from llm import LLM

ROOT = Path(__file__).resolve().parents[2]
PROMPT = (ROOT / "prompts" / "general" / "filter_folder.md").read_text()
LABELS = ("duplicate", "contradiction", "override", "stale", "tension")


async def run(llm, rules_path, out_dir, repeats=1):
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for f in json.loads((ROOT / rules_path).read_text())["folders"]:
        name, ids = f.get("repo") or f["folder"], {r["id"] for r in f["rules"]}
        for rep in range(repeats):
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
            print(f"filter {name} [repeat {rep}]: {len(f['rules'])} rules -> {kept} relations", flush=True)
        (out_dir / "filter.json").write_text(json.dumps(results, indent=1, ensure_ascii=False))
    pairs = {(r["folder"], frozenset((r["a"], r["b"]))) for r in results}
    summary = {"model": llm.model, "repeats": repeats, "candidate_pairs": len(pairs),
               "labels": dict(Counter(r["label"] for r in results)), "usage": dict(llm.usage)}
    (out_dir / "filter_summary.json").write_text(json.dumps(summary, indent=1))
    return results


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--rules", required=True)
    ap.add_argument("--repeats", type=int, default=1)
    args = ap.parse_args()
    asyncio.run(run(LLM(), args.rules, ROOT / "data" / "runs" / args.run, args.repeats))
