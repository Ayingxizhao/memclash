---
name: dta-whole-disc-export-measured
description: the whole DATA.DAT "Export contents" completes (~12-13 min, ~16.5k files, 2.3 GB); measured via async headless verbs; four real defects it exposed and how each was found
metadata:
  type: project
---

"Export contents does not complete" (Phase 11) was settled by measurement on 2026-09-17, not by
reading code. `exportstart` / `exportstatus` / `exportcancel` (`DcHeadless.cpp`,
`DcExportContentsStartAsync` in `src/DcExportDialog.cpp`) run the real walk on a worker thread;
the synchronous `exportcontents` cannot do a whole-disc run because `DispatchToUi()` has a
deliberate 30 s ceiling. Whole `DarkCloud\DATA.DAT`, Release, .blend + .png, this machine:
716 s quiet (791-934 s with other work running), 16,503 files, 5,856 skipped, 2 failed (both
zero-length retail `.mds`: `opdat/scene/0507cp.sne`, `0509cp.sne`), 2.3 GB.

Defects found only because the run was taken to completion and its numbers cross-checked:
1. 142 models refused: image name > Blender `ID.name` char[66] -> `FitIdName()` in
   `DcBlendWrite.cpp` (head + `~%08x` FNV-1a of the whole name).
2. 144 failures, one nameable (the log is compiled out of Release) -> `_export_failures.txt`.
3. Progress bar frozen ~190 s then restarted from 0 (the loose-texture pass called
   `setStatus()` only) -> `DcExportPhasePercent()`, three abutting bands. Probably the
   original bug report.
4. Reported file count exceeded files on disk by 316 -> a write ledger found 314 PNG paths
   written twice (same-named members of one `.img`); 307 identical, 7 different pictures that
   were being LOST -> `DcExportWriteLedger::claim()` keys the path on a content hash.

**Why:** every one of these was invisible to scoped exports and to the gates; only a full run
plus "do the numbers add up" exposed them.

**How to apply:** when a count is reported, reconcile it against an independent count (files on
disk) before believing it. A constant 2-file gap is still unexplained — suspects are the
.blend/.glb writers, which the ledger does not see. All pure logic for this lives in
`src/DcExportFailLog.h/.cpp` and is gated by `DcExportFailLogGate` (30 checks); the driver
script used was a scratch Node script over `HeadlessClient` (`app/port/headless.mjs`) — start,
poll `exportstatus` every 10 s, print the result line.

**Superseded detail (2026-09-17):** "the log is compiled out of Release" is no longer true. INFO/WARN/ERR/EXC are written by every build and Debug is the default configuration; see [[dta-diagnostics-and-debug-builds]]. The timings above are Release timings and have not been re-measured in Debug. Run an export only through the governed verbs ([[dta-resource-governor]]): this export plus a gate build plus the emulator is what made the machine unusable.
