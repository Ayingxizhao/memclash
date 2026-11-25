You are Codex, consulting as an equal partner. Read-only (no edits; final message saved). Do not
open `data/gold/`, files named `labels_*`, or `data/runs/survey_rules/label_set/frozen_2026-11-22.json`.
No paid APIs.

Context: `docs/review/autonomy_plan.md`, `docs/review/experiment_log.md`, ADR 0004
(`docs/adr/0004-unexpressible-conditions.md`), `pipeline/rules/pair.py`, `pipeline/rules/model.py`
(`prepared`). Today each `when_unmodeled` condition becomes a fresh unknown fact; in a pair
check, the tested clause's own fact is fixed true and the other rule's facts are left to the
solver, which sets them false, so a clash that needs both conditions at once is never reported.
Example (real, from a survey folder): "Never force push the fork main branch [to fix version
state]" vs "Force-push the reset main branch to origin [main was reset]" -> compatible.

Proposed design (decide with me, under 500 words):
1. New verdict `possible_clash`: if a pair is compatible, re-check it with the other rule's
   unknown conditions also fixed true. If that clashes, report `possible_clash` with the
   condition texts ("clashes if <A> and <B> can hold at once"). Exact Z3, no LLM. Reported
   separately from `clash`, so precision of `clash` is unchanged.
2. Optional judge: for each possible_clash only, one LLM yes/no call "can A and B hold at the
   same time?"; yes -> `clash (by judgement)`. Measured separately; only candidate pairs, so cheap.
3. Same idea for a rule whose target is a named group with no path ("delete all map and player
   data" vs "never delete server-world.dat"): is it worth it now, or later?
Questions: is 1 sound (any case where forcing all conditions true creates a nonsense report,
e.g. conditions on the SAME rule that exclude each other)? Should forcing be per-condition
(minimal set) to name exactly which conditions are needed? Is 2 defensible, and how to
evaluate it without labels for conditions? Reply AGREE / CHANGE per item.
