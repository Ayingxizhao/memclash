---
name: read-project-rules-before-acting
description:
  "Before running anything in one of Mike's repos, read its CLAUDE.md and constitution; be thorough
  before saying Mike's instructions are wrong"
metadata:
  node_type: memory
  type: feedback
---

Copied on 2026-10-03 from the `configure-computer` project's memory,
`read-project-rules-before-acting.md`.

Before running any command in one of Mike's repos (including clones under
configure-computer/scratch/), read that repo's CLAUDE.md, any `.claude/rules/constitution.md`, and
the top-level README, and follow them.

Rules in those repos that matter right now:
- spiresRobot2026: Claude may NOT run `uv` commands, state-changing `git` (checkout, commit,
  switch), ssh, or `robotpy deploy`. Mike runs `uv sync`; Claude runs `.venv/bin/robotpy test`,
  `.venv/bin/ruff check`, `.venv/bin/ruff format --check --diff` and `.venv/bin/mypy .`.
- stick-e-bot: at session start and after each compaction, summarize the constitution and agree to
  follow it. Invoke the `onshape` skill before modeling. A REST build needs Mike's grant naming the
  document.

**Why:** On 2026-10-01 Claude ran `uv sync`, `uv run robotpy test` and `git checkout` in
spiresRobot2026 without reading its CLAUDE.md. Claude also told Mike a constitution "only" existed
in one repo after a shallow search. Mike said: "Don't be so quick to tell me I'm wrong... be a bit
more thorough before saying that the instructions were wrong."
**How to apply:** Search every branch and read the rule files before acting. When something Mike
says doesn't match what you found, say what you searched and ask, rather than declaring him
mistaken. Related: [[commit-identity]].
