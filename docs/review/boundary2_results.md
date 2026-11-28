# Stopping rule breaks, rules Z3 can express: results

Plan: `docs/review/boundary2_prereg.md`; deviations in `data/runs/boundary2/changes.log`.
Code: `pipeline/rules/boundary2.py`. Data and scores: `data/runs/boundary2/` (`judge_s1/`).

## Question
On rules Z3 can express exactly, does the Z3 gate catch rule breaks as well as an LLM that reads
the rules in English?

## Material
- 50 new public repos (`repos_used.txt`). Rules extracted by Claude Haiku 5.5, then the same steps
  as round 1 (`boundary_results.md`): eligibility test, translation into the fixed schema,
  mechanical filter, and two AI reviewers who must both judge the translation exact.
- Scored set: 13 rules in 6 folders, 8 actions per rule (104), written blind to the translations
  and covering allowed cases, path and branch look-alikes, earlier-step cases and multi-step cases.
- Labels: two AI labellers agreed on all 104.
- 3 actions (S1-009, S1-049, S1-103) stage a parent folder without saying what it contains, so no
  checker or reader can decide them; they are dropped for every arm, leaving 101.

## Result (F1 for catching rule breaks, 101 actions)
| | F1 |
|---|---|
| Z3 | 0.97 |
| DeepSeek | 0.90 |
| Claude Haiku 5.5 | 0.89 |

**On rules it can express, Z3 beats both LLMs.** No arm blocked an allowed action.

## What Z3 missed (3)
All three are one rule, R9 ("Merge changes into main only when the user explicitly says to").
The translation required `user_asked` (the user asked for the task) instead of `user_confirmed`
(the user approved this step). In all three actions the user asked for the feature but did not
approve the merge, so Z3 allowed them. Both reviewers passed this translation. The solver decided
every translation correctly; the miss is in the translation.

## What Haiku missed (9)
All nine are the "never stage `src/...`" rules: Haiku allowed every staging of those folders,
including plain cases. A weaker LLM can fail a whole rule family at once.

## Speed
Z3: 0.3 s for 104 actions, same answer every run. Haiku: 16.5 s.

## Limits
13 rules in 6 folders, so intervals are wide. The actions and half of the labels were written by
Claude while a Claude model (Haiku) was judged.
