---
name: dcfm-system-mes-holds-every-name
description: meswin\system_1.mes (LanguageCode 1) holds every item/weapon/attachment/technique/place/georama name as ClsMes id-table text in the dialogue glyph codes; the record's message+100 is the id a menu asks; ItemGetMes's item+100 differs for old script weapons 21..80
metadata:
  type: project
---

2026-09-18. The "item name text was never traced" gap in every ported menu closed in one place:
retail's `LoadSystemMessage` @0x00140f70 reads `meswin/system_<LanguageCode>.mes` (1 on the US
build -> `meswin\system_1.mes`; `meswin/systeme.bin` the fallback) and `sysmes.cpp`'s
`InitSystemMes`/`ItemGetMes`/`SetSystemMes` @0x00160650 are its readers (both units are matched
in the decomp at `<projects>\dc1-decomp-tooling\decomp\dc1\src\main`). The catalogue has NO
`meswin\system.mes` and no `system_a_1.mes`: language 1 takes `system_1.mes` for the names and the
`system_ae.bin` fallback for the message-window templates. In the VFS the path is
`<isoName>\DATA.DAT\meswin\system_1.mes`.

Layout: `ClsMes::GetTextLineDataTop`'s id/offset header (u16 count; u16 lastTextOff; count x {id,
wordOff}; text at 2+2*count + 2*wordOff), the same block `StbScript.cpp` and `DcMenuMesCodec.h`
read. A message's span runs to the next entry's offset in FILE order (ids can share a span: four
reach "{FBFE} acquired."); each ends `FF01 FF00`. Glyphs are 0xFD00 + `StbGlyphChar` (now public in
`StbScript.h`); FF02 space. 633 ids: places 10..25, titles 56..66, statuses 70..83, weapons
101..180, attachments 181..231, bag items 232..355, save-space weapons 356..392 ("weapon No.277" is
retail's own), techniques 500+, georama parts/villagers 1000 + 200*village, event titles 2000+.
Slots: 50..55 are `{FAFA}..{FAFF}` (character names, filled from the save); glyph 0x1F follows each
character's first weapon (101, 121, 133, 146, 158, 170) and is shown as `<1F>`.

**The id a name is asked by:** the ComItemInfo record's message + 100 (`GetCommonItemDataSystemMsg`
@0x001d1000, `DcItemNameMessageId`). `ItemGetMes` shortcuts to item + 100 below 257 - measured
against the real tables (`DcSystemMesCheck`): identical for every attachment and bag item and for
Toan's twenty weapons, DIFFERENT for the old script weapon numbers 21..80 (item 43's record is
Xiao's Wooden Slingshot, item 21's is "weapon No.277") and item 256. So `DcSystemMesIdForItem`
asks the record first and uses the shortcut only when no tables are loaded.

**How to apply:** `src/Archives/DcSystemMes.h`; `DcSystemMes()` is loaded in `MainWindow.cpp` right
after the game tables; `DcSystemMesItemName(DcSystemMes(), id)` is what a view should draw, with
"#id" as its own fallback. Headless `sysmes [<id>]` / `itemname <no>`. To see a menu with real
data: `play <cfg>`, `playbegin`, `loadgame <data/saves/darkcloud0_16rc.bin>`, `testpausemenu`,
`playinject 0x2000 128 128 128 128 1` (Right; the Item tab is cursor 0, Weapon 1), `playinject 0x40
...` (Cross), then `weaponmenustatus` / `shot 0 <png>`. Fixture: `data/samples/meswin/` via
`dta fixtures extract`. Next names to wire from the same file: georama parts (`GetAtraMsgNo`).
See [[dta-a-right-frame-can-hide-a-wrong-run]] for judging a run by its log.
