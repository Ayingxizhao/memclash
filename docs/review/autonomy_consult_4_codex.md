1. **CHANGE — sound as a recall-oriented reporting rule.**

Report the union (`≥1/3`) because it reaches the pilot ceiling: 18/20, with no pilot false alarms. But call `k/3` **run support**, not confidence; three samples are too few for calibrated confidence. Show each run’s verdict, including compatible, missing/bad translation, and conflict type.

The main risk is multiplicity: unioning noisy runs increases the chance that at least one run invents a conflict on real rules. Also, run disagreement demonstrates instability, not necessarily genuine rule ambiguity. Use it as an **ambiguous/unstable candidate flag**, then separately measure its precision/recall against adjudicated ambiguity labels.

Within ~$0.10, run the exact final aggregation procedure on one predeclared real-folder subset:

- Select the git/file/task keyword rules before seeing outputs.
- Use **3 runs on the same subset**, not one run on three subsets.
- Hand-check every pair flagged in any run independently, then adjudicate disagreements.
- Report union precision, false flagged pairs / all eligible real-real pairs, per-run false alarms, and whether the folder had any false alarm.
- Preserve the full eligible-pair denominator; otherwise “zero false alarms” is hard to interpret.

One folder is a precision probe, not evidence of general real-folder precision.

2. **CHANGE — the sequence is right, with preregistration added.**

Recommended order:

1. Freeze v2.1 code, prompt/model settings, keyword selection, pair universe, union rule, verdict mapping, and ambiguity metrics.
2. Run the real-folder precision probe: one fixed subset × 3 runs; both reviewers independently check every union-flagged pair.
3. Make only a stop/go decision. If false alarms appear, diagnose on development data—do not proceed and reinterpret the aggregation afterward.
4. Run the frozen 30 exactly once as one evaluation batch: v2.1 two-step, 3 runs.
5. Score unchanged outputs against both original v2 labels and the pre-existing retrospective v2.1 conversion. Report per-run, `k/3`, union, majority, ambiguity-candidate performance, bad outputs, and cost.
6. Stop and report; no post-test fixes or reruns.

This should fit the budget based on E6’s ~$0.07 for three pilot runs. **Overall: proceed after these terminology and preregistration changes.**