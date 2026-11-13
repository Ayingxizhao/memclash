---
name: dta-trackb-source-was-unconfigured
description: trackb.source was never set in this checkout; setting it to the live dc1-decomp-tooling checkout and syncing turned 3 failing suites fully green
metadata:
  type: project
---

`local.config.json` did not exist in this checkout before 2026-09-17, so `trackb.source` was
unset, `refs/trackb` was empty, and `dta check all` showed `trackb`, `relink`, and `drive` all
FAILing for reasons that were really just "no Track B data" (relink's statefix scanner reading 0
sources, drive's adoption-verify reading 0/63 held, trackb's own join unavailable). None of these
were product bugs.

**Fix**: a real, live Track B checkout already exists on this machine at
`<projects>\dc1-decomp-tooling` — the same project `AGENTS.md` §7 names (as
`DCFM_TrackB_DecompTooling`, a stale path; the project has been re-derived and renamed since,
`dtb` tooling, same `decomp/dc1/{src,pending,include,config/match.txt}` layout this repo's
`dta.config.json` already expects). Added `local.config.json` (gitignored, machine-local) with
`trackb.source` pointing at it, then ran `dta trackb sync` — 137 files from 40 cited units, Track B
at commit `49d5b304`. **`refs/trackb/` is gitignored** — decided by the maintainer on 2026-09-17
("refs/trackb does not get published, it remains in the dev repo as gitignored"). It was tracked
for one day between the sync and the decision, never on origin; `dta distro audit` now FAILS on
any tracked refs/ file. So a fresh clone has an EMPTY `refs/trackb/` until `dta trackb sync` runs
with `trackb.source` configured, and every reader (trackb/relink/drive suites, the Track B screen)
skips or says so rather than fails on the empty copy.

Also found: `data/trackb-adoptions.json`'s 3 "proven, deliberately not implemented" evidence rows
(`CheckWeaponRot__14CDngStatusDataFi`, `GetWeaponHoleNum__Fi`, `MotionProcess__Fv`) had a stale
proof digest — Track B's decompiled text for those 3 had been reformatted (comments/structure)
since -PRIVATE's original recording, while `match.txt` still confirms all three as byte-exact
`match` rows at the same address/size. Read each current body against its recorded `why` reasoning
before re-recording (`dta trackb diff <symbol>`) — all three still held, semantically unchanged —
then refreshed via `dta trackb adopt --evidence <symbol> --why "..."` (same reasoning text).

**Result**: `trackb` 71/72→72/72, `relink` 175/178→186/186, `drive` 149/150→150/150, all FAIL→PASS.
`port`'s FAILs are separate — see [[dta-gates-had-never-been-built]] — and the adoption-holding
count (3/63 before a gate build/run) will only rise once gates are built and run, since most
adoptions name a C++ gate that must show a fresh PASS in `build/gates/<name>/result.json`.

**How to apply**: if `dta doctor` reports `trackb.source unset` and the roadmap's Phase 12 final
verification pass hasn't run, check for a live Track B checkout under `<projects>\` before
assuming Track B data is simply unavailable on this machine — it may just be unconfigured, and
wiring it up is a `local.config.json` edit plus one `dta trackb sync`, not new tooling work. See
[[dta-dependencies-are-gitignored-not-committed]] for the general commit/gitignore split this
repo draws between vendored dependencies and derived facts.
