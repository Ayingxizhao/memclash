"""Run the checks over a whole translation file and count the results.

Translation file (from cli.py translate):
  {"rules": [{"folder", "id", "file", "rule", "runs": [translation, ...]}], "usage": {...}}
"""

import json
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

from rules.agreement import agreement
from rules.pair import check_pair


def load_rules(path):
    """A rules file: {"folders": [{"repo" or "folder", "rules": [{"id", "file", "rule"}]}]}."""
    data = json.loads(Path(path).read_text())
    out = []
    for fo in data["folders"]:
        name = fo.get("repo", fo.get("folder"))
        out += [{"folder": name, "id": r["id"], "file": r.get("file", ""), "rule": r["rule"]}
                for r in fo["rules"]]
    return out


def statuses(rules, run):
    return Counter(r["runs"][run]["status"] for r in rules)


def check_all(rules, run=0):
    """Every pair of rules in the same folder, using translation number `run`."""
    by_folder = defaultdict(list)
    for r in rules:
        by_folder[r["folder"]].append(r)
    rows = []
    for folder, rs in by_folder.items():
        for ra, rb in combinations(rs, 2):
            verdict, detail = check_pair(ra["runs"][run], rb["runs"][run])
            if verdict != "skipped":
                rows.append({"folder": folder, "a": ra["id"], "b": rb["id"],
                             "rule_a": ra["rule"], "rule_b": rb["rule"], "verdict": verdict,
                             **detail})
    excluded = [{"folder": r["folder"], "id": r["id"], "rule": r["rule"], **r["runs"][run]}
                for r in rules if r["runs"][run]["status"] != "ok"]
    return {"counts": dict(Counter(x["verdict"] for x in rows)),
            "rule_status": dict(statuses(rules, run)),
            "pairs": rows, "excluded": excluded}


def agreement_all(rules):
    """For each rule: is the status the same in all runs, and, only when every run is `ok`,
    is the meaning the same (Z3)? Non-ok runs are not counted as "same meaning"."""
    rows = []
    for r in rules:
        st = [t["status"] for t in r["runs"]]
        all_ok = all(s == "ok" for s in st)
        rows.append({"folder": r["folder"], "id": r["id"], "rule": r["rule"], "status": st,
                     "same_status": len(set(st)) == 1,
                     "same_meaning": agreement(r["runs"]) if all_ok else None})
    ok_rows = [x for x in rows if x["same_meaning"] is not None]
    return {"rules": len(rows), "same_status": sum(x["same_status"] for x in rows),
            "all_ok": len(ok_rows), "same_meaning": sum(x["same_meaning"] for x in ok_rows),
            "rows": rows}


def estimate(rules, runs, prompt_words, out_tokens_per_call=200, retry_rate=0.1):
    """Rough token count for translating `rules` `runs` times (about 1.35 tokens per word).
    Prices are not known here; multiply by the provider's current price."""
    prompt_tokens = int(prompt_words * 1.35)
    calls = int(len(rules) * runs * (1 + retry_rate))
    rule_tokens = sum(int(len((r["file"] + " " + r["rule"]).split()) * 1.35) + 10 for r in rules)
    return {"rules": len(rules), "runs": runs, "calls": calls,
            "input_tokens": calls * prompt_tokens + int(rule_tokens * runs * (1 + retry_rate)),
            "output_tokens": calls * out_tokens_per_call}


FLAGS = ("clash", "exception", "state_conflict", "possible_clash")


def check_runs(rules):
    """Every pair in the same folder, checked in every run. A pair is reported if any run
    flags it, with its confidence (runs flagging it / runs) and the verdict of each run
    (autonomy log E6: run-to-run variance is large, so one run misses pairs)."""
    by_folder = defaultdict(list)
    for r in rules:
        by_folder[r["folder"]].append(r)
    n = len(rules[0]["runs"]) if rules else 0
    rows = []
    for folder, rs in by_folder.items():
        for ra, rb in combinations(rs, 2):
            verdicts = [check_pair(ra["runs"][k], rb["runs"][k])[0] for k in range(n)]
            k = sum(v in FLAGS for v in verdicts)
            if k:
                rows.append({"folder": folder, "a": ra["id"], "b": rb["id"], "rule_a": ra["rule"],
                             "rule_b": rb["rule"], "flagged_runs": k, "runs": n, "verdicts": verdicts})
    rows.sort(key=lambda x: -x["flagged_runs"])
    return rows
