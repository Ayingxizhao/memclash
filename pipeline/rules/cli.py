"""Commands for the git and file rule checker (docs/adr/0008).

  uv run python pipeline/rules/cli.py estimate  --rules data/dev/rules.json --runs 3
  uv run python pipeline/rules/cli.py translate --rules data/dev/rules.json --runs 3 \
      --out data/runs/rules/dev/translations.json [--folder NAME]
  uv run python pipeline/rules/cli.py check     --translations .../translations.json --out .../check.json
  uv run python pipeline/rules/cli.py agreement --translations .../translations.json --out .../agreement.json
  uv run python pipeline/rules/cli.py compare-old --translations data/runs/git/git_pilot/translate.json
  uv run python pipeline/rules/cli.py report    --translations .../translations.json --folder NAME --out demo/memclash/reports/x.json

Only `translate` calls the LLM (and costs money); the rest run locally. Tests: uv run pytest
"""

import argparse
import asyncio
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # pipeline/: rules.*, llm

from rules import report  # noqa: E402
from rules.translate import PROMPT, translate_all  # noqa: E402


def write(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj, indent=1))


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("estimate", "translate"):
        p = sub.add_parser(name)
        p.add_argument("--rules", required=True)
        p.add_argument("--runs", type=int, default=3)
        p.add_argument("--folder", help="only folders whose name contains this")
        if name == "translate":
            p.add_argument("--out", required=True)
            p.add_argument("--mode", choices=["one_step", "two_step"], default="one_step")
    for name in ("check", "agreement"):
        p = sub.add_parser(name)
        p.add_argument("--translations", required=True)
        p.add_argument("--out", required=True)
        if name == "check":
            p.add_argument("--run", type=int, default=1, help="which translation run (1, 2, 3)")
    p = sub.add_parser("score-labels", help="score translations against the frozen labelled set")
    p.add_argument("--translations", required=True)
    p.add_argument("--labels", default="data/runs/survey_rules/label_set/frozen_2026-11-22.json")
    p.add_argument("--split", help="only labels with this split (dev set: iterate / validate)")
    p.add_argument("--out", required=True)
    p = sub.add_parser("report", help="write a report file for the memclash interface")
    p.add_argument("--translations", required=True)
    p.add_argument("--folder", required=True)
    p.add_argument("--run", type=int, default=1)
    p.add_argument("--out", required=True)
    p = sub.add_parser("compare-old")
    p.add_argument("--translations", required=True)
    a = ap.parse_args(argv)

    if a.cmd in ("estimate", "translate"):
        rules = [r for r in report.load_rules(a.rules) if not a.folder or a.folder in r["folder"]]
        if a.cmd == "estimate":
            print(report.estimate(rules, a.runs, len(PROMPT.read_text().split())))
            return
        from llm import LLM
        llm = LLM()
        out = asyncio.run(translate_all(llm, rules, runs=a.runs, mode=a.mode))
        write(a.out, {"rules": out, "mode": a.mode, "usage": llm.usage})
        print(f"{len(out)} rules x {a.runs} runs, usage {llm.usage}")
        print("status, run 1:", dict(Counter(r["runs"][0]["status"] for r in out)))
    elif a.cmd == "check":
        rules = json.loads(Path(a.translations).read_text())["rules"]
        res = report.check_all(rules, run=a.run - 1)
        write(a.out, res)
        print("rules:", res["rule_status"], "| pairs:", res["counts"])
    elif a.cmd == "agreement":
        rules = json.loads(Path(a.translations).read_text())["rules"]
        res = report.agreement_all(rules)
        write(a.out, res)
        print(f"same status in all runs: {res['same_status']} of {res['rules']} | "
              f"same meaning: {res['same_meaning']} of {res['all_ok']} rules ok in every run")
    elif a.cmd == "score-labels":
        from rules.label_score import score, summary
        labels = [r for r in json.loads(Path(a.labels).read_text())["rules"]
                  if not a.split or r.get("split") == a.split]
        rows = score(labels, json.loads(Path(a.translations).read_text())["rules"])
        write(a.out, {"summary": summary(rows), "rows": rows})
        print(summary(rows))
    elif a.cmd == "report":
        from rules import export
        rules = json.loads(Path(a.translations).read_text())["rules"]
        rep = export.build(rules, a.folder, run=a.run - 1, source=a.translations)
        export.write(rep, a.out)
        print(rep["summary"])
    else:
        from rules.convert_old import compare
        counts, diffs = compare(a.translations)
        print({f"{o}->{n}": k for (o, n), k in counts.items()})
        for d in diffs:
            print(f"  {d['old']} -> {d['new']}: {d['a'][:70]} || {d['b'][:70]}")


if __name__ == "__main__":
    main()
