---
name: dcfm-manual-bin-is-clsmes-with-lines
description: The MANUAL tab's manual.bin is the same ClsMes container as system_1.mes, but 0xFF00 is a LINE break inside one message -- the shared decoder drops it, so a list of five topics reads as one run-on line.
metadata:
  type: project
---

`commenu\a_eng\manual\mndata.pak\manual.bin` is the ClsMes id/offset container
`Archives/DcSystemMes.h` already byte-verified (`u16 count; u16 lastTextOff; count x {u16 id,
u16 wordOff}`, words at **`2 + 2*count` BYTES + `2*wordOff`** -- the origin is 2+2*count, NOT
4+4*count, and getting that wrong shifts every message a few glyphs and makes the file look
corrupt rather than misread).

The trap is the word **0xFF00**. Across `system_1.mes` it separates one message from the next, so
`DcSystemMesDecodeWords` skips it. **Inside** one manual message it separates LINES, and the
manual keeps whole lists in a single id -- message 100 is the four category names, message
`category*1000 + 1000` is that category's topic names. Decoded with the shared walker they come
out as `"Diorama  Dungeon  Weapon  Saving/other"`, one run-on line with no way to tell which line
the cursor is on. `Archives/DcMenuManual.cpp` therefore carries its own `DcManualDecodeWords`
rather than changing a decoder five other screens depend on.

What the file holds, all confirmed by reading it: 69 ids -- 100 (the four categories),
`cat*1000 + 1000` (the topic names, 5/5/4/3 of them, which independently confirms
`ManualTgaNum`'s own limit table), and `cat*1000 + 1100 + (topic+1)*10 + sub` (the page
captions). Two glyph codes are not in the dialogue font's table: 0x5F reads as "/" in context and
0x00 is a controller-button icon; both are shown as `<NN>`, and
[[dcfm-atra-board-retail-model]]'s sibling note in `Archives/DcMenuManual.h` records the gaiji
cell that would settle 0x5F.

The MANUAL tab itself is only on the pause bar while **item 253** is in the bag
(`GetGameFlagForManualMenu` @0x00233560, which `GetMenuModeMax` subtracts from the tab count). It
is the last slot, so losing it shortens the bar and moves nothing.
