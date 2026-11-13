---
name: dcfm-item-tab-retail-model
description: The pause menu's Item tab as retail draws it -- ItemMenuModeDraw's call layout, PersonalBoard's cell grid/tags/frame/scroll bar/badge rectangles out of btlmenu.img's "perbrd", the "status" sheet in wepchara.img, PersonalBoardKeySub's grid grammar, money at CDngStatusData+0x4346 (lhu), and what was NOT found (the pointer sprite).
metadata:
  type: project
---

Decoded 2026-09-18 for batch G (`src/Archives/DcMenuItem.h` carries every rectangle):

- `ItemMenuModeDraw` @0x002059b0: ActiveItemDraw(58,74), DrawPersonalBoard(340,120,mode),
  CommonTrushDraw(562,268), CommonMoneyBoardDraw(355,288,[Dng+0x4346] **lhu**),
  ItemMenuCharaStatusDraw(58,180), DrawBtlMenuLRCursor(326,42,230), MenuHelpWinDraw(54,340),
  ItemNaviCursor, DrawMenuVibeItem at SysCur (the HELD item, not a pointer).
- Sheets: `perbrd` (PerBoardTex, 512x256) sits in btlmenu.img inside
  `commenu\a_eng\dungeon\dunmenu5.pak` (dunmenu4.pak's copy also carries `status`); the
  `status` sheet (CharaStatus: (0,0,224,80) active strip, (0,80,252,134) chara board, (296,0,44,44)
  slot frame) is the first sheet of `commenu\a_eng\wepchara.img`. `dta iso search string <name>`
  gives sectors; `scratchpad/list-commenu.mjs` (openDisc + catalogue rows) maps a sector to its
  DATA.DAT row -- `dta iso catalog` prints nothing without arguments.
- Board: cells perbrd (32,20) 40x40 from (x+19,y+6), clip y+9..y+169, icons at cell+(4,6); tags
  (256,i*48,256,48) at (x,y-46); frame four strips; scroll thumb at x+232; badge (256,144,48,48)
  at (x+210,y-39) with held count (x+244,y-34) over capacity (x+247,y-14) in the red digits
  (144,220,12,12); money digits white (0,220,12,12). DrawMenuNumber draws right-aligned, 12 px
  per digit, ones first.
- `PersonalBoardKeySub` @0x0022ec80: Up/Down by 5 with scrollRow kept within 4 rows (row-3),
  Right past column 4 -> state 2 (the trash), Left from state 2 -> state 1. Capacity =
  `PersonalRetMax(0)` = Dng+0x4360 byte. `GetNowModeMaxNum(0)` counts bag ids >= 132 over
  bagCap+3 slots plus active counts.
- NOT found: the sprite retail paints at SysCur (no `Cursor`/`SysCur` reader among the menu draw
  functions; `re asm callers` does not track data objects). The port marks the cursor cell.

**Why:** the first Item tab was a text list; this makes it the game's own screen.

**How to apply:** `DcGlView::DrawItemMenu` draws it; `EnsureItemTabSheetsLoaded` in
`src/DcEditorWindow.cpp` loads both sheets; `itemmenustatus` reports side/scrollRow/slots/held.
See [[dcfm-pause-menu-icon-sheets]] and [[dcfm-option-menu-retail-model]].
