You are the co-investigator on a class project (presented Dec 1). Work read-only (your final
message is saved). Do not open `data/gold/`, `labels_*`, `frozen_*`. No paid API calls.

Read `docs/review/experiment_log.md` section N (the end of the file), `docs/review/natural_consult_1_codex.md`,
`data/runs/natural/full_gold.json`, `data/runs/natural/score.json`.

The paid budget is spent (slightly over). Only free work remains: Codex and Claude time, Z3 on
saved translations, code.

The author wants a promising AND honest story for Dec 1. Our current reading:
1. Real clashes in memory folders exist (22 clear, 19 ambiguous in 5 folders / 1287 rules found
   by two LLM screens), but most (17/22) are about tool or command choice, values, or layout,
   outside our git/file/task vocabulary. The formal vocabulary covers ~1 in 4 clear clashes.
2. Even careful readers disagree: 27/43 agreement; 19/43 pairs ambiguous. "Is this a clash?"
   is often a judgement call (refinement vs contradiction, preference vs allowance).
3. Z3 on independent translations is precise but misses clashes because translation drops
   permissions, scope, and cross-rule links; a whole-folder LLM pass finds more, but at full
   size it misses some (R60/R213) and two LLMs agree on only 4 of 15 flags.

Questions:
1. Is this a presentable research story? Give a title, a 3-sentence abstract, and the 3-4
   findings with the exact numbers, plus the honest limits (judge = labeller overlap,
   union-of-screens recall, small n, Claude not blind).
2. Proposed design lesson / system: several cheap LLM screens (union) -> pairwise check ->
   Z3 only where the vocabulary fits, as an explainable witness -> ambiguous pairs to the
   human with both readings. Do our numbers support each arrow? Which arrow is unsupported?
3. What free work in the next few hours would most strengthen the story? (e.g. a taxonomy of
   the 41 clash/ambiguous pairs by type; checking whether union of the two LLM screens beats
   either; a Z3 vocabulary-coverage table; a pairwise re-check by a fresh Codex of a sample of
   non-flagged pairs to estimate missed clashes.) Rank at most 3.

Under 700 words. Plain language. End with AGREE / CHANGE and the exact next free step.
