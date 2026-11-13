---
name: dta-headless-fullscreen-stays-parked
description: Anything that sizes a window from MonitorFromWindow lands on a real monitor when headless; F11 did, and how it is tested now
metadata:
  type: project
---

Headless mode parks every window off the virtual desktop. `MonitorFromWindow(hwnd, MONITOR_DEFAULTTONEAREST)`
for a parked window returns a REAL monitor, so any code that moves a window to "its monitor" puts it on
the desktop. F11 fullscreen (`ToggleFullscreen`, `src/DcEditorWindow.cpp`) did exactly that: measured
2026-09-17, origin 6016,64 -> 3840,0, `offscreen=NO`. Fixed: when `DcHeadlessParkOrigin()` returns true the
fullscreen rect keeps the parked origin with the monitor's size, and both entering and leaving use
`SWP_NOACTIVATE` (leaving also turns `SW_SHOWNORMAL` into `SW_SHOWNOACTIVATE`, because
`SetWindowPlacement` activates what it restores).

**Why:** Phase 3's fullscreen had only ever been code-reviewed. Verifying it at runtime found the defect.

**How to apply:** before adding any window move/resize/maximize/centre-on-monitor code, ask what it does to
a parked window, and check `status` afterwards (`offscreen=yes`, `foreground=no`, and now `fullscreen=`).
`dta headless selftest` asserts the F11 round trip and Escape; the verdict is the pure function
`fullscreenFaults` in `app/port/headless.mjs` (six mutants in `dta check drive`). The IPC verb
`key <vk> [viewport]` sends WM_KEYDOWN/UP to a viewport's window procedure - it cannot reach code that
polls `GetAsyncKeyState`. Related: [[dta-diagnostics-and-debug-builds]], [[dta-gate-authoring-lessons]].
