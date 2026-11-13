---
name: dta-needle-file-check-never-ran
description: dta distro audit's forbidden-string check had never actually run in this checkout; the first run of it found the maintainer's real name in two tracked docs, and data/scrub-needles.json is not gitignored
metadata:
  type: project
---

`dta distro audit` prints `NOT MEASURED: ... the forbidden-string check did not run` whenever
`data/scrub-needles.json` is absent, which is the normal state of this checkout — the file is
kept outside every working tree on purpose (`docs/RELEASE_NOTES.md`: moved out entirely rather
than merely gitignored, because a list of what must never be published should not itself be
publishable). The audit is careful never to call that clean.

That warning had been printing, and being read past, for the whole of this checkout's history.
**The first time the check actually ran, it failed**, on five strings in two tracked documents:
`docs/DEV_ROADMAP.md` spelled the needles out verbatim in an entry describing the scrub itself
(including the maintainer's real first and last name), and `docs/TOOLING_INDEX.md` named the
excluded project three times as a folder name. A push would have put a real name on a public
repository. Both are scrubbed now; `TOOLING_INDEX.md` gained a `<refdecomp>` placeholder beside
the `<projects>` one it already had.

Two things made the gap durable, and both are fixed:

1. **There was no way to run the check without copying the file in.** `loadNeedles(file)` took a
   path but `auditSelf`/`cli` never passed one. `dta distro audit --needles <path>` now reads it
   from where it actually lives; a path that is not there is an ERROR, not a fallback, because a
   run that measured nothing must never read as a run that found nothing.
2. **`data/scrub-needles.json` was not gitignored.** `.gitignore` covers seven named `data/`
   SUBDIRECTORIES (`samples/`, `frame-baseline/`, `saves/`, …) and `data/` has seven tracked
   files of its own, so `data/` itself is not ignored — the obvious "just copy it in to run the
   check" move left the needle file one `git add -A` from being staged. Now ignored by name.

**How to apply**: before any push to the public remote, run
`dta distro audit --needles <the file outside the tree>` and read the verdict, not the summary
line. `NOT MEASURED` is not a pass. The 207 remaining DISCLOSED drive-rooted mentions are a
separate, documented decision (`docs/TOOLING_INDEX.md`'s own provenance table) — they expose
drive letters and folder naming, not identity, and they are a human call each time.

Related: [[dta-dependencies-are-gitignored-not-committed]].
