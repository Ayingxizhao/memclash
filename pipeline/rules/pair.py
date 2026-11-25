"""Check two translated rules for a clash (ADR 0003, 0008).

For every must_do / may_do / only_if clause X of either rule, and every situation (see
`situations`): is there one action that matches X and obeys every never / only_if clause of
both rules? If in some situation there is none (while X's own rule alone can be followed
there), the pair conflicts and that situation is the witness.
- must_do X: some action matching X must be possible.
- may_do X: each listed action must stay possible ("may commit or push" permits both).
- only_if X: if each rule alone allows some way to do X but no way obeys both, they conflict
  ("commit only in a worktree" vs "commit only outside one"). If the other rule simply forbids
  X, the agent can skip it: no conflict.

Verdicts: clash; exception (a may_do is blocked: the author may have meant an exception, so
it needs a priority rule); state_conflict (one path must and must not be in the repo,
state.py); compatible; invalid (a rule cannot be followed even on its own, or uses an unknown
name); skipped (a rule is unclear, not in scope, or bad output). Order of precedence:
invalid, clash, exception, state_conflict, possible_clash. `possible_clash` (Codex consult 2):
the pair clashes only if some unknown conditions hold at once; reported separately.
"""

from itertools import product

from z3 import And, BoolVal, InRe, Not, Solver, StringVal, unsat

from rules.model import Event, action_clauses, constraints, prepared, witness
from rules.patterns import glob_re, is_sat, target_re
from rules.state import check_states, state_clauses
from rules.vocab import AFTER_FIELDS, CMDS, FILE_ACTIONS, WORLD_BOOLS, expand, norm_name, task_name


def fields_named(clauses, parts=("where", "needs")):
    """(field, value) for every field in the given parts of the clauses."""
    for c in clauses:
        for part in parts:
            yield from c.get(part, {}).items()


def regions(formulas):
    """Every satisfiable inside/outside combination of the given formulas."""
    out = []
    for signs in product((True, False), repeat=len(formulas)):
        f = And([m if s else Not(m) for m, s in zip(formulas, signs)]) if formulas else BoolVal(True)
        if is_sat(f):
            out.append(f)
    return out


def earlier_situations(e, named):
    """Situations for the earlier step: nothing done earlier, or one kind of action done earlier
    (the rest stay open). For each kind that a rule names, its details (branch, path, task,
    success) take every region the rules tell apart (v2.1: details belong to that step)."""
    kinds = {c for v in named.get("after", []) for c in expand(v)}
    if "after_task" in named or "after_ok" in named:
        kinds.add("run")
    if "after_path" in named:
        kinds |= set(FILE_ACTIONS) if not kinds & set(FILE_ACTIONS) else set()
    br = sorted({str(v) for v in named.get("after_branch", [])})
    paths = [v for v in named.get("after_path", [])]
    tasks = sorted({task_name(v) for v in named.get("after_task", [])})
    out = [And([Not(p) for p in e.prior.values()])]
    for c in CMDS:
        if c not in kinds:
            out.append(e.prior[c])
            continue
        parts = [InRe(e.prior_branch[c], glob_re(q)) for q in br]
        if c in e.prior_path:
            parts += [InRe(e.prior_path[c], target_re(p)) for p in paths]
        if c == "run":
            parts += [e.prior_task == StringVal(t) for t in tasks]
        for r in regions(parts):
            if c == "run" and "after_ok" in named:
                out += [And(e.prior[c], r, e.prior_ok == BoolVal(v)) for v in (False, True)]
            else:
                out.append(And(e.prior[c], r))
    return out


def situations(e, x, clauses):
    """Every situation to test clause x in.
    - Facts the world fixes (user asked, tests passed, which processes run) take every value
      that EITHER rule tells apart, not only the facts x names: "push only when asked" must be
      tested against "always push at the end" in the case where the user did not ask.
    - Earlier actions (after, after_branch) are the agent's own: they are a situation only
      where a rule says when it applies (in `where`). In `needs` they are a step the agent can
      take first ("before creating a branch, check out main"), so they are left to the solver.
    - Number of files: values only from clause x itself, as in git_check.py.
    x's own unknown condition (when_unmodeled) holds. For may_do, each listed action is tested
    on its own."""
    named = dict()
    for k, v in fields_named(clauses):
        if k not in ("after", "min_files", "max_files") + tuple(AFTER_FIELDS):
            named.setdefault(k, []).append(v)
    for k, v in fields_named(clauses, ("where",)):
        if k == "after" or k in AFTER_FIELDS:
            named.setdefault(k, []).append(v)
    for k, v in fields_named([x]):
        if k in ("min_files", "max_files"):
            named.setdefault(k, []).append(v)
    dims = []
    if "_cond" in x["where"]:
        dims.append([e.cond(x["where"]["_cond"]) == BoolVal(True)])
    for k in WORLD_BOOLS:
        if k in named:
            dims.append([e.b[k] == BoolVal(v) for v in (False, True)])
    after_keys = ("after",) + tuple(AFTER_FIELDS)
    if any(k in named for k in after_keys):
        dims.append(earlier_situations(e, named))
    for name in sorted({norm_name(n) for names in named.get("running", []) for n in names}):
        dims.append([e.running(name) == BoolVal(v) for v in (False, True)])
    limits = [int(v) for k in ("min_files", "max_files") for v in named.get(k, [])]
    if limits:
        vals = sorted({v for t in limits for v in (t - 1, t, t + 1) if v >= 0} | {0, 1})
        dims.append([e.n_files == v for v in vals])
    if x["type"] == "may_do":
        cmds = expand(x["where"]["cmd"])
        dims.append([e.cmd == CMDS.index(c) for c in cmds])
    yield from (list(combo) for combo in product(*dims))


def check_actions(ca, cb):
    """ca, cb: prepared action clauses of rule a and rule b. Returns (verdict, detail)."""
    for own, other, tag in ((ca, cb, "a"), (cb, ca, "b")):
        for i, x in enumerate(own):
            if x["type"] not in ("must_do", "may_do", "only_if"):
                continue
            e = Event(f"{tag}{i}")
            base = [e.wellformed(), e.match(x["where"])]
            if x["type"] != "only_if" and not is_sat(*base, *constraints(e, own)):
                return "invalid", {"error": f"rule_{tag} clause {i} cannot be met on its own"}
            for fixed in situations(e, x, ca + cb):
                if not is_sat(*base, *fixed, *constraints(e, own)):
                    continue  # not a situation this rule can handle on its own
                if x["type"] == "only_if" and not is_sat(*base, *fixed, *constraints(e, other)):
                    continue  # the other rule simply forbids this action here: skip it
                if is_sat(*base, *fixed, *constraints(e, own), *constraints(e, other)):
                    continue
                s = Solver()
                s.add(*base, *fixed, *constraints(e, own))
                s.check()
                blockers = [j for j, c in enumerate(other)
                            if not is_sat(*base, *fixed, *constraints(e, own), *constraints(e, [c]))]
                verdict = "exception" if x["type"] == "may_do" else "clash"
                return verdict, {"by": f"rule_{tag} clause {i}", "action": witness(s.model(), e),
                                 "blocked_by": blockers}
    return "compatible", {}


def cond_texts(clauses):
    """unknown-fact name -> condition text, for prepared clauses."""
    return {c["where"]["_cond"]: c.get("when_unmodeled", "") for c in clauses if "_cond" in c.get("where", {})}


def check_conditional(ca, cb):
    """For a pair that is compatible: does it clash if some unknown conditions (ADR 0004) hold
    at the same time? Returns ("possible_clash", detail) with a subset-minimal set of the other
    conditions needed, or None. This proves only "the rules clash IF these conditions can hold
    at once"; whether they can is not decided here (Codex consult 2)."""
    texts = {**cond_texts(ca), **cond_texts(cb)}
    if not texts:
        return None
    for own, other, tag in ((ca, cb, "a"), (cb, ca, "b")):
        for i, x in enumerate(own):
            if x["type"] not in ("must_do", "may_do", "only_if"):
                continue
            e = Event(f"{tag}{i}")
            base = [e.wellformed(), e.match(x["where"])]
            own_cond = x["where"].get("_cond")
            lits = [(name, e.cond(name)) for name in texts if name != own_cond]
            if not lits:
                continue
            for fixed in situations(e, x, ca + cb):
                assume = [v for _, v in lits]
                if not is_sat(*base, *fixed, *constraints(e, own), *assume):
                    continue  # own rule cannot be followed under these conditions
                if x["type"] == "only_if" and not is_sat(*base, *fixed, *constraints(e, other), *assume):
                    continue
                s = Solver()
                s.add(*base, *fixed, *constraints(e, own), *constraints(e, other))
                if s.check(*assume) != unsat:
                    continue
                need = list(lits)  # shrink to a subset-minimal set of conditions
                for item in list(need):
                    trial = [v for n, v in need if n != item[0]]
                    if s.check(*trial) == unsat:
                        need = [p for p in need if p[0] != item[0]]
                conds = ([texts[own_cond]] if own_cond else []) + [texts[n] for n, _ in need]
                return "possible_clash", {"by": f"rule_{tag} clause {i}",
                                          "kind": "exception" if x["type"] == "may_do" else "clash",
                                          "conditions": conds}
    return None


def check_pair(ta, tb):
    """ta, tb: translations (status ok / unclear / not_in_scope / invalid_output)."""
    if ta.get("status") != "ok" or tb.get("status") != "ok":
        return "skipped", {"status": [ta.get("status"), tb.get("status")]}
    try:
        states = check_states(state_clauses(ta["clauses"]), state_clauses(tb["clauses"]))
        if states[0] == "invalid":
            return states
        ca = prepared(action_clauses(ta["clauses"]), "a")
        cb = prepared(action_clauses(tb["clauses"]), "b")
        actions = check_actions(ca, cb)
        if actions[0] != "compatible":
            return actions
        if states[0] != "compatible":
            return states
        return check_conditional(ca, cb) or states
    except (ValueError, TypeError, KeyError) as err:
        return "invalid", {"error": f"{type(err).__name__}: {err}"}
