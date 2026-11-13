---
name: reviews-implementations-in-browser
description: After parallel /workflow:implement runs the user reviews the branches in a real browser before merging — start each worktree's dev server and print the links
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9ffa8c3b-27d3-4d3c-9ea0-3c755f895592
  modified: 2026-08-05T09:35:59.088Z
---

When `/workflow:implement` runs finish, the user does **not** review by diff and test output alone. They ask for the finished branches to be **run**, e.g. *"Can you deploy both of the worktree agents, and then print out the links so I can look at them in a browser locally?"* — then, after looking: *"Shut them down. Then make sure you fetch and pull all the latest changes, then merge both of these to master and finalize."*

**Why:** implementation branches land unmerged by design (`/workflow:implement` never merges), so the user is the gate. They want to see the actual UI before the merge decision, not just be told the gates passed.

**How to apply:** when reporting completed implementation branches, offer to start each worktree's dev server and **print the URLs plainly** so they can be clicked (each agent worktree gets its own port in 5200–5499 — see `spec/development.md`). Expect the close-out sequence to be: view → shut the servers down → fetch/pull → merge the branches to `master` → `/workflow:finalise`.

**Worktrees are not durable storage.** Agent worktree *directories* under
`.claude/worktrees/` can vanish between sessions while `git worktree list` still
lists them (stale, often `locked`, so `git worktree prune` won't clear them —
sidestep a name collision with a new branch suffix rather than force-unlocking).
Anything uncommitted in a worktree is gone with it: a session-limit kill cost a
run its whole in-progress phase. So instruct orchestrators to **push each phase
the moment its gates pass**, never to accumulate unpushed work, and when a run
dies check `git ls-remote origin` — what's pushed is all that survived. See
[[stacking-implementation-branches]].

**Long-lived review worktrees go outside `.claude/worktrees/`.** The harness prunes that directory on session restart, so review servers left there 404 the next day. Anything the user is meant to look at *tomorrow* belongs in a sibling directory (e.g. `../sudokuquest-variants/<name>`) on a `variants/*` branch, which survives.

**Cleanup is automated now — don't do it by hand.** These review dev servers get orphaned (`npm run dev --prefix .../worktrees/agent-*` plus its `vite.js` child outlive the session and hold the worktree open), and a worktree stays `locked` with `.git/worktrees/<id>/locked` reading `claude agent <id> (pid N)`, which makes `git worktree remove` refuse. The user asked for that leak fixed at the root, not swept up per-incident (*"I want that problem solved so it doesn't keep happening"* — see [[prefers-root-cause-fixes]]), so the workflow plugin's `scripts/reap-worktrees.sh` now does it: dry run by default, `--apply` to act. `/workflow:merge` runs it as its last step and `/workflow:startup` sweeps the backlog. It reaps only worktrees that are under `.claude/worktrees/`, clean, and stale-locked (the lock pid names no running `claude` process), and deletes a branch only when it is fully merged — so live sessions' worktrees survive. Reach for the reaper rather than hand-killing processes and force-unlocking.

**Scoped exception:** `/workflow:implementall` (ported here 2026-09-07, now from the plugin) sweeps the whole `plans/` backlog unattended and merges each branch with no review gate — the user asked for that explicitly when it was introduced in CryptoHex: *"do not request reviews from the user before merging"*. The gate above still holds for an ordinary `/workflow:implement`; only an `implementall` sweep waives it, and its final report says plainly what landed unreviewed.
