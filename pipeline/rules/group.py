"""Check a GROUP of translated rules for a clash that no pair of them has (experiment log G).

A group clashes if, in some situation the rules name, no single action follows all of them,
while every pair inside the group can be followed together (so the clash needs all members).
Same test as pair.check_actions, with the other rules' clauses pooled, plus one addition:

- Only `must_do` / `may_do` trigger a check: "push only after tests pass" with "never run the
  tests" just means the agent never pushes; it clashes once a third rule demands a push.
- Earlier steps obey `never` clauses (and `only_if` clauses whose needs are not about earlier steps). A rule such as "push only after the tests pass" needs an
  earlier run; that earlier run is itself an action, so "never run the tests locally" applies
  to it. The pair checker leaves earlier steps free; here each earlier step of kind c (its
  branch, path, task as recorded on the event) must not match any `never` clause of the group.
  Deeper chains (the earlier step's own earlier steps) are not modelled.

State clauses and unknown-condition (possible_clash) checks are not extended to groups.
"""

from itertools import combinations

from z3 import And, BoolVal, Implies, Not, Solver, StringVal

from rules.model import Event, action_clauses, constraints, prepared, witness
from rules.pair import situations
from rules.patterns import is_sat
from rules.vocab import CMDS, FILE_ACTIONS, WORLD_BOOLS

ACT = ("must_do", "may_do")  # only obligations and permissions trigger a group check


def earlier_obeys(e, clauses):
    """Each earlier step that happened must not match a `never` clause."""
    nevers = [c for c in clauses if c["type"] == "never"]
    ifs = [c for c in clauses if c["type"] == "only_if"
           and not any(k == "after" or k.startswith("after_") for k in c["needs"])]
    if not nevers and not ifs:
        return []
    out = []
    for c in CMDS:
        p = Event(f"{e.tag}_p_{c}")
        same = [p.cmd == CMDS.index(c), p.s["branch"] == e.prior_branch[c]]
        if c in FILE_ACTIONS:
            same.append(p.s["path"] == e.prior_path[c])
        if c == "run":
            same.append(p.s["task"] == e.prior_task)
        same += [p.b[k] == e.b[k] for k in WORLD_BOOLS]
        same += [Not(v) for v in p.prior.values()]  # no deeper chain
        rules = [Not(p.match(n["where"])) for n in nevers]
        rules += [Implies(p.match(c2["where"]), p.match(c2["needs"])) for c2 in ifs]
        out.append(Implies(e.prior[c], And(p.wellformed(), *same, *rules)))
    return out


def cons(e, clauses):
    return constraints(e, clauses) + earlier_obeys(e, clauses)


def strip_after(c):
    """The clause with its earlier-step fields removed from `where` (for situations only)."""
    w = {k: v for k, v in c.get("where", {}).items() if not (k == "after" or k.startswith("after_"))}
    return {**c, "where": w}


def check_prepared(groups):
    """groups: list of prepared action-clause lists, one per rule. Returns (verdict, detail).
    Earlier-step situations come only from the tested rule's own clauses: the event records one
    earlier step per action kind, so fixing it from another rule ("after a test run") would
    wrongly rule out a different earlier run the tested rule needs (post-hoc fix, log G)."""
    for gi, own in enumerate(groups):
        other = [c for j, g in enumerate(groups) if j != gi for c in g]
        allc = own + [strip_after(c) for c in other]
        for i, x in enumerate(own):
            if x["type"] not in ACT:
                continue
            e = Event(f"g{gi}_{i}")
            base = [e.wellformed(), e.match(x["where"])]
            if not is_sat(*base, *cons(e, own)):
                return "invalid", {"error": f"rule {gi} clause {i} cannot be met on its own"}
            for fixed in situations(e, x, allc):
                if not is_sat(*base, *fixed, *cons(e, own)):
                    continue
                if is_sat(*base, *fixed, *cons(e, own), *cons(e, other)):
                    continue
                s = Solver()
                s.add(*base, *fixed, *cons(e, own))
                s.check()
                return ("exception" if x["type"] == "may_do" else "clash"), {
                    "by": f"rule {gi} clause {i}", "action": witness(s.model(), e)}
    return "compatible", {}


def prepare(translations):
    return [prepared(action_clauses(t["clauses"]), f"r{k}") for k, t in enumerate(translations)]


def check_group(translations):
    """translations: list of 2+ translations. Verdict for the whole group (not minimality)."""
    if any(t.get("status") != "ok" for t in translations):
        return "skipped", {}
    try:
        return check_prepared(prepare(translations))
    except (ValueError, TypeError, KeyError) as err:
        return "invalid", {"error": f"{type(err).__name__}: {err}"}


def group_only(translations):
    """('group_clash' / 'group_exception', detail) if the group clashes but no pair inside it
    does. A pair counts as clashing if the ordinary pair checker flags it (pair.check_pair) or
    the group test flags it as a pair. Otherwise ('pair_<verdict>', detail) or ('compatible', {})."""
    if any(t.get("status") != "ok" for t in translations):
        return "skipped", {}
    try:
        from rules.pair import check_pair
        g = prepare(translations)
        for a, b in combinations(range(len(g)), 2):
            v = check_pair(translations[a], translations[b])
            if v[0] in ("clash", "exception", "state_conflict", "possible_clash", "invalid"):
                return "pair_" + v[0], {"pair": [a, b], **v[1]}
            v = check_prepared([g[a], g[b]])
            if v[0] != "compatible":
                return "pair_" + v[0], {"pair": [a, b], **v[1]}
        v = check_prepared(g)
        return ("group_" + v[0] if v[0] != "compatible" else "compatible"), v[1]
    except (ValueError, TypeError, KeyError) as err:
        return "invalid", {"error": f"{type(err).__name__}: {err}"}


def relevant(t):
    """A rule can take part in a group clash only if it has action clauses."""
    return t.get("status") == "ok" and any(c["type"] in ACT + ("never", "only_if") for c in t.get("clauses", []))


def cmds_of(t):
    from rules.vocab import expand
    out = set()
    for c in t.get("clauses", []):
        for part in ("where", "needs"):
            w = c.get(part, {})
            if "cmd" in w:
                out |= set(expand(w["cmd"]))
            if "after" in w:
                out |= set(expand(w["after"]))
            if "after_task" in w or "after_ok" in w:
                out.add("run")
    return out


def scan_triples(rules, run=0):
    """rules: [{id, runs:[translation...]}] of ONE folder. Every triple whose members share an
    action kind pairwise-connected and that clashes only as a group, for saved run `run`."""
    ts = [(r["id"], r["runs"][run]) for r in rules if relevant(r["runs"][run])]
    cm = {i: cmds_of(t) for i, t in ts}
    found = []
    for (ia, ta), (ib, tb), (ic, tc) in combinations(ts, 3):
        if not any(c["type"] in ACT for t in (ta, tb, tc) for c in t["clauses"]):
            continue
        links = [bool(cm[ia] & cm[ib]), bool(cm[ia] & cm[ic]), bool(cm[ib] & cm[ic])]
        if sum(links) < 2:
            continue  # members must be connected through shared action kinds
        v = group_only([ta, tb, tc])
        if v[0].startswith("group_"):
            found.append({"ids": [ia, ib, ic], "verdict": v[0], "detail": v[1]})
    return found
