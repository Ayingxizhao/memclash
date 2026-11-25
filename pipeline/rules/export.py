"""Write a report file for the memclash interface (demo/memclash/).

  uv run python pipeline/rules/cli.py report --translations T.json --folder NAME --out R.json

The report is plain data; the interface only displays it. Plain-English text is written
here, from fixed phrases per action and field, so the interface never interprets the format.
A second file `<out>.js` sets `window.MEMCLASH_REPORT`, so the interface can open the report
from disk without a server.
"""

import json
from collections import Counter
from datetime import date
from itertools import combinations
from pathlib import Path

from rules.pair import check_pair

ACTION = {
    "commit": "commit", "stage": "stage files", "push_branch": "push a branch",
    "push_delete": "delete a branch on the remote", "force_push": "force push",
    "local_merge": "merge locally", "pr_create": "open a pull request", "pr_merge": "merge a pull request",
    "branch_create": "create a branch", "branch_delete": "delete a branch locally",
    "checkout": "switch branch", "pull": "pull", "rebase": "rebase", "reset_hard": "hard reset",
    "cherry_pick": "cherry-pick", "fetch": "fetch", "worktree_add": "add a worktree",
    "worktree_remove": "remove a worktree", "read": "read", "create": "create", "edit": "edit",
    "move": "move", "delete": "delete", "run": "run",
    "push": "push (any kind)", "merge": "merge (any kind)",
    "any_branch_delete": "delete a branch (locally or on the remote)",
}
BOOL = {  # field: (when true, when false)
    "user_asked": ("the user asked", "the user did not ask"),
    "user_confirmed": ("with the user's approval", "without the user's approval"),
    "tests_passed": ("tests passed", "tests did not pass"),
    "has_secret": ("a file holding secrets", "a file holding no secrets"),
    "files_shown": ("the files were shown to the user", "the files were not shown"),
    "secrets_checked": ("secrets were checked first", "secrets were not checked"),
    "admin_bypass": ("bypassing branch protection", "without bypassing branch protection"),
    "in_worktree": ("inside a separate worktree", "outside a worktree"),
}
AFTER = {  # "after ..." phrasing
    "commit": "a commit", "stage": "staging", "push_branch": "a push", "push_delete": "a remote branch delete",
    "force_push": "a force push", "local_merge": "a local merge", "pr_create": "opening a PR",
    "pr_merge": "a PR merge", "branch_create": "creating a branch", "branch_delete": "a local branch delete",
    "checkout": "switching branch", "pull": "a pull", "rebase": "a rebase", "reset_hard": "a hard reset",
    "cherry_pick": "a cherry-pick", "fetch": "a fetch", "worktree_add": "adding a worktree",
    "worktree_remove": "removing a worktree", "read": "a read", "create": "creating a file",
    "edit": "an edit", "move": "a move", "delete": "a delete", "run": "running a task",
    "push": "a push", "merge": "a merge", "any_branch_delete": "a branch delete",
}
TYPE = {"never": "Never", "must_do": "Must", "may_do": "May", "only_if": "Only if",
        "must_hold": "Must be in the repo", "never_hold": "Must not be in the repo"}


def actions(names):
    return " or ".join(ACTION.get(n, n) for n in names)


def facts(w):
    """Plain words for the fields of a where / needs box (without the action)."""
    out = []
    if "task" in w:
        t = w["task"]
        out.append(f"task “{t[6:]}”" if t.startswith("other:") else f"task “{t}”")
    if "suite" in w:
        out.append("the full test suite")
    if "path" in w:
        out.append("on " + ", ".join(w["path"]))
    if "path_except" in w:
        out.append("except " + ", ".join(w["path_except"]))
    if "dest_path" in w:
        out.append("to " + ", ".join(w["dest_path"]))
    if "kind" in w:
        out.append("a folder" if w["kind"] == "dir" else "a file")
    if "branch" in w:
        out.append(f"on branch {w['branch']}")
    if "after" in w:
        out.append("after " + " or ".join(AFTER.get(a, a) for a in w["after"])
                   + (f" into {w['after_branch']}" if "after_branch" in w else ""))
    elif "after_branch" in w:
        out.append(f"after an action on {w['after_branch']}")
    if "after_task" in w:
        t = w["after_task"]
        out.append("the earlier task being “" + (t[6:] if t.startswith("other:") else t) + "”")
    if "after_path" in w:
        out.append("the earlier action being on " + ", ".join(w["after_path"]))
    if "after_ok" in w:
        out.append("the earlier task " + ("succeeded" if w["after_ok"] else "failed"))
    if "running" in w:
        out.append("while " + ", ".join(w["running"]) + " runs")
    if "min_files" in w:
        out.append(f"with at least {w['min_files']} files")
    if "max_files" in w:
        out.append(f"with at most {w['max_files']} files")
    out += [BOOL[k][0 if v else 1] for k, v in w.items() if k in BOOL]
    return out


def clause_text(c):
    w = c["where"]
    if c["type"] in ("must_hold", "never_hold"):
        s = f"{TYPE[c['type']]}: " + ", ".join(w["in_repo"])
        if "path_except" in w:
            s += " (except " + ", ".join(w["path_except"]) + ")"
    else:
        act = actions(w.get("cmd", []))
        rest = facts({k: v for k, v in w.items() if k != "cmd"})
        what = " ".join([act] + ([", ".join(rest)] if rest else []))
        if c["type"] == "only_if":
            s = f"{what}, only if " + ", ".join(facts(c.get("needs", {})) or ["(nothing)"])
            s = s[0].upper() + s[1:]
        else:
            s = f"{TYPE[c['type']]} {what}"
    if c.get("when_unmodeled"):
        s += f" (only when: {c['when_unmodeled']}, which the format cannot check)"
    return s


def situation(action, named, afters):
    """Plain words for the situation the solver found: earlier actions, branch, world facts
    that either rule names. Values no rule names (solver placeholders, earlier actions no rule
    mentions) are left out."""
    out = []
    done = [a for a in action.get("after", []) if a in afters]
    if done:
        out.append("earlier: " + ", ".join(AFTER.get(a, a) for a in done))
    ab = action.get("after_branch", "")
    if ab and not ab.endswith("_after_branch"):
        out.append(f"on branch {ab}")
    for k in ("user_asked", "tests_passed"):
        if k in named:
            out.append(BOOL[k][0 if action.get(k) else 1])
    return out


def named_afters(*translations):
    from rules.vocab import expand
    out = set()
    for t in translations:
        for c in t.get("clauses", []):
            for part in ("where", "needs"):
                out |= set(expand(c.get(part, {}).get("after", [])))
    return out


def named_fields(*translations):
    names = set()
    for t in translations:
        for c in t.get("clauses", []):
            names |= set(c.get("where", {})) | set(c.get("needs", {}))
    return names


def build(rules, folder, run=0, model="deepseek-v4-flash", source=""):
    rs = [r for r in rules if r["folder"] == folder]
    out_rules = []
    for r in rs:
        t = r["runs"][run]
        out_rules.append({
            "id": r["id"], "file": r.get("file", ""), "rule": r["rule"], "status": t["status"],
            "word": t.get("word", ""), "reason": t.get("reason", ""),
            "left_out": t.get("left_out", ""), "retried": bool(t.get("retried")),
            "off_template": bool(t.get("template_errors")),
            "clauses": [{**c, "text": clause_text(c)} for c in t.get("clauses", [])],
            "unmodeled": [c["when_unmodeled"] for c in t.get("clauses", []) if c.get("when_unmodeled")],
        })
    findings = []
    for ra, rb in combinations(rs, 2):
        ta, tb = ra["runs"][run], rb["runs"][run]
        verdict, d = check_pair(ta, tb)
        if verdict not in ("clash", "exception", "state_conflict"):
            continue
        f = {"id": f"F{len(findings) + 1}", "type": verdict, "a": ra["id"], "b": rb["id"]}
        if verdict == "state_conflict":
            f["path"] = d["path"]
            f["situation"] = [f"the path {d['path']} must be in the repo and must not be"]
            f["needs"], f["blocked_by"] = d["must_hold"], d["never_hold"]
        else:
            who = ra if d["by"].startswith("rule_a") else rb
            other = rb if who is ra else ra
            i = int(d["by"].split()[-1])
            f["needs"] = {"rule": who["id"], "clause": i,
                          "text": clause_text(who["runs"][run]["clauses"][i])}
            f["blocked_by"] = [{"rule": other["id"], "clause": j,
                                "text": clause_text(other["runs"][run]["clauses"][j])}
                               for j in d["blocked_by"]]
            f["situation"] = situation(d["action"], named_fields(ta, tb), named_afters(ta, tb))
            if not f["situation"]:  # no situation fact involved: the clash holds whenever X is done
                w = who["runs"][run]["clauses"][i]["where"]
                f["situation"] = ["whenever the agent would " + " ".join(
                    [actions(w.get("cmd", []))] + facts({k: v for k, v in w.items() if k != "cmd"}))]
        findings.append(f)
    status = Counter(r["status"] for r in out_rules)
    return {
        "tool": "memclash", "format": 1, "created": date.today().isoformat(),
        "folder": folder, "model": model, "run": run + 1, "source": source,
        "summary": {"rules": len(out_rules), "checked": status.get("ok", 0),
                    "not_in_scope": status.get("not_in_scope", 0),
                    "unclear": status.get("unclear", 0),
                    "bad_output": status.get("invalid_output", 0),
                    "with_unknown_condition": sum(bool(r["unmodeled"]) for r in out_rules),
                    **{k: sum(f["type"] == k for f in findings)
                       for k in ("clash", "exception", "state_conflict")}},
        "rules": out_rules, "findings": findings,
    }


def write(report, out):
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(report, indent=1, ensure_ascii=False)
    out.write_text(text)
    out.with_suffix(".js").write_text(f"window.MEMCLASH_REPORT = {text};\n")
