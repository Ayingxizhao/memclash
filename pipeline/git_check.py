"""Git track: translate each rule ALONE into a fixed model of git operations, then check every
pair of translated rules exactly with Z3.

Unlike verify_pair.py, the LLM supplies no facts about how actions relate. What git means is
fixed in this file: `push_delete` is a push, `pr_merge` is a merge, `.env*` matches
`.env.example` (globs become Z3 regular expressions), and so on. The LLM only translates one
rule at a time (prompts/git_translate.md).

Model. One git operation (an "event") has the fields listed in FIELDS. A clause is
  never    where           -> the event must not match `where`
  only_if  where, needs    -> if the event matches `where`, it must meet `needs`
  must_do  where           -> some event matching `where` must happen
  may_do   where           -> an event matching `where` is permitted
Pair check. For every must_do / may_do clause X of either rule, and every situation X covers
(see `situations`): is there an operation that matches X and obeys every never / only_if clause
of both rules? If in some situation there is none (while X's own rule alone can be followed
there), the pair conflicts and that situation is the witness. For may_do, each listed operation
is tested on its own ("may commit or push" permits both). Otherwise the pair is compatible.

Usage:
  uv run python pipeline/git_check.py selftest
  uv run python pipeline/git_check.py translate --rules data/inject/dev_pilot_rules.json \
      --out data/runs/git_pilot/translate.json [--folder setflow]
  uv run python pipeline/git_check.py check --translations data/runs/git_pilot/translate.json \
      --out data/runs/git_pilot/check.json
"""

import argparse
import asyncio
import json
from itertools import combinations, product
from pathlib import Path

from z3 import (And, Bool, BoolVal, Concat, Full, Implies, InRe, Int, IntVal, Not, Or, Re,
                ReSort, Solver, String, StringSort, StringVal, sat)

ROOT = Path(__file__).resolve().parents[1]

CMDS = ["commit", "push_branch", "push_delete", "force_push", "local_merge", "pr_create",
        "pr_merge", "branch_create", "branch_delete", "checkout", "pull", "rebase", "reset_hard",
        "cherry_pick"]
# What git means is fixed here: every kind of push is a push, every kind of merge is a merge.
PUSHES, MERGES = ["push_branch", "push_delete", "force_push"], ["local_merge", "pr_merge"]
GROUPS = {"push": PUSHES, "any_push": PUSHES,
          "merge": MERGES, "any_merge": MERGES,
          "any_branch_delete": ["branch_delete", "push_delete"],
          "any": CMDS}
# Fields the world fixes (the situation) vs fields the agent chooses. A must_do clause must be
# possible in EVERY situation it covers; a may_do clause must be allowed for EACH operation it
# lists, in every situation it covers. Fields the rule leaves open are the agent's choice.
SITUATION = ["after", "after_branch", "n_files", "user_asked", "tests_passed"]
BOOLS = ["has_secret", "user_asked", "user_confirmed", "files_shown", "secrets_checked",
         "tests_passed", "admin_bypass"]
GLOBS = ["branch", "file", "after_branch"]
FIELDS = ["cmd", "after", "min_files", "max_files"] + GLOBS + BOOLS
TYPES = ["never", "only_if", "must_do", "may_do"]


def expand(names):
    out = []
    for n in names if isinstance(names, list) else [names]:
        if n in GROUPS:
            out += GROUPS[n]
        elif n in CMDS:
            out.append(n)
        else:
            raise ValueError(f"unknown operation {n!r}")
    return sorted(set(out))


def glob_re(pattern):
    parts = str(pattern).split("*")
    pieces = []
    for i, p in enumerate(parts):
        if p:
            pieces.append(Re(StringVal(p)))
        if i < len(parts) - 1:
            pieces.append(Full(ReSort(StringSort())))
    if not pieces:
        return Re(StringVal(""))
    return pieces[0] if len(pieces) == 1 else Concat(*pieces)


class Event:
    """Z3 variables for one git operation; `tag` keeps events of different clauses apart."""

    def __init__(self, tag):
        self.cmd = Int(f"{tag}_cmd")
        self.after = Int(f"{tag}_after")  # -1: no earlier operation
        self.n_files = Int(f"{tag}_n_files")
        self.s = {g: String(f"{tag}_{g}") for g in GLOBS}
        self.b = {k: Bool(f"{tag}_{k}") for k in BOOLS}

    def wellformed(self):
        return And(self.cmd >= 0, self.cmd < len(CMDS), self.after >= -1,
                   self.after < len(CMDS), self.n_files >= 0)

    def match(self, where):
        cs = []
        for k, v in where.items():
            if k not in FIELDS:
                raise ValueError(f"unknown field {k!r}")
            if k == "cmd":
                cs.append(Or([self.cmd == CMDS.index(c) for c in expand(v)]))
            elif k == "after":
                cs.append(Or([self.after == CMDS.index(c) for c in expand(v)]))
            elif k == "min_files":
                cs.append(self.n_files >= int(v))
            elif k == "max_files":
                cs.append(self.n_files <= int(v))
            elif k in GLOBS:
                cs.append(InRe(self.s[k], glob_re(v)))
            elif isinstance(v, bool):
                cs.append(self.b[k] == BoolVal(v))
            else:
                raise ValueError(f"{k} must be true/false")
        return And(cs) if cs else BoolVal(True)


def constraints(e, clauses):
    out = []
    for c in clauses:
        if c["type"] == "never":
            out.append(Not(e.match(c.get("where", {}))))
        elif c["type"] == "only_if":
            out.append(Implies(e.match(c.get("where", {})), e.match(c.get("needs", {}))))
    return out


def is_sat(*fs):
    s = Solver()
    s.add(*fs)
    return s.check() == sat


def validate(t):
    """Raise ValueError if a translation uses names outside the model."""
    for c in t.get("clauses", []):
        if c.get("type") not in TYPES:
            raise ValueError(f"unknown clause type {c.get('type')!r}")
        if c["type"] == "only_if" and not c.get("needs"):
            raise ValueError("only_if without needs")
        Event("v").match(c.get("where", {}))
        Event("v").match(c.get("needs", {}))


def witness(s, e):
    m = s.model()
    out = {"cmd": CMDS[m.eval(e.cmd).as_long()]}
    a = m.eval(e.after).as_long()
    if a >= 0:
        out["after"] = CMDS[a]
    for g in GLOBS:
        v = m.eval(e.s[g])
        out[g] = v.as_string() if hasattr(v, "as_string") else str(v)
    for k in BOOLS:
        out[k] = bool(m.eval(e.b[k], model_completion=True))
    return out


def check_pair(ta, tb):
    """Return (verdict, detail). verdict: conflict / compatible / invalid / unfit."""
    if not ta.get("fits") or not tb.get("fits"):
        return "unfit", {}
    try:
        validate(ta), validate(tb)
    except (ValueError, TypeError) as err:
        return "invalid", {"error": str(err)}
    ca, cb = ta["clauses"], tb["clauses"]
    for own, other, tag in ((ca, cb, "a"), (cb, ca, "b")):
        for i, x in enumerate(own):
            if x["type"] not in ("must_do", "may_do"):
                continue
            e = Event(f"{tag}{i}")
            base = [e.wellformed(), e.match(x.get("where", {}))]
            if not is_sat(*base, *constraints(e, own)):
                return "invalid", {"error": f"rule_{tag} clause {i} cannot be met on its own"}
            for fixed in situations(e, x, ca + cb):
                if not is_sat(*base, *fixed, *constraints(e, own)):
                    continue  # not a situation this rule can handle on its own
                if is_sat(*base, *fixed, *constraints(e, own), *constraints(e, other)):
                    continue
                s2 = Solver()
                s2.add(*base, *fixed, *constraints(e, own))
                s2.check()
                blockers = [j for j, c in enumerate(other)
                            if not is_sat(*base, *fixed, *constraints(e, own), *constraints(e, [c]))]
                return "conflict", {"by": f"rule_{tag} clause {i}", "event": witness(s2, e),
                                    "blocked_by": blockers}
    return "compatible", {}


def sample(pattern):
    return str(pattern).replace("*", "x")


def situations(e, x, clauses):
    """Every situation to test for clause x: one value per situation field that x itself names
    (fields x does not name stay open: a rule is tested in the situations it talks about).
    Sample values come from both rules. For may_do, each listed operation is tested."""
    mentioned = set(x.get("where", {}))
    dims = []
    if "after" in mentioned or "after_branch" in mentioned:
        dims.append([e.after == v for v in range(-1, len(CMDS))])
    if "after_branch" in mentioned:
        vals = {sample(c[p]["after_branch"]) for c in clauses for p in ("where", "needs")
                if "after_branch" in c.get(p, {})} | {"zz_other"}
        dims.append([e.s["after_branch"] == StringVal(v) for v in sorted(vals)])
    if "min_files" in mentioned or "max_files" in mentioned:
        ts = {int(c[p][k]) for c in clauses for p in ("where", "needs")
              for k in ("min_files", "max_files") if k in c.get(p, {})}
        vals = sorted({v for t in ts for v in (t - 1, t, t + 1) if v >= 0} | {0, 1})
        dims.append([e.n_files == v for v in vals])
    for k in ("user_asked", "tests_passed"):
        if k in mentioned:
            dims.append([e.b[k] == BoolVal(v) for v in (False, True)])
    if x["type"] == "may_do":
        cmds = expand(x["where"]["cmd"]) if "cmd" in x.get("where", {}) else CMDS
        dims.append([e.cmd == CMDS.index(c) for c in cmds])
    yield from (list(combo) for combo in product(*dims))


# ---------------------------------------------------------------- selftest (no LLM)

HAND = {
    "R1": {"fits": True, "clauses": [{"type": "must_do", "where": {
        "cmd": ["any_branch_delete"], "after": ["any_merge"], "after_branch": "main"}}]},
    "X1": {"fits": True, "clauses": [{"type": "never", "where": {
        "cmd": ["any_branch_delete"], "after": ["any_merge"], "after_branch": "main"}}]},
    "X3": {"fits": True, "clauses": [{"type": "must_do", "where": {
        "cmd": ["any_branch_delete"], "after": ["any_merge"], "after_branch": "main"}}]},
    "R2": {"fits": True, "clauses": [{"type": "must_do", "where": {
        "cmd": ["push_delete"], "after": ["pr_merge"]}}]},
    "R3": {"fits": True, "clauses": [{"type": "only_if", "where": {
        "cmd": ["any_push", "any_merge", "pr_create"]}, "needs": {"user_confirmed": True}}]},
    "R5": {"fits": True, "clauses": [{"type": "only_if", "where": {
        "cmd": ["any_push", "pr_create"]}, "needs": {"files_shown": True, "user_confirmed": True}}]},
    "X8": {"fits": True, "clauses": [{"type": "must_do", "where": {
        "cmd": ["pr_merge"], "max_files": 2, "user_confirmed": False}}]},
    "R6": {"fits": True, "clauses": [{"type": "never", "where": {
        "cmd": ["commit"], "has_secret": True}}]},
    "X13": {"fits": True, "clauses": [{"type": "may_do", "where": {
        "cmd": ["commit"], "has_secret": True}}]},
    "X15": {"fits": True, "clauses": [{"type": "never", "where": {
        "cmd": ["commit"], "has_secret": True}}]},
    "R7": {"fits": True, "clauses": [
        {"type": "never", "where": {"cmd": ["commit"], "file": ".env"}},
        {"type": "must_do", "where": {"cmd": ["commit"], "file": ".env.example", "has_secret": False}}]},
    "R8_exact": {"fits": True, "clauses": [
        {"type": "only_if", "where": {"cmd": ["commit"]}, "needs": {"secrets_checked": True}},
        {"type": "never", "where": {"cmd": ["commit"], "file": ".env"}},
        {"type": "never", "where": {"cmd": ["commit"], "has_secret": True}}]},
    "R8_glob": {"fits": True, "clauses": [
        {"type": "only_if", "where": {"cmd": ["commit"]}, "needs": {"secrets_checked": True}},
        {"type": "never", "where": {"cmd": ["commit"], "file": ".env*"}}]},
    "R3_lit": {"fits": True, "clauses": [{"type": "only_if", "where": {
        "cmd": ["push", "merge", "pr_create"]}, "needs": {"user_confirmed": True}}]},
    "X2": {"fits": True, "clauses": [{"type": "never", "where": {
        "cmd": ["any_branch_delete"], "after": ["pr_merge"], "after_branch": "main"}}]},
    "X14": {"fits": True, "clauses": [{"type": "may_do", "where": {
        "cmd": ["commit", "push"], "has_secret": True}}]},
    "R15": {"fits": True, "clauses": [{"type": "may_do", "where": {"cmd": ["any_merge"]}}]},
}
EXPECT = [("R1", "X2", "conflict"), ("R6", "X14", "conflict"), ("R3_lit", "X8", "conflict"),
          ("R3", "R15", "compatible"),("R1", "X1", "conflict"), ("R1", "X3", "compatible"), ("R3", "X8", "conflict"),
          ("R5", "X8", "compatible"), ("R2", "R5", "compatible"), ("R2", "R3", "compatible"),
          ("R6", "X13", "conflict"), ("R6", "X15", "compatible"),
          ("R7", "R8_exact", "compatible"), ("R7", "R8_glob", "conflict")]


def selftest():
    ok = True
    for a, b, want in EXPECT:
        got, detail = check_pair(HAND[a], HAND[b])
        ok &= got == want
        print(f"{'ok ' if got == want else 'BAD'} {a:9} {b:9} want {want:10} got {got:10} {detail}")
    print("all ok" if ok else "FAILED")


# ---------------------------------------------------------------- LLM translation and checking

async def translate(rules_path, out, folder=None):
    from llm import LLM
    prompt = (ROOT / "prompts" / "git_translate.md").read_text()
    llm = LLM()
    data = json.loads(Path(rules_path).read_text())
    seen, results = {}, {}
    for fo in data["folders"]:
        name = fo.get("repo", fo.get("folder"))
        if folder and folder not in name:
            continue
        for r in fo["rules"]:
            key = r["rule"]
            if key not in seen:
                ctx = "\n".join(f"- {x['rule']}" for x in fo["rules"] if x is not r)
                user = f"Other rules of the folder (context only):\n{ctx}\n\nRULE:\n{r['rule']}"
                seen[key] = await llm.chat_json([{"role": "system", "content": prompt},
                                                 {"role": "user", "content": user}])
            results.setdefault(name, []).append({"id": r["id"], "rule": r["rule"],
                                                 "translation": seen[key]})
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(results, indent=1))
    print(f"{len(seen)} rules translated, usage {llm.usage}")


def check(translations, out):
    data = json.loads(Path(translations).read_text())
    rows = []
    for folder, rules in data.items():
        for ra, rb in combinations(rules, 2):
            verdict, detail = check_pair(ra["translation"], rb["translation"])
            if verdict != "unfit":
                rows.append({"folder": folder, "a": ra["id"], "b": rb["id"], "verdict": verdict,
                             **detail})
    Path(out).write_text(json.dumps(rows, indent=1))
    from collections import Counter
    print(Counter(r["verdict"] for r in rows))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    t = sub.add_parser("translate")
    t.add_argument("--rules", required=True)
    t.add_argument("--out", required=True)
    t.add_argument("--folder")
    c = sub.add_parser("check")
    c.add_argument("--translations", required=True)
    c.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.cmd == "selftest":
        selftest()
    elif a.cmd == "translate":
        asyncio.run(translate(a.rules, a.out, a.folder))
    else:
        check(a.translations, a.out)
