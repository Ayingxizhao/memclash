"""Convert translations in the old git-only format (pipeline/git/git_check.py) to the new
format, and compare the old and new checker on the same saved translations. Used once, to
check that the new checker agrees with the old one apart from the bugs it fixes.

Old -> new: `fits` -> `status`; field `file` -> `path`; groups any_push / any_merge -> push /
merge; group `any` -> every git action; an only_if with no needs (old: an unknown
prerequisite that never blocks) -> needs {}.
Note: old patterns let `*` cross folders; converted patterns use the new meaning.
"""

import json
from collections import Counter
from itertools import combinations
from pathlib import Path

from rules.pair import check_pair
from rules.vocab import GIT_CMDS

OLD_GROUPS = {"any_push": ["push"], "any_merge": ["merge"],
              "any": [c for c in GIT_CMDS if c != "stage"]}


def names(v):
    out = []
    for n in v if isinstance(v, list) else [v]:
        out += OLD_GROUPS.get(n, [n])
    return out


def facts(old):
    new = {}
    for k, v in old.items():
        if k == "file":
            new["path"] = [v]
        elif k in ("cmd", "after"):
            new[k] = names(v)
        else:
            new[k] = v
    return new


def convert(old):
    if not old.get("fits"):
        return {"status": "not_in_scope", "reason": old.get("reason", "")}
    clauses = []
    for c in old.get("clauses", []):
        n = {"type": c["type"], "where": facts(c.get("where", {}))}
        if c["type"] == "only_if":
            n["needs"] = facts(c.get("needs", {}))
        if c.get("when_unmodeled"):
            n["when_unmodeled"] = c["when_unmodeled"]
        clauses.append(n)
    return {"status": "ok", "reason": "", "clauses": clauses, "left_out": old.get("left_out", "")}


# old verdict -> the new verdicts that mean the same
SAME_VERDICT = {"conflict": {"clash", "exception", "state_conflict"}, "compatible": {"compatible"},
                "invalid": {"invalid"}, "unfit": {"skipped"}}


def compare(path):
    """Old vs new verdict for every pair in one saved translation file."""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "git"))
    import git_check

    data = json.loads(Path(path).read_text())
    counts, diffs = Counter(), []
    for folder, rules in data.items():
        for ra, rb in combinations(rules, 2):
            old, _ = git_check.check_pair(ra["translation"], rb["translation"])
            new, detail = check_pair(convert(ra["translation"]), convert(rb["translation"]))
            same = new in SAME_VERDICT[old]
            counts[(old, new)] += 1
            if not same:
                diffs.append({"folder": folder, "a": ra["rule"], "b": rb["rule"], "old": old,
                              "new": new, **detail})
    return counts, diffs
