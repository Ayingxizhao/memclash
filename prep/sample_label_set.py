"""Pick the rules for the frozen hand-labelled set (plan: .lavish/two_step_plan.html, step 2).

  uv run python prep/sample_label_set.py

From the rules extracted from 5 survey folders (data/runs/survey_rules/rules, memory folder +
CLAUDE.md, ADR 0009):
- the 8 rules of the 4 known clashes (always included);
- 16 rules drawn at random from rules that mention git, files or running a task (keyword test,
  written before looking at the sample);
- 6 rules drawn at random from the other rules, as a control for "not in scope".
Fixed seed, so the draw can be repeated.
"""

import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "data" / "runs" / "survey_rules" / "rules"
OUT = ROOT / "data" / "runs" / "survey_rules" / "label_set" / "selection.json"
SEED = 2520

KNOWN = [  # (folder, rule id), from the survey (docs/review, data/runs/survey)
    ("sparkling__ruflo-patch", "R118"), ("sparkling__ruflo-patch", "R131"),
    ("martinambrus__RDForward", "R60"), ("martinambrus__RDForward", "R213"),
    ("QuagKhai003__assessment", "R24"), ("QuagKhai003__assessment", "R156"),
    ("jamieleecho__space-bandits", "R28"), ("jamieleecho__space-bandits", "R81"),
]

IN_SCOPE = re.compile(
    r"\bgit\b|\bgh\b|\bcommit|\bpush|\bpull\b|\bmerg|\brebase|\bbranch|\bcheckout|worktree"
    r"|\bstag(e|ed|ing)\b|gitignore|\brepo\b|repositor|\bPRs?\b|pull request"
    r"|\bfiles?\b|\bfolders?\b|\bdirector(y|ies)\b|\bdelet|\bremov|\brenam|\bmove\b|\bcreate\b"
    r"|\bedit\b|\bwrite\b|\bread\b|\boverwrit|\.md\b|\.json\b|\.py\b|\.c\b|/"
    r"|\brun (the )?(tests?|build)|\bdeploy|\bmigrat|\blint|\bpublish|\brelease|\brestart",
    re.I)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--n-scope", type=int, default=16)
    ap.add_argument("--n-other", type=int, default=6)
    ap.add_argument("--no-known", action="store_true", help="do not force the known-clash rules in")
    ap.add_argument("--exclude", default="", help="a selection.json whose rules are left out")
    a = ap.parse_args()
    excl = set()
    if a.exclude:
        excl = {(r["folder"], r["id"]) for r in json.loads(Path(a.exclude).read_text())["rules"]}
    pool = []
    for p in sorted(RULES.glob("*.json")):
        d = json.loads(p.read_text())
        pool += [{"folder": p.stem, "id": r["id"], "file": r["file"], "rule": r["rule"]}
                 for r in d["rules"]]
    pool = [r for r in pool if (r["folder"], r["id"]) not in excl]
    known = [] if a.no_known else [r for r in pool if (r["folder"], r["id"]) in set(KNOWN)]
    rest = [r for r in pool if (r["folder"], r["id"]) not in set(KNOWN)]
    rng = random.Random(a.seed)
    scope = [r for r in rest if IN_SCOPE.search(r["rule"])]
    other = [r for r in rest if not IN_SCOPE.search(r["rule"])]
    pick = ([{**r, "why": "known clash"} for r in known]
            + [{**r, "why": "random, mentions git/files/tasks"} for r in rng.sample(scope, a.n_scope)]
            + [{**r, "why": "random, control"} for r in rng.sample(other, a.n_other)])
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"seed": a.seed, "pool": len(pool), "keyword_pool": len(scope),
                               "rules": pick}, indent=1, ensure_ascii=False))
    print(f"pool {len(pool)} rules, keyword pool {len(scope)}, picked {len(pick)}")
    for r in pick:
        print(f"{r['folder'][:18]:18} {r['id']:5} [{r['why'][:10]}] {r['rule'][:95]}")


if __name__ == "__main__":
    main()
