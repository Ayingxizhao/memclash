# Natural-folder findings (2026-11-23)

Data: `data/runs/natural/`. Log: `experiment_log.md` section N. Consults:
`hybrid_lit_codex.md`, `natural_consult_1_codex.md`, `natural_consult_2_codex.md`.

## Working title
**Finding clashes in real coding-agent memory: retrieval and translation dominate the observed failures**

## Findings
1. **Real clashes exist, and most are outside a git/file vocabulary.** Five real folders, 1,287
   rules (~196k same-folder pairs). Two whole-folder LLM screens (Codex all 5 folders; DeepSeek
   2 folders) plus one known pair gave 43 candidates. Labelled by a fresh blind Codex and by
   Claude (not blind): 22 clear clashes, 19 ambiguous, 2 compatible. Types of clear clashes:
   tool or command choice 12, plan step vs standing rule 4, value 2, file layout 2, permission
   vs prohibition 2. Only 5/22 fit the formal vocabulary.
2. **"Is this a clash?" is often a judgement call.** The two labellers agreed on 27/43; typical
   disagreements: a specific rule that refines a general one, a preference vs an allowance, a
   permission that can be obtained first (R60/R213).
3. **Translation, not solving, limits the formal pipeline.** On 951 pairs with saved
   translations, Z3 found 1/2 clear clashes (R118/R131; missed R24/R156) with 1 false alarm;
   whole-folder LLM screens found 2/2 with 0, and also flagged R60/R213, which the final
   adjudication made ambiguous (first count, before N4: Z3 1/3, LLM 3/3). Z3's errors: a
   dropped "may" (R24/R156), a target with no path ("map and player data", R60/R213), a lost
   scope ("non-code changes", the R20/R74 false alarm).
4. **A single whole-folder LLM pass has imperfect, unmeasured recall at full size.** At full size Codex missed R60/R213 (found in
   the 84-rule subset). On two folders Codex found 5/6 clear clashes and DeepSeek 4/6 (+1
   false); the union found 6/6, and the two shared only 4 of 15 flags. A blind pairwise review
   of 200 random unflagged pairs that share >= 2 content words (seed 2520, pool 4,860) found 3
   more clashes (single Codex judge, not adjudicated): 3/200 = 1.5% of the sample; applied
   to the pool, about 73 missed clashes (wide interval, about 15-210), versus 22 found.
5. **The cheap candidate step also loses clashes.** Word overlap >= 1 keeps 13.5% of pairs
   and 19/22 clear clashes; >= 2 keeps 2.5% and 13/22.

## Proposed design (not an established result; cost and recall of exhaustive pairwise checking unmeasured)
candidate step (better than word overlap; unmeasured) -> pairwise check of every candidate
(finding 4) -> Z3 only where the vocabulary fits, as an explainable witness (finding 1, 3;
no evidence that Z3 improves decisions) -> ambiguous pairs to a person with both readings
(finding 2).

## Limits
Candidates come from LLM screens, so recall over all pairs is unknown; labels are two model
labellers (Claude not blind), not people; five folders; the probe is one judge; DeepSeek ran
once on two full folders; spend in this phase ~$0.14, over the $0.10 limit (cut-off replies
were retried; fixed in llm.py).
