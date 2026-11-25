You are an adjudicator in a research experiment. Work read-only (your final message is saved).
Read ONLY `data/runs/natural/probe_unflagged.json` and, for context about each folder,
`data/runs/natural/full_blind.json`. Do not open anything else under `data/` or `docs/review/`,
and no `labels_*` or `frozen_*` files. No paid API calls.

Each item is a pair of rules from one coding-agent memory folder. These pairs were sampled at random from pairs that share words;
most are compatible. Judge each item with this definition only:

- `clash`: in some situation that both rules talk about, no single action follows both rules
  (an explicit permission, "you may X", that the other rule forbids or limits also counts).
- `compatible`: otherwise (different topics, a preference vs an allowance, one rule merely
  refines the other with no conflict, or both can always be followed).
- `ambiguous`: a reasonable reader could go either way; say what the reading depends on.

Use the folder's other rules only to understand terms. Be strict: name the concrete situation.

Output a JSON array (```json block) of {"item", "label": "clash"|"compatible"|"ambiguous",
"in_vocab": true|false, "why": "<one line>"}. `in_vocab` is true only if the clash is about git
actions (commit, push, branch, merge, rebase...), creating/editing/moving/deleting specific files
or folders, or running a named task (tests, build, deploy); false if it turns on which tool or
command style to use, numeric values, code style, or wording.
