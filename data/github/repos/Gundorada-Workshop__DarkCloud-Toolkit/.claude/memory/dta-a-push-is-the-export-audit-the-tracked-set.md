---
name: dta-a-push-is-the-export-audit-the-tracked-set
description: origin IS the public repo, so `dta distro audit` audits git ls-files before a push and `dta distro package` builds the allow-listed end-user zip; what the first audit found, and the one decision left open
metadata:
  type: project
---

Phase 10 (2026-09-17). `git remote -v` here is the public `Gundorada-Workshop/DarkCloud-Toolkit`, and
it already carries `app/`, `harness/`, `patches/`. So `dta distro export` (stage a private tree into
a clone of the public one) has nothing to do in this checkout - it is history, as `distro.mjs`
already says - and **a push is the export**. Two verbs took its place:

- **`dta distro audit`** (`app/distro/audit.mjs`, also run by `dta check distro`): audits
  `git ls-files`. FAILS on a never-publish path, PERSON (a profile path naming an account;
  `Users\x`, `Users\...`, `%USERPROFILE%` are nobody), CHECKOUT (the maintainer's checkout layout).
  DISCLOSED (everything else) is counted and named, never failed, never called clean. `vendor/` and
  `src/third_party/` text is not read - editing upstream's text to pass an audit would falsify it.
- **`dta distro package`** (`app/distro/package.mjs`): the end-user zip. An ALLOW-list - Release
  exe, licences, the docs the README links to - then `packageFaults` re-checks source AND
  destination against `DEV_ONLY` and `NEVER_PUBLISH`. It reads `src/x64/Release/DCFM.exe`, never
  the staged Debug `build/product/DCFM.exe`, and `debugCrtImports` looks inside the file.
  `build({ stage: false })` exists so a package build cannot replace the binary the gates drive.

**What the first audit found:** 1 PERSON + 48 CHECKOUT mentions, in comments, docs, committed
memory, and one generated file - `dta trackb sync` was writing the ABSOLUTE path of the Track B
checkout into the committed `refs/trackb/ledger.json` (fixed: it records the basename; `sourceGit`
identifies the checkout). The first version of the scanner read one spelling of a path and called
the tree nearly clean; forward slashes and doubly-escaped strings hid ten more.

**Why:** `dta check core` fails on a path that is USED. Nothing measured a path merely SPELLED, and
a push publishes both.

**How to apply:** in prose write `<projects>\name`; in a test use a made-up root (`E:\\Elsewhere`).
Run `dta distro audit` before any push. **Decided 2026-09-17:** `refs/trackb` is NOT published -
untracked, gitignored, and a tracked refs/ file now FAILS the audit (see
[[dta-trackb-source-was-unconfigured]]). `vendor/` stays as it is, by the same decision. Related:
[[dta-vendor-toolchain-is-committed-not-gitignored]], [[dta-dependencies-are-gitignored-not-committed]].
