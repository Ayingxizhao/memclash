# Experiment log: finding clashes in real memory folders

Summary of results: `natural_findings.md`. Code: `pipeline/rules/natural_test.py`,
`pipeline/rules/lexical.py`, `pipeline/rules/group.py`; data: `data/runs/natural/`.

## N. LLM alone vs Z3 on real folders
- N1. 951 same-folder pairs among the 84 rules with saved translations. Z3 flags 2: R118/R131
  (real) and R20/R74 (false alarm). Misses are translation losses: the "may" of R156 dropped;
  "map and player data" left out (needs the other rule).
- N2. Whole-folder LLM, one call per folder (`prompts/rules/folder_judge.md`): DeepSeek found all
  clear clashes in the 84-rule set, 0 false (5 calls, ~$0.025).
- N3. Full folders (1,287 rules, 119-394 per folder, ~196k pairs), screened by whole-folder LLM
  calls. DeepSeek on two folders: 2 calls, 94k output tokens (~47k per call), ~$0.06.
- N4. Union of screen flags: 43 pairs plus one known pair, labelled independently by two AI
  reviewers and checked by the author. Final: 22 clash, 19 ambiguous, 2 compatible. Only 5 of 22
  clear clashes are inside the git/file/task vocabulary; the rest turn on which tool or command
  style to use, numeric values, plan steps or file layout.
- N5. Head to head on the pairs with saved translations: Z3 1 of 2 clear clashes, 1 false
  alarm; whole-folder LLM 2 of 2, 0 false.
- N6. Word-overlap candidate filter (`lexical.py`): >= 1 shared word keeps 13.5% of pairs and
  19 of 22 clear clashes; >= 2 keeps 2.5% and 13 of 22.
- N7. Missed-clash probe: 200 random unflagged pairs with >= 2 shared words, judged by a blind AI
  reviewer: 3 clashes, 197 compatible. Recall over all pairs is unknown.

## Cost measurements used for the speed and cost estimates
- Translation: 48 rules, two steps, one run: 99 calls, 65k output tokens, about 1 minute
  off-peak, about $0.04.
- One DeepSeek whole-folder call on an 84-rule folder: 47k output tokens, about $0.03.
- DeepSeek output speed in the action tests: 145-169 tokens/s.
- Z3 timing on round-2 translations, one laptop: all same-folder pairs (4,139) median 5.1 ms
  (`data/runs/boundary2/clash_timing.json`); whole-folder check of 2-51 rules, 51 rules in
  6.3 s (`data/runs/boundary2/group_timing.json`).
- Gate per action (estimate for a live gate: one call per action, resending the rules). Rules and
  instructions about 1,500 input tokens for the 51-rule memory. Output per action from the logs:
  Haiku ~96 tokens (10,009 for 104 actions), DeepSeek ~270 (24,801 and 37,335 for 114 actions, two
  runs, reasoning included). API prices per 1M tokens: Haiku 5.5 $0.10 in / $0.50 out; DeepSeek 4.1
  Flash off-peak $0.15 in (cache miss) / $0.60 out (api-docs.deepseek.com pricing page, 2026-11-28).
  Time: output tokens at ~200 tok/s (Haiku) and 145-169 tok/s (DeepSeek) plus ~1 s to start a call.
  Result: Haiku ~1.5 s and ~$0.0002, DeepSeek ~3 s and ~$0.0004, Z3 ~5 ms (0.5 s per 100) and $0.
