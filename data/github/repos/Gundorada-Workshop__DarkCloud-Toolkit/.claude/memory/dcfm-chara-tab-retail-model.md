---
name: dcfm-chara-tab-retail-model
description: The pause menu's Chara tab is a polar carousel, and the figures beside it come from CDngStatusData, not the combat mirror
metadata:
  type: reference
---

The Chara tab (BattleMenuSelect tab id 3) is not a list. `InitMenuChara @0x001f72e0`,
`BattleMenuCharaKey @0x001f7440` and `DrawCharaSelect @0x001f7e30` make it a ring of six seats,
radius 118, centred on (394,120) in 640x448 space, phase pi so seat 0 sits at the left where the
status figures point. Seat assignment is `ring[i] = (i - activeChar) mod 6`, so the active
character starts at the front.

Three things about it are easy to get wrong, and each is now pinned by a check in
`harness/DcMenuCharaCheck.cpp`:

- **The turn is driven by a HELD direction, not an edge.** `On(0x3000)` is Up-or-Right and
  `On(0xC000)` is Down-or-Left. The port reads `w.pad.cur` for those two and the `down`
  parameter only for Cross and Circle.
- **The turn's first frame is the frame the direction was seen on.** `t` runs 1..21, so a press
  plus twenty idle frames lands it. Counting the press as frame zero makes it 22 frames long and
  breaks every timing check.
- **The figures do not come from `w.userStatus`.** That mirror is only filled while DCFM's own
  combat is running. An imported retail save carries the real pair in CDngStatusData's own
  `maxLife[6]`/`nowLife[6]` at +0x06 and +0x12 -- immediately after `activeChar` (+4) and
  `partyNum` (+5), which `DcSaveRetail.cpp` already reads from the same block at save+0x540C.
  Read the mirror first and let the image win whenever its `maxLife` is above zero; a zero there
  means the block was never filled, and letting it win would mark a live party dead and dim every
  portrait. That is exactly what the first build of this tab did.

The sheets are `commenu\a_eng\charatex.img`: `dgring` is the backdrop ring (drawn additive),
`nonchara`/`nonchara2` are the "?" faces for a character who has not joined. The portraits
themselves are btlmenu.img's `charaface`, which the Weapon tab already uploads --
charatex.img's own copy is the same sheet, so it is not loaded twice. See
[[dcfm-pause-menu-icon-sheets]] and [[dcfm-weapon-tab-retail-model]].
