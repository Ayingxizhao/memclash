You judge whether two rules from a coding agent's memory folder clash. You get both rules and
the files they came from. Use this definition and nothing else:

- `clash`: in some situation that both rules talk about, no single action follows both rules.
- `exception`: one rule explicitly permits something ("you may X") that the other forbids or
  limits; the permission cannot be used in some situation both rules cover.
- `compatible`: otherwise. Two rules about different things, or that can always both be
  followed, are compatible. Rules that say the same thing in different words are compatible.

Read each rule's scope carefully (which files, which branch, which kind of change, when).
Return one JSON object: {"verdict": "clash" | "exception" | "compatible", "situation": "<one
line: the situation where they clash, or why they are compatible>"}
