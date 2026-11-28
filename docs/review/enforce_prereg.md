# Stopping rule breaks, all action rules: plan (2026-11-24)

## Question
When an agent proposes a concrete git, file or task action, does checking it with Z3 against
translated rules decide "allowed / breaks rule X" better than an LLM that reads the rules in
English?

## Material
1. **Rules.** Every real rule with a saved translation that passes a fixed eligibility test,
   judged from the English text and `pipeline/rules/vocab.py` only (prompt
   `prompts/review/enforce_select.md`): the rule forbids, permits, or sets a precondition on one
   agent action the vocabulary names (a git command, a file action on a path, or running a
   task), and one proposed action plus its earlier step is enough to tell whether it is broken.
   Not eligible: writing style or content, tools or commands outside the vocabulary, obligations
   to do something eventually, values the vocabulary lacks. No hand picking.
2. **Actions.** An AI helper writes actions per selected rule without seeing translations or
   checker output: an obvious violation, a subtle violation, the closest allowed action, and a
   near-miss on scope or exception. A second set is adapted from real situation shapes in local
   Claude Code session logs (`prep/log_situations.py`). Each action is a structured event
   `{cmd, branch, path, task, flags, prior steps}`; both methods get the same event.
3. **Labels.** For each action, the set of rules of its folder that it breaks, judged from the
   English rules. Two AI labellers label independently before any arm runs; the author settles
   disagreements; unresolved ones are kept as "ambiguous" (reported, not scored).
4. **Review (once, before actions exist).** Two AI reviewers each check the translations of the
   selected rules (prompt `prompts/review/enforce_review.md`); the author settles disagreements.
   Result: `data/runs/natural/enforce_review_final.json`.

## Arms
- **Z3**: reviewed translations, checked by `pipeline/rules/enforce.py`.
- **LLM**: DeepSeek and Claude Haiku 5.5, each reading all rules of the action's folder in
  English and judging the folder's actions in one batched call (prompt
  `prompts/review/enforce_judge.md`), answering `{"action", "allowed", "rule_ids", "reason"}`.

## Measures
- Violation precision, recall and F1 ("breaks some rule" vs "allowed").
- Time and cost per 100 actions.
- A Z3 translation failure, an untranslated rule, or an `invalid` result counts as "allowed"
  (a miss if the action breaks that rule). Nothing is excluded after the run.

## Rules for the run
One run per arm. No change to prompts, translations, checker, rules or labels after any arm runs;
fixing a crash or a format error is allowed and logged.

## Limits known in advance
Reviews and labels come from two AI models, settled by one person.
