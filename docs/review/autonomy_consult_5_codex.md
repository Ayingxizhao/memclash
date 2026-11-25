1. **AGREE — pair judgments**

- **R20–R74: False alarm.** R20 governs non-code changes; R74 governs code. Their branch instructions apply to disjoint work categories.
- **R20–R152: False alarm.** Same reasoning independently: R152 duplicates R74’s text, so code gets its own branch while non-code work stays on the current branch.

2. **CHANGE — diagnosis is right, proposed fix is not yet sufficient/general**

The semantic principle is sound: a condition belonging to an entire requirement should constrain every clause translating that requirement.

However, the proposed `same req id` propagation would **not fix run 1 as recorded**. Its clauses map to different requirements:

- `commit-non-code-on-current-branch`
- `no-new-branch`

Thus there is no same-ID sibling from which to propagate the condition. Propagating across all requirements in a rule would be unsafe because separate requirements may have different conditions.

Also, copying any clause’s `when_unmodeled` to every same-requirement clause is sound only if Step 1 correctly formed a single requirement and the condition is requirement-wide. A clause may contain a local qualifier; that should not automatically become global. Prefer representing the shared condition explicitly at the requirement level, then conjoining it with any clause-local condition.

**Yes, strengthen Step 1 validation.** Each requirement’s quote should contain—or explicitly inherit—the words establishing its trigger/scope. For R20, the no-new-branch requirement must retain “non-code changes.” An exact condition quote or structured inherited-condition reference is safer than a heuristic word check.

3. **CHANGE — diagnose/fix before final evaluation**

Do not run the frozen evaluation yet. The observed false-alarm rate is small (2/435, one distinct textual conflict), but the proposed repair does not address the actual run-1 structure, and run 3 demonstrates complete condition loss.

Fix requirement-level condition preservation, add focused tests for split and multi-clause requirements, and update the preregistered fingerprint before the one-shot final evaluation. No further broad probing is necessary once that deterministic failure is covered.