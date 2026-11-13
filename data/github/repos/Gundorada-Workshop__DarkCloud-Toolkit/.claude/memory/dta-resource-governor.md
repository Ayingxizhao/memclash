---
name: dta-resource-governor
description: Three governors share one set of thresholds (tooling, DCFM, patched PCSX2); always launch heavy work through them; the machine is shared with other autonomous loops
metadata:
  type: project
---

On 2026-09-17 the user's machine became unusable ("I can barely move the mouse cursor") while this
tooling ran an export, a gate build and the emulator at once. The fix is a governor in three places
that agree on what "busy" means (CPU 70/85/95 %, free memory 6144/3072/1536 MB and 25/12/6 %):

- `app/core/governor.mjs` - samples the whole machine once a second. Lanes, MSBuild nodes, DCFM's
  worker ceiling and child priority all come from it; one heavy process at a time (`admitHeavy`).
  Third signal: the time to start a trivial process, as a multiple of the quietest seen
  (2.5x / 4x / 6x). Brought over from the decomp tooling's `host-budget.mjs`: a spawn/disk storm
  starves the desktop while CPU and memory read low.
- `src/DcGovernor.cpp` - DCFM's own, started by `--headless`; decides once synchronously at start
  (memory needs no history), then every second. IPC verb `governor`.
- `patches/pcsx2/004-governor.patch` (`DcfmGovernor.h`, header-only) - the emulator's own. Reads
  `DCFM_GOVERNOR`, `DCFM_PRIORITY`, `DCFM_GOVERNOR_STATUS`, which `app/port/pcsx2.mjs` sets from
  `emulatorEnv()`. The suite `forkpatch` compares its twelve thresholds with the tooling's.

**Fourth signal, added the same day after a second complaint** ("You are thrashing my Hard Disk and SSD
with 100% usage. This must also be a reasonable limit such as 75-85%"): disk ACTIVE TIME (100 - idle %)
of the disks the work lands on, 75/85/95 %, in all three governors. A full Debug gate build + run had
held two disks at 100% while CPU was under its limit.
- Tooling: `app/core/disk.mjs` runs ONE long-lived `typeperf "\PhysicalDisk(*)\% Idle Time" -si 1`
  (Node has no disk counters); relevant disks = repo, temp, system. `_Total` is dropped (an average
  over eleven idle disks hides a saturated one). typeperf needs ~2 s for its first row, so
  `admitHeavy` waits (bounded) for the first reading before deciding.
- DCFM and the emulator header read `IOCTL_DISK_PERFORMANCE` on `\\.\X:` opened with access 0: no
  PDH, no library, no elevation. DCFM also watches the opened image and the export destination.
- I/O PRIORITY is separate from the priority class and Node cannot set it. `app/native/dta-lowio.cpp`
  (built by `dta governor helper` into build/tools/) sets `ProcessIoPriority` on the dta process;
  children INHERIT it (verified child + grandchild via the helper's `get self`). low normally,
  very_low at high/critical; never raised above what was inherited.
- No reading is NaN / -1 and must never read as idle or as saturated.

**Why:** the machine is SHARED. While this was being built, the decomp project's loop (serve plus
three workers) and an unrelated Unity build were running and free memory sat near 5 GB of 32.
Whole-machine sampling lets separate projects back off from each other with no shared state.

**How to apply:** never start MSBuild, DCFM or PCSX2 other than through the `dta` verbs, and never
stack two heavy jobs by hand. `dta doctor` shows the machine's level. `--no-governor` exists for
timing comparisons only. Do not mount the ISO (`Mount-DiskImage`): DCFM's VFS reads the image file.
