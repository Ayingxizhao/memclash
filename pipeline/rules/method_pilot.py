"""Precommitted 20-pair comparison (docs/review/method_audit.md; Codex audit pilot 3).

  uv run python pipeline/rules/method_pilot.py run     # paid: direct judge + joint translation
  uv run python pipeline/rules/method_pilot.py score   # no calls; also scores the current method

Methods on the same pairs (data/runs/method_pilot/pairs.json, gold fixed beforehand):
- current: rule-alone two-step translations already saved (3 runs), Z3 per run;
- direct: one LLM call per pair, verdict under the ADR 0003 definition (prompts/rules/pair_judge.md);
- joint: each rule translated (one-step template) with the other rule shown as context so
  shared names line up, then Z3.
"""

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rules.pair import check_pair  # noqa: E402
from rules.translate import load, translate_rule  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / "data" / "runs" / "method_pilot"
FLAG = ("clash", "exception", "state_conflict", "possible_clash")
JOINT_NOTE = ("\n\n## Context rule\nAn OTHER RULE from the same folder is shown after the rule, "
              "only so that you name shared conditions, paths, branches and tasks with the same "
              "words. Translate only RULE.")
SOURCES = [ROOT / "data/runs/rules/pilot/B21f_3runs.json", ROOT / "data/runs/rules/probe/quagkhai_3runs.json",
           ROOT / "data/runs/rules/label_set/FINAL_v21_two_step.json"]


def current_translations():
    out = {}
    for p in SOURCES:
        for r in json.loads(p.read_text())["rules"]:
            out.setdefault((r["folder"], r["id"]), r["runs"])
    return out


async def run():
    from llm import LLM
    llm = LLM()
    pairs = json.loads((D / "pairs.json").read_text())["pairs"]
    judge = (ROOT / "prompts" / "rules" / "pair_judge.md").read_text()
    prompt, validator = load()

    async def one(p):
        user = (f"RULE A (file {p['file_a']}): {p['rule_a']}\nRULE B (file {p['file_b']}): {p['rule_b']}")
        direct = await llm.chat_json([{"role": "system", "content": judge},
                                      {"role": "user", "content": user}], temperature=None, run=1)
        ja = await translate_rule(llm, prompt + JOINT_NOTE, validator, p["file_a"],
                                  p["rule_a"] + f"\nOTHER RULE (context only): {p['rule_b']}", run=1)
        jb = await translate_rule(llm, prompt + JOINT_NOTE, validator, p["file_b"],
                                  p["rule_b"] + f"\nOTHER RULE (context only): {p['rule_a']}", run=1)
        return {"pair": p["pair"], "direct": direct, "joint": [ja, jb]}

    res = await asyncio.gather(*(one(p) for p in pairs))
    (D / "results.json").write_text(json.dumps({"results": res, "usage": llm.usage}, indent=1))
    print("usage", llm.usage)


def score():
    pairs = json.loads((D / "pairs.json").read_text())["pairs"]
    res = {r["pair"]: r for r in json.loads((D / "results.json").read_text())["results"]}
    cur = current_translations()
    rows = []
    for p in pairs:
        ra, rb = cur.get((p["folder"], p["a"])), cur.get((p["folder"], p["b"]))
        cur_v = [check_pair(ra[k], rb[k])[0] for k in range(3)] if ra and rb else ["missing"] * 3
        r = res[p["pair"]]
        joint_v = check_pair(*r["joint"])[0]
        rows.append({"pair": p["pair"], "gold": p["gold"], "current_runs": cur_v,
                     "direct": r["direct"].get("verdict"), "direct_why": r["direct"].get("situation", ""),
                     "joint": joint_v})
    pos = [x for x in rows if x["gold"] != "compatible"]
    neg = [x for x in rows if x["gold"] == "compatible"]

    def rate(xs, f):
        return f"{sum(map(f, xs))}/{len(xs)}"
    methods = {
        "current, run 1": lambda x: x["current_runs"][0] in FLAG,
        "current, any of 3 runs": lambda x: any(v in FLAG for v in x["current_runs"]),
        "current, >=2 of 3 runs": lambda x: sum(v in FLAG for v in x["current_runs"]) >= 2,
        "direct LLM judge": lambda x: x["direct"] in FLAG,
        "joint translation + Z3": lambda x: x["joint"] in FLAG,
    }
    print(f"{'method':26} found (of {len(pos)} clashes)   false alarms (of {len(neg)} compatible)")
    summary = {}
    for name, f in methods.items():
        summary[name] = {"found": sum(map(f, pos)), "false_alarms": sum(map(f, neg))}
        print(f"{name:26} {rate(pos, f):>10}                {rate(neg, f):>6}")
    (D / "score.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1))
    for x in rows:
        print(x["pair"], x["gold"], "| current", x["current_runs"], "| direct", x["direct"], "| joint", x["joint"])


if __name__ == "__main__":
    asyncio.run(run()) if sys.argv[1] == "run" else score()
