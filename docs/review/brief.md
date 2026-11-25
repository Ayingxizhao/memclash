# Reviewer brief

You are reviewing a student project in the middle of development. Today is 2026-11-21. The
project is presented on 2026-12-01, so about 10 days of work are left. We want honest critique,
not encouragement.

## The problem

Coding agents (Claude Code, Codex, Cursor, ...) keep a memory folder: markdown files of rules
the user or the agent wrote on different days ("never push to main", "use the MCP tool for
GitHub reads", "you may create PRs with gh"). Over time some rules contradict each other, and
the agent then follows one rule and breaks the other. Our project tries to find those pairs.

Research question (from `README.md`): for rules in agent memory, does a solver-assisted check
leave fewer conflicting rule pairs than keeping every rule or asking an LLM, and how much of its
error comes from translating rules into logic?

## What a "clash" is (ADR 0003)

Two rules clash if, in some situation the rules name, no single action satisfies both.
must = obligation, never = prohibition, may = strong permission (the action must stay possible),
only if = conditional obligation. Example of a clash under this definition: "use tool G for any
GitHub read" vs "use tool M to look up a job ID", because a lookup is a kind of read and the
agent uses one tool per action.

## What exists

1. Dataset: real memory folders from GitHub, split into rules. Dev: 5 folders (125 rules).
   Held-out: 10 folders (389 rules), labelled by others, not yet used. Large: 4 folders
   (677 rules), used as tuning data.
2. Negative result (`gate_v1/`): one fixed format for every rule, objects copied as free text,
   checked by Z3. Found 0 of 10 labelled conflicts.
3. General method (`pipeline/general/`): LLM lists related pairs, LLM judges each pair, then an
   LLM writes the pair as logic and Z3 confirms. On dev, Z3 kept 8 of the judge's 21 conflict
   flags (all real by the author's reading); the judge misses about half the labelled conflicts.
4. Exact git method (`pipeline/git/git_check.py`): an LLM translates each rule alone into
   clauses over a fixed git model (operations such as commit, push, merge, reset; facts such as
   branch, file, user asked, tests passed). What git means is code, not LLM judgment. Z3 checks
   every pair. On a small planted-rule pilot: 6 of 6 planted git conflicts caught, 0 of 3
   rewordings flagged. (Two checker bugs were fixed on that same pilot.)
5. Planted-rule test (`pipeline/eval/`): a second model writes conflicting rules and rewordings
   for real rules.

Decisions are recorded in `docs/adr/0001` to `0007`. Please read them.

## The current bottleneck

On the 4 large folders, a keyword + LLM filter kept 212 git rules. The git checker reports
**0 clashes** there. To check that, two readers (Codex and Claude) looked for clashes by hand and
the author labelled every flagged pair (`data/runs/git/large_filter/reference_labels.json`):
11 clashes, 2 that depend on a word's meaning, 3 not clashes. **The checker finds 0 of the 11.**

All 11 involve things the git model cannot express:
- 9 are about which tool to use (MCP tool vs a `gh` wrapper vs the CLI), e.g. "use the MCP tool
  for every GitHub read" vs "look up the run ID with gh-cc-var". The model has no tool field, so
  the translator drops the tool and Z3 never sees it.
- 1 is about "dev-bot testing", 1 depends on "backlog sweep". Unexpressible conditions become
  unknown facts (ADR 0004), and two rules naming the same condition get different facts, so
  their clash is missed.

Two things are missing: (a) a place to store words like the tool name, and (b) relations
between words ("a lookup is a kind of read", "these two tools exclude each other"). Z3 accepts
any names; it is the relations that make words clash. The earlier `gate_v1` attempt had open
words but no relations and found nothing.

## Options being considered

- **A. Add fields by hand** (tool, a few named conditions). About 1 day. Fits these folders;
  likely overfits to them.
- **B. Fixed logic, open words built by the LLM through tools (current recommendation).** The
  rule shape, the meaning of must/never/may/only if, three relation kinds (is a kind of, same
  as, cannot both be true) and "one tool per action" stay fixed in code. Per folder, the LLM
  builds a word list while translating, through tool calls such as `add_word(kind, name)` and
  `relate(a, "kind_of", b)`, which the checker validates. The word list is saved and a person can
  review each relation. Z3 then checks every pair as today. About 2–3 days.
- **C. Same as B, but the word list is built in one batch call per folder** before translation.
  About 2 days.

Planned measures: at least 8 of 11 reference clashes found, 0 invented clashes, the pilot still
6/6 and 0/3, stable across 3 runs; then one run on the held-out folders with everything frozen.

## The author's open doubt

Judging whether two words mean the same thing ("lookup" vs "read") is the hard part of natural
language. Our current view: that is the LLM's job, not ours. Our contribution would be to make
each such judgment an explicit, reviewable statement that Z3 then reasons over exactly, instead
of hiding it inside an LLM's yes/no answer. We are not sure a reviewer would accept that as a
contribution, or whether this problem matters at all.

## Rules for you

- Do not read any file matching `data/gold/labels_*` (held-out labels; reading them would spoil
  the final test).
- Do not edit or create files except your review file.
- Do not call any paid LLM API or run anything that does (`pipeline/llm.py`). Reading code and
  running `uv run python pipeline/git/git_check.py selftest` is fine.
- If you are unsure of a fact, say so instead of guessing.
