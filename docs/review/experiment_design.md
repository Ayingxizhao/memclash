# Experiment design: git and file rule checker (v2, after Codex review)

Date: 2026-11-22. Method: vocabulary v2 (ADR 0008), prompt `prompts/rules/translate.md`,
checker `pipeline/rules/`. Model: `deepseek-v4-flash`, served by DeepSeek as
DeepSeek-V4.1-Flash-1017 (older saved runs used an earlier model; not directly comparable).
Default sampling; each rule translated alone (rule + file name). Codex review:
`docs/review/experiment_review_codex.md`.

## Questions

1. Stability: do repeated runs of a rule give the same status, and (when all are `ok`) the
   same meaning (Z3, `agreement.py`)?
2. Correctness: does each translation say what the English says (hand check)?
3. Planted clashes: are the planted clashes found, and are paraphrases left alone? For other
   flagged pairs: real clash or false alarm? (Unflagged real pairs are not reviewed, so this
   does not measure how many real clashes are missed.)
4. Coverage: how many rules are skipped (not in scope, unclear with the word, bad output)?
5. Verdict stability: the verdict of each pair across runs.

## Run A: pilot

Data: `data/inject/dev_pilot_rules.json`: one real folder (setflow) in three copies, each with
planted rules (`data/inject/dev_pilot.json`). 64 rule entries, **32 unique rules** (the real
rules repeat across copies; the cache translates each unique rule once per run). All counts
are reported per unique rule. Cost: ~100 calls, under $0.10 (under $1 if answers are long).

Planted rules are used **as written**: they test whether the translator reads natural wording
("keep the branch" means "never delete it"). They are not reworded to fit the vocabulary.

Expected outcome, fixed before running:

| Host | Planted | Expected |
|---|---|---|
| R1 delete branch after merge to main | X1, X2 keep/retain branch | clash (in scope) |
| | X3 paraphrase ("remove") | compatible and same meaning; `unclear` ("remove") counts as a miss, cause reported |
| R3 confirm files before push/merge/PR | X7, X8 merge small PRs without confirmation | clash (in scope) |
| | X9 paraphrase | compatible and same meaning |
| R6 never commit credentials | X13, X14 may commit/store secrets | exception (in scope) |
| | X15 paraphrase ("add") | compatible and same meaning; `unclear` ("add") counts as a miss |
| R9 load credentials from env | X16-X18 (hardcode / paraphrase) | out of scope (code contents); if translated, reported separately |
| R11 run pipeline on 6 seed DJs | X10-X12 (12 DJs / paraphrase) | the count is unmodeled: expected not found (vocabulary limit) |
| R12 don't use system Python | X4-X6 | out of scope (tool choice) |

Scoring, fixed before running:
- A planted clash counts as found only if both rules are `ok` and the verdict is the expected
  one. Any other result (unclear, not_in_scope, invalid_output, invalid, another verdict)
  counts as not found, with the cause.
- A paraphrase counts as correct only if both are `ok`, they mean the same, and the pair is
  `compatible`.

Procedure and stop rule:
1. Translate **run 1 only**. Compute everything below for run 1.
2. Stop and fix (no runs 2-3) if 4 or more of the 32 unique rules end as `invalid_output`, or
   fewer than 4 of the 6 in-scope planted clashes are found.
3. Otherwise translate runs 2 and 3 (run 1 is reused from the cache) and compute stability.

Measures:
- Bad output: rules ending `invalid_output`; rules that needed the retry.
- Planted: found per run (of 6); paraphrases correct per run (of 3).
- Correctness: hand-check **all 32 run-1 translations**, each for action, conditions, force
  (never / only if / must / may) and anything dropped. Claude does a first pass; the author
  confirms.
- Other flagged pairs: each read by hand, labelled real clash / false alarm with the cause
  (translation, vocabulary limit, checker), reported as "x of y unique flagged pairs".
- Stability (runs 1-3): status the same in all runs (all rules); meaning the same (only rules
  `ok` in all runs); for every pair flagged in any run, its three verdicts, and the count with
  the exact same verdict in all runs.
- Skipped: counts of not_in_scope / unclear (with the word) / invalid_output.

Limits: the pilot was used to tune the old git prompt, so it is tuning data (ADR 0007). One
folder, small counts, reported as counts ("5 of 6"), not rates.

## Later runs (decided after A)

- B: 5 dev folders (125 rules): stability and a hand-checked sample.
- C: 4 large folders (212 git rules) against the 11 reference clashes (ADR 0006); most are
  about tool choice (out of scope), so few are expected.
- D: 60 survey folders, for file rules; needs rule extraction first and its own estimate.
- Held-out: git only, once, after the method is frozen.
