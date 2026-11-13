---
name: dta-queue-manager-loose-iso-fix
description: ChangeQueue::exportNewIso() swept every enabled queued change into DcIsoGrowRebuild's input the moment ANY change grew, but GrowPathFromVPath cannot express a loose ISO9660 file (TITLE.BIN, DUN.BIN) — the whole export aborted, not just the ungrowable item
metadata:
  type: project
---

`src/ChangeQueue.cpp`'s `exportNewIso()`, whenever any enabled change needed
`DcIsoGrowRebuild` (a `DATA.DAT`-catalog item too large for its slot), routed EVERY enabled
change through the rebuild's `sets` input — including unrelated loose ISO9660 files
(`VfsNodeKind::IsoFile`: `TITLE.BIN`, `DUN.BIN`, anything under `MODULES`/`CONF`/...) that
`GrowPathFromVPath()` cannot express as a catalog path (no `DATA.HED`/`HD2` row). The whole
export aborted with `"cannot express ... as a catalog path for the rebuild"` — not just the
oversized item, everything queued alongside it, even edits that would have patched cleanly on
their own.

Fixed by excluding `VfsNodeKind::IsoFile` items from `anyChangeGrows()`'s detection and from the
rebuild's `sets`, then always running the existing direct-patch phase afterward for any such
items (or for everything, if nothing needed the rebuild at all — unchanged prior behavior).
Provably safe because `DcIsoGrowRebuild` never touches the ISO9660 directory tree, only
`DATA.DAT`'s own bytes, `DATA.HED`/`HD2`, and `DMMY.`'s own directory record — a loose file's
LBA/size read from the ORIGINAL disc are still correct against the freshly rebuilt
`destIsoPath`. A loose file that itself needs to grow past its own slot remains unsupported (see
[[dta-conf-net-cascade-ported]]'s note on `DcIsoGrow.cpp` having no root-file cascade at all),
but now fails with `PatchAt`'s own clear, per-item message and is skipped, not fatal to the
batch. Ported into -PRIVATE's `product/ChangeQueue.cpp` too, same day.

**How to apply:** `ChangeQueue::exportNewIso()`'s two phases (rebuild, then direct-patch) can
both run in one export now — `destReady`/`catalogApplied` track whether the rebuild ran and how
many items it already applied, so the "no changes could be applied" failure check downstream
still counts them correctly. Don't reintroduce an unconditional "route everything through the
rebuild" sweep; it silently reverts this fix.
