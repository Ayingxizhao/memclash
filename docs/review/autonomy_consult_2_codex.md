1. **CHANGE.** The re-check is useful, but “force every unknown true” is not sound evidence that a clash is genuinely possible. Conditions within one rule—or across rules—may be mutually exclusive (“during reset” vs “before reset,” different repositories, alternative workflows). Z3 proves only:

> The rules clash under the assumption that these opaque conditions co-occur.

Call it `possible_clash` only with that explicit meaning. Also re-check each tested clause against relevant unknown-conditioned constraints, not indiscriminately every condition: unknowns on unrelated `must_do`/`may_do` clauses cannot contribute.

2. **CHANGE: use a minimal sufficient condition set.** Testing conditions one at a time would miss interactions requiring A+B. Instead, start with all relevant conditions true and shrink the assumptions to a subset-minimal unsatisfiable core. Report:

> clashes if A and B hold at once

This removes irrelevant conditions and makes judging feasible. It does not prove A and B can co-occur; that remains the judge’s job. Deduplicate identical normalized condition texts, but do not automatically equate them semantically yet.

3. **AGREE, with a separate evidence tier.** An LLM judgement of condition co-occurrence is defensible because it answers a narrow semantic question, but do not merge it into ordinary `clash`. Preserve `clash_by_judgement` (or `clash`, `basis=condition_judgement`) in metrics and output. Include rule context, because condition fragments alone may be misleading. “Yes” should mean there exists a coherent ordinary scenario where all minimal conditions hold simultaneously—not merely that their wording is non-contradictory.

Without existing labels, build evaluation specifically for this stage:

- Blindly hand-adjudicate all generated candidates, independently by two reviewers; resolve disagreements.
- Add planted condition pairs covering compatible, contradictory, nested, temporal, and different-object cases.
- Report candidate precision, judge precision/recall, disagreement rate, and end-to-end added true clashes/false alarms.
- Keep ordinary `clash` precision unchanged and report judgement-derived results separately.

4. **CHANGE: defer named-group overlap.** It is analogous operationally but not logically: it requires semantic set membership (“server-world.dat” belongs to “map/player data”), not condition co-occurrence. Treating it as an unknown Boolean risks opaque false alarms. Add it later as `possible_target_overlap`, ideally backed by a small explicit ontology/alias table or separately evaluated judgement step.