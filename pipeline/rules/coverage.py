"""Coverage check for two-step translation (plan: .lavish/two_step_plan.html, section 4c).

Plain code, no LLM. It enforces that nothing is dropped silently:
1. every step-1 quote is an exact piece of the rule (ignoring case and extra spaces);
2. every requirement gets exactly one disposition allowed by its step-1 `keep` (ALLOWED):
   a clause, or `left_out` with a matching reason; every clause names a known requirement.
The check links ids only: it cannot tell whether a clause really says what its requirement
says. That is measured against the labels, not claimed here.
Words of the rule that no quote covers are reported, not rejected (author's decision, Q4).
"""

import re

from rules.template import KEEP, LEFT_OUT_REASONS

# Short function words that carry no requirement; only used for the report-only word check.
STOP = set("a an the and or of to in on for with by at as is are be it its this that these those "
           "your you we our any all each every from into than then when if only do does not no "
           "never always must should may can will".split())


def norm(s):
    return " ".join(str(s).lower().split())


def step1_errors(rule, step1):
    errs = []
    if step1.get("status") not in ("ok", "not_in_scope"):
        errs.append(f"status must be ok or not_in_scope, not {step1.get('status')!r}")
    reqs = step1.get("requirements") or []
    if not reqs:
        errs.append("no requirements listed")
    ids = [r.get("id") for r in reqs]
    if len(set(ids)) != len(ids) or not all(ids):
        errs.append("requirement ids must be present and unique")
    text = norm(rule)
    for r in reqs:
        if not norm(r.get("quote", "")):
            errs.append(f"{r.get('id')}: quote is empty")
        elif norm(r.get("quote", "")) not in text:
            errs.append(f"{r.get('id')}: quote is not an exact piece of the rule: {r.get('quote')!r}")
        aw = norm(r.get("applies_when", ""))
        if aw and aw not in text:
            errs.append(f"{r.get('id')}: applies_when is not an exact piece of the rule: {r.get('applies_when')!r}")
        if r.get("keep") not in KEEP:
            errs.append(f"{r.get('id')}: keep must be one of {KEEP}")
    if step1.get("status") == "ok" and not any(r.get("keep") == "translate" for r in reqs):
        errs.append("status is ok but no requirement is marked translate")
    if step1.get("status") == "not_in_scope" and any(r.get("keep") == "translate" for r in reqs):
        errs.append("status is not_in_scope but a requirement is marked translate")
    return errs


# Allowed disposition per step-1 `keep`: a clause, or `left_out` with one of these reasons.
# `translate` may also be left out as `outside_vocabulary`: step 1 does not see the vocabulary,
# so a concrete git/file requirement can still lack words (e.g. cloning a repository).
ALLOWED = {"translate": {"clause", "unclear_word", "outside_vocabulary"},
           "vague": {"vague"}, "outside_vocabulary": {"outside_vocabulary"}}


def coverage_errors(step1, trace):
    """Every requirement gets exactly one disposition, allowed by its `keep` (ALLOWED)."""
    errs = []
    reqs = {r["id"]: r for r in step1.get("requirements", [])}
    covered = set(trace["clause_req"])
    for c in covered:
        if c not in reqs:
            errs.append(f"a clause names requirement {c!r}, which is not in the list")
    left = {}
    for x in trace["left_out"]:
        rid = x.get("req")
        if rid not in reqs:
            errs.append(f"left_out names requirement {rid!r}, which is not in the list")
        elif x.get("reason") not in LEFT_OUT_REASONS:
            errs.append(f"{rid}: left_out reason must be one of {LEFT_OUT_REASONS}")
        elif x.get("reason") == "unclear_word" and not x.get("word"):
            errs.append(f"{rid}: unclear_word needs the word")
        elif rid in left:
            errs.append(f"{rid} is in left_out twice")
        else:
            left[rid] = x
    for rid, r in reqs.items():
        got = (["clause"] if rid in covered else []) + ([left[rid]["reason"]] if rid in left else [])
        allowed = ALLOWED.get(r.get("keep"), set())
        if not got:
            errs.append(f"{rid} ({r.get('quote')!r}) has no clause and is not in left_out")
        elif len(got) > 1:
            errs.append(f"{rid} is both translated and left out")
        elif got[0] not in allowed:
            errs.append(f"{rid} is marked {r.get('keep')} in step 1 but was given {got[0]}")
    return errs


def apply_scopes(translation, step1, trace):
    """A requirement's scope (`applies_when`, an exact quote from step 1) belongs to every
    clause of that requirement. Unless step 2 says it expressed the scope with fields
    (`scope_encoded`), the scope is kept as an unknown condition on the clause (ADR 0004), so
    a split never turns a limited requirement into an unlimited one (Codex consult 5)."""
    scopes = {r["id"]: r.get("applies_when", "").strip() for r in step1.get("requirements", [])}
    for c, req, enc in zip(translation.get("clauses", []), trace["clause_req"], trace["scope_encoded"]):
        sc = scopes.get(req, "")
        if not sc or enc:
            continue
        have = c.get("when_unmodeled", "")
        if norm(sc) not in norm(have):
            c["when_unmodeled"] = f"{have}; {sc}" if have else sc
    return translation


def uncovered_words(rule, step1):
    """Words of the rule that no quote covers (report only)."""
    covered = " ".join(norm(r.get("quote", "")) for r in step1.get("requirements", []))
    def tokens(text):
        return [w.rstrip(".,;:/-") for w in re.findall(r"[a-z0-9_./-]+", text)]
    words = tokens(norm(rule))
    have = set(tokens(covered))
    return [w for w in words if w not in have and w not in STOP and len(w) > 2]
