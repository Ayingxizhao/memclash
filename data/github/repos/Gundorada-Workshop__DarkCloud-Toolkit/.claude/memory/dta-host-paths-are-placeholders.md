---
name: dta-host-paths-are-placeholders
description: the maintainer's real drive roots are written as placeholders in every tracked file, not as E:\DarkCloud_Toolkit etc; what survives the audit's DISCLOSED bucket is synthetic, OS defaults, or the game's own baked build paths
metadata:
  type: project
---

Before the first public push, every tracked file naming the maintainer's own drive layout was
rewritten to a placeholder root. `docs/TOOLING_INDEX.md` §3 carries the table; the roots are
`<extracts>`, `<ghidra>`, `<modkit>`, `<ps2sdk>`, `<oldbuild>`, `<bios>`, `<pcsx2>`,
`<paritysweep>`, `<disc>`, `<steam>`, beside the `<projects>` and `<refdecomp>` that already
existed. Only the ROOT is elided — the sub-structure under it is still the real one, because
that is the part that carries evidence.

106 substitutions across 45 files took `dta distro audit`'s DISCLOSED bucket from 207 mentions
of 168 distinct paths to 102 of 89.

**What is still in that bucket is meant to be, and must not be "cleaned up" reflexively:**

- **Synthetic test literals.** `E:\Elsewhere`, `E:\a\b.iso`, `C:\out\ruby.blend`, `Q:\nowhere`,
  `X:\a\b`, `Z:\old\dup.bin`. A classifier whose whole job is "is this a drive-rooted path"
  cannot be tested without drive-rooted paths; `app/gates/core.mjs` and `app/gates/port.mjs` are
  full of them on purpose.
- **OS defaults.** `C:\Windows`, `C:\Program Files` — real code paths on every Windows machine,
  naming nobody.
- **The game's own build machine.** `Y:\PS2\dc_data\...` is baked into the retail disc by
  Level-5's build, recovered from `DAT+0x17300`. It is RE evidence about Dark Cloud, not about
  this machine. Stripping it would destroy a finding.
- **Regex and escape false positives.** `s:\n`, `e:\n`, `m:\${nodes}` — a letter, a colon and an
  escape, which `app/gates/core.mjs` has a whole comment about getting right.

One product change came out of this rather than a rename: `Ps2AudioPreview.cpp`'s `DcDataRoots`
had two absolute paths to one developer's extract folders as a last-resort fourth tier, so the
shipped `Release\DCFM.exe` carried that machine's layout in its string table and would read those
folders on any machine that had them. The tier is gone; `%DCFM_DATA_ROOT%` (tier 2) does the same
job for anyone.

Related: [[dta-needle-file-check-never-ran]], [[dta-a-push-is-the-export-audit-the-tracked-set]].
