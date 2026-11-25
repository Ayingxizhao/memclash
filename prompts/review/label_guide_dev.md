You are labelling rules for a frozen test set. Work read-only (do not edit or create files;
your final message is saved). Do not open `data/gold/` or any file named `labels_*`, and do not
open anything in `data/runs/survey_rules/label_set/` or any other file in `data/runs/survey_rules/dev_set/`. Do not call
any paid API. Label independently: you will not see the other labeller's work.

## What to label

`data/runs/survey_rules/dev_set/selection.json` lists 30 rules (folder, id, file, rule). For
each, decide from **the rule text and its file name only** (this is all the translator gets),
using the fixed vocabulary in `docs/review/vocab_draft.md` (v2) and the format in
`prompts/rules/translate.schema.json`. `prompts/rules/translate.md` and `pipeline/rules/vocab.py`
list the exact names.

For each rule give:
1. `status`: `ok` (git, files or running a task, at least partly expressible),
   `not_in_scope` (code style, tool choice, how code is written, teaching style, ...), or
   `unclear` (a word the rule depends on has several meanings and the text does not settle it).
2. `requirements`: the rule split into single requirements, each with an exact `quote` (a piece
   of the rule text) and `keep`: `translate`, `vague` (no concrete action), or
   `outside_vocabulary` (concrete, but the vocabulary has no words for it). Every part of the
   rule that asks for something must be in some requirement.
3. `clauses` (only if status is `ok`): the correct translation, in the translation format,
   with `"req": "<requirement id>"` on each clause. Write only fields the rule states. A
   condition no field can express goes in `when_unmodeled`.
4. `note`: one line on anything debatable (another reading you considered and why you did not
   pick it).

Be literal: label what the rule says, not what the project probably meant. If two readings
are both reasonable, pick one, and say so in `note`.

## Output: one JSON object, nothing else

{"labeller": "<name>", "rules": [
  {"folder": "...", "id": "...", "status": "ok",
   "requirements": [{"id": "q1", "quote": "...", "keep": "translate"}],
   "clauses": [{"req": "q1", "type": "never", "where": {"cmd": ["force_push"], "branch": "main"}}],
   "note": "..."}
]}
