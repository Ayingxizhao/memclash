---
name: dcfm-georama-part-name-rule
description: A georama part's or villager's name is system message EditElementData[map*100+no].msg + 1000 + map*200, +40 past no 40 and again past 80, Queens part 1 + intFlag1 + 28 (GetAtraMsgNo @0x00218cc0); EditElementData is a named ELF symbol, 600 x 12 bytes, now in the DcGameTables manifest
metadata:
  type: project
---

2026-09-18. `GetAtraMsgNo(map, no)` @0x00218cc0: `no` outside 0..99 -> 999 (the empty entry);
else `GetEditAtraData(map, no)` @0x00158d80 = `EditElementData + map*1200 + no*12` (a named
object, st_size 0x1c20 = 6 maps x 100 x 12; fields {group, msg, count}, msg at +4, -1 when
unused), id = 1000 + map*200 + msg; on map 2 no 1 with `GetGameIntFlag(1) > 0`: + flag + 28
(1430..1432 are the washery's upgrade names); + 40 once no >= 40 (field parts: Fence, Lamp,
Cabin..), + 40 again once no >= 80 (villagers: Llama, Claude, Komacho..). The `no` is the part's
own cfg id (Norune `LAKE_PARTS 12` -> 1012 "Pond"); the `map` is MapNo. Callers: the focus
readout (MapNo, NowFocusParts+240) and the atora-select screen (MenuAtoraSel+12).

**Why:** the msg index is per record, not the part number -- Norune's three small windmills are
parts 9, 10, 11 with messages 9, 10, 11 but the trees at 13 carry count 2 and shift nothing;
without the +40 steps the field parts and villagers would reuse the building names.

**How to apply:** `DcSystemMesIdForGeoramaPart` / `DcSystemMesGeoramaPartName` in
`src/Archives/DcSystemMes.h` (table via `DcGameTableGet("EditElementData")`); the headless
`atraname` verb; gated in DcSystemMesCheck and DcGameTablesCheck. The file the names live in is
[[dcfm-system-mes-holds-every-name]]. Adding a manifest symbol changes kWantedCount, so a
per-disc cache written by the older manifest is rejected and re-extracted -- by design.
