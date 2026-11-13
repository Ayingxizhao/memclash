---
name: dcfm-world-map-name-is-menumovekey-table-plus-10
description: The world map's destination name is system message (MenuMoveKey's own 16-entry table at 0x00293710)[cursor slot] + 10, NOT 10 + slot; ids 10..25 of system_1.mes are the sixteen places; the cursor-position table (MapNoTransFunc index -> x,y) is at 0x00293750
metadata:
  type: project
---

2026-09-18. Retail names the world map's cursor slot through `MenuMoveKey` @0x00208490: it copies
sixteen int32 from 0x00293710 (file offset 0x193810 of SCUS_971.11, no symbol of its own),
indexes them by `MenuMove+4` -- the cursor slot `WorldMapMoveKey` stores after `GetNearWorldPos`
-- and sets the screen's message to the entry + 10. The table is
`{0,1,2,3,4,5,6,7,13,8,9,10,11,14,12,15}`. Ids 10..25 of `meswin\system_1.mes` are the sixteen
destinations (Norune Village .. Demon Shaft), and only the table's order puts a dungeon name on
every dungeon slot: slot 12 (mapNo 204, the Moon Sea) is 21 "Moon Sea"; the identity guess
`10 + slot` says 22 "Gallery of Time". An earlier reading of this session assumed the identity
from `MapNoTransFunc` (0x0020ad80), which is a DIFFERENT index: mapNo -> place index for the
cursor's screen position, through three tables (0x002938f0 int16 x5 for mapNo < 10, 0x00293900
int8 for 11..199, 0x002a20d0 int8 x6 for 200+), read into the x,y table at 0x00293750 (sixteen
int16 pairs; entries 1, 3 and 15 are 0,0) -- that one is the marker/cursor position, not the name.

**Why:** two tables index the same sixteen slots differently; using the position index for the
name misnames eight slots, and nothing on screen looks wrong until a dungeon slot reads as a town.

**How to apply:** `DcWorldMapPlaceNameId(slot)` in `src/Archives/DcMenuWorldMap.h` is the rule;
`DcGlView::DrawWorldMap` and the headless `testworldmap` reply use it; gated by
`DcMenuWorldMapCheck` (mutant control on `10 + slot`) and `DcSystemMesCheck` (the names). The
0x00293750 positions are the next thing to draw (a cursor marker) -- see
[[dcfm-system-mes-holds-every-name]] for the file the names live in. The chapter pac's
`allmenu.mes` ids 10..25 are help text in an undecoded glyph band, not names.
