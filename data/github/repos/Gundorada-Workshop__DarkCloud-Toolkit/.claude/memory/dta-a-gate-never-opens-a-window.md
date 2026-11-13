---
name: dta-a-gate-never-opens-a-window
description: Debug-CRT assertions open a modal dialog; every gate is linked with harness/common/gate_prelude.cpp so a failure is stderr + an exit code; how to mutate safely
metadata:
  type: feedback
---

Gates are Debug builds, and the Debug CRT reports a failed assertion - including the STL's own
"vector subscript out of range" - with a MODAL "Debug Assertion Failed!" dialog that waits for a
click. On 2026-09-17 a mutant shortened a list, a new harness indexed past the end, and the user got
that dialog on their desktop mid-run. They sent a screenshot of it.

**Why:** a gate that opens a window stops the run, intrudes on the machine's owner, and yields
"counts unavailable" instead of a reason. The user's machine is shared and they are working on it.

**How to apply:**
- `dta gate build` links `harness/common/gate_prelude.cpp` into EVERY gate (an object on the link
  line; a static initializer sets `_CrtSetReportMode(..., _CRTDBG_MODE_FILE)` to stderr,
  `_set_error_mode`, `_set_abort_behavior`, `SetErrorMode`). `dta check port` reads each built
  gate's link map for `dta_gate_prelude_linked` and fails on one without it. Never build a gate by
  hand around `dta gate build`.
- `DcGatePreludeCheck` proves it by tripping the real assertion in a child with a 10 s deadline. The
  child runs on its OWN desktop (`CreateDesktopW` + `STARTUPINFO.lpDesktop`), so even the gate's
  failure - and its mutant - is never visible. Use that pattern for anything that might show UI.
- In a harness, guard every index with the size it assumes (`p.size() == 3 && p[1]...`). A check
  must FAIL on a wrong size, not fall over it. Mutants shorten lists; that is what they are for.
- The product is a different matter: DCFM headless parks its windows off-screen
  ([[dta-headless-fullscreen-stays-parked]]); this fact is about the C++ gate executables.
