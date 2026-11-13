---
name: dcfm-fish-name-is-fishmsg-plus-30
description: A fish's name is system message FishMsg[fish] + 30 (GetFishMsgNo @0x001f2e00, FishMsg @0x00292aa0 = {10..19, 0..7}, so fish 0 Bobo is 40 and fish 10 Tarton is 30); the ranking records are CSaveData + 0x1e0 + rank*16 {fish, size} (GetFishingRank @0x00157f40)
metadata:
  type: project
---

2026-09-18. `GetFishMsgNo(fish)` @0x001f2e00: 0 outside 0..17, else `FishMsg[fish] + 30`, and
`FishMsg` (a LOCAL object at 0x00292aa0, eighteen int8) is `{10,11,..,19, 0,1,..,7}` -- the
message order (Tarton 30 .. Baron Garayan 37, Bobo 40 .. Umadakara 48/49) is not the fish order.
The record screen (FishRecordViewBoard) asks `GetFishingRankData(rank)` = `CSaveData::
GetFishingRank` @0x00157f40: rank 0..63 -> this + 0x1e0 + rank*16, {int32 fish @+0, float size
@+4}, null when size <= 0 or fish < 0; then `GetFishMsgNo(record.fish)`.

**Why:** "30 + fish" is the obvious guess and names fish 0 "Tarton"; the table says "Bobo".

**How to apply:** `DcSystemMesIdForFish`/`DcSystemMesFishName` in `src/Archives/DcSystemMes.h`
(the table is carried: a local symbol, eighteen bytes), `DcFishingRank` in
`src/Archives/DcMenuFishRecord.h` (reads `save.retailImage`); the headless `fishname` verb. The
file the names live in is [[dcfm-system-mes-holds-every-name]].
