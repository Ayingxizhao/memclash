"""memclash: check an agent's memory rules with Z3, for use from a coding agent (see integrations/pi/).

  PYTHONPATH=pipeline uv run python -m rules.memclash compile <repo> [--memory <file>]
      Extract rules from the repo's memory files (AGENTS.md, CLAUDE.md, .claude/memory/*.md, or
      only <file> if given), translate each into the fixed schema (LLM), and write
      <repo>/.memclash/rules.json.
  PYTHONPATH=pipeline uv run python -m rules.memclash gate <repo> '<tool call json>'
      {"tool": "bash"|"read"|"edit"|"write", "input": {...}, "prior": [events]} ->
      {"block": bool, "reason": str, "events": [...], "breaks": [...]}
  PYTHONPATH=pipeline uv run python -m rules.memclash clash <repo>
      Check all translated rules for clashes: every pair, then all rules together.
  PYTHONPATH=pipeline uv run python -m rules.memclash check <repo> <memory file> <new content file>
      Before the memory file is changed: compile the new content in <repo>/.memclash/preview/ and
      report the clashes that involve a rule the change adds, and old rules the change deletes
      that the new rule contradicts (a silent overwrite).

All output is JSON on stdout. Everything memclash writes stays in <repo>/.memclash/, including the
LLM cache, so running it never touches this project's data.
"""

import asyncio
import itertools
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

from rules.enforce import judge
from rules.group import check_group
from rules.pair import check_pair
from rules.trial_events import SED_I, WRITE, reads_env, simple_commands

MEMORY_FILES = ("AGENTS.md", "CLAUDE.md")
MEMORY_DIRS = (".claude/memory",)
GATE_TYPES = {"never", "only_if"}  # clause types a single action can break


# ---------------------------------------------------------------- compile
def memory_files(repo, only=None):
    repo = Path(repo)
    if only:
        return [repo / only]
    files = [repo / f for f in MEMORY_FILES if (repo / f).is_file()]
    for d in MEMORY_DIRS:
        files += sorted((repo / d).glob("*.md")) if (repo / d).is_dir() else []
    return files


def gate_clauses(tr):
    """The parts of a translation a single action can break exactly: never / only_if clauses with no
    condition the schema cannot check. must_do / may_do parts are left to the clash check."""
    if tr.get("status") != "ok":
        return []
    return [c for c in tr.get("clauses") or [] if c.get("type") in GATE_TYPES and not c.get("when_unmodeled")]


def gate_usable(tr):
    return bool(gate_clauses(tr))


def any_branch(tr):
    """A branch of exactly "*" is meant as "any branch", but in the schema `*` stops at "/" (so it
    misses fix/x). Drop it: no branch field already means any branch."""
    for c in tr.get("clauses") or []:
        for part in (c.get("where") or {}, c.get("needs") or {}):
            for k in ("branch", "after_branch"):
                if part.get(k) in ("*", ["*"]):
                    del part[k]
    return tr


async def _compile(repo, only=None):
    import llm as llm_mod
    out = Path(repo) / ".memclash"
    out.mkdir(exist_ok=True)
    llm_mod.CACHE_PATH = out / "llm_cache.jsonl"  # keep the cache inside the demo repo
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "prep"))
    from extract import extract_file
    from rules.translate import translate_all
    llm = llm_mod.LLM()
    rules = []
    files = memory_files(repo, only)
    for f in files:
        good, _ = await extract_file(llm, f.name, f.read_text())
        rules += [{"folder": "repo", "file": str(f.relative_to(repo)), "rule": r["rule"],
                   "quote": r["quote"]} for r in good]
    for i, r in enumerate(rules, 1):
        r["id"] = f"R{i}"
    # plain JSON (the strict-tool beta endpoint 404s); 3 tries per rule, keep the first valid one
    done = await translate_all(llm, rules, runs=3, use_tool=False)
    kept, left = [], []
    for r in done:
        runs = r.pop("runs")
        oks = [t for t in runs if t.get("status") == "ok"]
        # among valid tries, keep the one with the most clauses the checker can use exactly
        tr = any_branch(max(oks, key=lambda t: len(gate_clauses(t))) if oks else runs[0])
        rec = {**r, "translation": tr, "gate": gate_usable(tr)}
        (kept if tr.get("status") == "ok" else left).append(rec)
    sources = [str(f.relative_to(repo)) for f in files]
    json.dump({"sources": sources, "rules": kept}, open(out / "rules.json", "w"), indent=1)
    json.dump({"rules": left}, open(out / "untranslated.json", "w"), indent=1)
    return {"rules": len(rules), "translated": len(kept), "gate": sum(r["gate"] for r in kept),
            "untranslated": len(left), "sources": sources, "out": str(out / "rules.json")}


def load_rules(repo):
    p = Path(repo) / ".memclash" / "rules.json"
    return json.load(open(p))["rules"] if p.exists() else []


# ---------------------------------------------------------------- gate: tool call -> events
GIT_SIMPLE = {"commit": "commit", "rebase": "rebase", "cherry-pick": "cherry_pick", "pull": "pull",
              "fetch": "fetch"}
TASK_WORDS = {"test": "test", "tests": "test", "check": "test", "build": "build", "lint": "lint",
              "format": "format", "fmt": "format", "deploy": "deploy", "migrate": "migrate",
              "publish": "publish", "restart": "restart"}
RUNNERS = {"npm", "pnpm", "yarn", "bun", "gradle", "gradlew", "mvn", "mvnw", "make", "cargo", "go",
           "dotnet", "poetry", "uv", "tox", "nox", "just"}
DIRECT = {"pytest": "test", "jest": "test", "vitest": "test", "mocha": "test", "eslint": "lint",
          "ruff": "lint", "flake8": "lint", "prettier": "format", "black": "format"}


def current_branch(repo):
    # symbolic-ref also works in a new repo with no commits yet
    r = subprocess.run(["git", "symbolic-ref", "--short", "-q", "HEAD"], cwd=repo, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def rel(p, repo):
    if not p:
        return p
    a = os.path.normpath(os.path.join(repo, p))
    return os.path.relpath(a, repo) if a.startswith(os.path.abspath(repo)) else p


def task_of(words):
    """The task a command line runs, e.g. `./gradlew :core:test` -> test, `npm run build` -> build."""
    prog = Path(words[0]).name
    if prog in DIRECT:
        return DIRECT[prog]
    if prog in ("python", "python3") and words[1:3] == ["-m", "pytest"]:
        return "test"
    if prog in RUNNERS:
        if len(words) > 2 and words[1] in ("run", "exec", "x"):  # `uv run pytest`, `npm exec jest`
            inner = task_of(words[2:])
            if inner:
                return inner
        for w in words[1:]:
            last = w.split(":")[-1]
            if last in TASK_WORDS:
                return TASK_WORDS[last]
    return None


def git_events(w, branch, repo):
    """Events for one `git ...` or `gh pr ...` simple command."""
    if Path(w[0]).name == "gh":
        if w[1:3] == ["pr", "create"]:
            return [{"cmd": "pr_create", "branch": branch}]
        if w[1:3] == ["pr", "merge"]:
            return [{"cmd": "pr_merge", "branch": branch}]
        return []
    args = [a for a in w[1:] if not a.startswith("-")]
    flags = [a for a in w[1:] if a.startswith("-")]
    if not args:
        return []
    sub, rest = args[0], args[1:]
    if sub in GIT_SIMPLE:
        return [{"cmd": GIT_SIMPLE[sub], "branch": branch}]
    if sub == "add":
        return [{"cmd": "stage", "path": rel(p, repo), "branch": branch} for p in rest or ["."]]
    if sub == "push":
        target = rest[1].split(":")[-1] if len(rest) > 1 else branch
        if "--delete" in flags or "-d" in flags or (len(rest) > 1 and rest[1].startswith(":")):
            return [{"cmd": "push_delete", "branch": target}]
        force = any(f in ("-f", "--force", "--force-with-lease") or f.startswith("--force") for f in flags)
        return [{"cmd": "force_push" if force else "push_branch", "branch": target}]
    if sub == "merge":
        return [{"cmd": "local_merge", "branch": branch}]
    if sub in ("checkout", "switch"):
        if "-b" in flags or "-c" in flags:
            return [{"cmd": "branch_create", "branch": rest[0] if rest else ""}]
        return [{"cmd": "checkout", "branch": rest[0] if rest else ""}]
    if sub == "branch":
        if any(f in ("-d", "-D", "--delete") for f in flags):
            return [{"cmd": "branch_delete", "branch": b} for b in rest]
        return [{"cmd": "branch_create", "branch": b} for b in rest[:1]]
    if sub == "reset" and "--hard" in flags:
        return [{"cmd": "reset_hard", "branch": branch}]
    if sub == "worktree" and rest[:1] in (["add"], ["remove"]):
        return [{"cmd": "worktree_" + rest[0], "branch": branch}]
    return []


def events(call, repo):
    """Map one agent tool call to schema events (the same mapping the Claude Code trial used,
    extended to git, tasks and file commands run through bash)."""
    tool, inp = call.get("tool", ""), call.get("input", {}) or {}
    branch = current_branch(repo)
    path = inp.get("path") or inp.get("file_path")
    if tool in ("read", "grep", "find", "ls"):
        p = rel(path, repo)
        return [{"cmd": "read", "path": p, "branch": branch}] if p else []
    if tool == "edit":
        return [{"cmd": "edit", "path": rel(path, repo), "branch": branch}]
    if tool == "write":
        p = rel(path, repo)
        return [{"cmd": "edit" if os.path.exists(os.path.join(repo, p)) else "create", "path": p,
                 "branch": branch}]
    if tool != "bash":
        return []
    script, evs = inp.get("command", ""), []
    written = {m.group(1) for m in WRITE.finditer(script)} | {m.group(1) for m in SED_I.finditer(script)}
    for w in sorted(x for x in written if not x.startswith("/dev/") and x not in ("&1", "&2")):
        p = rel(w, repo)
        evs.append({"cmd": "edit" if os.path.exists(os.path.join(repo, p)) else "create", "path": p,
                    "branch": branch})
    if reads_env(script) and not any(e["path"].endswith(".env") for e in evs):
        evs.append({"cmd": "read", "path": ".env", "branch": branch})
    for w in simple_commands(script):
        while w and "=" in w[0] and not w[0].startswith("-"):
            w = w[1:]  # VAR=value prefixes
        if not w:
            continue
        prog = Path(w[0]).name
        if prog in ("git", "gh"):
            new = git_events(w, branch, repo)
            evs += new
            sub = [a for a in w[1:] if not a.startswith("-")][:1]
            if prog == "git" and sub in (["checkout"], ["switch"]) and new and new[0]["branch"]:
                branch = new[0]["branch"]  # later steps in the same command run on the new branch
        elif prog == "rm":
            evs += [{"cmd": "delete", "path": rel(p, repo), "branch": branch} for p in w[1:] if not p.startswith("-")]
        elif prog == "mv":
            ps = [p for p in w[1:] if not p.startswith("-")]
            if len(ps) == 2:
                evs.append({"cmd": "move", "path": rel(ps[0], repo), "dest_path": rel(ps[1], repo), "branch": branch})
        else:
            t = task_of(w)
            if t:
                evs.append({"cmd": "run", "task": t, "branch": branch})
    return evs


def gate(repo, call):
    rules = [r for r in load_rules(repo) if r["gate"]]
    trs = {r["id"]: {**r["translation"], "clauses": gate_clauses(r["translation"])} for r in rules}
    en = {r["id"]: r["rule"] for r in rules}
    evs, breaks = events(call, repo), {}
    prior = call.get("prior", [])
    tests = [p for p in prior if p.get("cmd") == "run" and p.get("task") == "test"]
    flags = {"tests_passed": bool(tests) and tests[-1].get("ok", False),  # the latest test run succeeded
             **call.get("flags", {})}  # facts the agent host knows, e.g. user_asked from the user's message
    for k, ev in enumerate(evs):
        # earlier steps of the same command count as done (in `lint && commit`, commit runs only
        # after lint succeeded); approximate for `;`, where a failed earlier step does not stop it
        before = prior + [{**e, "ok": True} for e in evs[:k]]
        tests = [p for p in before if p.get("cmd") == "run" and p.get("task") == "test"]
        fl = {**flags, "tests_passed": bool(tests) and tests[-1].get("ok", False), **call.get("flags", {})}
        full = {"path": None, "dest_path": None, "kind": "file", "task": None, "running": [],
                "flags": fl, **ev, "prior": before}
        for rid in judge(full, trs)["rule_ids"]:
            breaks.setdefault(rid, ev)
    reason = ""
    if breaks:
        reason = "Blocked by memclash: this action breaks a rule in the project memory:\n" + "\n".join(
            f"  - {en[r]} ({r})" for r in sorted(breaks))
    return {"block": bool(breaks), "reason": reason, "events": evs, "breaks": sorted(breaks)}


# ---------------------------------------------------------------- clash
def clash(repo):
    rules = load_rules(repo)
    found = []
    for a, b in itertools.combinations(rules, 2):
        verdict, detail = check_pair(a["translation"], b["translation"])
        if verdict in ("clash", "exception", "state_conflict", "possible_clash"):
            found.append({"rules": [a["id"], b["id"]], "english": [a["rule"], b["rule"]],
                          "verdict": verdict, "action": detail.get("action")})
    group = "compatible"
    if len(rules) > 2 and not found:  # pairs are fine: can all rules be followed together?
        group, detail = check_group([r["translation"] for r in rules])
        if group in ("clash", "exception"):
            found.append({"rules": [r["id"] for r in rules], "english": None, "verdict": "group_" + group,
                          "action": detail.get("action")})
    return {"rules": len(rules), "clashes": found}


def _sync_cache(src, dst):
    s, d = Path(src) / ".memclash" / "llm_cache.jsonl", Path(dst) / ".memclash" / "llm_cache.jsonl"
    if s.exists():
        d.parent.mkdir(parents=True, exist_ok=True)
        d.write_bytes(s.read_bytes())


def check(repo, memory, new_file):
    """Clashes a proposed memory file would add, judged before the file is written."""
    import shutil
    cur = Path(repo) / memory
    old_text = " ".join(cur.read_text().split()) if cur.exists() else ""
    tmp = Path(repo) / ".memclash" / "preview"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    (tmp / memory).parent.mkdir(parents=True, exist_ok=True)
    (tmp / memory).write_text(Path(new_file).read_text())
    _sync_cache(repo, tmp)  # unchanged rules translate from the cache
    asyncio.run(_compile(str(tmp), memory))
    _sync_cache(tmp, repo)  # keep the new translations for the real compile after the edit
    # a rule is new if its verbatim quote is not in the current file (the LLM may reword old rules)
    norm = lambda r: " ".join((r.get("quote") or r["rule"]).split())
    new = [r for r in load_rules(tmp) if norm(r) not in old_text]
    ids = {r["id"] for r in new}
    found = [c for c in clash(tmp)["clashes"] if ids & set(c["rules"])]
    # old rules the change deletes, where the new rule says the opposite: a silent overwrite
    new_text = " ".join((tmp / memory).read_text().split())
    removed = [r for r in load_rules(repo) if norm(r) not in new_text]
    replaced = []
    for o in removed:
        for n in new:
            verdict, detail = check_pair(o["translation"], n["translation"])
            if verdict in ("clash", "exception", "state_conflict", "possible_clash"):
                replaced.append({"removed": o["rule"], "new": n["rule"], "verdict": verdict,
                                 "action": detail.get("action")})
    return {"new_rules": [r["rule"] for r in new], "removed_rules": [r["rule"] for r in removed],
            "clashes": found, "replaced": replaced}


def main(argv=None):
    argv = argv or sys.argv[1:]
    cmd, repo = argv[0], os.path.abspath(argv[1])
    if cmd == "compile":
        only = argv[argv.index("--memory") + 1] if "--memory" in argv else None
        res = asyncio.run(_compile(repo, only))
    elif cmd == "gate":
        res = gate(repo, json.loads(argv[2]))
    elif cmd == "clash":
        res = clash(repo)
    elif cmd == "check":
        res = check(repo, argv[2], argv[3])
    else:
        raise SystemExit(__doc__)
    print(json.dumps(res, default=str))


if __name__ == "__main__":
    main()
