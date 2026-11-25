# Review: finding conflicting rules in coding-agent memory

Reviewer: Claude (outside review, 2026-11-21). I did not read `data/gold/labels_*` and made no
LLM calls. I ran `uv run python pipeline/git/git_check.py selftest` (18/18 ok).

## 1. Summary

The project collects real agent memory folders, splits them into rules, and tries to find rule
pairs that cannot both be followed. Its exact track has an LLM translate each git rule alone
into clauses over a fixed git model, and Z3 then checks every pair (`pipeline/git/git_check.py`).
On the large tuning folders it finds 0 of 11 reference clashes, because the clashes are about
tool choice and named conditions the model cannot express. The proposed fix is to let the LLM
add words and word relations that Z3 then reasons over.

## 2. Is the problem worth solving?

Probably yes, but nothing in the repo shows it yet. Contradictory standing instructions are a
believable failure. Still, the only evidence of how often they happen is 11 clashes in 212 git
rules, and 9 of the 11 come from one folder (`Roudranil/variance`), mostly from one rule, R230
(`.lavish/clash_review.html`, P01–P05). That shows one user's tool-routing notes clash, not that
the problem is common. What would convince me: (a) a count over all collected folders of how many
have at least one clash, and (b) a few cases where an agent actually followed the wrong rule,
for example the same task run with and without the clashing pair in memory.

## 3. Clash definition (ADR 0003)

As formal logic it is sound, but as a measure of what users care about it gives wrong answers.
"Strong permission" plus "an exception is a clash" counts clearly stated exceptions as clashes:
- P08/P09: R245 "Permit creating a PR with gh-cc-var ... **as a CLI alternative to MCP**". The
  rule says outright that it is an alternative, yet it is labelled a clash.
- P11: R58 "Permit skipping dev-bot testing for test-only PRs" against R142 is a textbook
  exception (the specific rule wins over the general one), labelled a clash.
- P16: R48 explicitly says sweeps waive the review gate. **Both readers said no clash**, and the
  author still labelled it a clash.

So 4 of the 11 reference clashes are ones neither LLM reader called a clash; they exist only
because of the definition. I would split the label into "unresolved clash" and "clash the rules
resolve themselves (exception or stated alternative)". Only the first is a bug in the memory.
The "one tool per action" assumption is also a modelling choice that the reference depends on.

## 4. Contribution

"The LLM states word relations explicitly, Z3 reasons over them exactly" can be a real
contribution, but only if exactness buys something measurable. A strong LLM already does well:
Codex, reading the rules by hand, called P01–P05 clashes with confidence (`clash_review.html`).
The argument for Z3 has to rest on (a) clashes that need chained reasoning (A kind_of B, B
excludes C) or more than two rules, where pairwise LLM judging fails, (b) the same answer across
runs, and (c) auditability: a wrong answer traces back to one relation a person can fix. The
experiment: on the same 212 rules, run a strong LLM judge on all candidate pairs (3 runs) against
option B (3 runs). Report recall and precision, how often each method gives the same answer
across runs, and how many errors are fixed by correcting one relation. If the judge matches B on
recall and stability, the contribution reduces to auditability alone.

## 5. Options A / B / C

I would pick B, but with C's batch pass as a first step that B then corrects; that is cheap and
cuts down on inconsistent names. Reasons I would reject B:
- The 8/11 target is easy to game. Asserting `kind_of(lookup, read)`, `kind_of(search, read)`,
  and so on, plus `excludes(MCP, gh-cc-var)`, against R230 alone gives P01–P05 plus P07–P09.
  That is one folder and one schema.
- The LLM can invent relations that cause clashes. Every relation the LLM adds must be reported,
  and the invented-clash count must cover clashes that come only from LLM-made relations.
- Word lists are built per folder, so a relation may differ between runs; the stability
  measure has to cover the word list, not only the final verdicts.

## 6. Weakest points (most serious first)

1. **The reference is tiny, depends on the definition, and was built by people who tuned the
   method.** It has 11 positives, 9 from one folder, and at least 4 that are only clashes by
   definition. Pairs neither reader flagged were never reviewed (ADR 0006), so recall is not
   known. *Fix:* report results separately for "unresolved" and "self-resolved" clashes, add a
   random sample of about 100 unflagged pairs labelled by the author to estimate missed clashes,
   and report each folder separately.
2. **The held-out test may be too small to mean anything.** ADR 0007 says the 10 held-out
   folders have only 52 git-looking rules. I do not know how many labelled clashes those hold,
   but it may be a handful, and maybe none are about tool choice. *Fix:* before running, count
   the positives by checking only the label count (have a third party do it if needed), not
   the content. If there are fewer than about 10, say up front that the test only checks for
   invented clashes and report confidence intervals.
3. **The 0-clash result happens by design, not by measurement.** In `translate_v3_r0.json` only
   86 of 212 rules fit, and 76 clauses carry `when_unmodeled`, so most fitting clauses get a
   private unknown fact and can hardly ever clash (ADR 0004, `prepared()` in `git_check.py`).
   The drop from 20 false clashes to 0 bought precision by turning most clauses off. *Fix:* for
   each run, report how many rules fit, how many clauses are left inert, and how many pairs
   could possibly clash. Add the shared-condition fix that ADR 0004 already proposes; it is
   the same idea as option B's word list.

## 7. Evaluation

The reference is acceptable for tuning, but not as the main result (see 6.1). Note that the
"two readers" are both LLMs, so the reference is itself LLM judgment filtered by the author.
That should be stated, and it blurs the comparison with an "LLM judge". Measures: add precision
and recall with intervals for each folder, agreement between readers before the author decided
(the labels exist in `claude_clashes_v2.json` and `codex_clashes.json`), and error attribution
(translation vs model vs relation), because the research question asks about it. **Missing
baseline:** an LLM judge on the same large-folder git pairs. `results.jsonl` holds only dev runs
(gate_v1 and the judge, F1 0.32 on 10 labelled conflicts). The "keep every rule" baseline in the
research question is not defined as a number anywhere I could find.

## 8. Anything else

- The check is pairwise only (`check_pair` in `git_check.py`). Clashes that need three rules
  are missed, and a third rule that resolves a pair (R48, R246) is ignored. That ties directly
  into the exception problem in section 3.
- The review page's plain-word summaries sometimes lean toward a clash: R230 ("remote/project
  reads, branch lists, and operations for which MCP returns 403") is summarised as "when reading
  anything from GitHub, use tool G". The author labelled from those summaries.
- ADR 0006 says paying for more LLM calls was ruled out, while B needs LLM calls on every folder
  and 3 runs. Check the budget.
- Each model has one event with one "after" step, so rules about order in time ("after each
  clone batch") cannot be expressed. State this limit.
- The README's research question ("fewer conflicting rule pairs than keeping every rule") does
  not match what is measured (finding clashes). Rewrite it so it matches.
