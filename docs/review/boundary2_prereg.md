# Rules Z3 can express, round 2: plan (2026-11-25)

Follow-up to `boundary_prereg.md`: more real rules, from new repos, with the same method.

## Question
For rules already compiled and validated in the fixed git/file/task vocabulary, does Z3 decide
rule breaks more accurately than an LLM reading the same rules in English?

## New repos (mechanical)
- Source: the existing GitHub search hits (`data/github/search_hits.jsonl`).
- Fetch with `prep/github_scrape.py fetch --out-dir data/github/boundary2 --seed 2520`, same
  quality filter as before (3-40 rule files, not a fork, >= 80% English, one folder per owner).
  Order = the scraper's seeded shuffle of the hit list. Listing or fetch failures are logged and
  skipped.
- Repos and owners already used in earlier studies are excluded up front
  (`data/runs/boundary2/excluded.txt`).

## Rules (no hand picking)
1. Extraction: Claude Haiku 5.5 (headless Claude Code) with the extraction prompt
   (`prep/extract.py`), one call per memory file; quotes must be verbatim.
2. An LLM judges every rule with `prompts/review/enforce_select_full.md` (eligibility).
3. An LLM translates the eligible ones (`prompts/review/boundary_translate.md`).
4. Fixed filter: status ok; only `never` / `only_if`; no `when_unmodeled`; compiles.
5. Two AI reviewers each judge exactness (`prompts/review/boundary_review.md`); a rule is kept
   only if both say exact.

## Actions and labels
A fresh Claude helper writes 8 actions per kept rule from the English rule, the vocabulary field
list and the name list, blind to translations: the six round-1 categories, plus (7) a violation
reached only through a multi-step history and (8) an allowed action that differs from a
violation only in a detail a skim would miss. Two AI labellers label every action; agreement =
gold; disagreements are excluded as ambiguous.

## Arms (same rules, same events)
- **Z3**: validated translations, `pipeline/rules/enforce.py`.
- **LLM**: DeepSeek and Claude Haiku 5.5, one batched call per folder,
  `prompts/review/enforce_judge.md`.

## Measures
Violation precision, recall and F1; results by action category; time.

## Rules for the run
No change to rules, translations, prompts, checker or labels after any arm runs. Changes are logged
in `data/runs/boundary2/changes.log`.

## Known limits
Claude writes the actions and half of the labels while a Claude model (Haiku) is judged.
