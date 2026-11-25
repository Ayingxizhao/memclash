## Title

**The Solver Wasn’t the Bottleneck: Detecting Conflicts in Real Repository Instructions**

## Three-sentence abstract

Across five memory folders containing 1,287 rules, two LLM screens produced 42 distinct candidate pairs; after adding one known pair, review classified 22 as clear clashes, 19 as ambiguous, and 2 as compatible. Only 5/22 clear clashes fit our git/file/task formal vocabulary, while independent translation often discarded permissions, scope, and links between rules, causing Z3 to miss conflicts despite reasoning precisely over its inputs. The resulting design is a human-centered screening pipeline: use multiple cheap semantic screens for candidate generation, check pairs explicitly, invoke Z3 only for explainable witnesses inside its vocabulary, and send competing interpretations to a human.

## Findings

- **Natural conflicts exist but mostly fall outside the formal vocabulary.** Among 43 reviewed candidates from five folders, 22 were clear clashes, 19 ambiguous, and 2 compatible. Only 5/22 clear clashes were in-vocabulary; 17/22 concerned tool or command choice, values, layout, or similar distinctions.

- **Conflict is partly a judgment problem.** The two labellers agreed on 27/43 pairs; the final rule—agreement becomes the label, disagreement becomes ambiguous—produced 19/43 ambiguous cases.

- **Translation, not solving, was the main formal bottleneck.** On the earlier 951-pair benchmark, saved-translation Z3 found 1/3 benchmark-clear clashes and produced 1 false alarm. Misses involved dropped permission (“may”), omitted scope/content, and a missing cross-rule link.

- **Whole-folder screening helped, but scale and stability remain problems.** On the 84-rule subset, both LLMs recovered 3/3 benchmark-clear clashes with no clear false positives. At full size, Codex missed R60/R213, and across the two jointly screened large folders the LLMs shared only 4 of 15 flags.

## Does the evidence support the proposed system?

- **Several screens → union:** weakly supported. Codex yielded 21 clear clashes; DeepSeek yielded 4, with 3 overlapping, so the union added exactly **1 additional clear clash** over Codex alone. It also added ambiguous and compatible candidates, so union improves candidate yield, not demonstrated recall.

- **Union → pairwise check:** supported. Of 43 candidates, 21 were not clear clashes: 19 ambiguous and 2 compatible.

- **Pairwise check → Z3 where vocabulary fits:** vocabulary-based routing is supported by only 5/22 clear clashes being expressible. However, the claim that Z3 improves decisions is **unsupported**: no evidence shows it finding complementary real clashes or reliably validating LLM flags. Its defensible role is an auditable, conditional witness.

- **Ambiguous pairs → human with both readings:** strongly supported by 19/43 ambiguous outcomes and only 27/43 labeller agreement.

Honest limits: these are candidates from the **union of screens**, so recall over all ~196,000 pairs is unknown; the “judge” is labeller overlap rather than external truth; there are only five folders and three earlier benchmark-clear clashes; Claude was not blind; R60/R213’s status itself changed under later review.

## Best free work

1. Taxonomize all 41 clash/ambiguous pairs by conflict type, scope issue, and vocabulary coverage, with explicit coding rules.
2. Publish the incremental union table: 35 Codex flags, 11 DeepSeek flags, 4 shared; 21 versus 4 clear clashes, with one clear clash added by union.
3. Have a fresh Codex pairwise-review a preregistered sample of non-flagged pairs. Report it as a missed-clash probe, not a recall estimate unless sampling is genuinely random.

**CHANGE — exact next free step:** code all 41 clash/ambiguous pairs into a fixed taxonomy—command/tool choice, numeric value, layout, permission, scope/refinement, git/file/task, and other—recording one primary type and whether the current Z3 vocabulary can express it.