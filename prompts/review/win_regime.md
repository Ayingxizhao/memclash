You are a research advisor on a class project (presented Dec 1). Work read-only; your final
message is saved. Do NOT open `data/gold/labels_*`, `frozen_*`, or held-out folders. No paid API
calls.

Project: detect clashes between rules in coding-agent memory folders. Pipeline: an LLM
translates each rule into a fixed git/file/task vocabulary (pipeline/rules/vocab.py,
two-step translator), then Z3 checks pairs (pipeline/rules/pair.py) and groups of three
(pipeline/rules/group.py). Read docs/review/experiment_log.md (esp. sections N and G),
docs/review/natural_findings.md, docs/review/group_bench_prereg.md,
docs/review/hybrid_lit_codex.md, and data/runs/natural/ (score.json, full_gold.json,
group_bench*.json) as needed.

The problem: in every test so far a single whole-folder LLM call matches or beats the Z3
pipeline (planted pairs: LLM 20/20 vs Z3 15-18/20; three-rule groups: DeepSeek 5/8 vs Z3 1/8).
The advisor says a project whose method cannot beat one LLM call over the memory file is not
presentable. We need an HONEST regime where the Z3 pipeline beats the plain LLM, shown by a
fair, preregistered test, not by tuning on results already seen.

Answer, concisely, with evidence from the files:
1. From data we ALREADY have (free): is there any slice where Z3 already beats the LLM? E.g.
   in-scope clashes at full folder size (LLM misses R60/R213 at full size; probe suggests ~73
   missed clashes), the fully translated groups, false alarms, stability across runs, recall
   as folder size grows. Give exact numbers and say whether the slice was chosen post hoc.
2. Propose the 2-3 most promising regimes where Z3 should win for a principled reason (e.g.
   large folders / long context, many rules interacting or chains of 3+, subtle scope such as
   globs and branch patterns, exhaustive "no clash" certification, incremental updates and
   cost, run-to-run consistency). For each: why the LLM should fail, why our Z3 side should
   not (check our vocabulary and translator actually cover it), and a cheap test design
   (Codex can write material and judge for free; DeepSeek paid budget about $0.05 total;
   translation costs about $0.0008 per rule; one whole-folder call about $0.02-0.03).
   Include fixed win conditions and the threat that material is written to favour Z3, and
   how to defuse it (e.g. clashes written from natural-rule style, LLM baselines given the
   best prompt, multiple LLM runs, Codex as a second LLM baseline).
3. Rank them by chance of a real, defensible win in 1 week, and recommend one.
4. A framing for the paper/talk (title + 3-sentence pitch) that is honest about the earlier
   losses and leads with the regime where the hybrid wins. Say what claims we must NOT make.

Be blunt. If you think no honest win is likely, say so and give the best honest framing.
