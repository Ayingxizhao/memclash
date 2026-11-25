"""Git track: translate each rule ALONE into a fixed model of git operations, then check every
pair of translated rules exactly with Z3.

Unlike verify_pair.py, the LLM supplies no facts about how actions relate. What git means is
fixed in this file: `push_delete` is a push, `pr_merge` is a merge, `.env*` matches
`.env.example` (globs become Z3 regular expressions), and so on. The LLM only translates one
rule at a time (prompts/git/git_translate.md).

Model. One git operation (an "event") has the fields listed in FIELDS. A clause is
  never    where           -> the event must not match `where`
  only_if  where, needs    -> if the event matches `where`, it must meet `needs`
  must_do  where           -> some event matching `where` must happen
  may_do   where           -> an event matching `where` is permitted
Pair check. For every must_do / may_do clause X of either rule, and every situation X covers
(see `situations`): is there an operation that matches X and obeys every never / only_if clause
of both rules? If in some situation there is none (while X's own rule alone can be followed
there), the pair conflicts and that situation is the witness. For may_do, each listed operation
is tested on its own ("may commit or push" permits both). For only_if clause X ("when you do
this, do it this way"), the operation X names is imagined: if each rule alone allows some way to
do it but no way obeys both, the pair conflicts ("commit only in a worktree" vs "commit only
outside one"). If the other rule simply forbids the operation, the agent can skip it: no
conflict. Otherwise the pair is compatible.

Usage:
  uv run python pipeline/git/git_check.py selftest
  uv run python pipeline/git/git_check.py translate --rules data/inject/dev_pilot_rules.json \
      --out data/runs/git/git_pilot/translate.json [--folder setflow]
  uv run python pipeline/git/git_check.py check --translations data/runs/git/git_pilot/translate.json \
      --out data/runs/git/git_pilot/check.json
"""

import argparse
import asyncio
import json
import random
import re
from itertools import combinations, product
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # shared LLM client: pipeline/llm.py

from z3 import (And, Bool, BoolVal, Concat, Full, Implies, InRe, Int, IntVal, Not, Or, Re,
                ReSort, Solver, String, StringSort, StringVal, sat)

ROOT = Path(__file__).resolve().parents[2]

CMDS = ["commit", "push_branch", "push_delete", "force_push", "local_merge", "pr_create",
        "pr_merge", "branch_create", "branch_delete", "checkout", "pull", "rebase", "reset_hard",
        "cherry_pick", "fetch", "worktree_add", "worktree_remove"]
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
         "tests_passed", "admin_bypass", "in_worktree"]
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
        # which operations were done earlier (any number of them, not only the last one), so
        # "check out main first" and "pull main first" can both hold. after_branch is still one
        # branch shared by all earlier operations.
        self.prior = {c: Bool(f"{tag}_prior_{c}") for c in CMDS}
        self.n_files = Int(f"{tag}_n_files")
        self.s = {g: String(f"{tag}_{g}") for g in GLOBS}
        self.b = {k: Bool(f"{tag}_{k}") for k in BOOLS}
        self.tag = tag

    def cond(self, name):
        """An unknown yes/no fact: the condition a rule names but the model cannot express."""
        return Bool(f"{self.tag}_cond_{name}")

    def wellformed(self):
        return And(self.cmd >= 0, self.cmd < len(CMDS), self.n_files >= 0)

    def match(self, where):
        cs = []
        for k, v in where.items():
            if k == "_cond":
                cs.append(self.cond(v))
                continue
            if k not in FIELDS:
                raise ValueError(f"unknown field {k!r}")
            if k == "cmd":
                cs.append(Or([self.cmd == CMDS.index(c) for c in expand(v)]))
            elif k == "after":
                cs.append(Or([self.prior[c] for c in expand(v)]))
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
        if c["type"] == "only_if" and not c.get("needs") and not c.get("when_unmodeled"):
            raise ValueError("only_if without needs")
        if "cmd" in c.get("needs", {}):
            raise ValueError("an operation in needs (write 'before X do Y' as needs after: [Y])")
        Event("v").match(c.get("where", {}))
        Event("v").match(c.get("needs", {}))


def prepared(t, tag):
    """Clauses with a left-out condition (`when_unmodeled`) apply only when an unknown fact of
    their own holds. That fact is never named by another rule, so such a clause cannot clash
    with every other rule; at worst a clash is missed."""
    out = []
    for i, c in enumerate(t.get("clauses", [])):
        c = dict(c)
        if c.get("when_unmodeled") and c["type"] == "only_if" and not c.get("needs"):
            # "X only after <something the model cannot express>": an unknown prerequisite
            # the agent can meet, so this clause never blocks anything on its own
            c["needs"] = {"_cond": f"{tag}{i}"}
        elif c.get("when_unmodeled"):
            c["where"] = {**c.get("where", {}), "_cond": f"{tag}{i}"}
        out.append(c)
    return out


def witness(s, e):
    m = s.model()
    out = {"cmd": CMDS[m.eval(e.cmd).as_long()]}
    done = [c for c in CMDS if bool(m.eval(e.prior[c], model_completion=True))]
    if done:
        out["after"] = done
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
    ca, cb = prepared(ta, "a"), prepared(tb, "b")
    for own, other, tag in ((ca, cb, "a"), (cb, ca, "b")):
        for i, x in enumerate(own):
            if x["type"] not in ("must_do", "may_do", "only_if"):
                continue
            e = Event(f"{tag}{i}")
            base = [e.wellformed(), e.match(x.get("where", {}))]
            if x["type"] != "only_if" and not is_sat(*base, *constraints(e, own)):
                return "invalid", {"error": f"rule_{tag} clause {i} cannot be met on its own"}
            for fixed in situations(e, x, ca + cb):
                if not is_sat(*base, *fixed, *constraints(e, own)):
                    continue  # not a situation this rule can handle on its own
                if x["type"] == "only_if" and not is_sat(*base, *fixed, *constraints(e, other)):
                    # nothing forces this operation, and the other rule simply forbids it here
                    # ("never push" vs "push only after tests"): the agent can skip it
                    continue
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


def situations(e, x, clauses):
    """Every situation to test for clause x: one value per situation field that x itself names
    (fields x does not name stay open: a rule is tested in the situations it talks about).
    Sample values come from both rules. For may_do, each listed operation is tested."""
    mentioned = set(x.get("where", {}))
    dims = []
    if "_cond" in mentioned:  # the clause's own unknown condition holds in its own situation
        dims.append([e.cond(x["where"]["_cond"]) == BoolVal(True)])
    if "after" in mentioned or "after_branch" in mentioned:
        # nothing done earlier, or one given operation done earlier (the rest stay open)
        dims.append([And([Not(p) for p in e.prior.values()])] + [p for p in e.prior.values()])
    if "after_branch" in mentioned:
        # one situation per possible inside/outside combination of the branch patterns both
        # rules name, checked exactly (release-* and *-prod overlap at release-prod)
        pats = sorted({str(c[p]["after_branch"]) for c in clauses for p in ("where", "needs")
                       if "after_branch" in c.get(p, {})})
        regions = []
        for signs in product((True, False), repeat=len(pats)):
            inside = [InRe(e.s["after_branch"], glob_re(q)) for q in pats]
            f = And([m if s else Not(m) for m, s in zip(inside, signs)])
            if is_sat(f):
                regions.append(f)
        dims.append(regions)
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
    # large-folder design check: "first check out main" with an operation inside needs
    "L235_bad": {"fits": True, "clauses": [{"type": "only_if", "where": {"cmd": ["branch_create"]},
                                            "needs": {"cmd": ["checkout"], "branch": "main"}}]},
    "L235": {"fits": True, "clauses": [{"type": "only_if", "where": {"cmd": ["branch_create"]},
                                        "needs": {"after": ["checkout"]}}]},
    "L237": {"fits": True, "clauses": [{"type": "must_do", "where": {"cmd": ["branch_create"], "branch": "feat/*"}}]},
    # "never commit to the local clones": condition the model cannot express
    "L6_cond": {"fits": True, "clauses": [{"type": "never", "where": {"cmd": ["commit"]},
                                           "when_unmodeled": "in the local clones"}]},
    "L6_nocond": {"fits": True, "clauses": [{"type": "never", "where": {"cmd": ["commit"]}}]},
    "L46": {"fits": True, "clauses": [{"type": "must_do", "where": {"cmd": ["commit"], "file": "data/*"}}]},
    # two "when you do X, do it this way" rules (review fix: these were never tested)
    "W_in": {"fits": True, "clauses": [{"type": "only_if", "where": {"cmd": ["commit"]},
                                        "needs": {"in_worktree": True}}]},
    "W_out": {"fits": True, "clauses": [{"type": "only_if", "where": {"cmd": ["commit"]},
                                         "needs": {"in_worktree": False}}]},
    "P_never": {"fits": True, "clauses": [{"type": "never", "where": {"cmd": ["push"]}}]},
    "P_tests": {"fits": True, "clauses": [{"type": "only_if", "where": {"cmd": ["push"]},
                                           "needs": {"tests_passed": True}}]},
    "P_ok": {"fits": True, "clauses": [{"type": "only_if", "where": {"cmd": ["any_push"]},
                                        "needs": {"user_confirmed": True}}]},
    "P_force_no": {"fits": True, "clauses": [{"type": "only_if", "where": {"cmd": ["force_push"]},
                                              "needs": {"user_confirmed": False}}]},
    # large folder R235 / R236: two different steps before creating a branch; both can be done
    "L235_main": {"fits": True, "clauses": [{"type": "only_if", "where": {"cmd": ["branch_create"]},
                                             "needs": {"after": ["checkout"], "after_branch": "main"}}]},
    "L236_main": {"fits": True, "clauses": [{"type": "only_if", "where": {"cmd": ["branch_create"]},
                                             "needs": {"after": ["pull"], "after_branch": "main"}}]},
    # overlapping branch patterns: a merge into "release-prod" matches both
    "G_rel": {"fits": True, "clauses": [{"type": "must_do", "where": {
        "cmd": ["branch_delete"], "after": ["pr_merge"], "after_branch": "release-*"}}]},
    "G_prod": {"fits": True, "clauses": [{"type": "never", "where": {
        "cmd": ["branch_delete"], "after": ["pr_merge"], "after_branch": "*-prod"}}]},
    "G_dev": {"fits": True, "clauses": [{"type": "never", "where": {
        "cmd": ["branch_delete"], "after": ["pr_merge"], "after_branch": "dev-*"}}]},
}
EXPECT = [("L235_bad", "L237", "invalid"), ("L235", "L237", "compatible"),
          ("L6_cond", "L46", "compatible"), ("L6_nocond", "L46", "conflict"),
          ("R1", "X2", "conflict"), ("R6", "X14", "conflict"), ("R3_lit", "X8", "conflict"),
          ("R3", "R15", "compatible"),("R1", "X1", "conflict"), ("R1", "X3", "compatible"), ("R3", "X8", "conflict"),
          ("R5", "X8", "compatible"), ("R2", "R5", "compatible"), ("R2", "R3", "compatible"),
          ("R6", "X13", "conflict"), ("R6", "X15", "compatible"),
          ("R7", "R8_exact", "compatible"), ("R7", "R8_glob", "conflict"),
          ("W_in", "W_out", "conflict"), ("P_never", "P_tests", "compatible"),
          ("P_ok", "P_force_no", "conflict"), ("R3", "R5", "compatible"),
          ("L235_main", "L236_main", "compatible"),
          ("G_rel", "G_prod", "conflict"), ("G_rel", "G_dev", "compatible")]


def selftest():
    ok = True
    for a, b, want in EXPECT:
        got, detail = check_pair(HAND[a], HAND[b])
        ok &= got == want
        print(f"{'ok ' if got == want else 'BAD'} {a:9} {b:9} want {want:10} got {got:10} {detail}")
    print("all ok" if ok else "FAILED")


# ---------------------------------------------------------------- LLM translation and checking

async def translate(rules_path, out, folder=None, repeat=0, prompt_name="git_translate",
                    only=None):
    """repeat 0 lists the other rules in file order; repeat i > 0 shuffles them with seed i,
    so each repeat is a separate LLM call for the same rule (used to measure consistency).
    only: a filter.json from `filter`; then only kept rules are translated, and the context
    lists only the other kept rules of the folder."""
    from llm import LLM
    prompt = (ROOT / "prompts" / "git" / f"{prompt_name}.md").read_text()
    llm = LLM()
    data = json.loads(Path(rules_path).read_text())
    keep = None
    if only:
        keep = {(r["folder"], r["id"]) for r in json.loads(Path(only).read_text()) if r["keep"]}
    jobs, results = {}, {}
    for fo in data["folders"]:
        name = fo.get("repo", fo.get("folder"))
        if folder and folder not in name:
            continue
        rules = [r for r in fo["rules"] if keep is None or (name, r["id"]) in keep]
        for r in rules:
            key = r["rule"]
            if key not in jobs:
                others = [x for x in rules if x is not r]
                if repeat:
                    random.Random(repeat).shuffle(others)
                ctx = "\n".join(f"- {x['rule']}" for x in others)
                user = f"Other rules of the folder (context only):\n{ctx}\n\nRULE:\n{r['rule']}"
                jobs[key] = llm.chat_json([{"role": "system", "content": prompt},
                                           {"role": "user", "content": user}])
            results.setdefault(name, []).append({"id": r["id"], "rule": r["rule"]})
    keys = list(jobs)
    done = dict(zip(keys, await asyncio.gather(*(jobs[k] for k in keys))))
    for rules in results.values():
        for r in rules:
            r["translation"] = done[r["rule"]]
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(results, indent=1))
    print(f"{len(jobs)} rules translated, usage {llm.usage}")


# ---------------------------------------------------------------- which rules are about git

# Written from git's own command list and GitHub terms, not from the test rules.
GIT_WORDS = re.compile(
    r"\bgit\b|\bgh\b|github|gitlab|\bcommit|\bpush|\bpull\b|\bpulls\b|\bpulled\b|\bfetch|\bmerg"
    r"|\brebase|\bbranch|\bcheckout|\bcheck out\b|\bswitch to\b|cherry.pick|\bstash|\btags?\b"
    r"|\btagged\b|\breset\b|\brevert|\bamend|\bsquash|fast.forward|force.push|--force|worktree"
    r"|submodule|\bclone|\borigin\b|upstream|\bremote\b|\bHEAD\b|\bmain\b|\bmaster\b"
    r"|pull request|\bPRs?\b|version.control|\brepo\b|\brepos\b|repositor|gitignore|\bstag(e|ed|ing)\b"
    r"|\bdiff\b|\bbisect|\bblame\b|pre-commit|branch protection|merge queue|\bupstream",
    re.I)


async def filter_rules(rules_path, out):
    """Two independent nets: GIT_WORDS and a short LLM yes/no question without folder
    context (prompts/git/git_filter.md). A rule is kept if either says git."""
    from llm import LLM
    prompt = (ROOT / "prompts" / "git" / "git_filter.md").read_text()
    llm = LLM()
    data = json.loads(Path(rules_path).read_text())
    rows, calls = [], []
    for fo in data["folders"]:
        name = fo.get("repo", fo.get("folder"))
        for r in fo["rules"]:
            rows.append({"folder": name, "id": r["id"], "rule": r["rule"],
                         "keyword": bool(GIT_WORDS.search(r["rule"]))})
            calls.append(llm.chat_json([{"role": "system", "content": prompt},
                                        {"role": "user", "content": f"RULE:\n{r['rule']}"}]))
    for row, ans in zip(rows, await asyncio.gather(*calls)):
        row["llm"] = bool(ans.get("git"))
        row["reason"] = ans.get("reason", "")
        row["keep"] = row["keyword"] or row["llm"]
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(rows, indent=1))
    from collections import Counter
    print(Counter((r["keyword"], r["llm"]) for r in rows), "(keyword, llm)")
    print(f"kept {sum(r['keep'] for r in rows)} of {len(rows)}, usage {llm.usage}")


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


# ---------------------------------------------------------------- consistency of translations

def meaning(t, e):
    """The three parts of a translation's meaning, as formulas over one operation e:
    what it forbids or restricts, what it requires, what it permits."""
    cs = prepared(t, "m")
    rules = And(constraints(e, cs)) if constraints(e, cs) else BoolVal(True)
    must = Or([e.match(c.get("where", {})) for c in cs if c["type"] == "must_do"] or [BoolVal(False)])
    may = Or([e.match(c.get("where", {})) for c in cs if c["type"] == "may_do"] or [BoolVal(False)])
    return rules, must, may


def same_meaning(ta, tb):
    """True if two translations of one rule mean the same: both 'not git', or both valid and,
    for every possible operation, they restrict, require and permit exactly the same."""
    if not ta.get("fits") or not tb.get("fits"):
        return not ta.get("fits") and not tb.get("fits")
    try:
        validate(ta), validate(tb)
    except (ValueError, TypeError):
        return False
    e = Event("m")
    return all(not is_sat(e.wellformed(), x != y) for x, y in zip(meaning(ta, e), meaning(tb, e)))


def consistency(paths, out, pairs=()):
    """Compare repeated translations of each rule; `pairs` = (rule id, rewording id, folder)."""
    runs = [json.loads(Path(p).read_text()) for p in paths]
    by_text = [{r["rule"]: r for rules in run.values() for r in rules} for run in runs]
    rows = []
    for text, r0 in by_text[0].items():
        ts = [b[text]["translation"] for b in by_text]
        agree = [same_meaning(ts[0], t) for t in ts[1:]]
        rows.append({"id": r0["id"], "rule": text, "fits": [bool(t.get("fits")) for t in ts],
                     "same_as_first": agree, "all_same": all(agree)})
    re_rows = []
    for host, para, folder in pairs:
        for k, run in enumerate(runs):
            rs = {r["id"]: r["translation"] for r in run[folder]}
            re_rows.append({"run": k, "rule": host, "rewording": para,
                            "same": same_meaning(rs[host], rs[para])})
    Path(out).write_text(json.dumps({"rules": rows, "rewordings": re_rows}, indent=1))
    n, fit = len(rows), [r for r in rows if any(r["fits"])]
    print(f"rules {n}: same meaning in all {len(runs)} runs: {sum(r['all_same'] for r in rows)}"
          f" | git rules {len(fit)}: {sum(r['all_same'] for r in fit)}")
    print(f"rewordings: same meaning as their rule in {sum(r['same'] for r in re_rows)} of {len(re_rows)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    t = sub.add_parser("translate")
    t.add_argument("--rules", required=True)
    t.add_argument("--out", required=True)
    t.add_argument("--folder")
    t.add_argument("--repeat", type=int, default=0)
    t.add_argument("--prompt", default="git_translate", help="prompt file in prompts/git/ (without .md)")
    t.add_argument("--only", help="filter.json from `filter`: translate only kept rules")
    f = sub.add_parser("filter")
    f.add_argument("--rules", required=True)
    f.add_argument("--out", required=True)
    c = sub.add_parser("check")
    c.add_argument("--translations", required=True)
    c.add_argument("--out", required=True)
    s = sub.add_parser("consistency")
    s.add_argument("--translations", nargs="+", required=True)
    s.add_argument("--out", required=True)
    s.add_argument("--rewordings", default="", help="host:rewording:folder,... e.g. R1:X3:repo#paraphrase")
    a = ap.parse_args()
    if a.cmd == "selftest":
        selftest()
    elif a.cmd == "translate":
        asyncio.run(translate(a.rules, a.out, a.folder, a.repeat, a.prompt, a.only))
    elif a.cmd == "filter":
        asyncio.run(filter_rules(a.rules, a.out))
    elif a.cmd == "check":
        check(a.translations, a.out)
    else:
        pairs = [tuple(p.split(":", 2)) for p in a.rewordings.split(",") if p]
        consistency(a.translations, a.out, pairs)
