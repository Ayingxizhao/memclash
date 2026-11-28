# Rules Z3 can express, round 1: plan (2026-11-24)

Follow-up to `enforce_results.md`, with a narrower set of rules.

## Goal
Build a set of real rules that are compiled and validated in the fixed git/file/task vocabulary,
so that Z3's verdicts on them are exact. This set is the rule set of the live gate
(`hidden_rules_prereg.md`).

## Rules (mechanical, no hand picking)
1. An LLM judges every real rule with the eligibility test (`prompts/review/enforce_select_full.md`).
2. An LLM translates the eligible rules (`prompts/review/boundary_translate.md`).
3. Fixed filter: status ok; only `never` / `only_if`; no `when_unmodeled`; compiles.
4. Two AI reviewers each judge whether each translation is exact for every single action
   (`prompts/review/boundary_review.md`). A rule is kept only if both say exact; exclusions and
   reasons are published.

## Actions and labels (check of the kept rules)
A fresh AI helper with no access to translations or checker output writes 6 actions per kept
rule: exact boundary violation; adjacent allowed case; path/glob or exception pair; near-identical
path or branch; one-step history violation; closest allowed history case. Two AI labellers label
every action independently; agreement = gold, disagreements are excluded as ambiguous.

## Rules for the run
No change to rules, translations, prompts or labels after the check runs; crash or format fixes
are logged.
