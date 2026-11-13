---
name: dcfm-allmenu-mes-has-a-language-copy
description: allmenu.mes was recorded as undecodable, but the copy that was measured is the Japanese one -- the a_eng copy next to it reads back with the glyph table the port already had
metadata:
  type: reference
---

Dark Cloud's pause menu addresses one message file by id from a dozen screens: `allmenu.mes`,
which `BattleMenuTexEnter` @0x001f59c0 pulls out of the background pack beside `btlmenu.img` and
hands to `InitMenuMesSet` @0x0022c140.

The disc carries it **twice**:

- `commenu\map\dark.pac\allmenu.mes` — 89,036 bytes, 447 ids. The **Japanese** copy. Its letters
  are font-page indices below 0x0200, which no glyph table resolves, so almost nothing in it
  falls inside the 0xFD00 band.
- `commenu\a_eng\map\dark.pac\allmenu.mes` — 77,488 bytes, 495 ids. Same container, same layout,
  and its letters are ordinary **0xFD00+g** codes: the ones `StbScript.cpp`'s `GlyphChar` already
  decoded for .stb dialogue, `system_1.mes` and `manual.bin`.

An earlier pass measured the first one, found 43 glyph-band words in the whole file, and recorded
the text as undecodable — which is a true statement about that file and a wrong conclusion about
the format. The language copy reads back as English with no new machinery. Every `commenu`
asset this port reads already comes from `a_eng`; this file was the one that did not.

The word grammar around the letters is `ClsMes::MakeMesWinTbl` @0x0014f8d0: 0xFF00/0xFF01 end a
line, 0xFF02 is a space, 0xFF03 ends the message, 0xFD00..0xFD9C is a glyph (the letters, or a
gaiji button icon for the codes the table does not resolve), 0xF7xx justifies, 0xF8xx sets the
space width, **0xF9xx advances the pen by its low byte** (what the English file puts between
words, usually 0xF908), 0xFAFA..0xFAFF are the six character-name slots and 0xFBF3..0xFBFA /
0xFBFF are value slots. `InitMenuMesSet` picks the font cell from `GetMenuLangFlag`: 16x22 for
Japanese, **11x20** for every other language — which is the cell DCFM already drew menu text with.

Which id a screen asks for is usually a small table, and one of those was already half-read in
this repo: the pause menu tab bar's help line is the **tenth word of the `MenuIcon` record**
(@0x002945a0, 40-byte stride, field +36), which `DcMenuBattlePause.cpp` had transcribed as
"a message id, not used here". Its fourteen values are 11, 12, 13, 14, 16, 24, 26, 15, 17, 18,
22, 23, 19, 21, the same in every language row, and they read back as "Item / Use current item
or Set active items.", "Weapon / Change and customize weapons." and so on. The id follows the
ICON, not the slot, so MOVE's line changes when the player is indoors.

Rule of thumb this leaves: **before concluding a .mes is undecodable, check whether an `a_eng`
copy of it exists.** And its companion: a table field already dismissed as unused is worth
re-reading once the file it points into decodes. Ported in `src/Archives/DcMenuHelpWin.h`; read
off the disc with `dta headless send 'helpmes <id>'`.
Related: [[dcfm-manual-bin-is-clsmes-with-lines]].
