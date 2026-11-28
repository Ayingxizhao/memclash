---
name: pipeline-metrics
description: "Rolling per-feature cost/turn/review measurements for the planning pipeline — appended by pipeline-retrospector at feature close, read by pipeline-maintenance to tell whether an ecosystem change actually landed"
metadata: 
  node_type: memory
  type: project
  originSessionId: 62ef5686-d2bf-4021-a940-22275557ab60
  modified: 2026-08-05T16:44:43.260Z
---

One row per finished feature, appended by `pipeline-retrospector` at close (its output #1) from
`python3 ~/.claude/skills/pipeline-maintenance/pipeline-stats.py <project> --sessions <ids>`.

**Why this file exists.** A single run's cost means nothing on its own. `/pipeline-maintenance`
changes rules that govern every future run and previously had no way to tell whether a change helped,
hurt, or did nothing — it argued from recollection. This is the series that makes the improvement
loop empirical. Part of the ecosystem recorded in [[pipeline-ecosystem]]; proposals live in
[[pipeline-improvement-inbox]].

**Record the model each tier ran on.** A tier's cost is not comparable across features that ran it
on different tiers, and the two seed rows below differ in exactly that way.

**Never hand-estimate a row.** The figure an agent can see (`totalTokens` on an Agent tool result)
**excludes cache reads**, which are 60–95% of a run — it understates by ~170×. Run the script.

## Rows

| feature | date | commits | total tokens | cost | implementer tier | turns/commit | reviews/commit | peak ctx |
|---|---|---|---|---|---|---|---|---|
| `06-fbm` | 2026-07-26 | 6 | 122.5M | $113.68 | Sonnet 5 | 93 | 1.0 | 208k |
| `07-sde-bridge` | 2026-07-29 → 08-04 | 8 | 478.8M | $445.24 | Opus 5 | 217 | 1.6 | 385k |
| `var-pi.github.io F1` | 2026-08-09 → 08-10 | 2 | 56.7M | $67.01 | **mixed**: Opus 5 (c01), Sonnet 5 (c02) | 115 | 1.5 | 198k |
| `var-pi.github.io F2` | 2026-08-10 | 3 | 126.7M | $124.09 | **mixed**: Opus 5 (c01, c02), Sonnet 5 (c03) | 144 | 1.0 | 260k |
| `bip-lab F1` | 2026-08-12 → 08-21 | 6 | 153.4M | $166.86 | **mixed**: Opus 5 (c01–c05), Sonnet 5 (c06) | 116 | 0.83 (1.0 per code commit) | 288k |

### Notes on `bip-lab F1`

**Six sessions, and the pending block above is now replaced by this one.** `364cf6bf` ran Phases 1–4
and **dispatched nothing** — the first run under the 2026-08-20 deletion of "the planning session
also dispatches commit 01"; `e37dc3bf` (c01), `bb945cfb` (c02 **and** c03, two bare invocations in
one terminal session), `31111d13` (c04), `b5649952` (c05), `48c19f69` (c06 and the close-out).
Tiers: coordinator, `feature-plan-reviewer`, `feature-readme-writer` and all five
`commit-code-reviewer` passes on Opus 5; implementer **Opus 5 on c01–c05, Sonnet 5 on c06**, which
the plan's §0 named. One operator intervention (the `@info`/architecture-purity question), **no
re-dispatch**, one marginal gate, and one dispatch that returned without committing and was
recovered by resuming its own session. Cost counts this retrospector only to the point it read the
meter (~$0.7); its tail is uncounted.

- **The run straddles two ecosystem versions.** c01–c03 ran the 2026-08-12 files; c04–c06 ran the
  2026-08-20 ones. Anything measured against this row is measured across that line.
- **Phases 1–4 fell to 19%, and the amortization prediction held.** $32.16 for zero commits ($23.20
  coordinator + $8.96 `feature-plan-reviewer`) — nearly the same absolute cost as F2's ~$39, over
  **six** commits instead of three, so the share went 35% → 31% → **19%** across three features.
  Read coordinator share against commit count, still; the fixed cost is ~$32–39 per feature.
- **Dispatch-session coordinator is now near-trivial:** $6.92 / $3.66 / $3.81 / $1.49 / $3.15 across
  the five execution sessions — **$19.03 for six commits, 11% of the run**. `bb945cfb`'s $3.66 for
  two commits in one terminal session is still the cheapest per commit the series has recorded.
- **One commit is a fifth of the feature, and it is turns not diff.** c05, the repository's first
  experiment: **176 turns, 30.8M cache-read, $32.01** with its review, peak context **288k** — the
  highest implementer peak in the series. It fixed an `experiments/` layout seventeen further
  features inherit, stood up a second Julia environment, rendered five figures and ran a
  vector-vs-raster media measurement. The remaining five commits sit in a narrow $14.89–$20.49 band
  on 91–126 turns, so per-commit cost tracked *novelty of the increment's infrastructure*, not diff
  size (c01 is 631 lines at $16.31; c05 is 1,137 at $32.01; c02 is 354 at $14.89).
- **Third tier data point, and unlike F1/F2's it is not clean.** c06 on Sonnet: 103 turns, 9.85M
  cache-read, **$7.88** implementer-only, against Opus c01–c05 at $10.98–$26.44 on 91–176 turns.
  Tokens per turn are flat (95.6k, against c01's 88.8k and c04's 93.2k), so the saving is again unit
  price rather than less work — but c06 is the **README** commit and dispatched
  `feature-readme-writer` (Opus, $7.83) inside it, so the increment cost $15.70 and the job is not
  the same job c01–c05 did. What it does show, against the weak Sonnet-quality signal recorded on
  `var-pi.github.io F2`: the Sonnet implementer found the run's only marginal gate itself, resolved
  it in favour of the condition's intent, said so, and corrected an Opus child on a factual point.
- **`commit-code-reviewer` steady at 15% / $24.56 for five dispatches**, 1.0 rounds per code commit,
  no re-dispatch — the same shape as both `var-pi.github.io` rows.
- **Context is still not binding, but 288k is the top of the series** (29% of the window, nothing
  compacted); main session 266k. Note against the standing deferral of API-doc artifacts in
  [[pipeline-improvement-inbox]], whose reopen condition is a **rising implementer peak**: the peak
  did cross the 198k–260k band — but on the plotting-and-figures commit, not on a commit that had to
  scan implementation files, so the datum is recorded and the item is **not** re-proposed.

### Notes on `var-pi.github.io F2`

**Four sessions:** `fc96650a` ran Phases 1–4 and dispatched **nothing**; `b2bbfd25`, `79207dbe`,
`ec16498f` each ran one commit, the last also the close-out. Tiers: coordinator,
`feature-plan-reviewer` and all three `commit-code-reviewer` passes on Opus 5; implementer Opus 5 on
c01 and c02, **Sonnet 5 on c03**. No operator intervention, no re-dispatch, no marginal gate (the
feature has no stochastic gate at all — every check is an exactness check). Cost counts this
retrospector only to the point it read the meter (~$0.6); its tail is uncounted.

- **This row measures the pre-compaction ecosystem.** `agents/*.md`, `skills/feature-plan`,
  `reviewer-core` and `handoff-core` were all rewritten between 18:03 and 18:09 on close-out day —
  after the last commit landed at 17:59. Anything measured against this row is measured against the
  files as they stood *before* that pass.
- **F1's warning about coordinator share came true, so the two rows are not comparable on it.** F1's
  planning session also dispatched commit 01; F2's did not (it stopped at Phase 4, against
  `feature-plan` Phase 5's *"the planning session runs Phases 1–4 and then this phase for the first
  commit"*, a sentence deleted on 2026-08-20 after a third planner read it the same way). The planning session alone is **68% of coordinator cache-read** (24.0M of 35.2M, ~$29);
  with `feature-plan-reviewer`'s $9.77 inside it, **Phases 1–4 cost ~$39, 31% of the feature, for
  zero commits**. Until that boundary is unambiguous, compare *dispatch-session* coordinator cost
  (~$14 for three commits, 11%), never the aggregate.
- **Second clean tier comparison, and it replicates F1's.** c03 on Sonnet: 142 turns, 20.0M
  cache-read, **$10.40** implementer-only. c01 on Opus: 136 turns, 19.4M cache-read, **$19.47**. 4%
  *more* tokens for **47% less money** — again essentially all unit price, not less work. F1 measured
  9% fewer tokens for 57% less.
- **One quality signal against the tier, weak but recorded.** The feature's only two must-fix findings
  were both on c03 (Sonnet), both disclosure defects in tracked bytes, and the implementer's first
  repair of one reintroduced the other. Across this project, **all three disclosure incidents have
  landed on a Sonnet dispatch** (2 of 5 dispatches); zero on 3 Opus dispatches. n=3, and
  `commit-code-reviewer` caught every one. Not a reason to reverse §0's discrimination — a reason the
  right control is a mechanical pre-stage check, filed in [[pipeline-improvement-inbox]].
- **Per-commit cost tracks diff weight, not commit count.** c02 is the most expensive ($29.67 with its
  review) and carries the largest diff (2,638 lines, 12 rules, 108 tests) and the feature's only
  contract change. c01 $26.64, c03 $14.72.
- **Context is still not binding but this is the top of the series:** peaks 203k–260k, 20–26% of the
  window, nothing compacted.

### Notes on `var-pi.github.io F1`

Two working sessions, not three: `edf4de5e` ran Phases 1–4 **and** commit 01's dispatch; `b28e3167`
ran commit 02 and the close-out. Tiers: planner/coordinator, `feature-plan-reviewer` and
`commit-code-reviewer` all Opus 5; implementer Opus 5 on commit 01, Sonnet 5 on commit 02. No
operator intervention, no re-dispatch, no marginal gate. Cost includes this retrospector's own
dispatch only up to the point it read the meter (~$3 of the total); its tail is uncounted.

- **The cleanest tier comparison the series has so far.** Two commits of comparable size, same
  project, back to back, differing almost only in model: commit 01 (Opus) 123 turns / 14.11M
  cache-read / **$23.84**; commit 02 (Sonnet) 107 turns / 12.89M cache-read / **$10.21**. Sonnet used
  **9% fewer tokens for 57% less money** — i.e. the saving is essentially all unit price, not less
  work — and quality did not move (1 review round vs 2, no re-dispatch, 15 new tests, 8 mutants
  killed, 63 green). This is direct support for `feature-plan-reviewer`'s "marked on none is the
  finding to hunt" objective.
- **The coordinator share (35%, $22.28) is not a regression** against `07-sde-bridge`'s 20%. It is
  the fixed Phases 1–4 cost — explore, plan-time measurement, three review rounds driven — amortized
  over **two** commits instead of eight. Read coordinator share against commit count, never alone.
- **Per-commit cost is dominated by review rounds and tier, not by feature size.** The
  `commit-code-reviewer` tier ran 3 dispatches for 2 commits (12%, $7.74); the extra round on commit
  01 is most of the gap between the two commits' turn counts.
- **Context is nowhere near binding.** Peaks 171k–198k, 17–20% of the window, on a session that
  carried planning *and* a dispatch. Whatever argues for splitting that session, it is not context.

### Notes on the seed rows

Both were measured retroactively on 2026-08-05, from transcripts, during the maintenance session
that wrote this file — they are the baseline every later change is judged against.

- **Cost is concentrated and super-linear in turns.** Fitting `07-sde-bridge`'s seven execution
  dispatches gives `cache_read ∝ turns^1.56` (R²=0.948, n=7). Two of its eight commits were 60% of
  the implementer tier; the cheapest was 3%. Turn count is the lever; model tier is the smaller,
  linear one.
- **The tier split shifted between the two rows.** `06-fbm` ran the implementer on Sonnet 5 at 35%
  of run cost; `07-sde-bridge` ran it on Opus 5 at 60%. The Opus run used **2.3× more turns per
  commit** — but the feature was also much larger, so this is *not* clean evidence that the tier
  caused it. What it does rule out is the worry that Sonnet needs materially more turns: it did not.
- **The coordinator is not free.** 20% of `07-sde-bridge` ($90) went to the main session — 346 turns
  and 60M cache-read accumulated across a five-day unattended chain. This is the cost that
  one-commit-per-session dispatch is meant to reset.
- **Context is not yet binding, but the old note is stale.** Peaks of 208k → 385k sit at 21–39% of
  the 1M window, so nothing compacted. The retired claim worth not resurrecting is the 2026-07-24
  "context is not the bottleneck" framing measured against a 200k window — the *headroom* is what
  changed, not the conclusion.
