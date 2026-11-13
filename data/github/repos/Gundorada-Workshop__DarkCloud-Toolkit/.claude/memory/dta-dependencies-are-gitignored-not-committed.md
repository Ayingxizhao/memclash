---
name: dta-dependencies-are-gitignored-not-committed
description: rom/, vendor/, pcsx2/, and derived data/ are present in this checkout's working tree for local building and gate-running, but are deliberately gitignored, not committed — do not "fix" that by committing them
metadata:
  type: project
---

This repo's large dependencies — the retail disc image (`rom/`), vendored third-party tools and
the PCSX2 fork (`vendor/`), the emulator working tree (`pcsx2/`), and disc-derived fixture
corpora under `data/` — were copied into the working tree from `DCFM_TrackA_PortTooling-PRIVATE`
so this checkout can actually build the product and run its gates. They are gitignored on
purpose, not an oversight: this repo is the eventual PUBLIC dev distro (`README.md` /
`CONTRIBUTING.md` already frame it as MIT-licensed and PR-welcoming), and `CONTRIBUTING.md`'s
"Never commit game data" section is a hard rule, not a preference. `git status` will show these
directories as present-but-untracked; that is the correct, intended state.

**Why this matters:** `dta doctor` reports `rom`, `vendor`, `pcsx2-dcfm-parity`, `ps2-bios`, etc.
as `ok`, which could read as "these are part of the repo" to an agent that has not checked
`.gitignore`. They are not. Before running `git add -A` or any broad staging command, verify
`git status --porcelain` does not show these as about to be added — if it does, `.gitignore` was
edited or bypassed, which is itself a bug to fix, not a state to commit through.

**How to apply:** when porting a fix from -PRIVATE that touches one of these directories'
*content* (e.g. a gate fixture, a vendored tool version), the fix itself is fine to bring over
and commit if it lives in a tracked path (`app/`, `harness/`, `src/`, `docs/`) — but never commit
the dependency tree itself. See [[dta-includeDirs-was-stale]] and
[[dta-conf-net-cascade-ported]] for two porting passes that touched tracked config/code beside
these gitignored trees without ever staging the trees themselves.
