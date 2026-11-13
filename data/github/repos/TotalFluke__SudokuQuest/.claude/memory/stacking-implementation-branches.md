---
name: stacking-implementation-branches
description: "When one plan depends on another still in flight, stack the /implement worktree on the sibling branch instead of waiting for a merge"
metadata: 
  node_type: memory
  type: project
  originSessionId: dfac6e76-2996-4671-8cdf-6b3be774774c
  modified: 2026-08-05T09:25:45.402Z
---

`/implement` cuts every worktree from `origin/master`, so a plan whose
dependencies live on an unmerged sibling branch appears blocked. It usually
isn't. Check what the sibling branch has actually **pushed** before believing a
plan's own "blocked" note — `progress.md` blockers are written when the plan is
authored and go stale fast.

To stack, instruct the orchestrator to do this once in its own fresh worktree
(overriding the skill's ban on branch switching, which still binds phase agents):

```bash
git fetch origin
git checkout -B implementations/<plan>-2 origin/implementations/<dependency>
git cherry-pick <earlier phase commits of this plan>
```

The `-2` suffix is needed because the plain branch name is usually already
checked out in the earlier run's worktree, and git refuses a second checkout.

Two things to get right:

- **Partition by dependency, not by phase number.** Work driven off types the
  sibling has already pushed can start immediately; only items needing its
  *uncommitted* phases get deferred. Tell the agent to re-fetch and rebase
  before finalising, and to defer-and-report rather than stub the engine or
  lower a gate if the dependency still hasn't landed.
- **Look for superseded work in the dependency.** If both plans rewrite the same
  file, the later plan often replaces the earlier one's version wholesale — that
  phase is dead work and the only real conflict source. Cancelling it is cheaper
  than merging it. Redirecting another session's live agent is the user's call,
  so hand them the instruction rather than sending it.

Record the stacking in `progress.md`: the branch must be merged **after** its
base. Relates to [[reviews-implementations-in-browser]].
