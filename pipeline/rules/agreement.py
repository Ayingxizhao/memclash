"""Do two translations of the same rule mean the same? Used to measure agreement across the
three translation runs (ADR 0008). Checked with Z3, not by comparing text, so clause order,
groups vs listed actions, and equivalent patterns do not count as differences.

Two `ok` translations mean the same when all of these hold:
- restrictions: for every possible action, the never / only_if clauses allow exactly the
  same actions;
- obligations: each must_do of one has an equivalent must_do in the other, and the other way
  round. "Must do A and B" (two clauses) is NOT "must do A or B" (one clause). Each obligation
  is compared together with the rule's own restrictions, since only that part can be done;
- permissions: the same set of permitted actions, one per listed action ("may A or B" = "may
  A" + "may B");
- repository states: for must_hold and for never_hold, the paths covered are the same.
A `when_unmodeled` condition is one shared unknown fact per rule: whether a clause has one is
compared, its wording is not (runs word the same condition differently).
Two translations that are not `ok` mean the same when the status is the same (and, for
unclear, the same word).
"""

from z3 import And, BoolVal, InRe, Or, String

from rules.model import Event, action_clauses, constraints
from rules.patterns import is_sat
from rules.state import state_clauses, target
from rules.vocab import expand, norm_name


def unmodeled_shared(clauses):
    """Every when_unmodeled clause gets the same unknown fact, so wording does not matter."""
    out = []
    for c in clauses:
        c = dict(c)
        if c.get("when_unmodeled"):
            c["where"] = {**c["where"], "_cond": "unmodeled"}
        out.append(c)
    return out


def equivalent(e, f, g):
    return not is_sat(e.wellformed(), f != g)


def same_classes(e, fs, gs):
    """Every formula in fs has an equivalent in gs and the other way round."""
    return (all(any(equivalent(e, f, g) for g in gs) for f in fs)
            and all(any(equivalent(e, g, f) for f in fs) for g in gs))


def parts(t, e):
    cs = unmodeled_shared(action_clauses(t["clauses"]))
    rules = constraints(e, cs)
    restrict = And(rules) if rules else BoolVal(True)
    musts = [And(e.match(c["where"]), restrict) for c in cs if c["type"] == "must_do"]
    mays = [e.match({**c["where"], "cmd": [cmd]})
            for c in cs if c["type"] == "may_do" for cmd in expand(c["where"]["cmd"])]
    return restrict, musts, mays


def covered(clauses, kind, p):
    """Paths covered by all must_hold (or never_hold) clauses, as a formula over path p.
    Clauses with and without an unknown condition are kept apart."""
    out = {}
    for c in state_clauses(clauses):
        if c["type"] == kind:
            out.setdefault(bool(c.get("when_unmodeled")), []).append(InRe(p, target(c)))
    return {k: Or(v) for k, v in out.items()}


def same_states(ta, tb):
    p = String("agree_path")
    for kind in ("must_hold", "never_hold"):
        a, b = covered(ta["clauses"], kind, p), covered(tb["clauses"], kind, p)
        if set(a) != set(b):
            return False
        if any(is_sat(a[k] != b[k]) for k in a):
            return False
    return True


def same_meaning(ta, tb):
    sa, sb = ta.get("status"), tb.get("status")
    if sa not in ("ok", "unclear", "not_in_scope") or sb not in ("ok", "unclear", "not_in_scope"):
        return False  # bad output or an unknown status means nothing, so it agrees with nothing
    if sa != "ok" or sb != "ok":
        if sa != sb:
            return False
        return sa != "unclear" or norm_name(ta.get("word", "")) == norm_name(tb.get("word", ""))
    try:
        e = Event("agree")
        ra, ma, pa = parts(ta, e)
        rb, mb, pb = parts(tb, e)
        return (equivalent(e, ra, rb) and same_classes(e, ma, mb) and same_classes(e, pa, pb)
                and same_states(ta, tb))
    except (ValueError, TypeError, KeyError):
        return False  # an invalid translation agrees with nothing


def agreement(translations):
    """translations: the runs of one rule. True if every run means the same as the first."""
    first, *rest = translations
    return all(same_meaning(first, t) for t in rest)



def vote(translations):
    """Group the runs of one rule by meaning (Z3, same_meaning) and return
    (winning translation or None, group sizes). A group of more than half of ALL runs wins
    (failed runs count in the total but never form a group); otherwise the rule is unstable
    and None is returned."""
    groups = []
    for t in translations:
        if t.get("status") not in ("ok", "unclear", "not_in_scope"):
            continue  # a failed run never wins a vote
        for g in groups:
            if same_meaning(g[0], t):
                g.append(t)
                break
        else:
            groups.append([t])
    groups.sort(key=len, reverse=True)
    sizes = [len(g) for g in groups]
    if sizes and sizes[0] * 2 > len(translations):
        return groups[0][0], sizes
    return None, sizes
