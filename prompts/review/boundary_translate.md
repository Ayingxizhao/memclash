You translate rules into a fixed formal vocabulary for a research experiment. Work read-only;
your final message is saved. Open ONLY: `data/runs/natural/boundary_rules_english.json` (86 real
rules), `pipeline/rules/vocab.py`, `pipeline/rules/model.py`, `pipeline/rules/patterns.py`,
`docs/adr/0003-clash-definition.md`, `docs/adr/0004-unexpressible-conditions.md`,
`docs/adr/0008-git-and-file-vocabulary.md`, `data/runs/natural/enforce_names.json`. Do not open
any other file under `data/`. No paid API calls.

For EACH rule give its translation in this format (the format `model.py` reads):
{"status": "ok" | "not_in_scope" | "unclear", "clauses": [...] or null, "left_out": "<parts of the
rule the vocabulary cannot say, or empty>"}
Clause types: never, only_if (with "needs"), must_do, may_do, must_hold, never_hold; fields only
from vocab.py; `when_unmodeled` for a condition the vocabulary cannot check (ADR 0004).
Translate the meaning faithfully: do not drop conditions, do not invent paths or branches the rule
does not name. For tasks and running processes use names from enforce_names.json when one fits;
otherwise "other:<short lowercase words>", and list each such new name under "new_names".

Output only a JSON object in a ```json block:
{"rules": [{"folder": "...", "id": "R..", "translation": {...}, "new_names": ["other:..."]}]}
covering all 86 rules.
