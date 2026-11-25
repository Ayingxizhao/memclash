You are an independent research consultant for a class project. Work read-only in the repo
(do not edit or create files; your final message is saved as your report). You may search the
web. Do not open `data/gold/` or any file named `labels_*`. Do not call any paid LLM API.

## Context (read these first)

- `README.md`, `docs/adr/0002-narrow-to-git-rules.md`, `docs/adr/0003-clash-definition.md`,
  `docs/adr/0004-unexpressible-conditions.md`
- `pipeline/git/git_check.py` (the current fixed git model: operations, fields, clause types
  never / only_if / must_do / may_do, and `same_meaning`, which checks with Z3 whether two
  translations of one rule mean the same)
- `prompts/git/git_translate.md` (how an LLM translates one rule into that model)

The project: coding agents keep memory folders of instructions. An LLM translates each
instruction alone into a fixed format; Z3 checks every pair for a clash ("in some situation the
rules name, no single action satisfies both"; an explicit "may" must stay possible). We now want
to cover two families with ONE fixed format, without needing to understand tool names:

1. git rules (already modelled): e.g. "never force push" vs a template that force-pushes;
   "you may delete merged branches when asked" vs "never delete branches"; "never push without
   an explicit ask" vs "the final step pushes to main".
2. file rules: read / create / edit / delete a path, commit it, keep it out of git, under
   conditions like "only with the user's approval", "only by a given agent", "not while X runs".
   e.g. "delete all map and player data" vs "never delete server-world.dat without permission";
   "create game/objects/XX-name/" vs "objects are game/objects/XX-name.c, no subfolders";
   "never commit vendor/" vs "vendor/cmake stays committed".
   Also "run tests / build only when asked" vs "always run all tests after a change".

We will translate each rule 3 times and use `same_meaning` to measure agreement across runs.

## Questions to answer

1. **Prior art for the vocabulary.** How do existing systems write rules about these actions?
   Cover at least: Claude Code permission rules (Read/Edit/Write/Bash patterns), Codex sandbox and
   approval policies, gitignore and git attributes semantics, GitHub branch protection / rulesets,
   AWS IAM or Cedar or OPA/Rego for file-like resources, AppArmor/SELinux path rules, POSIX/ACL.
   For each: the actions, how targets are matched (glob, regex, prefix), how conditions are
   written, and how conflicts are resolved (deny wins, most specific wins, order).
2. **Fixed or extensible schema?** Should the action list, target matching and condition list be
   fixed in code, or open with a small set of relation types? Argue from prior art and from the
   need for exact checking and for measurable agreement across 3 translations. Recommend one.
3. **A concrete schema proposal.** Actions (with which group into which, e.g. "edit" includes
   "rename"?), target matching (glob semantics, directory vs file, gitignore-style negation?),
   actors, conditions (user asked, user approved, while X running, ...), and how "keep out of git"
   relates to "commit". Say exactly what Z3 needs (sorts, regex for globs, booleans) and what
   stays unexpressible. Keep it as small as possible while covering the examples above.
4. **Literature on conflict detection in such rule sets** (firewall/ACL anomaly detection,
   XACML/policy conflict analysis, Margrave, deontic or norm conflict in multi-agent systems).
   Give 3–6 references you actually found, with one line each on what they check and how ours
   differs. Mark any you only saw an abstract of.
5. **Risks.** What will make translations disagree across runs even with a fixed schema, and how
   to reduce it (e.g. canonical forms, fewer optional fields). What agreement across runs does and
   does not show.

## Output

Markdown, under about 2000 words, sections 1–5 above, then a 5-bullet summary. Cite URLs for
prior art. If unsure, say so; do not invent references.
