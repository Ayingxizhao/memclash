---
name: Branch policy — never commit directly to main
description: All work, including chores, must use a dedicated branch and be merged only after user approval
type: feedback
---

Never commit directly to `main`. Every change — feature, fix, refactor, chore, doc update — must go on its own branch and be merged into main only when the user explicitly agrees.

**Why:** We committed a "chore: remove redundant includes" directly to main without branching. Even the smallest changes must follow the branch → review → merge workflow.

**How to apply:** Before any `git add` / `git commit`, confirm the working branch is not `main`. If it is, create a branch first. Only merge to main when the user says so (same principle as the "sync" rule for pushing).
