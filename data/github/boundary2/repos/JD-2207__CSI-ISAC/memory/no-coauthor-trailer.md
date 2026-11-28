---
name: no-coauthor-trailer
description: Never add Co-Authored-By (or any AI-attribution) trailers to commits in this project — user must be sole contributor
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f613f78b-84ad-430d-b890-1e6c3d164eb1
  modified: 2026-07-28T11:27:45.544Z
---

Do NOT add `Co-Authored-By: Claude ...` — or any other AI-attribution trailer, footer, or
"Generated with" line — to git commits, PR bodies, or tags in this project. This overrides
the default commit-message convention.

**Why:** this is the user's master's-thesis repo (github.com/JD-2207/CSI-ISAC). Authorship is
academically meaningful, not cosmetic — they want to appear as the sole contributor. On
2026-07-28 a trailer I added surfaced Claude as a contributor on GitHub and had to be removed
by amending and force-pushing.

**How to apply:** write the commit body only (summary + bullets), stop there, no trailer. If a
commit that already carries one has been pushed, fix with `git commit --amend` + verify the
tree hash is unchanged + `git push --force-with-lease`. See [[csi-isac-github-repo]] for the
repo layout and push mechanics.
