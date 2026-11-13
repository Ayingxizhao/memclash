---
name: dta-pcsx2-src-patch-003-drift
description: RESOLVED 2026-09-17. Patch 003 never "drifted" - the series was pinned to a commit of the project's private PCSX2 fork (not upstream) and shipped without the base patch 003 is written on top of. Now pinned to real upstream 2ce2cb64 with 000 added; reproduces the fork byte for byte
metadata:
  type: project
---

**Resolved 2026-09-17.** `dta pcsx2 fork ensure` exits 0 and the Headless configuration's pre-build
step no longer fails.

What was actually wrong (none of it was drift):

- The series pinned `e6be7b07d883...`. That is the HEAD of the project's own working fork
  (`dcfm-parity` branch; the repository lives outside this one - the user pointed at it), NOT an
  upstream commit. GitHub answers 422 for it and `git fetch` answers "not our ref". No clone of
  upstream could ever check it out, which is why `vendor/pcsx2-src` sat on upstream master.
- `003-parity-build.patch` is exactly `git diff 0a7bd30 e6be7b0` of that fork. Its CONTEXT lines
  contain code (the `MsgOs2*` PINE opcodes 0x40-0x4E, `OS2WATCH`) that no patch in the series added:
  the four commits before it (`2ce2cb6..0a7bd30`, the headless debugger) were never exported.
- `001-pine-extension.patch` (the Chronicle protocol, PINE 0xC0+) is from a different lineage. It
  applies to upstream alone and conflicts with 000+003 in PINE.cpp. Nothing in this repository
  speaks 0xC0; `app/port/pcsx2.mjs` speaks 0x40-0x51 and 0x60-0x67.
- The old status line's "148/641 added lines present" was closing braces and `break;` matching by
  coincidence. See [[dta-patch-status-is-measured-not-counted]].

The series now: pin `2ce2cb6459439d9e289bf48e42e4dc11bcb1e422` (real upstream, the fork's
merge-base); `000-os2-headless-debugger`, `002-savestate-tlb`, `003-parity-build` and
`004-governor` required; `001` optional, with its reason in `patches/pcsx2/series.json`. Applied to
the pin, the tree is byte-identical to the fork's own working tree in all 12 files except
SaveState.cpp, which differs only by 002.

**Rebuilt the same day.** `dta pcsx2 build all` (vendored cmake + ninja, `vendor/pcsx2-deps` copied
from the old build tree's deps/, latest MSVC, RelWithDebInfo + `/DPCSX2_DEVBUILD /D_DEVEL`) compiled
the patched tree in 15 minutes at `-j 3` with zero errors. `dta pcsx2 build install` replaced
`vendor/pcsx2-dcfm-parity/pcsx2-qt/pcsx2-qt.exe` (old one kept as `.bak` beside it); parity selftest
17/17; the emulog shows `(DcfmGovernor) auto-profile on`. The window title reads "[Devel]", which is
the devbuild define, not CMake's Devel build type (that one crashes at startup against Release
deps). Not yet measured: the emulator throttling itself during a long sweep. See
[[dta-resource-governor]].
