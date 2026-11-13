---
name: dta-cache-migration-first-execution
description: the %AppData%\.dcfm cache migration was code-reviewed only; its first execution (DcDataRootMigrateGate, temp trees) found it re-created the DCFM\DCFM nesting bug
metadata:
  type: project
---

Phase 8's `MigrateLegacyRootOnce()` (`src/DcDataRoot.h`) was marked done on a code review. On
2026-09-17 it was executed for the first time — `MigrateLegacyRoots(newRoot, docRoot,
localAppDataRoot)` now takes the legacy roots as parameters so
`harness/DcDataRootMigrateGate.cpp` can run it on trees under %TEMP% — and one of 16 checks
failed: a nested `Documents\DCFM\DCFM` that survived the heal (one of its files lost a clash)
was moved as a FOLDER into the new root. Fix: `MergeTreeInto(src, dst, skipTopLevel)`.

**Why:** code that touches the user's profile looked untestable, so it went unexecuted; making
the roots parameters cost four lines and found a bug at once.

**How to apply:** when a function is "untestable" because it reads a machine-global location,
split it into a parameterised core plus a one-line wrapper and gate the core. Treat any
roadmap item that says "code review, not run" as open. Related: [[dta-whole-disc-export-measured]].
Still unverified: a real product launch on a profile with a real `Documents\DCFM`.
