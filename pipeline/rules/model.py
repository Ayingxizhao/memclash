"""One action as Z3 variables, and one translated rule as Z3 formulas over it.

A clause's `where` (and `needs`) is a set of fields; `Event.match` turns it into a formula that
is true when the action has those fields. `never` and `only_if` clauses become constraints on
the action (`constraints`). `must_do` / `may_do` are tested by pair.py; `must_hold` /
`never_hold` are repository states, handled by state.py.
"""

from z3 import And, Bool, BoolVal, Implies, InRe, Int, Not, Or, String, StringVal

from rules.patterns import glob_re, target_re
from rules.vocab import (AFTER_FIELDS, BOOLS, BRANCH_FIELDS, CMDS, FIELDS, FILE_ACTIONS, PATH_FIELDS,
                         STATE_TYPES, expand, norm_name, task_name)


def _paths(v):
    """A path pattern may be written as one string or a list; a bare string must not be read
    letter by letter (fix logged in docs/review/boundary_results.md)."""
    return [v] if isinstance(v, str) else list(v)


class Event:
    """Z3 variables for one action; `tag` keeps the actions of different clauses apart."""

    def __init__(self, tag):
        self.tag = tag
        self.cmd = Int(f"{tag}_cmd")
        # which actions happened at some earlier point (several can be true)
        self.prior = {c: Bool(f"{tag}_prior_{c}") for c in CMDS}
        # details of the earlier step of each kind (v2.1): its branch, its path, and for run its
        # task and whether it succeeded
        self.prior_branch = {c: String(f"{tag}_prior_branch_{c}") for c in CMDS}
        self.prior_path = {c: String(f"{tag}_prior_path_{c}") for c in FILE_ACTIONS}
        self.prior_task = String(f"{tag}_prior_task")
        self.prior_ok = Bool(f"{tag}_prior_ok")
        self.n_files = Int(f"{tag}_n_files")
        self.s = {f: String(f"{tag}_{f}") for f in PATH_FIELDS + BRANCH_FIELDS + ["task"]}
        self.b = {k: Bool(f"{tag}_{k}") for k in BOOLS}
        self.is_dir = Bool(f"{tag}_is_dir")
        self.suite_all = Bool(f"{tag}_suite_all")

    def running(self, name):
        """Process `name` is running (one yes/no per name)."""
        return Bool(f"{self.tag}_running_{norm_name(name)}")

    def cond(self, name):
        """An unknown yes/no fact: a condition the rule names but the vocabulary cannot express."""
        return Bool(f"{self.tag}_cond_{name}")

    def wellformed(self):
        return And(self.cmd >= 0, self.cmd < len(CMDS), self.n_files >= 0)

    def is_cmd(self, names):
        return Or([self.cmd == CMDS.index(c) for c in expand(names)])

    def earlier(self, where):
        """An earlier step of one of the `after` kinds, with all the after_* details on that same
        step. Without `after`, the details pick the kinds they can describe."""
        task, path, ok, br = (where.get(k) for k in ("after_task", "after_path", "after_ok", "after_branch"))
        if "after" in where:
            kinds = expand(where["after"])
        else:
            kinds = ["run"] if task is not None or ok is not None else FILE_ACTIONS if path is not None else CMDS
        if (task is not None or ok is not None) and "run" not in kinds:
            raise ValueError("after_task / after_ok need run in after")
        if path is not None and not set(kinds) & set(FILE_ACTIONS):
            raise ValueError("after_path needs a file action in after")
        if ok is not None and not isinstance(ok, bool):
            raise ValueError("after_ok must be true/false")
        opts = []
        for c in kinds:
            if (task is not None or ok is not None) and c != "run":
                continue
            if path is not None and c not in FILE_ACTIONS:
                continue
            f = [self.prior[c]]
            if br is not None:
                f.append(InRe(self.prior_branch[c], glob_re(br)))
            if path is not None:
                f.append(InRe(self.prior_path[c], target_re(path)))
            if task is not None:
                f.append(self.prior_task == StringVal(task_name(task)))
            if ok is not None:
                f.append(self.prior_ok == BoolVal(ok))
            opts.append(And(f))
        return Or(opts)

    def match(self, where):
        cs = []
        if "path_except" in where and "path" not in where:
            raise ValueError("path_except without path")
        if "after" in where or any(k in where for k in AFTER_FIELDS):
            cs.append(self.earlier(where))
        for k, v in where.items():
            if k == "_cond":
                cs.append(self.cond(v))
            elif k not in FIELDS:
                raise ValueError(f"unknown field {k!r}")
            elif k == "cmd":
                cs.append(self.is_cmd(v))
            elif k == "path":
                cs.append(InRe(self.s["path"], target_re(_paths(v), _paths(where.get("path_except", [])))))
            elif k == "dest_path":
                cs.append(InRe(self.s["dest_path"], target_re(_paths(v))))
            elif k == "path_except" or k == "after" or k in AFTER_FIELDS:
                continue  # part of `path` / of the earlier step (self.earlier)
            elif k in BRANCH_FIELDS:
                cs.append(InRe(self.s[k], glob_re(v)))
            elif k == "kind":
                if v not in ("file", "dir"):
                    raise ValueError(f"kind must be file or dir, not {v!r}")
                cs.append(self.is_dir == BoolVal(v == "dir"))
            elif k == "task":
                cs.append(self.s["task"] == StringVal(task_name(v)))
            elif k == "suite":
                if v != "all":
                    raise ValueError(f"suite must be 'all', not {v!r}")
                cs.append(self.suite_all)
            elif k == "running":
                cs.append(And([self.running(n) for n in v]))
            elif k == "min_files":
                cs.append(self.n_files >= int(v))
            elif k == "max_files":
                cs.append(self.n_files <= int(v))
            elif isinstance(v, bool):
                cs.append(self.b[k] == BoolVal(v))
            else:
                raise ValueError(f"{k} must be true/false")
        return And(cs) if cs else BoolVal(True)


def check_clause(c):
    """Rules of the format the schema cannot express on its own."""
    if "cmd" in c.get("needs", {}):
        raise ValueError("an action in needs (write 'before X do Y' as needs after: [Y])")
    if c["type"] == "only_if" and "needs" not in c:
        raise ValueError("only_if without needs")


def action_clauses(clauses):
    out = [c for c in clauses if c["type"] not in STATE_TYPES]
    for c in out:
        check_clause(c)
    return out


def constraints(e, clauses):
    """What `never` and `only_if` clauses demand of action e."""
    out = []
    for c in clauses:
        if c["type"] == "never":
            out.append(Not(e.match(c["where"])))
        elif c["type"] == "only_if":
            out.append(Implies(e.match(c["where"]), e.match(c["needs"])))
    return out


def prepared(clauses, tag):
    """A clause with `when_unmodeled` applies only when an unknown fact of its own holds
    (ADR 0004). No other rule names that fact, so at worst a clash is missed."""
    out = []
    for i, c in enumerate(clauses):
        c = dict(c)
        if c.get("when_unmodeled"):
            c["where"] = {**c["where"], "_cond": f"{tag}{i}"}
        out.append(c)
    return out


def witness(model, e):
    """The action the solver found, in the translation's own field names."""
    out = {"cmd": CMDS[model.eval(e.cmd).as_long()]}
    done = [c for c in CMDS if bool(model.eval(e.prior[c], model_completion=True))]
    if done:
        out["after"] = done
        for c in done:  # details of the earlier steps, where the solver fixed them
            v = model.eval(e.prior_branch[c])
            if hasattr(v, "as_string") and v.as_string():
                out.setdefault("after_branch", v.as_string())
            if c in e.prior_path:
                v = model.eval(e.prior_path[c])
                if hasattr(v, "as_string") and v.as_string():
                    out.setdefault("after_path", v.as_string())
        if "run" in done:
            v = model.eval(e.prior_task)
            if hasattr(v, "as_string") and v.as_string():
                out["after_task"] = v.as_string()
            out["after_ok"] = bool(model.eval(e.prior_ok, model_completion=True))
    for f, v in e.s.items():
        v = model.eval(v)
        if hasattr(v, "as_string") and v.as_string():
            out[f] = v.as_string()
    for k in BOOLS:
        out[k] = bool(model.eval(e.b[k], model_completion=True))
    return out
