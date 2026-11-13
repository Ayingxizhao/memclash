---
name: dta-frame-check-jitter-is-measured-across-time
description: dta headless frame-check - baselines stay local; back-to-back captures are identical so jitter must be measured with spaced captures and kept in the baseline manifest
metadata:
  type: project
---

`dta headless frame-check [--bless]` (app/port/headless.mjs) is the pixel-regression gate: six fixed
framings, three captures each, 600 ms apart. The baseline is a render of game content, so it lives in
the gitignored `data/frame-baseline/` and is never committed; with no baseline the verb checks only
what needs none and exits BLOCKED (2).

**Why the design is what it is (measured 2026-09-17):** two captures taken back to back were 0.000%
different, while the same build against its own baseline from another run was 1.1-2.7% different, so
the first real run FAILED a build against itself. Water, flames, scrolling textures and PT_GLIGHT's
`rand()` advance between runs but not between consecutive `shot` commands. Spaced captures show the
true jitter (0-3.4%). Allowed = max(0.5%, 3 x max(run jitter, baseline jitter)); the run's capture
closest to the baseline is the one compared. A deliberately wrong baseline frame reads 83.3%.

**How to apply:** re-bless (`--bless`) only on a build you trust, after an intended visual change. There
is no verb to freeze animation time; if one is added, the jitter term can shrink and the gate gets
sharper. It cannot see a regression smaller than a framing's jitter. Verdicts are pure functions
(`frameVerdict`, `frameSanityFaults`, `baselineProblem`, `worstPairwise`) with mutants in
`dta check drive`. Related: [[dta-headless-fullscreen-stays-parked]].
