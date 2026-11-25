You review rule translations for a research experiment. Work read-only; your final message
is saved. Open ONLY: `data/runs/natural/enforce_rules.json` (19 real rules with one saved
machine translation each, field `run1`), `pipeline/rules/vocab.py`, `pipeline/rules/model.py`,
`pipeline/rules/patterns.py`, `docs/adr/0003-clash-definition.md`,
`docs/adr/0004-unexpressible-conditions.md`, `docs/adr/0008-git-and-file-vocabulary.md`.
Do not open any other file under `data/`. No paid API calls.

Use: the translations will be used to check single agent actions ("does this proposed git /
file / task action break the rule?"). For EACH rule:

1. `translation_ok`: true if `run1` would decide every single proposed action the same way the
   English rule does (allowed vs broken), within what the vocabulary can say. Ignore wording;
   judge meaning. `when_unmodeled` notes a condition the vocabulary cannot check.
2. If not ok: `fixed` = the corrected translation, same JSON format as `run1` (`status`,
   `clauses`, `left_out`), using only names from vocab.py. If the rule cannot be expressed so
   that single actions are judged correctly, use status "not_in_scope" or "unclear".
3. `clarified_rule`: the English rule rewritten only to remove ambiguity for a reader who
   must judge single actions, keeping its meaning; or "" if it is already clear. Do not add
   facts the rule does not state.
4. `note`: <= 20 words on your reasoning.

Output only a JSON object in a ```json block:
{"rules": [{"folder": "...", "id": "R..", "translation_ok": true|false, "fixed": {...}|null,
"clarified_rule": "...", "note": "..."}]} covering all 19 rules.
