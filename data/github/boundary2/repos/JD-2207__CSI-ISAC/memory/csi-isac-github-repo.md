---
name: csi-isac-github-repo
description: "The user's GitHub repo is JD-2207/CSI-ISAC with a layout that does NOT match the local workspace; the local csi_isac clone points at the upstream, not theirs"
metadata: 
  node_type: memory
  type: project
  originSessionId: f613f78b-84ad-430d-b890-1e6c3d164eb1
  modified: 2026-07-28T11:28:01.492Z
---

The user's own repo is **https://github.com/JD-2207/CSI-ISAC.git**, branch `main` (only branch).

**Trap:** `C:\Users\javid\Documents\Javier\CSI` is NOT a git repo, and the git repo at
`CSI\csi_isac\` (folder renamed from `StochasticRTcomparison` on 2026-08-12) still has
`origin = jmoraispk/StochasticRTcomparison` — the UPSTREAM project it was cloned from, not the
user's. Never push there.

**Path mapping** (repo path -> local source):
- `src/...`    -> `CSI\csi_isac\src\...`
- `memory/...` -> `C:\Users\javid\.claude\projects\c--Users-javid-Documents-Javier-CSI\memory\...`
- `thesis_code_walkthrough_QA.md`, `figures/*.svg` -> `CSI\` (repo root)

**Workflow that works:** clone CSI-ISAC to scratchpad, copy changed files in per the mapping,
commit, push. Scope = update already-tracked files + new `src/exp/*.py` only. NEVER stage
`src/data` (27 GB), `src/checkpoint`, `src/results` — untracked and must stay so.

**Gotchas:** most files show as "modified" by byte-compare but differ only in CRLF/LF — use
`git diff --stat` after copying to see the real set. The user pushes themselves via `!`
(no `gh` CLI installed; a credential dialog may report "User cancelled" yet still succeed —
verify with `git ls-remote origin main`). Commits carry NO co-author trailer:
[[no-coauthor-trailer]].
