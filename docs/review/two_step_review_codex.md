## Review

The implementation has the planned two-call shape, source quotes, requirement IDs, retry, semantic vote, and reporting-only uncovered-word check. However, it does **not yet enforce the plan’s central claim that nothing can be dropped silently**.

### 1. Instructions and formats

There are material contradictions:

- The inherited one-step prompt says an ambiguous word makes the whole rule `unclear` with no clauses ([translate.md](/Users/yingxizhao/dev/cs2520/projects/prompts/rules/translate.md:7)). Step 2 instead says status is `ok` whenever any clause exists ([translate_step2.md](/Users/yingxizhao/dev/cs2520/projects/prompts/rules/translate_step2.md:11)). Thus a mixed rule—one translatable requirement and one ambiguous requirement—has different status semantics in A and B.
- `translate.md` says to split the rule into requirements, while the appended step-2 instructions say not to split again. The latter probably intends to override the former, but the combined system prompt contains both.
- Step 2 says every requirement without a clause goes in `left_out`; coverage checks this only for `keep: translate`. `vague` and `outside_vocabulary` requirements can disappear without a clause or `left_out`.
- The plan says every `translate` requirement gets a clause. The code instead permits such a requirement to be put in `left_out` with any fixed reason—including `vague` or `outside_vocabulary`, contradicting step 1’s classification.
- `to_translation_step2` ignores the model’s reported status and recomputes it. That can be reasonable, but then status should not be presented as a meaningful model field. Schema deviations are merely reported after acceptance.

### 2. Bugs and loopholes

- Empty quotes pass: normalized `""` is a substring of every rule ([coverage.py](/Users/yingxizhao/dev/cs2520/projects/pipeline/rules/coverage.py:37)). There is no nonempty constraint on IDs, quotes, or requirements.
- A concrete `translate` requirement can be silently dropped by listing it as `left_out: vague`; coverage accepts it.
- A `vague`/`outside_vocabulary` requirement can be omitted from `left_out` entirely.
- Coverage checks only ID linkage, so an unrelated clause can name an ID and “cover” it. This is an inherent limit, but the report must not claim semantic coverage.
- Two `invalid_output` runs vote as a majority: `same_meaning` treats any equal non-`ok`, non-`unclear` statuses as equivalent ([agreement.py](/Users/yingxizhao/dev/cs2520/projects/pipeline/rules/agreement.py:80)).
- Requirement scoring is clause recall, not the planned “correctly translated or correctly left out” measure. It ignores labelled exclusions, and one produced clause can satisfy multiple equivalent labelled clauses because matching is not one-to-one ([label_score.py](/Users/yingxizhao/dev/cs2520/projects/pipeline/rules/label_score.py:27)).
- Missing translated records are silently skipped. `vote_rule_right` excludes unstable rules from its denominator, so abstaining more can raise the reported score.

### 3. A/B fairness

A and B currently apply different ambiguity/status policies. B also has up to four calls per run—one retry per stage—versus two for A, while the plan’s cost table states one versus two calls. B may also stop after step 1 for out-of-scope rules. Actual calls, retries, tokens, and latency must be reported.

### 4. Required changes

1. **MUST:** Define one status policy for mixed ambiguous/translatable rules and apply it identically to A, B, and labels. Use a standalone step-2 prompt or explicitly supersede conflicting one-step sections.
2. **MUST:** Make coverage enforce exactly one disposition per requirement: `translate` → clause or `unclear_word`; `vague` → `left_out:vague`; `outside_vocabulary` → matching exclusion. Reject contradictory classifications, simultaneous clause/`left_out`, empty quotes, and empty IDs.
3. **MUST:** Exclude `invalid_output` and unknown statuses from semantic groups and voting; count them explicitly as failures.
4. **MUST:** Repair scoring: one-to-one requirement matching, include correctly excluded labelled requirements, fail/count missing records, and report vote accuracy over all rules with unstable rules incorrect/abstained—not only stable rules.
5. **MUST:** Report actual call/retry/token totals for each arm and describe B as a larger-compute system comparison, not a controlled single-factor ablation.
6. **COULD:** Add overlap/duplicate-quote diagnostics and clearly label uncovered-word coverage as observational, not an enforced guarantee.

I did not inspect any forbidden label or gold data.