# Open coding — agent_a

5 dev folders, 125 rules, 34 recorded relations (machine-readable: `agent_a.json`).
All quotes verified verbatim against the files (whitespace/markdown-normalized).
Index (`MEMORY.md`) lines that only restate a file were not extracted as rules; index lines
that add or change content were.

## Per folder

### Consteon/web-spreadsheet-example (41 rules, 9 relations)
- **contradiction (medium)** R35 "db-analyst scope is non-destructive SELECTs only per CLAUDE.md" vs
  R32 "db-analyst must never execute DDL … or DML mutations … without explicit user confirmation first."
  Same file: SELECT-only (prohibition) vs mutation allowed after confirmation (permission).
- **override (medium)** index R40 "…DDL/DML on shared DBs need explicit user confirmation first" vs R32
  (all DBs). Index narrows the rule's scope.
- **contradiction (medium)** R3 "fix the value, not the target enum" vs R6 "Schema fix (column type
  change) is on the table when the constraint contradicts real domain." Situation: a user-intended
  label is missing from the target enum.
- **other (medium)** R36 "Always confirm the exact target database…" vs R37/R38 "if the user specifies
  a database name, use exactly that" / ask only on ambiguity. Disagree on when to confirm.
- **other (high)** stale index: R41 "latest: don't trim user values…" — that lesson is the *first*
  entry of code-improvement.md, not the latest.
- **duplicate (high) ×2** general R21 "any CASE...WHEN expression must explicitly CAST…" subsumes
  R13 (NUMERIC) and R19 (TIMESTAMPTZ).
- **duplicate (high)** R32 vs R34 "Never auto-execute mutations even if logically required."
- **other (low)** R29 "Never copy nearby modules as reference" vs R24 "Do not change … catch block —
  it matches the file-wide pattern." Local-convention vs reference tension; may not be real.

### MCMike0399/from-tcp-to-http (20 rules, 4 relations)
- **duplicate (high) ×3** course-design rules restated in user_profile.md (text resources R1/R17,
  no videos R2/R18, don't withhold R8/R19).
- **other (low)** R20 "Values self-directed research … over being spoon-fed by an AI" vs R6 "Generate
  boilerplate fast." Soft preference tension, satisfiable together.
- No contradictions.

### M-Hernandez/setflow (16 rules, 7 relations)
- **other (medium)** R2 "After `gh pr merge`, run … `git push origin --delete <branch>`…" vs
  R5 "Before any `git push` or `gh pr create`, show the user the list of changed files and ask for
  confirmation." Routine cleanup triggers the precondition of another rule.
- **other (high)** stale index: R16 "#4 and #5 next" vs R11 "#17 is the next issue".
- **other (low)** R7 commit ".env.example" vs R8 "verify no .env files … are staged" (wording ambiguity).
- **duplicate ×4** user_profile.md restates confirm-before-push, no stale branches, no credentials;
  R3/R5 restate each other in one file.

### shabelson-picker/applied_math (38 rules, 12 relations) — richest folder
- **contradiction (high) ×3** R8 "Each module = my plain-text lecture notes (no LaTeX, …)" vs
  R20 "write its math in LaTeX from the start", vs R18 (LaTeX conventions for course notes), and vs
  no-latex-explanations.md R33 "those source files use LaTeX". Older rule never removed.
- **contradiction (high)** index R36 "explain math in plain text, never LaTeX" vs R33: the index drops
  the rule's scope (chat only).
- **override (high)** R6 "One module per chapter … following the book" vs R19 "CLRS is now the
  primary text." Newer decision; older structure rule left in place.
- **other (high)** stale index R37 "built around the Sedgewick-Flajolet book" vs R19.
- **contradiction (medium)** R3 "Don't … lean on outside knowledge" vs R10 "introduced as a
  repurposing of something familiar".
- **override (medium)** R7 "Lazy expansions … only … when we actually hit friction" vs R4 "Build
  prerequisites explicitly" (teaching-stance file).
- **other (medium)** R21 "Resume at Module 1 §4" — from a 2026-07-11 status block, predates the
  2026-08-29 re-pacing.
- **other (low)** R38 "simple formal English" (DS proofs) vs R14/R15 high register, "Do NOT simplify".
- **other (high)** dangling reference: `ds-formal-proof-practice.md` is indexed but missing.
- **other (medium)** unindexed file: `aofa-course-teaching-stance.md`.
- Also (fact, not rule): aofa-course.md says the top folder "holds only" `course/`, while
  ds-class-cheatsheet.md lists ex1/–ex5/, presentations/, extra/, cheatsheet.md there.

### thesteve0/local-llm-benchmark (10 rules, 2 relations)
- **duplicate (high)** R4 vs R7: metrics from llama.cpp server `timings` (cross-file).
- **other (medium)** dangling reference `[[user-hardware]]`.
- R6 vs R8 (Ramalama labels kept on historical tables) is an explicit exception: not a relation.

## Catalog (my categories)

| Type | Definition | Count | Example |
|---|---|---|---|
| **Superseded rule left in place** | A newer decision changes behavior; the older rule stays in memory unchanged | 5 | "no LaTeX" in module notes vs "write its math in LaTeX from the start" |
| **Index drift** | MEMORY.md entry is stale or drops/changes the scope of the file it summarizes | 5 | index "never LaTeX" vs file "chat = unicode, course PDFs = LaTeX" |
| **Genuine cross-rule conflict** | Two current rules prescribe incompatible behavior in an overlapping situation (incl. permission vs prohibition, general principle vs specific policy) | 4 | "SELECT-only" vs "mutations after confirmation" |
| **Trigger/scope ambiguity** | One rule's procedure falls inside another rule's trigger, or rules disagree on when a step is required | 3 | auto `git push --delete` vs "confirm before any git push" |
| **Soft preference tension** | Vague preferences pulling in different directions; satisfiable together | 3 | "don't spoon-feed" vs "generate boilerplate fast" |
| **Duplicate / subsumption** | Same requirement restated (user_profile vs feedback, body vs How-to-apply) or special case of a general rule | 11 | CAST rule for NUMERIC subsumed by "any CASE...WHEN must CAST" |
| **Broken structure** | Dangling link, missing indexed file, unindexed file | 3 | `ds-formal-proof-practice.md` indexed but absent |

Folder-level: 3/5 folders have at least one medium/high non-duplicate problem (Consteon,
setflow, applied_math); 2/5 have a labelled `contradiction`.

**Observation:** the most common real problems are *temporal* (superseded rules, stale index,
stale "next step"), not two equally current rules disagreeing. A conflict checker for memory
therefore needs time/version information and a supersede action, and the index should be
treated as derived content (regenerate, don't trust).

## Scope dimensions (rough counts over 125 rules)
- Tool/command (git push, gh pr merge, llama serve, cpptools, db-analyst sub-agent): ~25
- Artifact/file (course notes, cheat sheet, models/*.md, a specific repository file): ~25
- Code construct/pattern (CASE...WHEN, repository functions, catch blocks, async function): ~20
- Task type (recommending resources, evaluating docs, teaching, migrations, seeding rows): ~25
- Output medium/style (chat vs PDF, register, line width, Hebrew): ~12
- Time/state (after merge, before commit, until user says skip, "next issue", status dates): ~10
- Agent role (db-analyst, coder): ~8

## Hard to formalize
- Vague: "Be direct.", "Explain clearly.", "Don't artificially withhold information.",
  "Teach everything from the ground up, self-contained and thorough" — no checkable action.
- Preference strength: user_profile statements ("Values self-directed research … over being
  spoon-fed") are preferences, not rules; "can be noted as supplementary" (weak permission).
- Numeric/approximate: "~70 chars", "30–45 min sessions", "~40 sets".
- Temporal/ephemeral: "#17 is the next issue", "Resume at Module 1 §4", "until then, cover it
  properly", "open the combinatorics toolbox expansion early".
- Judgment conditions: "when the constraint contradicts real domain", "values that look like real
  credentials", "If there is any ambiguity".
- Syntactic code patterns (`THEN CAST(${…} AS NUMERIC)`): checkable by a linter, awkward as typed logic.
