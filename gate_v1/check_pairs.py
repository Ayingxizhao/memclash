"""Stage B: check every rule pair of a folder with Z3.

Labels (same order as prompts/label_pairs.md; stale and tension are not formalized):
  none           different actions, or the scopes cannot both hold
  contradiction  scopes overlap and the two demands cannot both be met
  override       contradiction pattern, and one scope lies strictly inside the other
  duplicate      same demand, and the scopes are equal or one contains the other
A flag is `soft` when one of the two rules is only a preference (Pref).

Usage:  uv run python gate_v1/check_pairs.py --run own_v3
Input:  data/runs/<run>/records.json, vocab_additions.json
Output: data/runs/<run>/flags.json, pairs_summary.json
"""

import argparse
import json
from collections import Counter
from itertools import combinations
from pathlib import Path

from z3 import Not, Solver, Xor, sat

from encode import World
from validate import Vocab

ROOT = Path(__file__).resolve().parents[1]
MOD_CLASS = {"O": "require", "Pref": "require", "F": "forbid", "P": "permit"}


def is_sat(*fs):
    s = Solver()
    s.add(*fs)
    return s.check() == sat


def check(world, a, b):
    """a, b: records. Return (label, detail dict)."""
    if world.canonical(a["action"])[0] != world.canonical(b["action"])[0]:
        return "none", {}
    sa, sb = world.scope(a), world.scope(b)
    if not is_sat(sa, sb):
        return "none", {}
    ea, eb = world.effect(a), world.effect(b)
    a_in_b, b_in_a = not is_sat(sa, Not(sb)), not is_sat(sb, Not(sa))
    ca, cb = MOD_CLASS[a["modality"]], MOD_CLASS[b["modality"]]
    soft = "Pref" in (a["modality"], b["modality"])

    if not (ca == cb == "permit") and not is_sat(sa, sb, ea, eb):
        if a_in_b != b_in_a:                       # strict containment: the narrower rule wins
            return "override", {"specific": "a" if a_in_b else "b", "soft": soft}
        return "contradiction", {"soft": soft}
    if ca == cb and not is_sat(Xor(ea, eb)) and (a_in_b or b_in_a):
        subsumed = None if (a_in_b and b_in_a) else ("a" if a_in_b else "b")
        return "duplicate", {"subsumed": subsumed}
    return "none", {}


def run(run_name, use_merges=True, out="flags"):
    run_dir = ROOT / "data" / "runs" / run_name
    rows = json.loads((run_dir / "records.json").read_text())
    vocab = Vocab()
    for t in json.loads((run_dir / "vocab_additions.json").read_text()):
        vocab.add({k: v for k, v in t.items() if k != "source"}, t["source"])
    merges = run_dir / "merges.json"                 # optional output of merge_vocab.py
    alias = json.loads(merges.read_text()).get("alias", {}) if merges.exists() and use_merges else {}
    world = World(vocab, alias)

    valid = [r for r in rows if r["status"] == "valid"]
    glob = [r for r in valid if r["folder"] == "global"]
    folders = list(dict.fromkeys(r["folder"] for r in rows))
    flags, per_folder = [], {}
    for folder in folders:
        own = [r for r in valid if r["folder"] == folder]
        # global rules are loaded in every session: pair them with each folder's rules;
        # global-global pairs are reported once, under "global"
        pairs = list(combinations(own, 2))
        if folder != "global":
            pairs += [(g, r) for g in glob for r in own]
        count = Counter()
        for a, b in pairs:
            label, detail = check(world, a["record"], b["record"])
            count[label] += 1
            if label == "none":
                continue
            for key in ("specific", "subsumed"):
                if detail.get(key):
                    detail[key] = (a if detail[key] == "a" else b)["id"]
            flags.append({"folder": folder, "a": a["id"], "b": b["id"], "label": label, **detail,
                          "action": a["record"]["action"]["name"],
                          "rule_a": a["rule"], "rule_b": b["rule"]})
        per_folder[folder] = {"rules_checked": len(own), "pairs": len(pairs),
                              "unchecked_rules": sum(r["folder"] == folder and r["status"] != "valid" for r in rows),
                              **{k: count[k] for k in ("duplicate", "contradiction", "override")}}

    total = Counter(f["label"] for f in flags)
    summary = {"run": run_name, "pairs": sum(f["pairs"] for f in per_folder.values()),
               "flags": len(flags), **{k: total[k] for k in ("duplicate", "contradiction", "override")},
               "folders": per_folder}
    (run_dir / f"{out}.json").write_text(json.dumps(flags, indent=1, ensure_ascii=False))
    (run_dir / "pairs_summary.json").write_text(json.dumps(summary, indent=1))
    return flags, summary


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--no-merges", action="store_true", help="ignore merges.json")
    args = ap.parse_args()
    flags, summary = run(args.run, use_merges=not args.no_merges)
    for f in flags:
        extra = " (soft)" if f.get("soft") else ""
        print(f"{f['label']:13}{extra} {f['folder'][-22:]:22} {f['a']:>4} <-> {f['b']:<4} [{f['action']}]")
        print(f"      a: {f['rule_a'][:110]}\n      b: {f['rule_b'][:110]}")
    print(json.dumps({k: v for k, v in summary.items() if k != "folders"}, indent=1))
