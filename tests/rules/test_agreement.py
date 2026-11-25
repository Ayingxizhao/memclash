"""Do two translations of one rule mean the same? (rules/agreement.py)"""

import pytest

from rules.agreement import agreement, same_meaning


def ok(*clauses):
    return {"status": "ok", "reason": "", "clauses": list(clauses), "left_out": ""}


def c(type_, **where):
    return {"type": type_, "where": where}


SAME = {
    "clause order does not matter":
        (ok(c("never", cmd=["push"]), c("must_do", cmd=["commit"])),
         ok(c("must_do", cmd=["commit"]), c("never", cmd=["push"]))),
    "a group equals its listed actions":
        (ok(c("never", cmd=["push"])), ok(c("never", cmd=["push_branch", "push_delete", "force_push"]))),
    "two never clauses equal one with both actions":
        (ok(c("never", cmd=["push"]), c("never", cmd=["rebase"])),
         ok(c("never", cmd=["push", "rebase"]))),
    "may A or B equals may A plus may B":
        (ok(c("may_do", cmd=["commit", "pull"])), ok(c("may_do", cmd=["commit"]), c("may_do", cmd=["pull"]))),
    "equivalent patterns written two ways":  # a/**/b already covers a/b
        (ok(c("never", cmd=["delete"], path=["src/**/x.db"])),
         ok(c("never", cmd=["delete"], path=["src/x.db", "src/**/x.db"]))),
    "obligation read together with the rule's own restriction":
        (ok(c("must_do", cmd=["push"]), c("never", cmd=["force_push"])),
         ok(c("must_do", cmd=["push_branch", "push_delete"]), c("never", cmd=["force_push"]))),
    "unknown condition worded differently":
        (ok({**c("never", cmd=["push"]), "when_unmodeled": "during a hotfix"}),
         ok({**c("never", cmd=["push"]), "when_unmodeled": "while hotfixing"})),
    "repo state split or combined":
        (ok(c("never_hold", in_repo=["dist/"]), c("never_hold", in_repo=["build/"])),
         ok(c("never_hold", in_repo=["build/", "dist/"]))),
    "both not in scope":
        ({"status": "not_in_scope", "reason": "style"}, {"status": "not_in_scope", "reason": "tabs"}),
    "both unclear on the same word":
        ({"status": "unclear", "word": "Write", "reason": ""}, {"status": "unclear", "word": "write", "reason": "x"}),
}

DIFFERENT = {
    "must do A and B is not must do A or B":
        (ok(c("must_do", cmd=["commit"]), c("must_do", cmd=["push_branch"])),
         ok(c("must_do", cmd=["commit", "push_branch"]))),
    "bare name (any depth) vs root folder":
        (ok(c("never", cmd=["delete"], path=["vendor/"])),
         ok(c("never", cmd=["delete"], path=["vendor", "vendor/**"]))),
    "different path":
        (ok(c("never", cmd=["delete"], path=["a/"])), ok(c("never", cmd=["delete"], path=["b/"]))),
    "folder vs only its contents":
        (ok(c("never", cmd=["delete"], path=["vendor/"])), ok(c("never", cmd=["delete"], path=["vendor/**"]))),
    "never vs may":
        (ok(c("never", cmd=["push"])), ok(c("may_do", cmd=["push"]))),
    "condition present vs absent":
        (ok({**c("never", cmd=["push"]), "when_unmodeled": "during a hotfix"}), ok(c("never", cmd=["push"]))),
    "only_if needs differ":
        (ok({"type": "only_if", "where": {"cmd": ["push"]}, "needs": {"user_asked": True}}),
         ok({"type": "only_if", "where": {"cmd": ["push"]}, "needs": {"user_confirmed": True}})),
    "repo state: different paths":
        (ok(c("must_hold", in_repo=["docs/"])), ok(c("must_hold", in_repo=["docs/api/"]))),
    "repo state: must vs never":
        (ok(c("must_hold", in_repo=["docs/"])), ok(c("never_hold", in_repo=["docs/"]))),
    "ok vs unclear":
        (ok(c("never", cmd=["push"])), {"status": "unclear", "word": "push", "reason": ""}),
    "unclear on different words":
        ({"status": "unclear", "word": "write", "reason": ""}, {"status": "unclear", "word": "add", "reason": ""}),
    "an invalid translation agrees with nothing":
        (ok(c("never", cmd=["erase"])), ok(c("never", cmd=["erase"]))),
}


@pytest.mark.parametrize("name", SAME)
def test_same(name):
    a, b = SAME[name]
    assert same_meaning(a, b) and same_meaning(b, a)


@pytest.mark.parametrize("name", DIFFERENT)
def test_different(name):
    a, b = DIFFERENT[name]
    assert not same_meaning(a, b) and not same_meaning(b, a)


def test_agreement_over_three_runs():
    a = ok(c("never", cmd=["push"]))
    b = ok(c("never", cmd=["push_branch", "push_delete", "force_push"]))
    assert agreement([a, b, a])
    assert not agreement([a, b, ok(c("never", cmd=["commit"]))])
