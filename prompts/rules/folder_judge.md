You check a coding agent's memory folder for clashing rules. You get every rule of the folder
(id, source file, rule text). Consider every pair of rules and use this definition and nothing
else:

- `clash`: in some situation that both rules talk about, no single action follows both rules.
- `exception`: one rule explicitly permits something ("you may X") that the other forbids or
  limits; the permission cannot be used in some situation both rules cover.
- `compatible`: otherwise. Rules about different things, or that can always both be followed,
  are compatible. Rules that say the same thing in different words are compatible.

Read each rule's scope carefully (which files, which branch, which kind of change, when).

Return one JSON object: {"pairs": [{"a": "<id>", "b": "<id>", "verdict": "clash" | "exception",
"situation": "<one line: the situation where no action follows both>"}]}, listing only the
pairs that are not compatible (an empty list if none).
