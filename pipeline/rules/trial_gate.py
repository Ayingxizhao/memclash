"""Gate for the agent trial: hooks and stub tools call this before a gateable act.

  python -m rules.trial_gate <aux_dir> '<event json>'
Logs every decision to <aux>/hooklog.jsonl. Exit 1 (= block) only when <aux>/policy.json has
"gate": true and Z3 finds a broken compiled rule; otherwise exit 0.
"""

import json
import sys
import time
from pathlib import Path

from rules.enforce import judge

RULES = Path(__file__).resolve().parents[2] / "data" / "runs" / "natural" / "boundary_rules.json"


def rules_for(folder):
    return {r["id"]: r["translation"] for r in json.load(open(RULES))["rules"] if r["folder"] == folder}


def english(folder):
    return {r["id"]: r["rule"] for r in json.load(open(RULES))["rules"] if r["folder"] == folder}


def decide(aux, ev):
    cfg = json.load(open(Path(aux) / "policy.json"))
    full = {"branch": "", "path": None, "dest_path": None, "kind": "file", "task": None,
            "running": [], "prior": [], **ev}
    full["flags"] = {**cfg["flags"], **ev.get("flags", {})}
    paths = ev.get("paths") or [ev.get("path")]
    hits = {}
    for p in paths:
        r = judge({**full, "path": p}, rules_for(cfg["folder"]))
        for rid in r["rule_ids"]:
            hits.setdefault(rid, []).append(p)
    blocked = bool(hits) and cfg.get("gate", False)
    with open(Path(aux) / "hooklog.jsonl", "a") as f:
        f.write(json.dumps({"t": time.time(), "src": "gate", "event": ev, "breaks": sorted(hits),
                            "blocked": blocked}) + "\n")
    return blocked, hits, english(cfg["folder"])


def main():
    aux, ev = sys.argv[1], json.loads(sys.argv[2])
    blocked, hits, en = decide(aux, ev)
    if blocked:
        print("BLOCKED by the project policy gate. This action breaks:", file=sys.stderr)
        for rid in sorted(hits):
            print(f"  - {en[rid]}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
