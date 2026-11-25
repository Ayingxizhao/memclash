"""Repository state: "X must be in the repo" (must_hold in_repo) vs "X must not be in the repo"
(never_hold in_repo). ADR 0008, section 7.

`in_repo:X` is a state (git calls it "tracked"), not an action. Two state clauses conflict
when one path matches both targets: the solver picks that path as the witness. This is its own
verdict, "state conflict", because ADR 0003 defines clashes over a single action. State
clauses are not linked to actions in this version (a `commit` rule and an `in_repo` rule are
not compared).

A never_hold with `when_unmodeled` applies only under an unknown fact the solver may set
false, so it never conflicts with another rule (ADR 0004).
"""

from z3 import InRe, Solver, String, sat

from rules.patterns import target_re
from rules.vocab import STATE_TYPES


def state_clauses(clauses):
    return [c for c in clauses if c["type"] in STATE_TYPES]


def target(c):
    w = c["where"]
    extra = set(w) - {"in_repo", "path_except"}
    if extra or "in_repo" not in w:
        raise ValueError(f"a state clause has in_repo and path_except only, not {sorted(extra)}")
    return target_re(w["in_repo"], w.get("path_except", []))


def overlap(must, never):
    """A path in both targets, or None."""
    p = String("repo_path")
    s = Solver()
    s.add(InRe(p, target(must)), InRe(p, target(never)))
    return s.model().eval(p).as_string() if s.check() == sat else None


def conflicts(musts, nevers, can_skip_never):
    for i, m in musts:
        for j, n in nevers:
            if can_skip_never and n.get("when_unmodeled"):
                continue
            path = overlap(m, n)
            if path is not None:
                yield i, j, path


def check_states(ta_clauses, tb_clauses):
    """Returns (verdict, detail): invalid / state_conflict / compatible."""
    sides = {}
    for tag, cs in (("a", ta_clauses), ("b", tb_clauses)):
        idx = list(enumerate(cs))
        musts = [(i, c) for i, c in idx if c["type"] == "must_hold"]
        nevers = [(i, c) for i, c in idx if c["type"] == "never_hold"]
        for i, j, path in conflicts(musts, nevers, can_skip_never=False):
            return "invalid", {"error": f"rule_{tag} clauses {i} and {j} demand opposite states",
                               "path": path}
        sides[tag] = (musts, nevers)
    for own, other in (("a", "b"), ("b", "a")):
        for i, j, path in conflicts(sides[own][0], sides[other][1], can_skip_never=True):
            return "state_conflict", {"must_hold": f"rule_{own} clause {i}",
                                      "never_hold": f"rule_{other} clause {j}", "path": path}
    return "compatible", {}

