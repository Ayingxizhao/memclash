# Preregistration: final probe and evaluation (2026-11-22)

Agreed with Codex (`docs/review/autonomy_consult_4_codex.md`). Written before running.

**Frozen method (v2.1).** Two-step translation (`cli.py translate --mode two_step`),
`deepseek-v4-flash` on the official API, thinking mode on, 3 runs, one rule at a time.
Fingerprint of prompts + checker code: `5f0800e56193839e`.

**Aggregation.** Each pair is checked in each run. Reported if any run flags it
(clash / exception / state_conflict / possible_clash), with **run support** k/3 and every
run's verdict. Majority vote and per-run results are reported too. Rules whose runs give
different meanings are **unstable candidates** for "ambiguous".

**1. Precision probe (real folder).** QuagKhai003/assessment, rules matching the keyword
filter of `prep/sample_label_set.py` (78), random 30 (seed 5):
`data/runs/survey_rules/probe_quagkhai_rules.json`. Pair universe: all 435 pairs of these
30 rules. Every union-flagged pair is judged real / false alarm independently by Claude and
Codex, then adjudicated. Report: union precision, false flagged pairs / 435, per-run false
alarms. Stop/go only: if false alarms appear, diagnose on dev data; no reinterpretation.

**2. Final evaluation, once.** The frozen 30 rules, v2.1 two-step, 3 runs, one batch. Score
the unchanged outputs against the original v2 labels and the retrospective v2.1 conversion
(`frozen_v2.1_2026-11-22.json`). Report per-run, vote, k/3, unstable-candidate precision /
recall against the ambiguous labels, bad outputs, cost. No fixes or reruns after it.

## Update before the final evaluation (after consults 5-6)
Method changed after the probe (requirement scopes; step-1 category correction), agreed with
Codex. Fingerprint at the final evaluation: `601c34c4f45a259c`. Everything else above is unchanged.
