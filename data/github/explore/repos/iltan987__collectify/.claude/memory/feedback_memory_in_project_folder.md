---
name: Memory lives in the project folder, not per-user
description: All memory files for this repo must be written to .claude/memory/ (git-tracked, shared), never to the per-user ~/.claude/projects/... location
type: feedback
---

For this repository, memory files MUST be written to `.claude/memory/` inside the
project (this directory). Do NOT write memories to the per-user location
`~/.claude/projects/.../memory/`, even if the harness
system prompt points there as the default.

**Why:** The user wants every collaborator who clones this repo to inherit the same
memories. Per-user memory is invisible to teammates; project-folder memory is
committed to git and shared with the whole team. Stated explicitly by the user.

**How to apply:**
- New memory files → `.claude/memory/<name>.md`.
- Index file → `.claude/memory/MEMORY.md` (one line per memory, same format as
  the default system).
- The per-user `~/.claude/projects/.../memory/MEMORY.md` contains a single-line
  pointer redirecting the harness to `.claude/memory/MEMORY.md` so auto-load
  still works. Do not re-populate the per-user folder with content.
- When the user asks to remember or forget something, make the change here.
- Also codified in `.specify/memory/constitution.md` Principle V
  (NON-NEGOTIABLE).
