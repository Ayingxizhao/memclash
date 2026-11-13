---
name: dta-a-right-frame-can-hide-a-wrong-run
description: frame-check also judges the product's log and its `guesses`; scene composers take SameStemOnly companions and wantPng=false; the material->sheet rule is one header; wall-clock is too noisy to gate
metadata:
  type: project
---

2026-09-17. Two defects sat behind frames that were pixel-correct, so no gate saw them:

- **Borrowed rigs.** No script declares a dungeon piece, so `MdsGatherExportAssets` guessed
  companions by filename. In an `.mpd` the only candidates are somebody else's: every piece of
  `d01main_a` got an item's `.mot` and the area's `texanime.cfg` ("only candidate in the container,
  name unrelated") - 102 WARNs per open. The rule is now `src/Archives/MdsCompanionGuess.h`
  (tiers 100/90/70/40/10; policies `Any` / `SameStemOnly` / `None`), passed to the gather as its
  last argument; a refused guess is never READ. `DcSceneCompose`'s `PrefabCache::Get` asks for
  `SameStemOnly`. `GetProp` (a `.chr`, a character's own container) and the cutscene loader (which
  strips `companionsGuessedWeak` after the fact) were left as they were. Gate:
  `MdsCompanionGuessCheck`.
- **516 untrue errors.** Passing `wantPng=false` from the composer (it renders; 226 PNG encodes per
  run were computed and dropped) exposed that the material->sheet lookup - two copies in
  `MdsExportFull.cpp` - asked only `texturesPng`, which a render caller leaves empty on purpose. The
  cutscene path had been logging these all along. One rule now: `src/Archives/MdsTextureKey.h`
  (`MdsSheetKeyForMaterial` over EITHER map, `MdsMaterialSheetIsMissing` +
  `MdsExportAssets::texturesPngSkipped`). Behaviour change on purpose: an unnamed material matches
  nothing (it used to take the first sheet in the container). Gate: `MdsTextureKeyCheck`.

**So `dta headless frame-check` reads the run** (22 assertions): `runLogFaults(cli.review)` - any
ERR/EXC, a minidump, an unclosed log - `sceneGuessFaults(parseGuesses(...))` from the new headless
verb `guesses [clear]`, and a **work budget** per scene-open from `work [reset]`. Pure halves are in
`dta check drive`.

**The work budget is the performance gate.** `src/DcWorkCounters.h` (header-only atomics):
`vfs_read`, `vfs_read_bytes`, `vfs_list`, `mds_gather`, `tim2_decode`, `png_encode`, counted inside
`VfsBrowser::readFile`/`list`, the gather, and `Tim2SavePngToMemory`. The counts reproduce EXACTLY
across runs (Norune 431 reads / 94,853,597 bytes; d01main_a 129 / 42,652,322). `png_encode` must be
0 with or without a baseline; the rest may exceed the blessed counts (kept in
`data/frame-baseline/baseline.json` under `work`) by 5 % + 2. Proven by rebuilding the product with
each defect put back. Gate for the counters: `DcWorkCountersCheck`.
Acted on the same day: `src/Archives/MdsGatherShared.h` - what the gathers of ONE compose share
(archives read, sheets decoded, keyed by archive AND stem), a member of the composer's PrefabCache so
it dies with the compose and needs no invalidation; passed as the gather's last argument, used only
when wantPng is false. And `DcSceneManifest::build` sniffs 4 bytes before reading a root file: it
was reading DMMY (63 MB of padding) whole on every first scene-open. `--trace=2` now logs every
VFS read with its size - that is how to trace a budget's bytes. Blessed counts after: Norune 342
reads / 24,937,207 bytes / 61 decodes; d01main_a 96 / 2,358,002 / 18.

**Why:** a log that cries wolf stops being read, and a render gate only sees what reaches the
framebuffer. `HeadlessClient` already reviews the product's log on close (`cli.review`); any
driving verb can assert on it the same way.

**How to apply:**
- A caller that RENDERS passes `wantPng=false`; a caller that loads pieces nobody inspects one by
  one passes `MdsCompanionGuess::SameStemOnly`.
- To mutate a header-only rule that `MdsModel.h` includes, point the harness at a mutated COPY
  (`harness/common/_mut_header.h`, removed afterwards) - mutating the real header recompiles ~20
  product sources per mutant. See [[dta-a-gate-never-opens-a-window]] for mutating safely.
- Do NOT gate scene-open wall time: the same dungeon opened in 4.4 s, 3.7 s and 4.7 s across three
  runs of a Debug build on this shared machine. Count work instead (encodes, reads, log lines).
- Bash heredocs DO halve backslashes even with a quoted delimiter here; write patch scripts with
  the Write tool.
