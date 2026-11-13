---
name: dcfm-name-slots-are-two-runs
description: ClsMes's ten name-splice slots are NOT a contiguous run of codes -- 0xFBFE..0xFBFB are slots 0..3 and 0xFBF2..0xFBED are slots 4..9, with the eight value slots sitting in the gap between them
metadata:
  type: reference
---

`MakeMesWinTbl_system` @0x0014eb70 is what fills a `{name}` hole in a menu message: it reads the
low byte of the word and picks a field of the `ClsMes` object, then splices that field's message
in from **system_1.mes** through `GetTextLineDataTop_system`.

The obvious reading — ten slots counting down from 0xFBFE — is wrong. The low bytes are two
separate runs:

- **254, 253, 252, 251** are slots 0..3, at `+0x16e0`, `+0x16e4`, `+0x16e8`, `+0x16ec`.
- **242, 241, 240, 239, 238, 237** are slots 4..9, at `+0x16f0` through `+0x1704`.
- The eight low bytes **between** them (250..243, i.e. 0xFBFA..0xFBF3) are the **value** slots,
  and low byte 255 (0xFBFF) is the window's own number at `+0x1728`. Both return 0 from this
  function, which is how retail tells the two kinds apart.

So a decoder that treats 0xFBFA as "name slot 4" is off by the whole value band and will splice
a name where retail prints a figure. `DcHelpNameSlotIndex` in `src/Archives/DcMenuHelpWin.cpp`
encodes the two runs; `DcMenuHelpWinCheck` has a mutant control for exactly the collapse into
one contiguous run.

The caller that shows the shape is `WeaponMenuSelect__Fv` @0x001fcdf0: its epilogue at +3504
sets `valueFlag = 1`, clears the second value, writes `slot 0 = GetWeaponMsgNo2(attached) + 100`
when that is positive, writes the value, then calls `MakeMesWin`. Which is why message 174,
"Can be built up to {FBFE}.", names a weapon and 590 prints a number.

Related: [[dcfm-allmenu-mes-has-a-language-copy]], [[dcfm-manual-bin-is-clsmes-with-lines]].
