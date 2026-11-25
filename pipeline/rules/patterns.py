"""File-name and branch patterns (vocabulary v2, docs/adr/0008, section 4), as Z3 regexes.

Part of pipeline/rules/: the git and file rule checker. pipeline/git/git_check.py stays
unchanged so earlier results can be rerun. Tests: tests/rules/test_patterns.py.
"""

from z3 import (AllChar, Complement, Concat, InRe, Intersect, Option, Re, ReSort, Solver, Star,
                String, StringSort, StringVal, Union, sat)

RE = ReSort(StringSort())
ANY = Star(AllChar(RE))                                  # any text, "/" included
SEG_CHAR = Intersect(AllChar(RE), Complement(Re("/")))   # one character that is not "/"


def is_sat(*fs):
    s = Solver()
    s.add(*fs)
    return s.check() == sat


# ---------------------------------------------------------------- patterns (ADR 0008, section 4)

def glob_re(pattern):
    """Wildcards: `*` = any text inside one folder level, `?` = one character that is not "/",
    `**` = any depth. `a/**/b` also matches `a/b`; `a/**` matches everything inside a/."""
    p, pieces, i = str(pattern), [], 0
    lit = ""
    while i < len(p):
        if p.startswith("**/", i):
            pieces += [Re(lit)] if lit else []
            lit = ""
            pieces.append(Option(Concat(ANY, Re("/"))))  # zero or more folder levels
            i += 3
        elif p.startswith("**", i):
            pieces += [Re(lit)] if lit else []
            lit = ""
            pieces.append(ANY)
            i += 2
        elif p[i] in "*?":
            pieces += [Re(lit)] if lit else []
            lit = ""
            pieces.append(Star(SEG_CHAR) if p[i] == "*" else SEG_CHAR)
            i += 1
        else:
            lit += p[i]
            i += 1
    pieces += [Re(lit)] if lit else []
    if not pieces:
        return Re("")
    return pieces[0] if len(pieces) == 1 else Concat(*pieces)


def path_re(pattern):
    """A path pattern as written by the translator, made canonical in code:
    - paths are relative to the repo root ("./" and a leading "/" are dropped);
    - `X/` is the folder X itself and everything in it;
    - a name with no "/" (`server-world.dat`, `*.md`) matches at any depth."""
    p = str(pattern).strip()
    p = p[2:] if p.startswith("./") else p
    p = p.lstrip("/")
    folder = p.endswith("/")
    bare = "/" not in p          # checked before the trailing "/" is dropped: `vendor/` is not bare
    p = p.rstrip("/")
    if bare:
        p = "**/" + p
    r = glob_re(p)
    return Union(r, glob_re(p + "/**")) if folder else r


def target_re(include, exclude=()):
    """In some include pattern and in no exclude pattern (order never matters, no `!`)."""
    r = Union(*[path_re(x) for x in include]) if len(include) > 1 else path_re(include[0])
    if exclude:
        ex = Union(*[path_re(x) for x in exclude]) if len(exclude) > 1 else path_re(exclude[0])
        r = Intersect(r, Complement(ex))
    return r


def matches(regex, text):
    v = String("probe")
    return is_sat(v == StringVal(text), InRe(v, regex))
