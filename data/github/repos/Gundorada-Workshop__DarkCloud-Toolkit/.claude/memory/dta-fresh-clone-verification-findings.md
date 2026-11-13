---
name: dta-fresh-clone-verification-findings
description: the first real `git clone --local` + dta check all run in this checkout's history; found and fixed 2 real bugs, and confirmed a large disclosed gap (FAIL vs SKIP for a missing disc/build-output) is bigger than previously scoped
metadata:
  type: project
---

Phase 12's checklist item "`dta check all` both in place and from a fresh `git clone --local`"
had never actually been run. Doing it (2026-09-17) surfaced real findings beyond what running it
only in-place could.

**Clone mechanics, for next time**: `git clone --local` defaults to hardlinks, which fail across
drives (`Improper link`) — the scratchpad temp dir is on `C:`, this repo is on `D:`. Clone to a
path on the SAME drive. Separately, `vendor/cmake`'s deeply-nested doc tree hits Windows'
~260-char path limit on an ordinary (non-hardlink) checkout unless the destination path itself is
short — cloned to `<drive>\dta-clone-test` (short, drive-root-adjacent) rather than nesting under the
already-long scratchpad path, and that alone fixed it; `core.longpaths=true` was passed too, belt
and suspenders. A bare clone is legitimately ~1.8GB, because `vendor/cmake`+`vendor/mingw64`+
`vendor/ninja` ARE tracked and cloned — see [[dta-vendor-toolchain-is-committed-not-gitignored]].

**Two real bugs found and fixed, both "check throws/fails instead of skipping when a legitimately
gitignored, machine-local artifact is absent"** (same family as
[[dta-gates-had-never-been-built]]'s port.mjs fixes, found by the SAME exercise one layer deeper):

1. `app/gates/distro.mjs`'s "the oracle is where the exclusion list expects it" did a bare
   `fs.existsSync` on `data/gametables-oracle/DcMonstorTable.inc` -- retail game data, correctly
   gitignored per `CONTRIBUTING.md`, absent on every checkout but the maintainer's own that has
   manually populated it. `docs/KNOWN_ISSUES.md` §6 already SAYS a checkout without it should
   report "the differential did not run," not a smaller pass -- the C++ harness already does this;
   this one Node-side sanity check didn't. Fixed with the same `if (exists) check else skip`
   idiom used throughout this codebase.
2. `app/gates/model.mjs`'s "the add-on zip" section (`buildAddonZip()`) threw an uncaught
   exception -- not just a FAIL, a suite CRASH -- when `vendor/blender-scripts/io_dcfm_mds` is
   absent, which is always, on any machine but the maintainer's (gitignored). A second block
   right next to it (checking each companion script "is vendored", and the add-on's own
   file/line count) had the same unconditional-existence-check gap. Both guarded the same way,
   verified in BOTH states (present: still 82/82 in the main tree; absent: 29/29 clean in the
   clone, was a crash before).

**A third, much larger finding, NOT fixed this pass -- scoped as future work**: `port`, `stb`,
`re` and `relink` all show real FAILs in a bare fresh clone that are not bugs in what they assert,
but ARE a classification gap: they correctly detect that `rom/DarkCloud.iso` (or its extracted
files, or `data/samples/`, or `build/gates/*/result.json` from a not-yet-run gate build/run) is
absent, and report it -- honestly, per this project's own disclosure discipline -- but as a hard
FAIL rather than a SKIP, unlike `iso`/`fmt`/`audio`/`model`'s already-established graceful pattern.
`port.mjs`'s own "retargeting a foreign absolute path" section says outright in its own comment:
"The disc and the samples ARE here, so the literals are rewritten" -- the section's whole design
assumes they exist; it was never meant to run meaningfully without them, it just never learned to
say so instead of failing. This is NOT a brand-new gap: `docs/DEV_ROADMAP.md` Phase 9 §2/§3 already
flags part of this exact section ("make the check... independent of whether that drive happens to
be mounted right now") as open, disclosed, not-yet-done work -- this pass confirms the scope is
wider than §2/§3 alone (stb's `data/stb_decode/*.json` checks and re/relink's disc-extraction
checks are the same pattern, in different files) and gives it a name: FAIL-vs-SKIP for an absent
disc/build-output prerequisite, across (at least) 4 suites. A `git clone --local` + full setup
(supply a disc, run `dta gate build/run --all`) was NOT attempted this pass (would reuse the disc
image and re-run a ~12-minute gate build) -- that would be the next, stronger version of this
check: does 14/14 hold in a SECOND, independently-set-up checkout, not just this one.

**The second clone, WITH the disc, was run 2026-09-17** (`build/fresh-clone/`, junctions for
`rom/`, `pcsx2/` and the nine gitignored `vendor/` subtrees, `local.config.json` copied): product
build clean in 108.7 s, 174/174 gates built, selftest 36/36, frame-check right (no baseline there).
Every remaining gap was ONE class one layer down - the gate runner and four harnesses reporting an
absent `data/samples`/`data/vu` as FAIL or as a crash - plus one gate (`DcGovernorGate`) that
measured its own lowered I/O priority as "given". All closed the same day; see
[[dta-suite-blocked-verdict]] for the runner rule. Reproduce a harness gap by running its exe
directly from an empty directory (no junctions); reproduce the governor one by running the exe
directly from a shell whose I/O priority nobody lowered.

**How to apply**: before claiming `dta check all` is "the same from any checkout," actually run a
fresh clone — this pass found 2 real, fixable bugs and one real, larger, previously-underscoped
gap that only shows up that way; running the suite only in-place cannot find either category.
