# Rules Z3 can express, round 1: the gate's rule set

Plan: `docs/review/boundary_prereg.md`. Data: `data/runs/natural/boundary_*`. Scripts:
`pipeline/rules/boundary_run.py`, `pipeline/rules/boundary_score.py`.

## Role
This round built the set of rules the live gate holds in the hidden-rules trial
(`hidden_rules_results.md`): `data/runs/natural/boundary_rules.json`, 25 real rules from public
memory folders.

## How the 25 rules were chosen
1. An eligibility test kept rules about one concrete git, file or task action
   (`prompts/review/enforce_select_full.md`).
2. An LLM translated each eligible rule into the fixed schema (`prompts/review/boundary_translate.md`).
3. A mechanical filter kept translations that compile, use only `never` / `only_if` clauses, and
   have no condition the schema cannot check.
4. Two AI reviewers each judged whether the translation means exactly what the English rule says
   (`prompts/review/boundary_review.md`); a rule was kept only if both said yes.

## Checker fix found in this round
Some translations wrote a path as a single string (`"path": ".env"`) instead of a list, and the
checker read the string letter by letter; event paths like `./.env` were also not normalised.
Fix: `model._paths` (string -> list) and `enforce._clean` (drop `./`), with the test
`test_string_path_and_dot_slash`. The gate uses the fixed checker.
