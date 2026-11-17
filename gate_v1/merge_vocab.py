"""Merge step: find behaviors that mean the same but got different names.

Follows the pattern of ARc (cluster variable descriptions by embedding similarity) and EDC
(embeddings shortlist candidates, an LLM confirms):
  1. Every behavior used in a run becomes one item: a bool action, or one value of an enum
     action ("math_notation=latex"). Its text = name + definition + one example rule.
  2. Embed the items (bge-m3) and shortlist each item's nearest neighbors.
  3. DeepSeek judges each shortlisted pair: same / opposite / different.
  4. "same" pairs are joined into clusters; each cluster gets one canonical name.
Embeddings alone are not trusted: opposites ("use LaTeX" / "use plain text") sit close together.

Usage:
  uv run python gate_v1/merge_vocab.py --run dev_v1 [--candidates-only]
Output: data/runs/<run>/merges.json
"""

import argparse
import asyncio
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pipeline"))  # shared LLM client
from llm import LLM

from validate import Vocab

ROOT = Path(__file__).resolve().parents[1]
EMBED_MODEL = "bge-m3"
TOP_K, MIN_SIM = 3, 0.55
PROMPT = """Two behaviors from a vocabulary that describes rules for a coding agent are shown, each with
its definition and an example rule that was encoded with it. Decide their relation:
- "same": doing one IS doing the other; a rule requiring A and a rule requiring B demand the
  same thing. Different wording or level of detail does not matter.
- "opposite": doing one means NOT doing the other.
- "different": anything else, including same topic but different behavior.
Return JSON: {"relation": "same|opposite|different", "reason": "one sentence"}"""


def behaviors(rows, vocab):
    """item key -> {text, example, folders}. Int actions are skipped (numbers are compared, not merged)."""
    items = {}
    for r in rows:
        if r["status"] != "valid":
            continue
        act = r["record"]["action"]
        spec = vocab.actions[act["name"]]
        if spec["type"] == "int":
            continue
        key = act["name"] if spec["type"] == "bool" else f"{act['name']}={act['value']}"
        it = items.setdefault(key, {"doc": spec.get("doc", ""), "example": r["rule"], "folders": set(), "n": 0})
        it["folders"].add(r["folder"])
        it["n"] += 1
    for key, it in items.items():
        it["text"] = f"{key.replace('_', ' ').replace('=', ' is ')}. {it['doc']} Example rule: {it['example']}"
    return items


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--candidates-only", action="store_true", help="stop after the embedding shortlist")
    args = ap.parse_args()
    run_dir = ROOT / "data" / "runs" / args.run
    rows = json.loads((run_dir / "records.json").read_text())
    vocab = Vocab()
    for t in json.loads((run_dir / "vocab_additions.json").read_text()):
        vocab.add({k: v for k, v in t.items() if k != "source"}, t["source"])
    items = behaviors(rows, vocab)
    keys = list(items)

    llm = LLM()
    resp = await llm.client.embeddings.create(model=EMBED_MODEL, input=[items[k]["text"] for k in keys])
    vecs = [d.embedding for d in resp.data]
    norm = [sum(x * x for x in v) ** 0.5 for v in vecs]
    sim = lambda i, j: sum(a * b for a, b in zip(vecs[i], vecs[j])) / (norm[i] * norm[j])

    cands = {}
    for i in range(len(keys)):
        near = sorted(((sim(i, j), j) for j in range(len(keys)) if j != i), reverse=True)[:TOP_K]
        for s, j in near:
            # only behaviors used in a common folder can meet in a pair check
            if s >= MIN_SIM and items[keys[i]]["folders"] & items[keys[j]]["folders"]:
                cands[tuple(sorted((keys[i], keys[j])))] = round(s, 3)
    cands = sorted(cands.items(), key=lambda kv: -kv[1])
    print(f"{len(keys)} behaviors, {len(cands)} candidate pairs")
    out = {"run": args.run, "behaviors": len(keys), "candidates": [{"a": a, "b": b, "sim": s} for (a, b), s in cands]}

    if not args.candidates_only:
        parent = {k: k for k in keys}

        def find(k):
            while parent[k] != k:
                k = parent[k]
            return k

        for c in out["candidates"]:
            a, b = items[c["a"]], items[c["b"]]
            msg = [{"role": "system", "content": PROMPT},
                   {"role": "user", "content": f"A: {c['a']}\n  definition: {a['doc']}\n  example: {a['example']}\n\n"
                                               f"B: {c['b']}\n  definition: {b['doc']}\n  example: {b['example']}"}]
            ans = await llm.chat_json(msg)
            c["relation"], c["reason"] = ans.get("relation"), ans.get("reason")
            print(f"{c['sim']:.2f} {c['relation']:9} {c['a']}  <->  {c['b']}", flush=True)
            if c["relation"] == "same":
                parent[find(c["a"])] = find(c["b"])
        clusters = {}
        for k in keys:
            clusters.setdefault(find(k), []).append(k)
        out["clusters"] = [sorted(v, key=lambda k: -items[k]["n"]) for v in clusters.values() if len(v) > 1]
        # alias: every member -> the most used member of its cluster
        out["alias"] = {k: c[0] for c in out["clusters"] for k in c[1:]}
    (run_dir / "merges.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    for c in out["candidates"][:40]:
        if args.candidates_only:
            print(f"{c['sim']:.2f}  {c['a']}  <->  {c['b']}")


if __name__ == "__main__":
    asyncio.run(main())
