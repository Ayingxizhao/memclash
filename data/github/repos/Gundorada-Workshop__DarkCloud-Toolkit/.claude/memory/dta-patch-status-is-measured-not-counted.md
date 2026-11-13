---
name: dta-patch-status-is-measured-not-counted
description: app/port/pcsx2-fork.mjs rules - a patch is "applied" only if it REVERSES cleanly in a scratch copy; a series goes in all-or-nothing; git's global core.autocrlf reaches `git apply` even outside a repository
metadata:
  type: feedback
---

The PCSX2 patch client (`app/port/pcsx2-fork.mjs`, suite `forkpatch`) is modelled on the decomp
tooling's patch client. Its rules, each from a real failure:

- **Applied = reverses cleanly. Pending = applies cleanly. Anything else = drifted, with git's own
  reason.** Never infer status from "the lines it adds occur in the file".
- **Measure backwards, then forwards.** Reverse from the last patch to the first in a scratch copy
  (two patches may touch neighbouring lines), then re-apply forwards.
- **Verify the whole series in scratch, then write.** The old `apply` wrote patch 1 before finding
  out patch 3 would not go in.
- **Line endings.** A Windows clone with `core.autocrlf=true` checks the vendored tree out CRLF. The
  scratch copy is normalised to LF and each file gets ITS ending back on write. `git apply` runs
  with `-c core.autocrlf=false -c core.eol=lf`: the user's global autocrlf otherwise turns an LF
  scratch copy into CRLF even with no repository around it (`GIT_CEILING_DIRECTORIES` is set too).
  `*.patch text eol=lf` is in `.gitattributes`.
- **An unanchored `pcsx2/` in .gitignore also hides `patches/pcsx2/`.** Already-tracked patches are unaffected, so
  the first NEW ones (000, 004, series.json) silently missed `git add -A`. The rule is `/pcsx2/` now, and
  the suite runs `git check-ignore` over every file of the series. (The decomp repo hit the same bug.)
- `series.json` may mark a patch `required:false` only with a `why`; such a patch reads
  `foreign-base` and is stepped over, and `ensurePlan` must answer `nothing` for it, or every
  incremental build is sent back through `apply`.

**Why:** the series shipped broken for days and every symptom read as "drift"; see
[[dta-pcsx2-src-patch-003-drift]].

**How to apply:** when adding a PCSX2 patch, diff against the pinned tree with the earlier patches
applied, list it in `series.json`, and run `dta pcsx2 fork status` - it must read `pending`, then
`applied` after `dta pcsx2 fork apply`. `dta pcsx2 fork revert` takes the series back out.
