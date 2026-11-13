---
name: dta-gates-had-never-been-built
description: dta gate build/run --all had never been executed in this checkout; running them plus fixing 3 latent product/->src rename bugs got dta check all to 14/14 for the first time
metadata:
  type: project
---

Before 2026-09-17, no gate had ever been built or run in this checkout (`build/gates/` was empty,
every `result.json` absent). `port`'s own suite could see this directly: "0 of 22 declared gate(s)
have been run", "158 never built". This is distinct from [[dta-trackb-source-was-unconfigured]]
(the `trackb`/`relink`/`drive` fixes) — this note is the `port` suite's own remaining FAILs.

**Fix, part 1 — actually run the pipeline.** `dta gate build --all --parity` (158 harnesses, ~12
min at `harness.parallelBuilds: 2` — the config default of 4 hit `C1060: compiler is out of heap
space` on 8 sources under this machine's ~3GB-free memory pressure; lowered via `local.config.json`,
a legitimate machine override per `config.mjs`'s own design, not a `dta.config.json` change. The
same pressure hits the CMake/MinGW path: Ninja's default parallelism OOMs `cc1plus`; run
`vendor\ninja\windows-x86_64\ninja.exe -C build\Release -j2` against the already-configured tree
instead of `build.bat`, which exposes no `-j`. This machine sits at ~3-4 GB free of 32 GB
throughout a session — plan every parallel compile around that, not around core count.) then
`dta gate run --all`: 158 built (0 unresolved), 120 PASS / 32 BLOCKED (declared-unavailable
fixtures) / 4 SKIPPED (GPU) / 2 NEEDS ARGS, 0 FAIL, 21,497 individual checks. `DcRigCheck` and
`DcToneParity` are two genuine, pre-existing `run:assert` gates (not `run:crash`) — real, disclosed
product findings, not something this pass introduced or should silently "fix".

**Fix, part 2 — 3 real bugs the fresh run then exposed, all instances of the same
product-was-renamed-to-src bug family `dta-includeDirs-was-stale` already found once:**

1. `app/gates/port.mjs`'s "legacy parity index" section (`idx.size > 90`, `legacyLinkList(...)`,
   `parity(...).verdict`) unconditionally asserted against `legacy/build-bats/` — -PRIVATE's own
   parity-comparison scaffold, which `AGENTS.md` §3 explicitly documents as NOT existing in this
   checkout. Every one of those checks could only ever FAIL here, forever, regardless of anything
   this repo's own tooling does right — a permanent false signal, not real breakage. Fixed by
   guarding the section on `fs.existsSync(LEGACY_BATS)` (now exported from `app/port/deps.mjs`)
   with an `s.skip(...)`, matching the same available/unavailable idiom already used for
   `refs/trackb` elsewhere in this codebase (see `app/gates/relink.mjs`'s `ingest-baseline`).
2. Same file, a separate check ("the header this port keeps real logic in exists to be covered")
   hardcoded literal `'product/Archives/DcGamePad.h'` / `'product/Archives/DcCombat.cpp'` test
   strings — this repo's real layout is `src/Archives/...` (`layout.product` = `"src"`). Fixed to
   derive the string via `path.relative(ROOT, path.join(PRODUCT, 'Archives/...'))` instead of a
   literal, so it tracks `dta.config.json`'s `layout.product` automatically.
3. `app/port/gate-report.mjs`'s `isProduct()`/`archives` filters ALSO hardcoded `'product/'` /
   `'product/Archives/'` prefixes — silently made `dta check port`'s own printed
   `(product/Archives: 0/0)` coverage note wrong in EVERY prior run in this checkout (always 0/0,
   never the real count) without ever failing a check, since nothing asserted on that specific
   number. Fixed the same way: derive `PRODUCT_PREFIX`/`ARCHIVES_PREFIX` from the `PRODUCT`/
   `ARCHIVES` constants in `app/core/paths.mjs` rather than hardcoding. Now reads
   `(product/Archives: 84/85)`, the first real measurement.
4. A fourth, adjacent finding in the same file: a `s.mutant(...)` at line ~836 read
   `path.join(ROOT, 'product', 'DcPerfMonitor.cpp')` (also stale) — `s.mutant`'s own
   `try{caught=fn()===false}catch{caught=true}` (`app/core/gates.mjs`) treats ANY thrown exception
   as "mutant caught", so the ENOENT from the wrong path was silently counted as a passing mutant
   for years without ever exercising `semanticSource`'s real logic. Fixed to use `PRODUCT` instead
   of the literal. A general lesson, not just this one site: an `s.mutant` whose callback can throw
   for an unrelated reason (a bad path, a missing fixture) passes vacuously — read what it actually
   asserts, not just whether it's green, when auditing gate quality.

**Result**: `dta check all` → **14/14 suites green**, the first time in this checkout's recorded
history (`docs/DEV_ROADMAP.md`'s own Phase 12 entry: "has never run" / "7/14-green baseline"
before this). Re-grep `app/` for `'product/` and bare `'product'` path-join literals before trusting
a future "18 files" count from Phase 9/10's own notes — this pass swept and found exactly these 3
real bugs plus several correctly-intentional non-bugs (task-name/kind-discriminator strings, and
`app/distro/export.mjs`'s already-reviewed historical `from: 'product'` mapping).

**How to apply**: when `dta check port` (or any suite) reports a FAIL whose note mentions
`legacy/`, `refs/trackb`, or another -PRIVATE-only fixture, check `AGENTS.md`'s own "what is
authoritative" table and doctor's report before assuming it is a real regression — it may be a
documented environmental difference the check itself needs to skip on, not fail on. And whenever
`dta.config.json`'s `layout.product`/`layout.archives` are touched again, re-grep for `'product/`
and bare `'product'` literals the same way — this bug family recurs because the rename was a
config edit, not a codemod, so any hand-written test string written against the OLD layout survives
silently until something re-derives the real count.
