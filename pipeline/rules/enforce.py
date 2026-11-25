"""Runtime enforcement: does one proposed action break a translated rule?

An action is a structured event (docs/review/enforce_prereg.md, Material 2):
  {"cmd", "branch", "path", "dest_path", "kind", "task", "flags": {bool: ...},
   "running": [task names], "prior": [{"cmd", "task", "branch", "path", "ok"}, ...]}
Every Z3 variable of `model.Event` is fixed to the event's value, and each `never` / `only_if`
clause is checked under that assignment. Unknown conditions (`when_unmodeled`) are taken as
false, so such a clause never blocks (prereg: counts as "allowed"). `must_do`, `may_do` and
repository states cannot be judged from one action and are skipped.
Tests: tests/rules/test_enforce.py (hand-written cases only).
"""

from z3 import And, BoolVal, Not, Solver, StringVal, sat

from rules.model import Event, action_clauses, constraints, prepared
from rules.vocab import BOOLS, CMDS, FILE_ACTIONS, norm_name, task_name


def _names(clauses, key):
    """Every name a clause mentions under `key` (e.g. running processes)."""
    out = set()
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == key:
                    out.update(v)
                else:
                    walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)
    walk(clauses)
    return out


def _clean(p):
    """Event paths are repo-relative like rule patterns: "./x" and "/x" mean "x"."""
    p = (p or "").strip()
    p = p[2:] if p.startswith("./") else p
    return p.lstrip("/")


def facts(e, ev, clauses):
    """Formulas fixing Event `e` to the concrete event `ev`."""
    fs = [e.cmd == CMDS.index(ev["cmd"])]
    fs += [e.s["branch"] == StringVal(ev.get("branch") or "")]
    fs += [e.s[f] == StringVal(_clean(ev.get(f))) for f in ("path", "dest_path")]
    t = ev.get("task")
    fs.append(e.s["task"] == StringVal(task_name(t) if t else ""))
    fs.append(e.is_dir == BoolVal(ev.get("kind") == "dir"))
    fs.append(e.suite_all == BoolVal(bool(ev.get("suite_all", False))))
    fs.append(e.n_files == int(ev.get("n_files", 1 if ev.get("path") else 0)))
    flags = ev.get("flags", {})
    fs += [e.b[k] == BoolVal(bool(flags.get(k, False))) for k in BOOLS]
    running = {norm_name(n) for n in ev.get("running", [])}
    fs += [e.running(n) == BoolVal(norm_name(n) in running) for n in _names(clauses, "running")]
    # earlier steps: the newest step of each kind carries the details (one per kind, vocab v2.1)
    last = {}
    for p in ev.get("prior", []):
        last[p["cmd"]] = p
    for c in CMDS:
        fs.append(e.prior[c] == BoolVal(c in last))
        if c in last:
            fs.append(e.prior_branch[c] == StringVal(last[c].get("branch") or ""))
            if c in FILE_ACTIONS:
                fs.append(e.prior_path[c] == StringVal(_clean(last[c].get("path"))))
    run = last.get("run")
    fs.append(e.prior_task == StringVal(task_name(run["task"]) if run and run.get("task") else ""))
    fs.append(e.prior_ok == BoolVal(bool(run and run.get("ok", True))))
    return fs


def unknown_false(e, n):
    return [e.cond(f"c{i}") == BoolVal(False) for i in range(n)]


def check(ev, translation):
    """Indexes of the clauses of one translated rule that the event breaks ([] = allowed)."""
    if not translation or translation.get("status") != "ok" or not translation.get("clauses"):
        return []
    cls = prepared(action_clauses(translation["clauses"]), "c")
    e = Event("ev")
    base = facts(e, ev, cls) + unknown_false(e, len(cls))
    broken = []
    for i, c in enumerate(cls):
        cs = constraints(e, [c])
        if not cs:  # must_do / may_do: not judged from one action
            continue
        s = Solver()
        s.add(e.wellformed(), *base, Not(And(cs)))
        if s.check() == sat:
            broken.append(i)
    return broken


def judge(ev, rules):
    """rules: {rule_id: translation}. Returns {"allowed", "rule_ids", "clauses"}."""
    hits = {}
    for rid, tr in rules.items():
        try:
            b = check(ev, tr)
        except (ValueError, KeyError) as x:  # a translation the checker cannot use = allowed
            hits.setdefault("_errors", []).append(f"{rid}: {x}")
            continue
        if b:
            hits[rid] = b
    errors = hits.pop("_errors", [])
    return {"allowed": not hits, "rule_ids": sorted(hits), "clauses": hits, "errors": errors}
