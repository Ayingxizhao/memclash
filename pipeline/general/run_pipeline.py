"""Run the three stages on a rule list, into ONE run folder.

  1. filter_folder   one call per folder (repeated), proposes candidate pairs   -> filter.json
  2. judge_pair      one call per candidate pair, labels it                     -> judge.json
  3. verify_pair     formalizes each pair the judge calls a conflict; Z3 decides -> verify.json
A pair is reported when the judge labels it contradiction/override AND Z3 says conflict.

Usage:
  uv run python pipeline/general/run_pipeline.py --run dev_pipeline --rules data/dev/rules.json [--repeats 4]
Output in data/runs/<run>/: filter.json, judge.json, verify.json, reported.json, summary.json
  reported.json has the shape score.py expects (folder, a, b, label).
"""

import argparse
import asyncio
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # shared LLM client: pipeline/llm.py

import filter_folder
import judge_pair
import verify_pair
from llm import LLM

ROOT = Path(__file__).resolve().parents[2]
CONFLICT = ("contradiction", "override")


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--rules", required=True)
    ap.add_argument("--repeats", type=int, default=4, help="repeats of the folder call in stage 1")
    args = ap.parse_args()
    out_dir = ROOT / "data" / "runs" / args.run
    rel = lambda name: str((out_dir / name).relative_to(ROOT))
    llm = LLM()
    proposed = await filter_folder.run(llm, args.rules, out_dir, args.repeats)
    judged = await judge_pair.run(llm, args.rules, out_dir, candidates=rel("filter.json"))
    verified = await verify_pair.run(llm, args.rules, out_dir, rel("judge.json"))

    label = {(r["folder"], r["a"], r["b"]): r["label"] for r in judged}
    reported = [{"folder": v["folder"], "a": v["a"], "b": v["b"],
                 "label": label.get((v["folder"], v["a"], v["b"])) or label.get((v["folder"], v["b"], v["a"])),
                 "witness": v.get("witness"), "rule_a": v["rule_a"], "rule_b": v["rule_b"]}
                for v in verified if v["verdict"] == "conflict"]
    (out_dir / "reported.json").write_text(json.dumps(reported, indent=1, ensure_ascii=False))
    folders = json.loads((ROOT / args.rules).read_text())["folders"]
    summary = {"run": args.run, "rules": args.rules, "model": llm.model, "repeats": args.repeats,
               "all_pairs": sum(len(f["rules"]) * (len(f["rules"]) - 1) // 2 for f in folders),
               "candidate_pairs": len({(r["folder"], frozenset((r["a"], r["b"]))) for r in proposed}),
               "judge_conflict_flags": sum(r["label"] in CONFLICT for r in judged),
               "reported": len(reported), "usage": llm.usage}
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    asyncio.run(main())
