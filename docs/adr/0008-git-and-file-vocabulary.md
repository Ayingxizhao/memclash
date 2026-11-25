# 0008. One fixed vocabulary for git and basic file rules

Date: 2026-11-22. Status: Accepted. Extends 0002.

## Context
The survey of 60 more memory folders found that besides git, rules about files (read, create,
edit, move, delete, what stays in the repo) and about running commands are common and can be
written in a fixed form without knowing tool names. Two research reports
(`docs/review/schema_research_*.md`) found that comparable systems (GitHub rulesets, Claude
Code permissions, Cedar, AppArmor) all fix the action list in code and leave only names open.
Two critical reviews (`docs/review/attack_review_*.md`) asked that every item be justified and
that ambiguous words not be decided silently.

## Decision
- The vocabulary is `docs/review/vocab_draft.md` v2, written by Claude and Codex in five review
  rounds and approved by the author. It is fixed in code for the experiment; changes need a
  new version.
- Scope: git rules plus basic file rules and `run` with a fixed task list. If the file part
  gives poor results, it is dropped from the report.
- Words with more than one meaning are read from the rule's own text; if unclear, the rule is
  excluded and listed with the word.
- "In the repo" is a state. Opposite state requirements are reported as a separate verdict,
  "state conflict"; 0003 is unchanged.
- "May" vs "never" / "must" pairs are reported as their own category, "exception (needs a
  priority rule)", next to plain clashes.
- The translator sees only the rule, its file name and its section heading, not the folder's
  other rules, so that other rules cannot change how a rule is read.
- Claims say "solver-checked": exact with respect to the translations.

## Consequences
- The checker and prompt changes in section 8 of the vocabulary must be made before any
  translation run.
- Some rules a reader would understand from the folder become unclear; their number is reported.
- The held-out folders were selected with a git filter (0005), so the held-out claim stays
  git-only. File rules are reported on the survey folders, with three-run agreement and a
  hand-checked sample.
