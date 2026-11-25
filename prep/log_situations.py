"""Pull real situation shapes out of local Claude Code session logs (no contents kept).

A situation = one git / file / task tool call, reduced to: action kind, path kind, the 3 earlier
action kinds (with ok / failed), whether the user's last message asked for this kind of action,
and whether the user rejected the call. File contents, messages and names are dropped.
Used as inspiration for log-grounded test actions (docs/review/enforce_prereg.md).

Run: uv run python prep/log_situations.py  ->  data/runs/natural/log_situations.json
"""

import collections
import glob
import json
import os
import re

LOGS = os.path.expanduser("~/.claude/projects/*/*.jsonl")
OUT = "data/runs/natural/log_situations.json"

GIT = [("force_push", r"git push\b.*(--force|-f\b)"), ("push", r"git push\b"),
       ("commit", r"git commit\b"), ("stage", r"git add\b"), ("branch_create", r"git (checkout|switch) -[bc]\b|git branch \w"),
       ("branch_delete", r"git branch -[dD]\b"), ("checkout", r"git (checkout|switch)\b"),
       ("merge", r"git merge\b"), ("reset_hard", r"git reset --hard"), ("rebase", r"git rebase\b"),
       ("stash", r"git stash\b"), ("delete", r"\b(git rm|rm) ")]
TASK = [("test", r"\b(pytest|npm (run )?test|jest|vitest|go test|cargo test)\b"),
        ("build", r"\b(npm run build|tsc\b|cargo build|make\b|vite build)"),
        ("lint", r"\b(ruff|eslint|flake8|npm run lint)\b"), ("format", r"\b(black|prettier|ruff format)\b"),
        ("deploy", r"\b(wrangler deploy|vercel|fly deploy|railway up)\b"),
        ("restart", r"\b(restart|pkill|kill )"), ("start_server", r"\b(npm run dev|npm start|uvicorn|flask run|wrangler dev)\b"),
        ("install", r"\b(npm (i|install)|pip install|uv (add|sync))\b")]
ASK = {"commit": r"\bcommit", "push": r"\bpush", "force_push": r"\bforce", "stage": r"\b(commit|stage|add)",
       "branch_create": r"\bbranch", "branch_delete": r"\b(delete|remove).*branch", "checkout": r"\b(checkout|switch|branch)",
       "merge": r"\bmerge", "reset_hard": r"\breset", "rebase": r"\brebase", "delete": r"\b(delete|remove|rm)\b",
       "edit": r"\b(edit|fix|change|update|add|write|implement|go ahead|yes|ok)\b", "create": r"\b(create|write|add|make|go ahead|yes|ok)\b",
       "read": r".", "test": r"\btest", "build": r"\bbuild", "deploy": r"\bdeploy", "restart": r"\brestart",
       "start_server": r"\b(run|start|launch)", "lint": r"\blint", "format": r"\bformat", "install": r"\binstall", "stash": r"\bstash"}


def path_kind(p):
    p = (p or "").lower()
    b = os.path.basename(p)
    if b.startswith(".env"):
        return "env_example" if "example" in b else "env"
    if "/test" in p or b.startswith("test_") or ".test." in b:
        return "test"
    if b.endswith((".md", ".txt", ".rst")):
        return "docs"
    if b.endswith((".json", ".toml", ".yml", ".yaml", ".ini", ".cfg", ".lock")):
        return "config"
    if b.endswith((".jsonl", ".csv", ".dat", ".db", ".sqlite")):
        return "data"
    if b.endswith((".py", ".ts", ".tsx", ".js", ".go", ".rs", ".java", ".c", ".h", ".sh", ".tex", ".html", ".css")):
        return "code"
    return "other"


def kinds(tool, inp):
    if tool in ("Edit", "Write", "Read", "NotebookEdit"):
        k = {"Edit": "edit", "NotebookEdit": "edit", "Read": "read"}.get(tool) or "create"
        return [(k, path_kind(inp.get("file_path")))]
    if tool != "Bash":
        return []
    cmd = inp.get("command", "")
    out = [(k, None) for k, r in GIT if re.search(r, cmd)]
    if any(k == "force_push" for k, _ in out):
        out = [x for x in out if x[0] != "push"]
    if any(k == "branch_create" for k, _ in out):
        out = [x for x in out if x[0] != "checkout"]
    out += [(k, None) for k, r in TASK if re.search(r, cmd)]
    return out[:2]


def user_text(m):
    c = m.get("content")
    if isinstance(c, str):
        return c
    return " ".join(b.get("text", "") for b in c or [] if isinstance(b, dict) and b.get("type") == "text")


def rows():
    for f in sorted(glob.glob(LOGS)):
        last_user, history, pending = "", [], {}
        for line in open(f, errors="ignore"):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            m = d.get("message")
            if not isinstance(m, dict):
                continue
            blocks = m.get("content") if isinstance(m.get("content"), list) else []
            if d.get("type") == "user":
                for b in blocks:
                    if isinstance(b, dict) and b.get("type") == "tool_result" and b.get("tool_use_id") in pending:
                        s = pending.pop(b["tool_use_id"])
                        text = json.dumps(b.get("content", ""))[:400]
                        s["rejected"] = "doesn't want to proceed" in text or "rejected" in text
                        s["ok"] = not b.get("is_error") and not s["rejected"]
                        history.append((s["action"], s["ok"]))
                        yield s
                t = user_text(m)
                if t.strip() and "tool_result" not in json.dumps(blocks)[:50] and not t.startswith("<"):
                    last_user = t.lower()
            for b in blocks:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    for k, pk in kinds(b.get("name"), b.get("input") or {}):
                        pending[b["id"]] = {"action": k, "path_kind": pk,
                                            "earlier": [f"{a}:{'ok' if o else 'failed'}" for a, o in history[-3:]],
                                            "user_asked": bool(re.search(ASK.get(k, r"$^"), last_user))}
                        break


def main():
    S = list(rows())
    shapes = collections.Counter(json.dumps({k: s[k] for k in ("action", "path_kind", "earlier", "user_asked", "rejected", "ok")},
                                            sort_keys=True) for s in S)
    out = [{**json.loads(k), "count": n} for k, n in shapes.most_common()]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({"how": __doc__.strip().splitlines()[0], "n_calls": len(S), "situations": out}, open(OUT, "w"), indent=1)
    print(len(S), "calls,", len(out), "distinct situations ->", OUT)


if __name__ == "__main__":
    main()
