"""Coverage check for two-step translation (rules/coverage.py)."""

from rules.coverage import coverage_errors, step1_errors, uncovered_words

RULE = "Before any commit, verify no .env files, API keys, or secrets are staged."
S1 = {"status": "ok", "reason": "", "requirements": [
    {"id": "q1", "quote": "Before any commit, verify", "keep": "translate", "why": ""},
    {"id": "q2", "quote": "no .env files, API keys, or secrets are staged", "keep": "translate", "why": ""}]}


def test_good_step1_passes():
    assert step1_errors(RULE, S1) == []


def test_quote_must_be_an_exact_piece_of_the_rule():
    bad = {**S1, "requirements": [{**S1["requirements"][0], "quote": "check before committing"}]}
    assert any("not an exact piece" in e for e in step1_errors(RULE, bad))


def test_quote_ignores_case_and_spaces():
    ok = {**S1, "requirements": [{**S1["requirements"][0], "quote": "before  ANY commit"}]}
    assert step1_errors(RULE, ok) == []


def test_status_must_match_keep():
    bad = {**S1, "status": "not_in_scope"}
    assert any("not_in_scope but" in e for e in step1_errors(RULE, bad))


def test_dropped_requirement_is_refused():
    # the pilot error: the "no secrets staged" part translated nowhere and not left out
    trace = {"clause_req": ["q1"], "left_out": []}
    errs = coverage_errors(S1, trace)
    assert len(errs) == 1 and errs[0].startswith("q2")


def test_left_out_with_a_reason_is_accepted():
    trace = {"clause_req": ["q1"], "left_out": [{"req": "q2", "reason": "outside_vocabulary", "word": ""}]}
    assert coverage_errors(S1, trace) == []


def test_unknown_ids_and_reasons_are_refused():
    trace = {"clause_req": ["q1", "q9"], "left_out": [{"req": "q2", "reason": "too hard", "word": ""}]}
    errs = coverage_errors(S1, trace)
    assert any("q9" in e for e in errs) and any("reason must be" in e for e in errs)


def test_unclear_word_needs_the_word():
    trace = {"clause_req": ["q1"], "left_out": [{"req": "q2", "reason": "unclear_word", "word": ""}]}
    assert any("needs the word" in e for e in coverage_errors(S1, trace))


def test_uncovered_words_are_reported():
    s1 = {**S1, "requirements": [S1["requirements"][0]]}
    words = uncovered_words(RULE, s1)
    assert ".env" in words and "staged" in words and "before" not in words


def test_empty_quote_is_refused():
    bad = {**S1, "requirements": [{**S1["requirements"][0], "quote": " "}, S1["requirements"][1]]}
    assert any("empty" in e for e in step1_errors(RULE, bad))


def test_translate_requirement_cannot_be_called_vague():
    trace = {"clause_req": ["q1"], "left_out": [{"req": "q2", "reason": "vague", "word": ""}]}
    assert any("marked translate" in e for e in coverage_errors(S1, trace))


def test_vague_requirement_must_be_listed():
    s1 = {**S1, "requirements": S1["requirements"] + [{"id": "q3", "quote": "Before any commit", "keep": "vague", "why": ""}]}
    trace = {"clause_req": ["q1", "q2"], "left_out": []}
    assert any(e.startswith("q3") for e in coverage_errors(s1, trace))


def test_both_translated_and_left_out_is_refused():
    trace = {"clause_req": ["q1", "q2"], "left_out": [{"req": "q2", "reason": "outside_vocabulary", "word": ""}]}
    assert any("both" in e for e in coverage_errors(S1, trace))


def test_applies_when_must_be_an_exact_piece():
    bad = {**S1, "requirements": [{**S1["requirements"][0], "applies_when": "for code"}, S1["requirements"][1]]}
    assert any("applies_when" in e for e in step1_errors(RULE, bad))


def test_scope_is_attached_to_every_clause_of_its_requirement():
    from rules.coverage import apply_scopes
    rule = "Commit docs and other non-code changes on the current branch without checking out a new branch."
    s1 = {"requirements": [
        {"id": "q1", "quote": "Commit docs and other non-code changes on the current branch", "applies_when": "non-code changes"},
        {"id": "q2", "quote": "without checking out a new branch", "applies_when": "non-code changes"}]}
    t = {"status": "ok", "clauses": [{"type": "must_do", "where": {"cmd": ["commit"]}, "when_unmodeled": "for non-code changes"},
                                     {"type": "never", "where": {"cmd": ["branch_create"]}}]}
    trace = {"clause_req": ["q1", "q2"], "scope_encoded": [False, False]}
    out = apply_scopes(t, s1, trace)
    assert out["clauses"][0]["when_unmodeled"] == "for non-code changes"   # already there, unchanged
    assert out["clauses"][1]["when_unmodeled"] == "non-code changes"       # the split part keeps its scope
    assert rule  # the R20 case from the precision probe (experiment log E7)


def test_scope_left_alone_when_step2_encoded_it():
    from rules.coverage import apply_scopes
    s1 = {"requirements": [{"id": "q1", "quote": "x", "applies_when": "after a merge"}]}
    t = {"status": "ok", "clauses": [{"type": "must_do", "where": {"cmd": ["branch_delete"], "after": ["merge"]}}]}
    out = apply_scopes(t, s1, {"clause_req": ["q1"], "scope_encoded": [True]})
    assert "when_unmodeled" not in out["clauses"][0]
