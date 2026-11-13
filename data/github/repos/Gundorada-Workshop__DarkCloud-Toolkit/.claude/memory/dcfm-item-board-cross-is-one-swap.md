---
name: dcfm-item-board-cross-is-one-swap
description: Retail's Item board does not "use" or "drop" on Cross -- it runs MenuDataSwap twice against an IHAVEITEM record, which is pick up, put down and exchange in one primitive
metadata:
  type: reference
---

Dark Cloud's personal item board (`ItemMenuMainKey` @0x00202f10, SCUS_971.11) has no separate
pick-up, put-down or exchange arm. Cross over a bag slot runs `MenuDataSwap` twice -- once on the
ids (@0x00204254) and once on the counts (@0x00204274) -- between the bag slot and an `IHAVEITEM`
record that lives inside `PERSONAL_BOARD` itself at +0x30 (`InitPersonalBoardMode` @0x0022e740
clears it there; the global `BtlHaveItemPt` points at the same address, which is why the two names
look interchangeable in the disassembly). The record's fields: +0 where the pending action came
from, +4 what kind of thing is held (0 item, 1 weapon, 2 attachment), +12 the slot it was lifted
from, +16 the id, +18 the count.

Because it is a swap, an empty hand over a full slot lifts, a full hand over an empty slot puts
down, and a full hand over a full slot exchanges -- all from the one code path. An empty slot and
an empty hand are both spelled -1, so a swap between them changes nothing and needs no guard.
Circle while holding is `PersonalBoardItemCancel` @0x0022f550: the same two swaps against +12, the
ORIGINAL slot, so a carried item goes back where it came from rather than to wherever the cursor
has wandered.

Two different "is this a real item" floors coexist and were never reconciled: the hand is empty
below **81** (`PersonalBoardItemCancel`'s epilogue @0x0022f6f8 and `DrawMenuVibeItem` @0x0022e180
both use it), while `GetNowModeMaxNum` counts items at **132**. Each is kept as the literal retail
reads -- see `src/Archives/DcMenuItem.h`.

Ported in `DcItemMenuSwapWithSlot` / `DcItemMenuCancel`; gated by `harness/DcMenuItemCheck.cpp`
and driven on the real disc by `dta headless loop-check`. Related: [[dcfm-manual-bin-is-clsmes-with-lines]].
