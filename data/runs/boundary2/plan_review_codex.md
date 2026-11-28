1. **No headroom:** Round 1’s clear actions produced essentially perfect LLM scores. Reusing the same six categories is unlikely to distinguish systems; add harder, independently designed cases and a power/sensitivity analysis.

2. **Codex selection bias:** Codex screens eligibility, translates rules, reviews exactness, and is then an evaluated arm. This can select rules and representations unusually compatible with Codex.

3. **Claude leakage/alignment:** Claude generates actions and supplies half the gold labels while Claude Haiku is evaluated. Use model-independent generation/labeling or human adjudication.

4. **Synthetic leakage:** Codex-written synthetic rules are directly evaluated by Codex, making that comparison unfair. Use a held-out generator or exclude its originating model from synthetic comparisons.

5. **Ambiguity exclusion bias:** Removing every label disagreement preferentially removes difficult cases—the cases most capable of separating arms. Predefine adjudication and make an all-actions analysis primary or co-primary.

6. **Post-freeze fixes are underspecified:** “Fixes…go in changes.log” permits consequential checker changes and reruns, as happened in round 1. Define allowed fixes, tests before freezing, and whether corrected runs are sensitivity-only.

7. **Pooled primary is not defined:** Round 1 and round 2 use different LLM baselines, and round 1 has frozen versus corrected Z3 results. Specify exactly which runs are pooled and how missing/nonmatching arms are handled.

8. **Sampling is not fully reproducible:** “Until 100 repos are kept,” mutable search hits, fetch failures, and vaguely named candidate lists leave selection discretion. Freeze hashes, ordering, exclusions, failure handling, and stopping rules.

**Before freezing, I would fix all eight; at minimum 1–7.** Without those changes, the study will likely repeat the ceiling result, while model-linked selection and post-freeze corrections make any small difference difficult to interpret.
