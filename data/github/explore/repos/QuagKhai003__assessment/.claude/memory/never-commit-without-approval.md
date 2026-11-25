---
name: never-commit-without-approval
description: "Never commit or push without the user's explicit approval"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 41ea88ec-b02d-4d56-870d-77f0c67c4730
  modified: 2026-08-13T06:53:42.769Z
---

Git workflow rules for this project:
- **Every commit needs the user's approval** — docs AND code. Stage/prepare, then wait for the go before committing.
- **Docs / decisions / planning / non-code: commit on the current branch** — no need to check out a new branch.
- **Code: on its own dedicated branch.** Never work code directly on `main`/`master`; check out a branch and commit there after approval.
- **Never delete branches** — leave merged branches in place (the user corrected me for deleting a merged phase branch).
- **Pushing** to a remote needs approval regardless of what changed.

**Why:** User owns the git history and its timing; the assessment grades the commit story (§2.4). The docs relaxation is only about branch, not approval.

**How to apply:** Always wait for approval before any commit. Docs go on whatever branch we're on; code gets its own branch. Recorded in the repo's CLAUDE.md repo-etiquette too.
