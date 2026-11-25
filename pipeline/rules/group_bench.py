"""Three-rule clash test (docs/review/group_bench_prereg.md).

  uv run python pipeline/rules/group_bench.py folder   # paid: one whole-folder DeepSeek call
  uv run python pipeline/rules/group_bench.py z3       # free: scan every triple with group.py
  uv run python pipeline/rules/group_bench.py score    # free
"""

import asyncio
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / "data" / "runs" / "natural"
HOST = "QuagKhai003__assessment"
EXCLUDED = {"G6", "G8"}  # disputed by the fresh label check (prereg)


def folder_rules():
    """84 rules: the 36 host rules and the 48 test rules, shuffled with a fixed seed."""
    host = json.loads((D / "rules_blind.json").read_text())[HOST]
    test = json.loads((D / "group_bench_rules.json").read_text())["rules"]
    items = [(i, r["file"], r["rule"]) for i, r in host.items()] + [(r["id"], r["file"], r["rule"]) for r in test]
    random.Random(2520).shuffle(items)
    return items


async def folder():
    from llm import LLM
    llm = LLM()
    system = (ROOT / "prompts" / "rules" / "folder_group_judge.md").read_text()
    user = "\n".join(f"{i} (file {f}): {r}" for i, f, r in folder_rules())
    out = await llm.chat_json([{"role": "system", "content": system},
                               {"role": "user", "content": user}], temperature=None, run=1)
    (D / "group_bench_folder_deepseek.json").write_text(json.dumps({**out, "usage": llm.usage}, indent=1))
    print("usage", llm.usage, "clashes", len(out.get("clashes", [])))


def z3():
    from rules.group import group_only
    from rules.pair import check_pair
    from itertools import combinations
    host = {r["id"]: r for r in json.loads((ROOT / "data/runs/rules/probe/quagkhai_3runs.json").read_text())["rules"]}
    tr = {r["id"]: r["runs"][0] for r in json.loads((D / "group_bench_translations.json").read_text())["rules"]}
    tr.update({i: host[i]["runs"][0] for i, _, _ in folder_rules() if i in host})
    from rules.group import relevant, cmds_of, ACT
    ts = [(i, tr[i]) for i, _, _ in folder_rules() if i in tr and relevant(tr[i])]
    cm = {i: cmds_of(t) for i, t in ts}
    found, pairs = [], []
    for (ia, ta), (ib, tb) in combinations(ts, 2):
        v = check_pair(ta, tb)[0]
        if v in ("clash", "exception", "state_conflict", "possible_clash"):
            pairs.append({"ids": [ia, ib], "verdict": v})
    for (ia, ta), (ib, tb), (ic, tc) in combinations(ts, 3):
        if not any(c["type"] in ACT for t in (ta, tb, tc) for c in t["clauses"]):
            continue
        if sum([bool(cm[ia] & cm[ib]), bool(cm[ia] & cm[ic]), bool(cm[ib] & cm[ic])]) < 2:
            continue
        v = group_only([ta, tb, tc])
        if v[0].startswith("group_"):
            found.append({"ids": [ia, ib, ic], "verdict": v[0], "detail": v[1]})
    status = {i: t.get("status") for i, t in tr.items() if i.startswith("T")}
    (D / "group_bench_z3.json").write_text(json.dumps({"groups": found, "pairs": pairs, "status": status},
                                                       indent=1, default=str))
    print(len(ts), "rules in scope;", len(found), "group flags;", len(pairs), "pair flags")


if __name__ == "__main__":
    {"folder": lambda: asyncio.run(folder()), "z3": z3}[sys.argv[1]]()
