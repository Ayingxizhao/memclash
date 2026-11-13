---
name: dta-vendor-toolchain-is-committed-not-gitignored
description: vendor/cmake + vendor/mingw64 + vendor/ninja (~1.37GB) are tracked in git and already pushed to the public GitHub remote; DECIDED 2026-09-17 by the maintainer -- "vendor/ must remain", so it stays tracked as it is
metadata:
  type: project
---

**Status: DECIDED 2026-09-17. The maintainer's words: "vendor/ must remain." The tracked
`vendor/cmake`, `vendor/mingw64` and `vendor/ninja` stay tracked; no history rewrite, no
removal. The gitignored `vendor/` subtrees (ps2-bios, pcsx2-src, …) stay gitignored. The history
below is how the question arose.**

`.gitignore` blocks specific `vendor/` subdirectories (`ps2-bios/`, `pcsx2-src/`,
`pcsx2-dcfm-parity/`, `blender-scripts/`, `es/`, `koffi/`, `mkps2iso/`, `mkpsf2/`) but never a
blanket `vendor/` — so when `vendor/cmake`, `vendor/mingw64` and `vendor/ninja` (434M + 940M +
1.7M) were added in commit `ed97300` ("Add a self-contained CMake + Ninja + MinGW-w64 build
toolchain, vendored entirely inside the repo", 2026-09-13, authored `Dayuppy`, co-authored by an
earlier Claude session), nothing blocked them from being committed. This is already on
`origin/main` on the PUBLIC `github.com/Gundorada-Workshop/DarkCloud-Toolkit` (confirmed via the
browser: repo shows "Public", `vendor/cmake`/`mingw64`/`ninja` visible at `main`), pushed during
that same 2026-09-13 session — NOT pushed by the 2026-09-17 session that found this.

**Why it happened, on its own terms**: the commit's own message frames it as satisfying Hard Rule
1 (self-contained: "a fresh clone builds the same way on any machine with nothing to fetch
first") — a genuine, deliberate tradeoff, not an oversight of forgetting a `.gitignore` line. It
directly conflicts with the OTHER hard rule ("never commit... a large vendored dependency") and
with `CLAUDE.md`/`AGENTS.md`'s own explicit claim that `vendor/` is gitignored on purpose, which
was never reconciled or disclosed as an exception in those docs.

**Asked the user 2026-09-17** (`AskUserQuestion`, four options: leave history + fix docs / stop
future growth only / rewrite history + force-push / decide later) — they redirected to a
clarifying question first ("Clarify where you pushed this. This should be local only, not pushed
publicly anywhere") rather than picking an option. Answered with the facts above (this session
never ran `git push`; `git reflog` shows no push entries; `origin/main`'s tip predates this
session's start per the session's own initial `gitStatus` snapshot) and left the original question
open, since the user had not yet chosen among the four options at last check.

**A related, second instance found in the same fresh-clone pass**:
`vendor/blender-scripts/io_dcfm_mds` (the Blender MDS import/export bridge) is ALSO gitignored,
but unlike cmake/mingw64/ninja it is unambiguously first-party project code (`bl_info`:
`"author": "DCFM"`, shells out to this project's own `Tools/dc_mds_scene.mjs`) — not a vendored
third-party dependency at all. If it is never committed, this project's own ~4,601 lines of
Blender-integration source exist only on whichever machine(s) happen to have manually placed them
there, with no version-control backup. Not raised to the user yet as its own question (it surfaced
after the vendor/cmake conversation was already in progress) — worth asking about together with
the cmake/mingw64/ninja decision, since both are "should genuinely-authored-or-fetched-once
content under vendor/ be tracked" questions, just pointing in opposite directions (one argues for
REMOVING something already committed; this one argues for ADDING something that currently isn't).
See [[dta-fresh-clone-verification-findings]] for the graceful-degradation fix (skip when absent)
that was made regardless of this policy question — that fix is correct either way it resolves.

**How to apply**: do not assume either "the toolchain should be removed from history" or "it's
fine as-is, leave it" — both are live possibilities until the user actually answers. Do not
force-push, do not rewrite history, do not add `vendor/` (blanket) to `.gitignore`, and do not
commit `vendor/blender-scripts` without the user weighing in first. If a future session finds this
memory and the question is still open, re-surface it rather than assuming silence means either
answer.
