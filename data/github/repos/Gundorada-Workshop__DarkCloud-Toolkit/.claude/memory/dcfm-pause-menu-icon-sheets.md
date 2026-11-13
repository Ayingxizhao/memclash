---
name: dcfm-pause-menu-icon-sheets
description: Where the pause menu's item and weapon icons really live on the disc (commenu\itemicon.img 256x768 cells numbered 65..256, commenu\wepicon.img 256x640), why btlmenu.img's itemicon is only half a sheet, and that wepicon is asked for with block -1.
metadata:
  type: project
---

`BtlMenuTexBlockEnter` @0x001f58a0 asks the texture manager for eight names; `itemicon` from the
block it just read out of `btlmenu.img` (dungeon/dunmenu5.pak) but `wepicon` and `vilname` with
block **-1**, i.e. already resident, loaded elsewhere. On the disc:

- `commenu\itemicon.img` → sheet `itemicon`, 256x768: 24 rows of eight 32 px cells, the cell
  numbers painted on the art run 65..256. `DcItemIconCell` (RetCTex @0x0022dd90: col =
  (iconIndex&7)*32, row = (iconIndex>>3)*32) addresses this grid.
- `btlmenu.img`'s own `itemicon` is 256x512: the LOWER 16 rows of the same grid (starts at the
  row painted 129), so it is the wrong sheet for a row-from-zero rule.
- `commenu\wepicon.img` → sheet `wepicon`, 256x640 (StartBGReadItemMenuWepIcon @0x0024f642's).
- `commenu\a_eng\` carries its own copy of both; DCFM tries the language folder first.

**Why:** the first port loaded both from btlmenu.img, got "wepicon not in btlmenu.img", and would
have drawn item 65's icon from the cell painted 129.

**How to apply:** `EnsureMenuIconSheetsLoaded` in `src/DcEditorWindow.cpp`; `dumpsheet <dir>
<img> <sheet> <png>` shows any sheet; `iso search string <name>` finds which .img carries a name.
See [[dcfm-option-menu-retail-model]] for the Option tab's own sheet.
