Audit result: most counts match the artifacts, but two claims need correction.

1. Finding 3 uses a stale denominator. `full_gold.json` labels R60/R213 **ambiguous**, not clear. Therefore the final-label result is:

- Z3: **1/2 clear clashes**, plus one false alarm.
- Whole-folder LLM screens: **2/2 clear clashes**; they also flagged R60/R213, now ambiguous.

The existing **1/3** and **3/3** figures come from the earlier scoring reflected in `score.json` and section N1, before the final N4 adjudication. “Three Z3 misses” should likewise distinguish one clear miss from the ambiguous case.

2. “One whole-folder LLM pass does not scale” is overstated. The evidence establishes that one pass **can miss clashes at full-folder scale**, not general non-scalability. The probe’s **1.5%** is the observed sample rate (3/200), not literally the pool rate; applying it to 4,860 gives an estimate of about **73**, with the stated wide interval. Say: “A single pass has unmeasured and demonstrably imperfect recall.”

All other reported counts match the supplied artifacts/log: 43 candidates; 22/19/2 labels; 27/43 agreement; type counts 12/4/2/2/2; 5/22 in-vocabulary; two-folder 5/6, 4/6, union 6/6, four shared of 15; probe 200/4,860 with three flags; overlap figures 13.5%–19/22 and 2.5%–13/22.

**Title: CHANGE.** “The solver wasn’t the bottleneck” is broader than this small, selection-biased test supports. Suggested: **Finding clashes in real coding-agent memory: retrieval and translation dominate the failures observed**.

**Design lesson: CHANGE slightly.** Keep high-recall candidate generation → pairwise semantic review → Z3 as an explainable witness where expressible → human review for ambiguity. But describe exhaustive pairwise checking as a proposed design, not an established result; its cost and recall were not measured.

Sources: [natural_findings.md](/Users/yingxizhao/dev/cs2520/projects/docs/review/natural_findings.md), [experiment_log.md](/Users/yingxizhao/dev/cs2520/projects/docs/review/experiment_log.md:161).