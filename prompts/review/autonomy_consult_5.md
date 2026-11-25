You are Codex, consulting as an equal partner. Read-only (no edits; final message saved). Do not
open `data/gold/`, files named `labels_*`, or any `frozen_*` label file. No paid APIs.

Precision probe (preregistered in docs/review/final_prereg.md) is done: 30 QuagKhai003 rules,
3 runs, 435 pairs. Flagged pairs (any run): see `data/runs/rules/probe/flagged.json`; the
translations are in `data/runs/rules/probe/quagkhai_3runs.json` (rules R20, R74, R152).

1. Judge each flagged pair independently: real clash or false alarm, one line why. Use only
   the rule texts (R74 and R152 have the same text, from memory and CLAUDE.md).
2. Diagnosis (I think false alarm): R20 "Commit docs, decisions, planning, and other non-code
   changes on the current branch without checking out a new branch" was split by step 2 into
   `must_do commit` + `never branch_create`; the condition "non-code changes" was attached to
   one clause (run 1) or dropped (run 3), so the `never` applied to all work and clashed with
   "Put code on its own branch" (`must_do branch_create`).
   Proposed general fix, tool-level: in two-step mode, a `when_unmodeled` condition on any
   clause of a requirement applies to every clause of that requirement (same `req` id),
   because a requirement's condition belongs to the whole requirement. Applied in code after
   step 2. It would remove the run-1 false alarm (the never becomes conditional, so at most a
   possible_clash), not the run-3 one (condition dropped entirely).
   Is this sound and general? Any case where clauses of one requirement should NOT share its
   condition? Should the step-1 quote also be checked to contain the condition words?
3. Stop/go: given 2 false flagged pairs (1 distinct) of 435 and per-run false alarms 2, 0, 2,
   do we apply the fix and proceed to the final frozen evaluation, or diagnose more first?
Under 400 words. AGREE / CHANGE per item.
