---
name: dta-includeDirs-was-stale
description: dta.config.json's layout.product/layout.archives AND product.includeDirs both still spelled the pre-rename "product" path after the tree became src/ — the second one silently blocked every third-party compile until found
metadata:
  type: project
---

Two separate config fields carried the same stale assumption, fixed in two separate passes.
`dta.config.json`'s `layout.product` / `layout.archives` pointed at `"product"` /
`"product/Archives"` while the actual directory was `src/` — fixed first, unblocking the initial
gate builds. Missed the same bug class in `product.includeDirs`
(`["product", "product/third_party", ...]`), which meant EVERY third-party compile (ogg, vorbis,
glad) failed with `C1083: Cannot open include file` — silently, because the product build had
never actually been attempted end-to-end in this checkout before that point, so nothing had
surfaced it. Fixed by comparing against `src/DCFM.vcxproj`'s real
`AdditionalIncludeDirectories` (`$(ProjectDir);$(ProjectDir)third_party\glad;$(ProjectDir)third_party`)
and translating to repo-relative `src/...` paths. This was the fix that let `DCFM.exe` build for
the first time ever in this checkout (133 first-party + 27 third-party objects, ~64s,
`build/product/DCFM.exe`, 5.7 MB).

**How to apply:** a config file can have the SAME stale assumption spelled more than once, in
fields that look unrelated at a glance (`layout.*` vs `product.includeDirs`). Finding and fixing
one occurrence is not evidence the class of bug is gone — grep the whole config for the OLD
spelling (`"product"` as a bare path segment, not `"src"`) before declaring a rename complete.
