---
name: silent-semantic-merge-conflicts
description: "Merging implementation branches here routinely produces textually-clean but semantically-wrong results — verify by diffing resolved files against the branch tip, never by trusting the absence of conflict markers"
metadata: 
  node_type: memory
  type: project
  originSessionId: dfac6e76-2996-4671-8cdf-6b3be774774c
  modified: 2026-08-15T16:08:01.044Z
---

Parallel `/implement` branches in this repo cut from different points on
`master`, so `git merge` regularly produces results that are **clean textually
and wrong semantically**. Three real instances from one merge
(`slot-dropdowns-3` → `master`, commit `d2d60f7`):

- **A test body from one side spliced onto the other side's stale assertions.**
  `e2e/trial-resolution.spec.ts` got the branch's "nominate every kept piece"
  body but master's old "still rejects" assertions and comments — because
  master hadn't touched those exact lines relative to the merge-base even though
  the branch had rewritten them. No conflict marker appeared.
- **Two individually-valid fixture edits combining into a broken fixture.** Each
  side added a different field/node to a shared `fixtureCase()`; the union broke
  a test neither side broke alone.
- **"Take ours wholesale" silently deleting newer work.** A file the later
  branch never saw (a modal's wiring in `DeskView.svelte`) sat entirely outside
  the conflict hunks, so accepting one side dropped it invisibly.

A fourth shape, from `cloud-agent-runner` → `master` (merge `b2b5d31`,
2026-08-15): **sequentially-numbered new files colliding across branches.** The
branch added `spec/decisions/019-cloud-agents-on-github-actions.md`; while it
was in flight, `unidentified-subjects` merged `019-recovery-and-attribution-are-
separate-questions.md`. Different filenames, so git merged both in perfectly
cleanly, leaving two ADR 019s. Nothing fails — the damage is a reference that
silently points at the wrong document later. Same trap applies to any
monotonic-counter artefact (ADRs, save-format versions, migration files).

**Check this before every merge that adds a numbered file**: list the numbered
directory on `master` *and* on every unmerged sibling branch, not just on the
branch being merged. Renumber to the next free value and grep for the old
number afterwards — the rename touches the file, its own H1, and every
referring document. For a `SAVE_VERSION` collision the observed resolution
(commit `33b9fbb`, two branches both bumping 12→13) is to **chain the
migrations** — the later branch renumbers to the next free version with its
own migration step — never to collapse two branches' migrations under one
number. Keep the audit note describing the renumber rather than
overwriting it; here the number moved twice (planned 016 → filed 019 → merged
020) and the history is what makes a later reader trust the final number.

**How to apply:** after resolving, `git diff <branch-tip> -- <path>` every
touched file and read the result — the absence of markers proves nothing. Treat
a blanket "prefer branch X" instruction as applying only to the *conflicting
hunks*, never to whole files; if given one (including by me), restore the raw
markers and resolve hunk by hunk. Run `npm run check` as well as `test:all` —
vitest does not typecheck, so a newly-required field on a shared type shows up
only in `check`.

Also: only one session may work the primary checkout during a merge. A concurrent
session editing files there mid-merge nearly contaminated the commit, so `/merge`
now **takes a lock** for the whole run — the caller acquires it before spawning
the merge agent and releases it after. Don't work around a held lock by merging
in a worktree or bypassing the skill; wait, or ask the user whether the lock is
stale. Relates to [[stacking-implementation-branches]] and
[[reviews-implementations-in-browser]].
