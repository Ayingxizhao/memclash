---
name: dcfm-option-menu-retail-model
description: Retail's Option tab decoded whole — 12 rows in two pages, the cursor word (row+1)*10+choice, the label/kind tables, every OptionMenuDraw rectangle, the option2 sheet, the two settings outside SV_CONFIG_SYS (+0x650 short, DngStatus+0x433c).
metadata:
  type: project
---

The pause menu's Option tab (`Archives/DcMenuOption.h/.cpp`, ported 2026-09-18) is retail's own
screen. What the decodes established, so nobody re-derives it:

- **Rows** (InitMenuOption @0x0021e4d0 slot order): 0 SAVE CURSOR POSITION = CSaveData+0x650
  (GetMenuCursor: CMenuCursor's first short), 1 vibration +0x1c, 2 message speed +0x10, 3 stereo
  +0x14, 4 clock +0x08, 5 day/night +0x0c, 6 MAP DISPLAY DENSITY = CDngStatusData+0x433c (values
  0..2 a size, 3 off), 7 hit value 1 +0x28, 8 hit value 2 +0x24, 9 enemy HP gauge +0x2c, 10 names
  +0x20, 11 DOF +0x18 (a two-choice row in the menu; EdDrawDOF's 1/2 level is downstream).
- **Tables** (OptionMenuDraw @0x0021e020): label cell per row @0x00293ec0 =
  {10,8,4,5,2,3,9,11,12,13,6,7}; widget kind @0x00293ef0 = {0,0,1,2,0,1,3,0,0,0,0,0}
  (0 ON/OFF, 1 NORMAL/SPEEDY, 2 STEREO/MONO, 3 the 1/2/3/OFF widget).
- **Sheet**: `commenu\option.pac` → `option.img` → texture `option2` (the language folder has its
  own copy). Label cells 210x24: cell c at (c<7 ? 0 : 210, (c%7)*24). Choice cells 64x24 at
  y = 177 + kind*48 (first choice) / 201 + kind*48 (second), bright art in the x=0 column, dim in
  x=64; the chosen one is bright. Kind 3: three 32x24 cells at x = 128 (bright) / 160 (dim),
  y = 177 + k*24, drawn at x+238+k*36, then OFF from (0 or 64, 199) at x+346. EXIT is
  (452,226,60,29) drawn at (430,290); page arrows (416, 256 + a*32, 96, 32) at x = 32 / 520;
  the cursor cell is (178,248,16,16).
- **Layout**: row i at x = pageX + (i<6 ? 0 : 560), y = 90 + (i%6)*30; the label at (x, y+1),
  choices at x+238 / x+310. pageX eases a quarter per frame toward 136 (first page) or -424.
- **Cursor grammar** (MenuOptionKey @0x0021e9b0, word c = (row+1)*10 + choice, init 10): any
  shoulder button ±60 (the other page); Down at row 5/11 and Up at row 0/6 go to the EXIT button
  (f_04 = 1) else ±10; Right: c+1, on row 6 choice 4 → c = 10, on other rows choice 2 → choice 0
  and the other page (±60, ≥12 wraps); Left: choice−1, at choice 0 row 0 → c = 73, else the
  other page at choice 1; then `if row != 6 && choice >= 2: c -= 1` (once). Cross sets
  values[row] = choice. On EXIT: Down → c = 10 or **60** (retail's own, lands on row 5 from the
  second page), Up → 60 / 120, Cross → close (commit), Square → InitOptionFlag (all 0),
  Triangle → PrevOptionSetFunc (entry values). Circle anywhere closes. Closing always commits
  (ExitMenuOption @0x0021e780). Help text: CommonMenuMes2 MakeMesWin(349+row / 369 on EXIT).
- **Cursor frame target**: x = choice*71 + 348 (row 6: choice*36 + 348, choice 3: 456), y =
  (row%6)*30 + 90; EXIT: (402, 294); eased a quarter per frame; the waku starts 20 px right of
  it and is 60 / 36 / 64 wide.

**Why:** the old tab was a flat 10-row list with generic labels and a DOF "range 2" that retail's
menu does not have; the two extra rows were missing from `DcSaveData` (now `menuCursorSave`,
`dng.mapDensity`, native save v7).

**How to apply:** change the screen only against these decodes; the gate
`harness/DcMenuOptionCheck.cpp` pins each rule with a mutant control. See
[[dcfm-pause-menu-icon-sheets]] for the sibling sheets.
