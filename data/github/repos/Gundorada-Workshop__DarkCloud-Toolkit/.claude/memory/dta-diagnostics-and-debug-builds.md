---
name: dta-diagnostics-and-debug-builds
description: Debug is the default configuration everywhere; every headless run gets its own log under build/logs/dcfm, reviewed automatically; INFO/WARN/ERR/EXC are written by every build; `dta log` filters by level
metadata:
  type: project
---

Since 2026-09-17 (user instruction: "Always use debug builds with these features"):

- `product.configuration` is `Debug` (`/Od /MDd /Z7 /RTC1`, `_DEBUG`, `DCFM_VERBOSE_LOG`) for the
  product, every gate, `build.bat` and `build.sh`; `--release` is explicit. `/Z7`, not `/Zi`: a
  shared pdb fails parallel compiles with C1041. The `.pdb` is staged beside `build/product/DCFM.exe`.
- `src/DcLog` writes INFO/WARN/ERR/EXC in every build; only DBG/VRB/TRC are compile-gated. Level
  tags are 4 characters at column 15.
- `src/DcCrash` installs SEH, first-chance C++ (vectored), terminate, abort, purecall, invalid
  parameter and CRT report handlers - quiet (no dialogs) when headless - and writes `<log>.dmp`.
  A throw compiled into ANOTHER module is INFO, not EXC (Windows' shell throws
  `wil::ResultException` among its own DLLs constantly), EXCEPT the C++ runtime's DLLs
  (msvcp / vcruntime / ucrtbase), whose throws (`vector::at`, `stoi`) are made on the application's
  behalf and stay EXC. Rethrows are not counted.
- `app/port/headless.mjs` gives every launch `--log=build/logs/dcfm/<stamp>-<exe>-<port>.log`, lets
  the app exit by itself (8 s grace) so the log closes with `=== END LOG ===`, and prints a review.
  `dta log [file] --level= --min= --grep= --strict --json --list`.
- IPC verbs: `diag` (build kind, handlers, counts, log and dump paths) and `governor`.
- `dta doctor` has `governor` and `product.configuration` rows.

**How to apply:** after any headless run read the review; `dta log --strict` exits 1 on any ERR or
EXC. Fix what it shows before moving on. The first real run found two defects this way: a status
line reporting "0 MB free" before its first sample, and foreign exceptions logged as ours.
