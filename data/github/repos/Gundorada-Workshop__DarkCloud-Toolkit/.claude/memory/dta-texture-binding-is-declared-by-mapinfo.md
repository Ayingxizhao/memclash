---
name: dta-texture-binding-is-declared-by-mapinfo
description: The engine binds material to texture by NAME among entered IMG archives; a georama area's mapinfo.cfg declares which; declared picks are not guesses
metadata:
  type: project
---

A model names a material by bare stem; 63% of stems exist in several containers. The engine does not
search paths: `CTextureManager::EnterIMGFile` registers each archive member under its 32-byte entry
name and `SearchTextureName` compares the name only, scanning from the newest entry down
(refs/trackb/src/main/texture.cpp). WHICH archives are entered is on the disc: a georama area's
`mapinfo.cfg` has `CD "gedit/s31/"` then `GRD_IMG "e05b01.img",1`, `SKY_IMG 1,"e05s01.img",0` etc.
(the CD directory's archives live in its `img.pak`).

So in `src/Archives/MdsTextureResolve.cpp` a candidate inside an archive the model's own area declares
is bound first and is NOT a guess (`MdsDeclaredForModel`, `MdsDeclaredRank`, `DcCfgDeclaredImgs`).
Still a guess, reported once per (model, stem): the name in two declared archives (the engine keeps
the last entered within a texture BLOCK; block assignment is not decoded), or in no declared archive.

**Why:** the first reviewed headless selftest log had 174 `GUESSED texture` WARNs, every one of them a
correct pick. A log with 174 false warnings is a log nobody reads. After: 2 WARNs, both deliberate.

**How to apply:** a .cfg is ONE TOKEN STREAM, not lines - parse keywords then arguments, only `//`
comments are line-bound. Dungeon cfgs (`dun\*.cfg`, a different 40-entry command table) are NOT covered
yet: their models still resolve by resemblance. Gate: `harness/DcTextureDeclaredCheck.cpp` (synthetic
index via `IsoFileIndex::addArchiveMember`, no disc). See [[dta-diagnostics-and-debug-builds]].
