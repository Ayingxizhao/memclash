"""Runtime enforcement experiment: build the LLM judging prompts and run the Z3 arms.

Arms (docs/review/enforce_prereg.md): A1/A2 = LLM with raw / clarified rules, B1/B2 = Z3 with
saved run 1 / reviewed translations. Action sets: A (76 invented) + B (38 log-grounded).
  uv run python -m rules.enforce_run prompts   -> data/runs/natural/enforce_judge/<arm>/<folder>.txt
  uv run python -m rules.enforce_run z3        -> data/runs/natural/enforce_judge/B1.json, B2.json
  uv run python -m rules.enforce_run deepseek ARM  (paid; one call per folder)
"""

import asyncio
import json
import sys
import time
from pathlib import Path

from rules.enforce import judge

D = Path(__file__).resolve().parents[2] / "data" / "runs" / "natural"
OUT = D / "enforce_judge"
PROMPT = Path(__file__).resolve().parents[2] / "prompts" / "review" / "enforce_judge.md"


def actions():
    a = json.load(open(D / "enforce_actions_blind.json"))["actions"]
    b = json.load(open(D / "enforce_actions_log_blind.json"))["actions"]
    return a + b


def folder_rules(arm):
    if arm == "FULL":  # preregistered secondary arm: the full original folders
        return json.load(open(D / "full_blind.json"))
    R = json.load(open(D / "rules_blind.json"))
    if arm == "A2":
        clar = {(r["folder"], r["id"]): r["clarified_rule"]
                for r in json.load(open(D / "enforce_review_final.json"))["rules"] if r["clarified_rule"]}
        R = {f: {i: {**r, "rule": clar.get((f, i), r["rule"])} for i, r in rs.items()} for f, rs in R.items()}
    return R


def prompts(arm):
    R, A = folder_rules(arm), actions()
    tpl = PROMPT.read_text()
    out = {}
    for f in sorted({a["folder"] for a in A}):
        rules = "\n".join(f"{i}: {r['rule']}" for i, r in R[f].items())
        acts = "\n".join(json.dumps({"id": a["id"], **a["event"]}) for a in A if a["folder"] == f)
        out[f] = tpl.format(rules=rules, actions=acts)
    return out


def write_prompts():
    for arm in ("A1", "A2", "FULL"):
        (OUT / arm).mkdir(parents=True, exist_ok=True)
        for f, p in prompts(arm).items():
            (OUT / arm / f"{f}.txt").write_text(p)
        print(arm, {f: len(p) for f, p in prompts(arm).items()})


def run_z3():
    T = {r["id"]: r for r in json.load(open(D / "enforce_rules.json"))["rules"]}
    F = {r["id"]: r for r in json.load(open(D / "enforce_review_final.json"))["rules"]}
    OUT.mkdir(parents=True, exist_ok=True)
    for arm, src in (("B1", {k: (v["folder"], v["run1"]) for k, v in T.items()}),
                     ("B2", {k: (v["folder"], v["translation"]) for k, v in F.items()})):
        t0, res = time.perf_counter(), []
        for a in actions():
            rules = {k: tr for k, (f, tr) in src.items() if f == a["folder"]}
            r = judge(a["event"], rules)
            res.append({"action": a["id"], "allowed": r["allowed"], "rule_ids": r["rule_ids"], "errors": r["errors"]})
        dt = time.perf_counter() - t0
        json.dump({"arm": arm, "seconds": dt, "results": res}, open(OUT / f"{arm}.json", "w"), indent=1)
        print(arm, f"{dt:.2f}s", sum(not r["allowed"] for r in res), "blocked of", len(res))


async def run_deepseek(arm):
    import os
    os.environ["LLM_PROVIDER"] = "2"
    from llm import LLM
    llm, res, t0 = LLM(), [], time.perf_counter()
    for f, p in prompts(arm).items():
        out = await llm.chat_json([{"role": "user", "content": p}])
        res += out.get("actions", [])
    dt = time.perf_counter() - t0
    json.dump({"arm": f"{arm}_deepseek", "seconds": dt, "usage": llm.usage, "results": res},
              open(OUT / f"{arm}_deepseek.json", "w"), indent=1)
    print(arm, llm.usage, f"{dt:.0f}s")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "prompts":
        write_prompts()
    elif cmd == "z3":
        run_z3()
    elif cmd == "deepseek":
        asyncio.run(run_deepseek(sys.argv[2]))
