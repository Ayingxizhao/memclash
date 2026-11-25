"""Natural-pair test: LLM alone vs Z3 vs hybrids on real folders (docs/review/natural_test.md).

  uv run python pipeline/rules/natural_test.py folder    # paid: one whole-folder LLM call per folder
  uv run python pipeline/rules/natural_test.py verify    # paid: pairwise LLM judge on candidate pairs
  uv run python pipeline/rules/natural_test.py score     # no calls

Pairs: every same-folder pair among rules with saved 3-run translations
(data/runs/natural/pairs_all.json, built from the probe, dev and frozen runs); `z3` holds the
verdict of each saved run, so the Z3 arms cost nothing.
"""

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / "data" / "runs" / "natural"
FLAG = ("clash", "exception", "state_conflict", "possible_clash")


def key(folder, a, b):
    return (folder, *sorted((a, b)))


def load_pairs():
    return json.loads((D / "pairs_all.json").read_text())["pairs"]


async def folder(full_names=None):
    """One whole-folder call per folder. full_names: run on the FULL folders with these names
    (data/runs/natural/full_blind.json) instead of the 84-rule subset; results are merged into
    folder_full_deepseek.json."""
    from llm import LLM
    llm = LLM()
    system = (ROOT / "prompts" / "rules" / "folder_judge.md").read_text()
    if full_names:
        allr = json.loads((D / "full_blind.json").read_text())
        rules = {n: allr[n] for n in full_names}
        outp = D / "folder_full_deepseek.json"
        prev = json.loads(outp.read_text()) if outp.exists() else {"pairs": [], "usage": {}, "folders": []}

        async def one_full(f, rs):
            user = "\n".join(f"{i} (file {r['file']}): {r['rule']}" for i, r in rs.items())
            out = await llm.chat_json([{"role": "system", "content": system},
                                       {"role": "user", "content": user}], temperature=None, run=1)
            return [{"folder": f, **p} for p in out.get("pairs", [])]
        res = await asyncio.gather(*(one_full(f, rs) for f, rs in rules.items()))
        prev["pairs"] = [p for p in prev["pairs"] if p["folder"] not in rules] + [p for r in res for p in r]
        prev["folders"] = sorted(set(prev["folders"]) | set(rules))
        prev["usage"][",".join(full_names)] = llm.usage
        outp.write_text(json.dumps(prev, indent=1))
        print("usage", llm.usage, "flagged", sum(map(len, res)))
        return
    rules = json.loads((D / "rules_blind.json").read_text())

    async def one(f, rs):
        user = "\n".join(f"{i} (file {r['file']}): {r['rule']}" for i, r in rs.items())
        out = await llm.chat_json([{"role": "system", "content": system},
                                   {"role": "user", "content": user}], temperature=None, run=1)
        return [{"folder": f, **p} for p in out.get("pairs", [])]

    res = await asyncio.gather(*(one(f, rs) for f, rs in rules.items()))
    flat = [p for r in res for p in r]
    (D / "folder_deepseek.json").write_text(json.dumps({"pairs": flat, "usage": llm.usage}, indent=1))
    print("usage", llm.usage, "flagged", len(flat))


def candidates():
    """Pairs any cheap arm flags: Z3 in any saved run, or the whole-folder LLM."""
    pairs = {key(p["folder"], p["a"], p["b"]): p for p in load_pairs()}
    out = {k for k, p in pairs.items() if any(v in FLAG for v in p["z3"])}
    fd = D / "folder_deepseek.json"
    if fd.exists():
        out |= {key(p["folder"], p["a"], p["b"]) for p in json.loads(fd.read_text())["pairs"]}
    return [pairs[k] for k in sorted(out) if k in pairs]


async def verify():
    from llm import LLM
    llm = LLM()
    judge = (ROOT / "prompts" / "rules" / "pair_judge.md").read_text()
    cands = candidates()

    async def one(p):
        user = f"RULE A (file {p['file_a']}): {p['rule_a']}\nRULE B (file {p['file_b']}): {p['rule_b']}"
        out = await llm.chat_json([{"role": "system", "content": judge},
                                   {"role": "user", "content": user}], temperature=None, run=1)
        return {"folder": p["folder"], "a": p["a"], "b": p["b"], **out}

    res = await asyncio.gather(*(one(p) for p in cands))
    (D / "verify_deepseek.json").write_text(json.dumps({"pairs": res, "usage": llm.usage}, indent=1))
    print("usage", llm.usage, "checked", len(res))


def flagged(path, field="verdict"):
    p = D / path
    if not p.exists():
        return None
    return {key(x["folder"], x["a"], x["b"]) for x in json.loads(p.read_text())["pairs"]
            if x.get(field, "clash") in FLAG}


def score():
    pairs = load_pairs()
    gold = json.loads((D / "gold.json").read_text())
    pos = {key(g["folder"], g["a"], g["b"]) for g in gold["pairs"] if g["label"] == "clash"}
    amb = {key(g["folder"], g["a"], g["b"]) for g in gold["pairs"] if g["label"] == "ambiguous"}
    z3 = {key(p["folder"], p["a"], p["b"]): p["z3"] for p in pairs}
    allk = set(z3)
    arms = {
        "Z3 run 1": {k for k, v in z3.items() if v[0] in FLAG},
        "Z3 >=2 of 3": {k for k, v in z3.items() if sum(x in FLAG for x in v) >= 2},
        "Z3 any of 3": {k for k, v in z3.items() if any(x in FLAG for x in v)},
    }
    for name, path in [("Codex whole-folder", "screen_codex.json"),
                       ("DeepSeek whole-folder", "folder_deepseek.json")]:
        s = flagged(path)
        if s is not None:
            arms[name] = s
    ver = flagged("verify_deepseek.json")
    if ver is not None:
        arms["Z3 any, DeepSeek-verified"] = arms["Z3 any of 3"] & ver
        if "DeepSeek whole-folder" in arms:
            arms["DeepSeek folder, verified"] = arms["DeepSeek whole-folder"] & ver
            arms["(Z3 any or DS folder), verified"] = (arms["Z3 any of 3"] | arms["DeepSeek whole-folder"]) & ver
    print(f"{len(allk)} pairs; {len(pos)} clashes, {len(amb)} ambiguous (ambiguous excluded from both counts)")
    print(f"{'arm':34} found  false-alarms  flagged-ambiguous")
    summary = {}
    for name, s in arms.items():
        s = s & allk
        tp, fp, a = len(s & pos), len(s - pos - amb), len(s & amb)
        summary[name] = {"found": tp, "of": len(pos), "false_alarms": fp, "ambiguous_flagged": a,
                         "flagged": sorted("|".join(k) for k in s)}
        print(f"{name:34} {tp}/{len(pos)}   {fp:>5}         {a}")
    (D / "score.json").write_text(json.dumps(summary, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "score":
        score()
    elif cmd == "folder" and len(sys.argv) > 2:   # folder NAME [NAME...]: full folders
        asyncio.run(folder(sys.argv[2:]))
    else:
        asyncio.run({"folder": folder, "verify": verify}[cmd]())
