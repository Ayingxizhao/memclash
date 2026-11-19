"""Injection test, steps 2 and 3: build the injected folders, then score the pipeline on them.

build: one copy of the host folder per kind (conflict_direct / conflict_reworded / paraphrase),
       each holding the real rules plus the kept injected rules of that kind. So a folder never
       contains two injected rules for the same host.
score: for every injected rule, look at its target pair (host, injected) after each stage:
       in the filter's candidate set, flagged as a conflict by the pair judge, confirmed by Z3.
       Conflicts should pass all three; paraphrases should not be reported.

Usage:
  uv run python pipeline/eval/inject_eval.py build --inject data/inject/dev_pilot.json --rules data/dev/rules.json
  uv run python pipeline/general/run_pipeline.py --run inj_pilot --rules data/inject/dev_pilot_rules.json
  uv run python pipeline/eval/inject_eval.py score --inject data/inject/dev_pilot.json --run inj_pilot
Output of score: data/runs/<run>/inject_score.json
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFLICT = ("contradiction", "override")


def build(args):
    items = [it for it in json.loads((ROOT / args.inject).read_text()) if it["keep"]]
    source = {(f.get("repo") or f["folder"]): f for f in json.loads((ROOT / args.rules).read_text())["folders"]}
    folders = []
    for name in dict.fromkeys(it["folder"] for it in items):
        for kind in dict.fromkeys(it["kind"] for it in items):
            extra = [{"id": it["id"], "file": it["file"], "quote": it["rule"], "rule": it["rule"]}
                     for it in items if it["folder"] == name and it["kind"] == kind]
            folders.append({"folder": f"{name}#{kind}", "rules": source[name]["rules"] + extra})
            print(f"{name}#{kind}: {len(source[name]['rules'])} real + {len(extra)} injected rules")
    out = ROOT / args.inject.replace(".json", "_rules.json")
    out.write_text(json.dumps({"note": "real rules plus injected rules (ids X*)", "folders": folders}, indent=1, ensure_ascii=False))
    print("->", out.relative_to(ROOT))


def score(args):
    items = [it for it in json.loads((ROOT / args.inject).read_text()) if it["keep"]]
    run_dir = ROOT / "data" / "runs" / args.run
    load = lambda file: json.loads((run_dir / file).read_text())
    key = lambda r: (r["folder"], frozenset((r["a"], r["b"])))
    cand = defaultdict(set)                                    # pair -> repeats that proposed it
    for r in load("filter.json"):
        cand[key(r)].add(r.get("repeat", 0))
    judge = {key(r): r["label"] for r in load("judge.json")}
    z3 = {key(r): r["verdict"] + (" (2nd pass)" if r.get("first_verdict") and r["verdict"] != r["first_verdict"] else "")
          for r in load("verify.json")}
    rows, table = [], defaultdict(lambda: [0, 0, 0, 0])
    for it in items:
        k = (f"{it['folder']}#{it['kind']}", frozenset((it["host"], it["id"])))
        row = {**{f: it[f] for f in ("id", "host", "pattern", "kind")}, "filter_repeats": len(cand.get(k, ())),
               "judge": judge.get(k, "-"), "z3": z3.get(k, "-")}
        row["reported"] = row["judge"] in CONFLICT and row["z3"].startswith("conflict")
        rows.append(row)
        t = table[it["kind"]]
        t[0] += 1
        t[1] += k in cand
        t[2] += row["judge"] in CONFLICT
        t[3] += row["reported"]
        print(f"{it['id']:4} {it['host']:4} {it['pattern']:10} {it['kind']:17} filter {row['filter_repeats']}  judge {row['judge']:13} z3 {row['z3']}")
    print("\nkind               n  in filter  judge flag  z3 confirmed")
    for kind, t in table.items():
        print(f"{kind:17} {t[0]:2}  {t[1]:9}  {t[2]:10}  {t[3]:12}")
    # everything else the pipeline reported in the injected folders
    injected = {it["id"] for it in items}
    side = [(f, sorted(p)) for (f, p), v in z3.items() if v.startswith("conflict") and judge.get((f, p)) in CONFLICT
            and (f, p) not in {(f"{it['folder']}#{it['kind']}", frozenset((it["host"], it["id"]))) for it in items}]
    print(f"\nother reported conflicts: {len(side)} "
          f"({sum(bool(set(p) & injected) for _, p in side)} involve an injected rule)")
    for f, p in side:
        print("  ", f.split("#")[1], *p)
    (run_dir / "inject_score.json").write_text(json.dumps({"rows": rows, "table": {k: dict(zip(("n", "filter", "judge", "z3"), v)) for k, v in table.items()},
                               "other_reported": side}, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=("build", "score"))
    ap.add_argument("--inject", required=True)
    ap.add_argument("--rules")
    ap.add_argument("--run")
    args = ap.parse_args()
    build(args) if args.step == "build" else score(args)
