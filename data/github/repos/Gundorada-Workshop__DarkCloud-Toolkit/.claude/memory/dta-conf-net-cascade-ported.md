---
name: dta-conf-net-cascade-ported
description: app/iso/replace.mjs's growRootFile only walked root entries + MODULES' own children when cascading a grow; CONF/NET (10 files, two directories deep) went unpatched on a real built image until computeMovers/collectDirs replaced the MODULES-only special case — ported here from -PRIVATE's same-day fix
metadata:
  type: project
---

Ported from `DCFM_TrackA_PortTooling-PRIVATE` (dated 2026-09-13, the same day this was ported —
see that repo's own `dta-a6-main-growth-built-then-crashes.md` for the original discovery).
`growRootFile`'s cascade previously special-cased MODULES as the only non-root directory whose
children could need shifting. CONF/NET (10 network-config files, two directories deep) sits
physically after the growable root files and was invisible to that walk: a cascading grow
shifted their raw bytes correctly (`shiftRight` moves everything in its byte range blindly) but
left their own directory record pointing at the pre-shift LBA — confirmed by direct read-back on
a real, already-built grown image, not hypothesized.

`computeMovers`/`collectDirs` (`app/iso/replace.mjs`) replace the MODULES-only special case with
a generic walk of every ISO9660 directory at any depth. `app/gates/iso.mjs` gained a synthetic
MODULES/CONF/NET gate test (no 1.8 GB rebuild needed) with a mutant proving the old MODULES-only
walk misses the nested files. `dta check iso`: 192/192, 60 mutants caught.

**Also found while investigating the queue manager's `.bin` bug (see
[[dta-queue-manager-loose-iso-fix]]):** the shipped PRODUCT code's own grow engine,
`src/Archives/DcIsoGrow.cpp` (`DcIsoGrowRebuild`), is a SEPARATE implementation from this Node
tool — it only grows entries inside `DATA.DAT`'s own HD2/HED catalog, and has NO equivalent of
this root-file cascade at all. `TITLE.BIN`/`DUN.BIN` growth (as opposed to same-size replacement)
is unsupported in the shipped app, full stop — not merely missing this CONF/NET fix. That is a
separate, larger, not-yet-attempted feature; see `docs/DEV_ROADMAP.md` Phase 11.

**How to apply:** `app/iso/replace.mjs` (the dev tooling's disc-growth engine) and
`src/Archives/DcIsoGrow.cpp` (the shipped product's) are NOT the same code and do not stay in
sync automatically — a fix in one is not evidence the other has it too. Check both when
"disc growth" is the topic.
