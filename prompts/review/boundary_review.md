You review rule translations for a research experiment. Work read-only; your final message is
saved. Open ONLY `data/runs/natural/boundary_review_input.json` (47 rules, each with a
translation), `pipeline/rules/vocab.py`, `pipeline/rules/model.py`, `pipeline/rules/patterns.py`,
`docs/adr/0008-git-and-file-vocabulary.md`. No other files under `data/`. No paid API calls.

The translations will decide single proposed agent actions. Note how fields work: a bare file
name (no "/") matches at any depth; `after` names one earlier step of that kind (the newest);
`user_asked` = the user asked for this kind of work, `user_confirmed` = the user approved this
exact action.

For EACH rule answer `exact`: true only if, for EVERY possible single action describable in the
vocabulary, the translation says "allowed / broken" exactly as the English rule does. Any
dropped condition, extra condition, wrong field, or lost scope makes it false. Give a note.

Output only a JSON object in a ```json block:
{"rules": [{"folder": "...", "id": "R..", "exact": true|false, "note": "<= 20 words"}]} for all 47.
