You are an external reviewer for a class project. Work read-only (do not edit or create files;
your final message is saved). Do not open `data/gold/`, any file named `labels_*`, or any file in
`data/runs/survey_rules/label_set/` (the frozen test labels must stay unseen). Do not call any
paid API.

A two-step translator was just built, before its first paid run on 30 test rules. Plan:
`.lavish/two_step_plan.html` (sections 3-4). Code and instructions to review:
- `prompts/rules/requirements.md` (step 1: split a rule into requirements with exact quotes)
- `prompts/rules/translate.md` + `prompts/rules/translate_step2.md` (step 2: translate each)
- `pipeline/rules/template.py` (`requirements_tool`, `tool_step2`, `to_translation_step2`)
- `pipeline/rules/coverage.py` (code check: nothing dropped silently)
- `pipeline/rules/translate.py` (`translate_rule_two_step`), `pipeline/rules/agreement.py` (`vote`)
- `pipeline/rules/label_score.py` (how runs are scored against labels)
Context: `docs/review/vocab_draft.md`, `docs/adr/0008-git-and-file-vocabulary.md`,
`docs/review/tool_level_research_codex.md` (your own earlier research).

The author does not want fixes by adding instructions for specific errors seen; general,
tool-level choices are preferred.

Reply in Markdown, under about 700 words:
1. Do the instructions and formats do what the plan says? Any contradiction between
   `translate.md` and `translate_step2.md` (e.g. statuses, `left_out`, splitting), or between the
   prompts and the code checks?
2. Bugs or loopholes in the coverage check, the step-2 conversion, the vote, or the scoring
   (e.g. a way to pass the check while dropping a requirement; a scoring rule that is unfair to
   one-step vs two-step).
3. Anything that would make the A (one-step) vs B (two-step) comparison unfair or misleading.
4. Numbered, concrete changes, most important first. Mark each MUST (fix before running) or
   COULD. If none, write `AGREE`.
