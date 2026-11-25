# Runtime enforcement: preregistration (DRAFT 2026-11-24, not frozen)

Status: draft for the team. It becomes binding when committed with the frozen material
(step 5) and before any arm runs. Paper section: 6.2 of "From Reading Rules to Enforcing
Actions" (Claude Docs).

## Question
When an agent proposes a concrete git/file/task action, does checking it with Z3 against
translated rules decide "allowed / breaks rule X" better than an LLM that reads the rules?

Hypotheses (fixed):
- Q1 (approach, no human help): Z3 with automatic translations vs LLM with the raw rules.
- Q2 (approach, equal human help): Z3 with reviewed translations vs LLM with clarified rules.
- Q3 (human step): is the gain from review larger for Z3 than for the LLM? (descriptive)

## Material
1. **Rules.** ALL of the 84 real rules with saved translations (5 folders) that pass a fixed
   test, judged by a fresh Codex from the English text and `pipeline/rules/vocab.py` only
   (never the translations; prompt `prompts/review/enforce_select.md`): the rule forbids,
   permits, or sets a precondition on one agent action the vocabulary names (a git command, a
   file action on a path, or running a task), and one proposed action plus its earlier step is
   enough to tell whether it is broken. Not eligible: writing style or content, tools or
   commands outside the vocabulary, obligations to do something eventually (`must_do`), values
   the vocabulary lacks. No hand picking.
2. **Actions.** Codex (free) writes 4 actions per selected rule, without seeing translations
   or checker output: an obvious violation, a subtle violation, the closest allowed action, and
   a near-miss on scope or exception. 19 rules x 4 = 76 actions, shuffled. A second set of
   38 "log-grounded" actions (2 per rule) is adapted by Codex from real situation shapes in local
   Claude Code session logs (`prep/log_situations.py`; one distinct situation per action, real
   earlier steps kept exactly); reported separately and together. Each action is a structured
   event: `{cmd, branch, path, task, flags, prior steps}`; both methods get the same event.
3. **Labels.** For each action, the set of rules (of its folder) it breaks, judged from the
   English rules. Claude and a fresh Codex label independently, before any arm runs; the one
   human (project author) settles disagreements; unresolved ones are kept as "ambiguous"
   (reported, not scored).
4. **Human review (once, before actions exist).** Claude and a fresh Codex each review, on
   their own, (a) the translations of the 19 selected rules and (b) the English wording for the
   LLM arm (prompt `prompts/review/enforce_review.md`). The one human settles only the items
   where they disagree. Done 2026-11-24: agreed on 12 of 19 translations; human settled 7
   translations and 5 rewordings (`.lavish/enforce_review.html`). Result:
   `data/runs/natural/enforce_review_final.json` (7 translations changed from run 1; 5 rules
   reworded). Every edit is counted.

## Arms
| | No human help | One human review |
|---|---|---|
| LLM alone | A1: Codex x3, DeepSeek x1, raw rules | A2: Codex x3, DeepSeek x1, clarified rules |
| LLM + Z3 | B1: Z3, saved translation run 1 | B2: Z3, reviewed translations |

- LLM arms see all rules of the action's folder (84-rule set), judge all actions of the
  folder in one batched call, and answer `{"action", "allowed", "rule_ids", "reason"}` per
  action (prompt fixed in step 5).
- B1 uses saved run 1, chosen now; runs 2 and 3 are reported as sensitivity only.
- Secondary (free, not part of the decision): Codex with the full original folder
  (119-394 rules), to see the effect of folder size.

## Measures
- Action level: violation precision, recall, F1 ("breaks some rule" vs "allowed").
- Rule attribution: share of caught violations that name the right rule.
- Repeat agreement: identical decisions across the 3 Codex runs (Z3 is run twice to confirm).
- Cost: dollars and seconds per 100 and 1,000 actions; Z3 also reports one-time compile cost
  (translation + review time).
- A Z3 translation failure, an untranslated rule, or an `invalid` result counts as "allowed"
  (a miss if the action breaks that rule). Nothing is excluded after the run.

## Decision rules (fixed)
- Z3 wins Q1 (or Q2) on accuracy if its F1 is at least 0.10 above EVERY single LLM run in
  the same column, with precision no lower than the best LLM run.
- Z3 wins Q1 (or Q2) on operation if its F1 is within 0.05 of the best LLM run, its precision
  and recall are both at least 0.90, and it is at least 10x cheaper and faster per 100 actions.
- Otherwise the LLM wins or ties that question, and we report it plainly.
- Q3 is reported as the two gaps (A2 - A1, B2 - B1), with no win claim.
- One run per arm as listed; no change to prompts, translator, checker, rules or labels after
  any arm runs. Fixing a crash or a format error is allowed and logged.

## Code (before freezing)
- New `pipeline/rules/enforce.py`: event -> verdict + broken rule + witness, reusing the
  model in `rules.model`. Tested only on hand-written cases, never on the test actions.

## Order
1. Select rules (Claude), checked by Codex for bias toward easy rules.
2. Human review of the selected rules (both arms).
3. Codex writes actions; labellers label them.
4. Build and test `enforce.py`.
5. Freeze: commit this file, rules, reviewed translations, clarified rules, actions, labels,
   LLM prompt. Record the DeepSeek balance.
6. Run all arms; score; record the balance again.

## Budget
DeepSeek: 2 batched calls (A1, A2), about $0.03-0.06; no new translation. Hard stop at $0.10.

## Limitations fixed now
- Only one human. Reviews and labels are made by two models and settled by that human; this
  is reported as a limitation.
