---
name: dcfm-atra-board-retail-model
description: The Atra screen is two panels driven by EditPartsData, and its list ease is an arithmetic shift that a C++ division silently breaks
metadata:
  type: reference
---

The georama Atra screen is not one board. `DrawAtoraSelect @0x0021ae80` draws two panels: a
column of 256x120 **plates** down the left at x=56 on a 130 px pitch, one per part the village
still wants, and the player's own loose chips on the right at (340,120), five to a row of 40 px
cells. That right-hand panel is the *same* personal board the Item tab paints its bag on, in a
different mode, so it reuses `perbrd` and `PersonalBoardDrawWaku`'s four frame strips.

**The table that unlocks it.** Each plate needs `EditPartsData` (the symbol at 0x002540d0,
28,200 bytes, `village*4700 + parts*188`), which the runtime table store did not carry. Adding
`{"EditPartsData", 188}` is the whole enabling step. Inside a row: `+0x00 > 0` marks a live row,
`+0x08` is the 84x84 picture cell on `sozai`, and `+0x14 + i*28` holds six chip records whose
`+0` is the chip id.

**The chip kind is an indirection, and it is not the identity.** A hole's art comes from
`EditElementData[village][chipId + 40]`'s own `+0`, not from the chip id. Village 5 permutes
them (chip 0 wants kind 1, chip 2 wants kind 0, chip 11 wants kind 20) and villages 1 and 3 run
out early with -1. Shortcutting the lookup draws the wrong art on half the game.

**The list ease is a shift, not a division.** Retail does

```
d = (target - listY) >> 1;  n = d & 1;  if (d < 0 && n) n -= 2;  listY += d / 2 + n;
```

Written with a C++ `/ 2` for the first halving, the last step truncates toward zero instead of
flooring, becomes zero, and **the list stalls one pixel short of every plate for good**. The gate
has a one-pixel check for exactly that. Retail is also asymmetric: the same gap going back *up*
the list does shift to zero and does not close, so scrolling to the first plate settles a pixel
out. That is retail's and worth keeping. The right-hand board's ease is a separate thing again,
a **float** in retail; as an int it stops four pixels out and never lines up with its row.

**What cannot be drawn.** The relation arrows between chips, and the banner over a finished
part, are both driven by a link target at the live record's `+0x28 + i*32` and a further word at
`+0x40`. Retail's own `Save()` writes neither, so an imported save cannot carry them and there
is no source to draw from. See [[dcfm-menu-pointer-is-drawmenuobjectvibe]] for the hand this
screen points with, and [[dcfm-georama-part-name-rule]] for the names on the plates.
