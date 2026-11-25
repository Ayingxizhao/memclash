You are Codex, consulting on a class project as an equal partner. Work read-only (do not edit
or create files; your final message is saved). Do not open `data/gold/`, files named
`labels_*`, or `data/runs/survey_rules/label_set/frozen_2026-11-22.json` (test set). You may
read `data/runs/rules/label_set/score_*.json` (aggregate scores only). Do not call paid APIs.

Read `docs/review/autonomy_plan.md` and `docs/review/experiment_log.md`. The author wants us to
improve performance autonomously and only report back when results are good.

Decide with me (be concrete, under 600 words):
1. Is the plan sound? In particular the dev/test split (new dev set of ~30 other survey rules,
   labelled by both of us independently; disagreements = ambiguous).
2. Lever 1, canonical forms applied identically to labels and translations before comparing:
   which canonicalizations are semantically safe (meaning-preserving under our Z3 model) and
   which are not? Consider: dropping `kind: file` when every path has a file extension;
   `X/` vs `X` + `X/**`; dropping a `when_unmodeled` text difference (already ignored); sorting.
   Note `same_meaning` already compares by Z3, so only things Z3 treats as different matter.
3. Order of levers 2-4 and anything missing that would raise translation accuracy or clash
   recall more.
4. Reply `AGREE` / `CHANGE: ...` per item.
