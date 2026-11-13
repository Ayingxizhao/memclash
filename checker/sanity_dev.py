"""Plan step 4: hand-encoded dev cases -> Z3 must flag the conflicts and NOT flag the controls.

Encoding (design/schema_v1.md): each facet is a finite enum sort whose values are leaves;
a parent node is the set of its leaves. A rule = (scope over facet variables, modality, action).
  O(a): a must hold    F(a): a must not hold    P(a): a is allowed
Checks:
  overlap        SAT(scope1 & scope2 & axioms)
  contradiction  O/F pairs: overlap is SAT but adding both effects is UNSAT
                 P vs F on the same action: overlap is SAT (P allows what F forbids)
Run: uv run python checker/sanity_dev.py
"""

from dataclasses import dataclass

from z3 import And, Bool, BoolRef, BoolVal, Const, EnumSort, Int, Not, Or, Solver, sat

# ---- facets (finite sorts; values are leaves) ------------------------------------------
Medium, (CHAT, FILE) = EnumSort("Medium", ["chat", "file"])
Artifact, (M1_NOTES, M2_NOTES, CHEATSHEET, NO_ARTIFACT) = EnumSort(
    "Artifact", ["m1_notes", "m2_notes", "cheatsheet", "no_artifact"])
Actor, (AGENT, DB_ANALYST) = EnumSort("Actor", ["agent", "db_analyst"])
Op, (SELECT, DDL, DML) = EnumSort("Op", ["select", "ddl", "dml"])
Task, (INSTALL_PY, INSTALL_JS, OTHER_TASK) = EnumSort("Task", ["install_py_pkg", "install_js_pkg", "other"])

medium, art, actor, op, task = (Const(n, s) for n, s in
                                [("medium", Medium), ("art", Artifact), ("actor", Actor), ("op", Op), ("task", Task)])
confirmed = Bool("user_confirmed")  # situation attribute

# parent nodes = sets of leaves
AOFA_MODULE_NOTES = Or(art == M1_NOTES, art == M2_NOTES)
MUTATION = Or(op == DDL, op == DML)
CODE_INSTALL = Or(task == INSTALL_PY, task == INSTALL_JS)

# ---- actions + axioms ------------------------------------------------------------------
use_latex, execute_sql, use_pip, use_uv = Bool("use_latex"), Bool("execute_sql"), Bool("use_pip"), Bool("use_uv")
sentences = Int("sentences_per_idea")
AXIOMS = [Not(And(use_pip, use_uv))]  # mutex: one package manager per install


@dataclass
class Rule:
    name: str
    scope: BoolRef
    modality: str          # "O" | "F" | "P"
    action: BoolRef        # the action (for P/F/O) or a constraint on params (for O)


def effect(r: Rule):
    return {"O": r.action, "F": Not(r.action), "P": BoolVal(True)}[r.modality]


def solve(*fs):
    s = Solver()
    s.add(*fs, *AXIOMS)
    return s.check() == sat


def check(r1: Rule, r2: Rule) -> str:
    if not solve(r1.scope, r2.scope):
        return "none (no overlap)"
    mods = {r1.modality, r2.modality}
    if mods == {"P", "F"}:
        # P allows the action somewhere F forbids it -> conflict iff they are the same action
        return "contradiction (P vs F)" if r1.action.eq(r2.action) else "overlap, compatible"
    if not solve(r1.scope, r2.scope, effect(r1), effect(r2)):
        return "contradiction"
    return "overlap, compatible"


# ---- cases: (r1, r2, expected) --------------------------------------------------------
R8 = Rule("R8 module notes: no LaTeX", And(medium == FILE, AOFA_MODULE_NOTES), "F", use_latex)
R20 = Rule("R20 Module 2: write math in LaTeX", And(medium == FILE, art == M2_NOTES), "O", use_latex)
R31 = Rule("R31 chat: no LaTeX", medium == CHAT, "F", use_latex)
R33 = Rule("R33 course source files use LaTeX", And(medium == FILE, AOFA_MODULE_NOTES), "O", use_latex)
R36 = Rule("R36 index: never LaTeX", BoolVal(True), "F", use_latex)

DB_SCOPE = And(actor == DB_ANALYST, MUTATION)
R35 = Rule("R35 db-analyst SELECT-only", DB_SCOPE, "F", execute_sql)
R32 = Rule("R32 no mutation without confirmation", And(DB_SCOPE, Not(confirmed)), "F", execute_sql)
R32P = Rule("R32' (hypothetical) mutation allowed once confirmed", And(DB_SCOPE, confirmed), "P", execute_sql)

PIP = Rule("pip for Python installs", task == INSTALL_PY, "O", use_pip)
UV = Rule("uv for all code installs", CODE_INSTALL, "O", use_uv)
UV_JS = Rule("uv for JS installs only", task == INSTALL_JS, "O", use_uv)

N3 = Rule("exactly 3 sentences per idea", BoolVal(True), "O", sentences == 3)
N5 = Rule("exactly 5 sentences per idea", BoolVal(True), "O", sentences == 5)
N3A = Rule("~3 sentences as [2,4]", BoolVal(True), "O", And(sentences >= 2, sentences <= 4))
N5A = Rule("~5 sentences as [4,6]", BoolVal(True), "O", And(sentences >= 4, sentences <= 6))

CASES = [
    (R8, R20, "contradiction"),
    (R8, R33, "contradiction"),
    (R36, R33, "contradiction"),          # index drift; Z3 sees the conflict, dates would make it 'stale'
    (R31, R33, "none (no overlap)"),      # control: chat vs files, explicit scope split
    (R31, R20, "none (no overlap)"),      # control
    (R35, R32, "overlap, compatible"),    # control: implicit permission is not a conflict
    (R35, R32P, "contradiction (P vs F)"),
    (PIP, UV, "contradiction"),           # proposal example: overlap via hierarchy + mutex
    (PIP, UV_JS, "none (no overlap)"),    # control
    (N3, N5, "contradiction"),
    (N3A, N5A, "overlap, compatible"),    # approximation choice decides the outcome
]

if __name__ == "__main__":
    ok = 0
    for r1, r2, expected in CASES:
        got = check(r1, r2)
        ok += got == expected
        print(f"{'PASS' if got == expected else 'FAIL'}  {got:24} | {r1.name}  <->  {r2.name}")
    print(f"\n{ok}/{len(CASES)} cases as expected")
