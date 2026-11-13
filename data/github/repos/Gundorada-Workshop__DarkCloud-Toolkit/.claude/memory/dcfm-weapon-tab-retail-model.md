---
name: dcfm-weapon-tab-retail-model
description: The pause menu's Weapon tab as retail draws it -- WeaponMenuDraw/BtlWeaponDraw's layout (portrait row out of btlmenu.img's charaface, the "?" face and arrows out of btstatus2, the carousel at WeaponPos + i*214 with wepstatus's NOTHING frame and kage*.img shadows, names at y 114), WeaponSelectKey's state-0 keys, the action dialog rows and the attribute board, plus what was NOT found.
metadata:
  type: project
---

Decoded 2026-09-18 for batch H (`src/Archives/DcMenuWeapon.h` carries every rectangle):

- WepMenu @0x01d9ea70: +2 state (0 carousel, 1 dialog, 2 status board, 5.. attach boards), +4 slot,
  +5 character, +12 sub-state, +32 tag. WeaponPos @0x002a2d6c eases /4 toward 232 - slot*214; a
  panel is drawn while -96 <= x < 631. SysChara @0x00292b50 (12-byte rows: id, eased x) targets
  (i - character)*110 + 270; the portrait cell is charaface (id<3 ? 0 : 106, (id%3)*106, 106,106)
  drawn 100 px at y 14 -- charaface is 256x320, two columns of three faces with the option icons
  down the right edge (236/216, 80+row*20, 20x21). A character past BtlMenuStatusPt+5 shows
  btstatus2's "?" (140,140). Arrows btstatus2 (96,104,10,24) at 258-2*(ct%10) and mirrored at
  372+2*(ct%10), 30 ticks of 50 (ct$4025).
- State 0 draws no status board: BtlWeaponDraw skips the tag board for state 0 and draws only
  WeaponOptionStatusDraw(x+80,142); the names are WeaponNameDraw(114): slots cursor-1..cursor+1 at
  WeaponPos+22+slot*214, centred by GetWeaponNamePutX(x+66, width) = x+66-width/2. Empty slot:
  DrawMenuNothing(x-4,130,180,150,"wepstatus") = 18 px corners at (212,345)/(230,345)/(212,363)/
  (230,363), 4 px strips, "NOTHING" (250,466,134,34). Equipped: kage<name> (0,0,100,100) at
  (x+36,150,100,99). Bottom: RepairAndLevelUpDraw(78,324) = items {177,178} with GetNowItemNum
  (bag slots holding the id count one each, active slots add their count).
- WeaponSelectKey state 0: Left/Right clamp 0..9 (no wrap), R1|R2 (0x0a) next character, L1|L2
  (0x05) previous, Up/Down move the tag, Cross -> state 1, Circle -> BattleMenuFlag 18.
- Dialog (DrawWeaponSelectDialog 112,112): wepstatus label cells (288,y,96,32) 26 px apart:
  EQUIP 104, CUSTOMIZE 136, ATTRIBUTE 328, REPAIR 168, UPGRADE 200. Board (state 2):
  DrawWeaponTagBoard(394,100) = wepstatus (0,0,212,170); DrawWeaponStatusTag: WHp now =
  fptosi(+16 float), max = +12; Abs = +20 over GetWeaponMaxExp; digits (212,500,12,13), "/" at 332.
- WEAPON_HAVE: +4 At, +6 Ed, +10 Mp, +12 WHp max, +16 WHp now (float), +20 Abs, +22 tier, +238 flags.
- Where the sheets actually are (dumpsheet, this session): charaface, btstatus2 and wepstatus are
  all sheets of btlmenu.img in commenu/a_eng/dungeon/dunmenu5.pak (dunmenu4.pak carries a second
  copy), NOT of wepchara.img. The six shadows are each the only sheet of their own
  commenu/kage<name>.img, and the sixth is kageozu, not kageuzo (iso search string kage).
- SysCur, decoded later: WeaponMenuDraw copies a per-state target table (@4085, 0x00293370,
  twelve {s16 x, s16 y}) onto its stack every frame and eases the pointer a quarter of the gap
  toward it; InitWeaponSelect+368 starts it at (235,165). The three ported states want
  (192,165), (80, 112 + row*26) and (366, 134 + row*24). The sprite itself is
  [[dcfm-menu-pointer-is-drawmenuobjectvibe]], and the cell here is always the idle finger.
  Retail's dialog is a SEVEN-row space (rows 4..6 optional, packed, gated on
  NowWeaponStatusValue), not the five this port draws.
- NOT found: Sp's field; StayTex's
  home (NumberSprite digits); frame_image's sheet. The "+8 per digit" shift in WeaponNameDraw keys
  off +2, whose meaning was not read.

**Why:** the Weapon tab was a text list; this makes it the game's own screen.

**How to apply:** `DcGlView::DrawWeaponMenu` draws it from `DcWeaponTabView`;
`EnsureWeaponTabSheetsLoaded` in `src/DcEditorWindow.cpp` loads the sheets; `weaponmenustatus`
reports state/action/weaponPos. See [[dcfm-item-tab-retail-model]] and [[dcfm-pause-menu-icon-sheets]].
