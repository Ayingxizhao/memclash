---
name: No metrics or test counts in commit messages
description: Commit messages must not include benchmark numbers, binary sizes, or "N/N tests pass" lines. Those belong in the spec, not in git history.
type: feedback
---

Commit messages describe **what changed and why**. They must not include:

- Benchmark numbers ("9.6 ms → 11.2 ms (1.17×)")
- Binary or artefact sizes ("stripped: 48,077,000 → 37,650,040 B")
- Test pass/fail counts ("All 275 tests pass")
- Disk usage figures, memory deltas, throughput numbers

**Why:** Those numbers belong in the spec's close-out section (or in a CHANGELOG
entry, depending on the change). They're easy to look up by re-running the
relevant build/benchmark; embedding them in `git log` clutters the history
without preserving anything that the spec doesn't already preserve better.
Numbers in commit messages also tend to be the things readers gloss over —
the signal-to-noise ratio of a commit message drops fast when half of it is
columns of figures.

**How to apply:**

- For spec-driven work: put measurements in the spec's "## Measurement
  (close-out)" section. Reference the spec from the commit if needed:
  "see specs/0014-...md for size/perf numbers".
- Keep the commit body to: a short prose paragraph on the change, a bullet
  list of files touched and what each contains, and any non-obvious *why*
  that wouldn't be evident from reading the diff.
- A bare statement like "tests pass" is also redundant — the CI gate covers
  that. Reserve the commit body for content the diff can't communicate.
