## 1. Summary

The project asks whether coding agents' stored Git and GitHub rules contain conflicts worth surfacing to users. Its domain-specific method translates rules individually into a shared model and uses Z3 to look for situations where a rule cannot be honored alongside another (`pipeline/git/git_check.py`). The large tuning run found none of the 11 adjudicated clashes, motivating a proposal to let the LLM state vocabulary relations explicitly rather than hard-code every term (`data/runs/git/large_filter/check_v3_r0.json`, `data/runs/git/large_filter/reference_labels.json`, `docs/review/brief.md`).

## 2. Is the problem worth solving?

Yes, as a lint check: I would want an agent to flag a rule conflict before it chooses the wrong tool or skips a required step. I don't know how common or costly this is; the tuning cases establish that reviewers can find conflicts, not that agents encounter them often or that the conflicts cause harm (`docs/adr/0006-reference-labels.md`). Show a few replayable incidents from unselected repositories: the task triggers both rules, the agent makes a consequential choice, and a clarified rule changes that choice. Report how repositories were sampled and how many warnings users would have to inspect per useful finding.

## 3. Clash definition (ADR 0003)

I accept it for equally authoritative rules about the **same decision**, with explicit permission protected as an option rather than treated as an obligation. I would not equate every literal clash with a policy defect: “Always run tests, except for docs-only PRs” and a separately written permission to skip tests on docs-only PRs are consistent if the exception is already explicit; if the exception is conveyed only by a clearly higher-priority instruction, the raw clash is resolved, not actionable. The single-action rule can also overflag “review and then merge” if both obligations are incorrectly assigned to one slot, and it misses conflicts that arise only across a sequence. Define the decision slot and report unresolved conflicts separately from resolved exceptions (`docs/adr/0003-clash-definition.md`).

## 4. Contribution

Explicit, reusable relations and a checkable explanation could be a real empirical contribution, but solver precision cannot rescue wrong premises. On the same frozen folders and candidate pairs, compare a strong direct LLM judge, that judge given the **same** relation list, and the solver using it. Match the base model and report token cost; compare accuracy, paraphrase stability, and whether a blind reader can verify each explanation from the source rules. Hand-correct translations and relations separately on a small error sample and rerun offline to distinguish failures of translation, relation building, and checking. If the gains come entirely from sharing the glossary, credit the glossary, not Z3.

## 5. Options A / B / C

Pick **C** first, assuming a folder's rules fit in context: one frozen glossary is easier to inspect, replay, and compare across rule orders. Keep A as a narrow control, not evidence of generalization. B is worth trying if C repeatedly misses relations that become apparent only during translation. Reject B if rule order changes verdicts, later additions leave earlier translations stale, or it adds review cost without a clear held-out gain over C (`docs/review/brief.md`).

## 6. Weakest points

1. **Coverage is much lower than the filter count suggests.** In the archived large run, only 86 of 212 translations have `fits: true`, and 1,062 of 5,927 possible within-folder pairs are emitted; `check` omits `unfit` pairs (`data/runs/git/large_filter/translate_v3_r0.json`, `data/runs/git/large_filter/check_v3_r0.json`, `pipeline/git/git_check.py`). **Fix:** keep an explicit abstention count and trace each reference miss through filtering, fit, translation, and checking. Never count an abstention as compatible.
2. **The checker does not implement the full stated definition.** `constraints` includes only `never` and `only_if`, so two `must_do` clauses for mutually exclusive actions in the same slot don't block each other. Also, `situations` samples `after_branch` globs by replacing `*` with `x`: `release-*` and `*-prod` overlap at `release-prod`, which neither sample tests (`pipeline/git/git_check.py`). **Fix:** add both as hand-encoded regressions; implement same-slot obligation checks and use symbolic overlap or narrow the exactness claim explicitly.
3. **The headline tuning target rewards tailoring.** Nine of the 11 definite reference clashes are tool-choice cases, so 8/11 could be reached without handling either other type (`docs/adr/0006-reference-labels.md`, `docs/review/brief.md`). **Fix:** report results by clash type and folder, add unseen vocabulary cases and compatible near misses, and freeze the choice of method before the held-out run (`docs/adr/0007-tuning-vs-final-test.md`).

## 7. Evaluation

The two-reader union plus author adjudication is useful for debugging, not an exhaustive reference: one reader saw checker output and no one adjudicated pairs missed by both (`docs/adr/0006-reference-labels.md`). Blindly judge all new alerts and a prespecified stratified sample of unflagged pairs; keep the two conditional cases separate (`data/runs/git/large_filter/reference_labels.json`). Report precision, recall against known positives, coverage, and counts per folder. For three tuning repeats, compare **which** pairs recur, not just totals. Pilot scores are regression checks, and zero false alerts in a small sample does not establish zero false-alert risk. The missing comparison is a matched Git-only direct judge on the same held-out pairs under ADR 0003, not just the existing all-pairs dev baseline (`README.md`). Also, ADR 0005's roughly 2.5% bound is on the fraction of **rejected rules** that are Git rules, not the fraction of **all true Git rules** that the filter misses (`docs/adr/0005-git-filter.md`).

## 8. Anything else

Make the warning useful even when the tool cannot decide: show the two source lines, the triggering situation, and the relation a user can confirm or correct. Don't recommend deleting or rewriting either rule without knowing which one the user wants to win.
