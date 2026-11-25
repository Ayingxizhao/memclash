# Autonomous improvement plan (from 2026-11-22)

The author asked: push performance as far as possible without stopping to ask; consult Codex
at each important design decision and continue once we agree; keep each paid LLM test run
small (about $0.10); report everything tried only when performance is good or when stuck.

## Goal (what "good" means)

| Measure | Data | Now (baseline, one-step) | Target |
|---|---|---|---|
| Whole rule right (Z3 same meaning as label), clear rules | dev set (new, below) | to measure | ≥ 80% |
| Status right (ok / not_in_scope / unclear) | dev set | to measure | ≥ 90% |
| Ambiguity flag: runs disagree ⇒ rule ambiguous | dev set + frozen set | 1/10 ambiguous agree vs 14/20 clear (frozen, A) | report precision / recall |
| Planted clash recall, all expected pairs | pilot | 12/20 | ≥ 18/20 (2 are out of reach by design) |
| Planted false alarms | pilot | 0 | 0 |
| Real known clashes found | 4 survey clashes | 1/4 with perfect labels | raise where defensible; report reasons |
| Cost per rule | all | ~1 call | ≤ 3 calls |

## Rules for myself

1. **No tuning on the test set.** The frozen 30 rules (`frozen_2026-11-22.json`) are the test
   set: already used once for the A/B baseline; used again only for the final evaluation.
   All iteration uses a new **dev set** of other survey rules, labelled by Claude and Codex
   independently; rules they disagree on are marked ambiguous and scored only for the
   ambiguity flag.
2. **Tool-level before prompt-level.** Prefer canonical forms in code, checks, voting and
   solver-side changes. A prompt change is allowed only if it is general (defines a term),
   never a patch for one observed error, and Codex must agree it is general.
3. **Same rule for labels and translations.** Any canonical form applies to both.
4. **Budget.** Each paid test ≤ about $0.10 (sample ≤ 30 rules × 3 runs, off-peak when
   possible). Log the cost of every run.
5. **Consult Codex** on each important decision (new component, scoring change, definition
   change). Record the question and the outcome in the log.
6. **Log everything** in `docs/review/experiment_log.md`: what was tried, why, numbers, keep or
   drop.

## Levers to try (in order)

1. Canonical forms before comparing (e.g. `kind: file` implied by a file pattern; equivalent
   path forms; sorted lists): fairer scoring and more agreement across runs.
2. Voting over runs after canonicalization; runs-disagree flag for ambiguity.
3. Model settings: non-thinking mode (may make strict tool mode enforce the template, and is
   cheaper); test on a small sample.
4. Clash recall: rules dropped as "nothing left" or partly translated (pilot R14, R8);
   shared unknown conditions when two rules name the same condition (ADR 0004); named groups
   of files ("map data") vs a named file.
5. Anything else Codex and I agree on.
