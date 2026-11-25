"""Boundary stress test (docs/review/boundary_prereg.md): prompts, Z3 arm, DeepSeek arm.
  PYTHONPATH=pipeline uv run python -m rules.boundary_run prompts|z3|deepseek
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path

from rules.enforce import judge

D = Path(__file__).resolve().parents[2] / "data" / "runs" / "natural"
OUT = D / "boundary_judge"
PROMPT = Path(__file__).resolve().parents[2] / "prompts" / "review" / "enforce_judge.md"


def actions():
    return json.load(open(D / "boundary_actions_blind.json"))["actions"]


def prompts():
    R, A, tpl = json.load(open(D / "boundary_rules_blind.json")), actions(), PROMPT.read_text()
    out = {}
    for f in sorted({a["folder"] for a in A}):
        rules = "\n".join(f"{i}: {r['rule']}" for i, r in R[f].items())
        acts = "\n".join(json.dumps({"id": a["id"], **a["event"]}) for a in A if a["folder"] == f)
        out[f] = tpl.format(rules=rules, actions=acts)
    return out


def run_z3():
    T = json.load(open(D / "boundary_rules.json"))["rules"]
    t0, res = time.perf_counter(), []
    for a in actions():
        r = judge(a["event"], {x["id"]: x["translation"] for x in T if x["folder"] == a["folder"]})
        res.append({"action": a["id"], "allowed": r["allowed"], "rule_ids": r["rule_ids"], "errors": r["errors"]})
    dt = time.perf_counter() - t0
    json.dump({"arm": "Z3", "seconds": dt, "results": res}, open(OUT / "Z3.json", "w"), indent=1)
    print("Z3", f"{dt:.2f}s", sum(not r["allowed"] for r in res), "blocked", sum(bool(r["errors"]) for r in res), "errors")


async def run_deepseek():
    os.environ["LLM_PROVIDER"] = "2"
    from llm import LLM
    llm, res, t0 = LLM(), [], time.perf_counter()
    for f, p in prompts().items():
        res += (await llm.chat_json([{"role": "user", "content": p}])).get("actions", [])
    dt = time.perf_counter() - t0
    json.dump({"arm": "deepseek", "seconds": dt, "usage": llm.usage, "results": res},
              open(OUT / "deepseek.json", "w"), indent=1)
    print("deepseek", llm.usage, f"{dt:.0f}s")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    if sys.argv[1] == "prompts":
        for f, p in prompts().items():
            (OUT / f"{f}.txt").write_text(p)
        print({f: len(p) for f, p in prompts().items()})
    elif sys.argv[1] == "z3":
        run_z3()
    else:
        asyncio.run(run_deepseek())
