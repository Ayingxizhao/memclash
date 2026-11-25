You are an independent research reviewer for a class project. Work read-only (do not edit or
create files; your final message is saved). You may search the web. Do not open `data/gold/`,
files named `labels_*`, or any `frozen_*` label file. Do not call any paid LLM API.

## The project and its numbers

Coding agents keep memory folders of instructions. Our method: an LLM translates each rule
alone into a fixed formal vocabulary (git / file / task actions, conditions), then Z3 checks
every pair for a clash. Read `README.md`, `docs/review/experiment_log.md` (especially E0, E3,
E5-E9, F), `docs/review/autonomy_plan.md`, `docs/adr/0003-clash-definition.md`, `0004`, `0008`.

Key results: on a 30-rule dev set, "whole rule translated exactly right" (Z3 equivalence with a
hand label) rose from 55% to 73% over several iterations; on the untouched 30-rule test set it
went only from 49% to 51%. Two independent labellers (Claude, Codex) agreed on only 20/30 rules
in each set (Z3 equivalence). Clash detection on planted clashes: 15-18 of 20 found with 0
false alarms when a pair counts if any of 3 runs flags it; one real-folder probe gave 1 false
alarm in 435 pairs. Only ~6-10 rules per dev split were in scope.

## Questions

1. **Is the method wrong?** From the literature on natural language -> formal / policy /
   specification translation, autoformalization, and conflict or contradiction detection in
   rule sets (policies, requirements, norms, LLM instructions), what are the known failure
   modes of "translate each item alone, then check formally"? Which apply to us? Is there a
   better-supported method (e.g. direct pairwise LLM judgement, NLI contradiction detection,
   hybrid: solver proposes candidates and an LLM verifies, translating pairs jointly instead of
   alone, retrieval of related rules)? Cite work you actually found; mark abstract-only.
2. **Is the evaluation wrong?** Is exact Z3 equivalence to one label a fair accuracy measure
   when two labellers agree only 67% of the time? What do others use (inter-annotator
   agreement as a ceiling, multiple references, task-level metrics such as pair-verdict
   accuracy instead of translation accuracy)?
3. **Dev -> test transfer.** Is the gap better explained by overfitting to a tiny dev set, by
   sampling (dev and test differ in mix), or by label noise? What would a sound small-sample
   design look like (sizes, confidence intervals, held-out validation)?
4. **Cheap pilots.** Propose at most 3 experiments that need no LLM calls or only a few
   (total budget under $0.20) and would tell us which explanation is right or whether another
   method is better. Be concrete about data and measures.

Output: Markdown, under about 1500 words, sections 1-4, then a 5-bullet summary. Plain language.
Say plainly when unsure.
