---
name: prefers-root-cause-fixes
description: When offered a quick workaround vs a root-cause fix, the user picks the durable fix — offer it as the default
metadata:
  type: feedback
---

Faced with a choice between papering over a recurring annoyance and eliminating
its cause, the user chooses the cause. Asked about phantom uncommitted changes
after a merge, and offered both a one-off `git checkout` of the affected files
and a repo-wide `.gitattributes` line-ending pin, they answered simply:
*"I want the durable fix please."*

**Why:** the recurring symptoms cost more over time than the fix does once, and a
repo-level fix holds for every machine and every worktree — the same reasoning
behind [[prefers-in-repo-deploy-config]].

**How to apply:** when a problem has both a workaround and a root-cause fix,
present the durable one as the recommendation rather than leading with the quick
patch, and say what it costs. Expect the durable route to be chosen even when it
touches more files. Per `CLAUDE.md`, if the fix establishes a convention, record
it in `spec/` in the same change — the line-endings fix landed as
`.gitattributes` **plus** a note in `spec/development.md`.
