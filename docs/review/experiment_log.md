# Experiment log (autonomous phase, from 2026-11-22)

Plan: `docs/review/autonomy_plan.md`. Each entry: what, why, Codex outcome, numbers, cost, decision.

## E0. Baseline A vs B on the frozen 30 (before this phase)
- One-step: rule right 49% (clear 67%, ambiguous 13%), status 79%, 96 calls.
- Two-step: rule right 49% (clear 68%, ambiguous 10%), status 81%, 169 calls.
- Runs agree in all 3: ambiguous 1/10 vs clear 14/20 (one-step).
- Cost ≈ $0.15-0.23. Decision: two-step not kept as default; frozen set now reserved for final.

## C1. Codex consult on the plan (docs/review/autonomy_consult_1_codex.md) — adopted
- Dev set: label independently, then adjudicate disagreements (ambiguous / corrected / excluded);
  split 20 for iteration, 10 for dev validation. Frozen 30 evaluated once at the end.
- Canonicalization: drop the `kind: file` idea (not meaning-preserving in Z3); only rewrites
  proved equivalent by Z3, with property tests. Scoring stays strict.
- Known limit noted: agreement.py gives all `when_unmodeled` clauses of a rule one shared fact,
  the clash check gives each its own; affects the agreement measure only.
- Order: dev set -> non-thinking A/B -> deterministic gaps (partial translation, "nothing left",
  condition identity, named targets) -> voting last, kept only if it raises accuracy.
- Note: the requirement inventory (two-step) was already tried in E0 with no gain.

## E1. Non-thinking mode, 3-rule smoke test
- `LLM_THINKING=off` (DeepSeek `thinking: disabled`) lets the tool call be forced
  (`tool_choice` = the function); thinking mode rejects that.
- Output tokens per call ~230 vs ~1,000 with thinking (about 4x cheaper).
- Strict mode still does not enforce the template (20-24 template deviations per answer).
- Quality looked lower: conditions put in `needs` of a `must_do` (1 of 3 ended bad output).
- Cost < $0.01. Decision: test accuracy on the dev set before choosing.

## D1. Dev set built (data/runs/survey_rules/dev_set/dev_labels.json)
- 30 new survey rules (seed 7; 24 keyword + 6 control; frozen rules excluded).
- Claude and Codex labelled independently: 20 agreed (Z3). 10 adjudicated by principle (follow
  vocabulary v2; keep conditions; status policy): 8 corrected, 2 ambiguous (R80, R85).
- Split (seed 11): 20 iterate, 10 validate.

## C2. Codex consult on unknown conditions (docs/review/autonomy_consult_2_codex.md) — adopted
- New verdict `possible_clash`: compatible pairs re-checked with unknown conditions true; a
  subset-minimal set of conditions is reported ("clashes if A and B hold at once"). Separate
  from `clash`; proves only the conditional statement.
- LLM judge of co-occurrence: allowed later as a separate evidence tier with its own
  evaluation (planted condition pairs, two-reviewer adjudication). Named groups deferred.

## E2. possible_clash implemented (pair.check_conditional)
- Tests: real force-push pair -> possible_clash with both conditions; minimal set excludes an
  unrelated condition; old case L6_cond vs L46 now possible_clash (expected change, recorded).
- Pilot run 1: no possible_clash added (no false alarms); expected-pair recall unchanged 12/20
  (all 6 avoidable misses are translation errors: R14 "nothing left", R8 half translated).

## E3. Two-step on pilot; one-step think / no-think and two-step on dev (iterate 20)
| | status right | rule right | bad output | pilot expected pairs (exact / any conflict / +possible) |
|---|---|---|---|---|
| A one-step, thinking | 73% | 55% | 3 | 12 / 12 / 0 |
| A one-step, no thinking | 65% | 55% | 6 | - |
| B two-step, thinking | 85% | 60% | 0 | 12 / 15 / +3 (0 false alarms) |
- Pilot scorer fixed: expected pairs were counted as "other flags"; recall now reported exact,
  any-conflict, and possible_clash separately.
- Cost: ~$0.12 for the four runs (output 165k tokens, input 930k, mostly cached prompt).
- Decision: two-step becomes the default; non-thinking dropped (worse status, more bad output).
- Dev error analysis (two-step): the model wants to say "after a build" / "after editing X"
  and forces it into wrong fields (`needs.task`, `path` on a run); lists of paths in one
  must_do (OR in our format) where the rule means each file (R80); "how" rules turned into
  must_do (R386 "run test tasks sequentially").

## C3. Codex consult on earlier-step fields and path lists (autonomy_consult_3_codex.md) — adopted
- after_task / after_path (+ after_ok for success) must describe the SAME earlier step as
  `after`; after_branch has the same latent issue and moves to the same form.
- Path lists stay OR; conjunctions are written as separate clauses (format definition), no
  automatic splitting.
- Labels: v2 kept; mechanical conversion rubric written first (docs/review/vocab_v2_1_rubric.md);
  frozen v2.1 is a separate, retrospective artifact.
- Adjudication: R80 not ambiguous (trigger "when making a change"); R133 condition keeps "every
  local branch other than main"; other 8 agreed.

## E4. Vocabulary v2.1 implemented (before any v2.1 run)
- model: per-kind earlier-step details (prior_branch per action, prior_path per file action,
  prior_task / prior_ok for run); `after` + after_* fields match one earlier step.
- pair: earlier-step situations enumerate regions per named kind.
- template / schema / prompt: after_task, after_path, after_ok; prompt defines path lists as
  "any of them" and conjunctions as one clause per file (format definition).
- Tests: 179 pass (6 new: build success, file-specific after, same-step correlation).
- Labels converted by the rubric: dev v2.1 (R224, R194, R114); frozen v2.1 separate file
  (R28, R88 split; R363 adds "only after backing up"), retrospective.

## E5. v2.1 two-step: dev iterate (3 runs) and pilot (1 run)
- Dev (scored vs dev v2.1 labels): rule right 68% (v2.0 two-step 60%), requirements found
  15/30 (v2.0: 5/30), status 80% (85%), bad output 1 (0), vote 65% (60%).
- Pilot run 1: expected pairs 8 exact / 10 any (v2.0 run 1: 12 / 15 + 3 possible). The
  differences are step-2 sampling noise on rules untouched by v2.1 (R3 merge vs local_merge;
  X7 lost "without confirmation"; R8 lost "no secrets"), so one run per version is too noisy.
- Cost ~$0.07. Next: 3 runs per version on the pilot, compare means and majority votes.

## E6. v2.1 two-step, pilot, 3 runs
- Expected pairs per run (any conflict verdict): 10, 8, 18 of 20; exact: 8, 8, 12. Large
  run-to-run variance. Majority vote: 8 (rules whose runs disagree drop out).
- Pair flagged in >=1 run: 18/20 (= every pair in reach; the 2 misses are R7 state vs commit,
  out of reach by design). >=2 runs: 12/20. All 3: 6/20.
- False alarms: 0 in every run (no real-vs-real pair flagged).
- Cost ~$0.07.

## C4. Codex consult on reporting and finishing (autonomy_consult_4_codex.md) — adopted
- Report union over runs with "run support k/3" (not confidence); run disagreement = unstable
  candidate for ambiguity, measured separately. Preregistration: docs/review/final_prereg.md.

## E7. Precision probe (preregistered): QuagKhai003, 30 keyword rules, 3 runs, 435 pairs
- Statuses over 90 translations: ok 36, not_in_scope 50, unclear 4, bad output 0.
- Flagged in any run: 2 pairs (both 2/3 run support): R20 vs R74 and R20 vs R152 (R74 and
  R152 are the same text, from memory and CLAUDE.md), so 1 distinct pair.
- Claude: false alarm. R20 = commit NON-code changes on the current branch; R74 = put CODE on
  its own branch: complementary. Step 2 split R20 into must_do commit + never branch_create
  and attached "non-code" to one clause (run 1) or dropped it (run 3).
- Union precision 0/2; false flagged 2/435 (0.5%); per-run false alarms 2, 0, 2.
- Cost ~$0.06 (122 calls, 70k output tokens). Codex judgement and stop/go: consult 5.

## C5. Codex consult 5 (autonomy_consult_5_codex.md) — adopted
- Both flagged probe pairs: false alarm (Codex agrees independently).
- Root cause: step 1 split "without checking out a new branch" into its own requirement,
  losing its scope ("non-code changes"); same-req propagation would not fix it.
- Fix: step 1 records `applies_when` (exact quote of the words limiting each requirement, even
  from another part of the sentence); code attaches it to every clause of that requirement as
  an unknown condition unless step 2 marks `scope_encoded`. Tests: 182 pass.
- Then: check dev + pilot for regressions, refresh the preregistration fingerprint, run the
  frozen evaluation once.

## E8. Scope fix (applies_when): dev iterate + pilot, 3 runs each
- Dev (v2.1 labels): rule right 73% (was 68%), requirements found 21/30 (was 15), status 82%,
  bad output 1, vote 70%.
- Pilot: per run any-conflict 12, 8, 6 (was 10, 8, 18); union 14/20 (was 18/20); false alarms 0.
- Cause of the pilot drop: not the attached scopes (no lost pair got an extra condition). Step 1
  now marks R13 "Always confirm files with the user before push/merge" outside_vocabulary in
  3/3 runs ("a communication step"): our step-1 definition lists "what to tell the user" as
  outside, though approval before a git action is in the vocabulary (user_confirmed). Also
  R14 lost its branch part, X8 one bad output.
- Cost ~$0.13.

## C6. Codex consult 6 (autonomy_consult_6_codex.md) — adopted
- Step-1 categories corrected (general): `translate` includes requirements that limit or must
  precede a git/file/task action; "what to tell the user" removed from `outside_vocabulary`;
  a prerequisite in `applies_when` does not make a requirement outside.
- Precommitment: one pilot re-check (~$0.07); it will not prompt further development except
  an unmistakable execution/formatting failure. Then refresh the preregistration fingerprint
  and run the frozen evaluation once. Method fingerprint after this change: 601c34c4f45a259c.

## E9. Pilot re-check after the step-1 correction (one run of 3, precommitted)
- Per run any-conflict 9, 12, 7 (+ possible 0, 2, 2); union 15/20; >=2 runs 10; all 3: 3.
- False alarms 0. Misses: R14 (often skipped) and R7 (out of reach by design).
- Cost ~$0.10 (174 calls, 133k output). No further development (precommitment).

## F. Final evaluation, once (preregistered): frozen 30, v2.1 two-step, 3 runs
- Cost ~$0.10 (169 calls, 117k output tokens).
- vs original v2 labels: status right 80%, rule right 51% (clear 67%, ambiguous 20%),
  requirements found 23/63, extra clauses 37, bad output 2/90, vote 50%, unstable 2.
- vs v2.1 conversion (retrospective): rule right 51%, requirements found 23/72.
- Baseline on the same 30 (E0): one-step 49% (status 79%, req 18/63), two-step v2 49% (81%, 19/63).
- Unstable-candidate flag (runs differ in meaning): 12 flags, 4/10 ambiguous caught
  (recall 0.40, precision 0.33). E0 one-step: ambiguous rules agreed in all 3 runs 1/10.
- Known real clashes, per run: R24 vs R156 compatible x3 (missed; labels say exception);
  R28 vs R81 compatible x3 (expected: both can be done); R60 vs R213 skipped x3 (R60 not in
  scope); R118 vs R131 possible_clash, clash, possible_clash -> found by the union.
- Reading: dev gains (rule right 55% -> 73%) mostly did not transfer to the frozen set
  (49% -> 51%); the frozen rules contain more judgement calls (10/30 ambiguous).

## N. Natural-folder comparison: LLM alone vs Z3 (after the method audit; hybrid_lit_codex.md)
Budget asked: < $0.10. Code: `pipeline/rules/natural_test.py`; data: `data/runs/natural/`.
- N1 (free). 951 same-folder pairs among the 84 rules with saved 3-run translations. Z3 flags
  2: R118/R131 (real) and R20/R74 (false alarm). Adjudicated clashes: 3 clear (R24/R156,
  R60/R213, R118/R131), 2 ambiguous. Z3 found 1/3, 1 false alarm. Misses are translation
  losses: the "may" of R156 dropped; "map and player data" left out (needs the other rule).
- N2. Whole-folder LLM, one call per folder (prompts/rules/folder_judge.md): Codex (free,
  blind) 3/3, 0 false; DeepSeek (same model as the translator, 5 calls, ~$0.025) 3/3, 0
  false, + R28/R81 (ambiguous). Codex consult (natural_consult_1_codex.md): scale test next.
- N3. Full folders (1287 rules, 119-394 per folder, ~196k pairs). Codex all 5 folders (free):
  35 flags. DeepSeek on QuagKhai + ruflo (2 calls, 94k output, ~$0.06 off-peak) 11 flags; 3
  further attempts returned empty JSON (output cut off) and were retried: billed, not counted.
  Total spend in N about $0.14 (estimate; balance after: $1.15): OVER the $0.10 limit. Fix:
  llm.py no longer retries a reply cut off at the output limit and counts failed tokens.
- N4 (free). Union 43 pairs (+ known R60/R213), labelled by a fresh blind Codex and by Claude
  (not blind). Agreement 27/43. Final (both agree, else ambiguous): 22 clash, 19 ambiguous,
  2 compatible. Only 5/22 clear clashes are inside the git/file/task vocabulary; the rest turn
  on which tool or command style to use, numeric values, or file layout.
- N5. Codex full-folder single pass missed the known R60/R213 that it found in the 84-rule
  subset. On QuagKhai + ruflo: Codex 5/6 clear, 0 false; DeepSeek 4/6, 1 false; the two LLMs
  shared 4 of 15 flags.
- N6 (free). Word-overlap candidate filter (pipeline/rules/lexical.py): >=1 shared word keeps
  13.5% of pairs, 19/22 clear clashes; >=2 keeps 2.5%, 13/22.
- N7 (free). Missed-clash probe: random 200 of 4,860 unflagged pairs with >=2 shared words,
  blind fresh Codex: 3 clash (S2 pwsh vs powershell, S41 URL form, S169 Fabric companion vs
  skip client loader), 197 compatible. Summary: docs/review/natural_findings.md.

## G. Three-rule clashes (prereg: docs/review/group_bench_prereg.md)
- Code: `pipeline/rules/group.py` (set-level check; earlier steps obey never / simple only_if;
  only must/may trigger), `pipeline/rules/group_bench.py`; tests `tests/rules/test_group.py`.
- Material: 16 Codex-written groups (8 clash, 8 control); fresh Codex check disputed G6 (a
  pair already clashes) and G8 (reading-dependent): excluded -> 8 clash, 6 control. Folder:
  36 real QuagKhai rules + 48 test rules, shuffled (84 rules).
- Cost: translation 48 rules x two steps, one run (99 calls, 65k output, 1 min off-peak,
  balance $1.15 -> $1.11) + one DeepSeek whole-folder call (47k output, ~$0.03). Phase B
  total ~$0.07 (estimate was $0.05).
- Translation: 34 ok, 7 not in scope, 3 unclear, 4 bad output. Only G5, G7, G9 of the clash
  groups translated fully; tags (G2, G15) and "documentation files" (G4, G13) are outside the
  vocabulary; G11 became "never merge PRs"; G9's "after the full suite passes" became a world
  fact (so a pair clash).
- Execution bug fixed before scoring (allowed): the scan's relevance filter dropped only_if
  rules. Prereg Z3 result after that fix: 1/8 (G5), 0 control flags, 16 other group flags.
- Post-hoc fix (semantics, reported separately): earlier-step situations taken only from the
  tested rule (one earlier step per kind made other rules' "after a test run" block a needed
  lint run). After it: 1/8 (G5), 0 other flags.
- Whole-folder LLM (strict rule: the group, or the group + 1 rule): DeepSeek 5/8 (G2, G9,
  G11, G13, G15), 0 control flags; Codex 2/8 (G11, G15), 4/8 if twin rules with identical
  text in other groups count (G7, G9). Both also reported cross-group clashes (test rules from
  different groups clash with each other, e.g. "use squash merging" vs "never squash").
- Decision rule: Z3 does not beat the LLM arms on three-rule clashes. Its flags were precise
  (after the post-hoc fix), and the misses are translation and vocabulary losses plus one
  model limit (G7, a three-step cycle).
