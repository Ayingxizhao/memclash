---
name: dta-menutree-reads-the-menus-back
description: headless `menutree` dumps a menu bar with self-filling popups filled; Play > Testing pickers are filled on WM_INITMENUPOPUP from pure lists; Settings holds configuration, Help only help
metadata:
  type: project
---

Phase 2 closed 2026-09-17.

- **`menutree [main]`** (DcHeadless.cpp) walks a menu bar and sends each popup `WM_INITMENUPOPUP`
  first, exactly as opening it would - so a popup that fills itself on open is listed with what it
  WOULD show. `parseMenuTree` / `menuTreeFaults` (`app/port/headless.mjs`, gated in `dta check
  drive`) judge it: a command id on two items (the second silently does what the first does - the
  defect the original audit found by hand), an empty popup, an unfilled picker, a clickable item
  that sends nothing. The selftest reads both bars every run. This is how a menu change is verified
  without a person: build, `dta headless send ... menutree`, then `menu <id>` to actually pick.
- **Pickers.** `openlivebox` / `playenterinterior` / `mapjumptest` take session state, so each is a
  submenu filled when it opens (boxes are placed and opened while the bar stands still, so
  RebuildMenus time is too early). WHAT each list holds is pure: `src/Archives/DcPlayTestPicks.h`,
  gate `DcPlayTestPicksCheck`. Interiors are valued by INDEX (what the function takes), not by
  MAPJUMP `id`, which repeats per building. An opened box stays listed, greyed.
- **`DcPlayMapNoFolder`** is now the ONE MapNo -> gedit folder rule (0..8 = e01..e09, 11.. = s01..,
  9 and 10 retail's unused gap); DungeonMapJump resolves through it. On SCUS-97111 the villages
  present are e01-e05 and s01, s03, s04, s09, s11-s17 - the gaps are real content facts.
- **Menu layout:** Settings = external programs and components / what is kept on disk / startup
  behaviour. Help = About, check now, GitHub. `ID_HELP_SETUP_COMPONENTS` and
  `ID_HELP_CHECK_UPDATES_ON_STARTUP` kept their names though they moved: an id is not a place.
- In DcEditorWindow.cpp most statics live in an unnamed namespace; a forward declaration placed
  there needs its definition in `namespace { }` too, or it is a different function (C2129).

**Why:** a GUI change nobody can look at is unverified unless something reads the GUI back.

**How to apply:** `dta headless send --exe build/product/DCFM.exe --iso rom/DarkCloud.iso --timeout
180000 ...` - the Debug build needs more than the 30 s default to `playbegin`.
See [[dta-a-gate-never-opens-a-window]].
