# Stopping rule breaks, all action rules: results

Plan: `docs/review/enforce_prereg.md`. Scores: `data/runs/natural/enforce_judge/`; scripts
`pipeline/rules/enforce_run.py`, `pipeline/rules/enforce_score.py`.

## Question
When an agent proposes an action, does it break one of the memory rules? Z3 checks the action
against the translated rules; the baseline is an LLM that reads the same rules in English and
judges the action directly, with no translation.

## Material
- Real rules about concrete git, file and task actions from public memory folders, as selected by
  the eligibility test (`prompts/review/enforce_select.md`); the LLM arms see the rule folders.
- 334 actions, each either breaking a rule or allowed, written as structured events
  (`enforce.py`). Labels: two AI labellers independently, disagreements settled by the author.

## Result (F1 for catching rule breaks, 334 actions)
| | F1 |
|---|---|
| Z3 | 0.78 |
| DeepSeek | 0.87 |
| Claude Haiku 5.5 | 0.85 |

**The LLM wins on all action rules.**

## Why Z3 loses
- Every Z3 miss comes from a rule it cannot express, or a condition it cannot check that is
  switched off (ADR 0004). Z3 never mis-checked a rule it could express.
- Z3 rarely blocks wrongly (precision about 0.95), so its losses are misses: breaks of rules
  that were translated only in part, or not at all.
- A partial translation keeps a rule's core action, which most breaking actions hit; breaks that
  hinge on a dropped condition slip through. This is why Z3 still scores well above zero.

## Speed and cost per 100 actions
| | Time | Money |
|---|---|---|
| Z3 | 0.5 s | $0, same answer every run |
| Claude Haiku 5.5 | 16 s | subscription, not billed |
| DeepSeek | 150 s | about $0.01 |
Z3's one-time cost is translating the rules (see `natural_findings.md`, speed and cost).

## Limits
Actions are written to be clear cases; real traffic is messier. Labels are two AI labellers and
the author. Talk-level evidence, no significance claims.
