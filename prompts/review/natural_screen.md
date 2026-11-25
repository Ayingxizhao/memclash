You are a judge in a research experiment. Work read-only (do not edit or create files; your
final message is saved). Do not open `data/gold/`, files named `labels_*`, `frozen_*`, anything
under `data/runs/rules/`, `data/runs/natural/pairs_all.json`, or `docs/review/`. Do not call any
paid API. Do not look at the folders on disk; judge only the rules given.

Read `data/runs/natural/rules_blind.json`: five coding-agent memory folders, each a list of rules
(id, source file, rule text). Consider EVERY pair of rules within the same folder (951 pairs in
all) and judge each pair with this definition and nothing else:

- `clash`: in some situation that both rules talk about, no single action follows both rules.
- `exception`: one rule explicitly permits something ("you may X") that the other forbids or
  limits; the permission cannot be used in some situation both rules cover.
- `compatible`: otherwise. Rules about different things, or that can always both be followed,
  are compatible. Rules that say the same thing in different words are compatible.

Read each rule's scope carefully (which files, which branch, which kind of change, when). A
named group may refer to concrete files named in another rule ("save data" vs a list of save
files); judge what an agent working in that folder would reasonably understand.

Output only: a JSON array (in a ```json block) of every pair you judge NOT compatible:
{"folder", "a", "b", "verdict": "clash"|"exception", "confidence": "high"|"low",
"situation": "<one line: the situation where no action follows both>"}; use `a` < `b` in the
order the ids appear in the file. All other pairs are taken as compatible. Then one line with
the number of pairs flagged per folder.
