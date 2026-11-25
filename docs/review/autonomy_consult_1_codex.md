1. **CHANGE:** The dev/test separation is sound, but “labeler disagreement = ambiguous” is not. Disagreement can be annotation error or different interpretations of the schema. Independently label ~30 rules, then adjudicate disagreements into:

   - genuinely ambiguous;
   - one label corrected;
   - unresolved/excluded.

Keep adjudication notes and agreement statistics. Use perhaps 20 rules for iteration and 10 as a held-out dev-validation set; 30 repeatedly tuned rules will overfit quickly. The frozen 30 should be evaluated exactly once at the end. Run disagreement should be evaluated as an ambiguity classifier, not used to define ambiguity. Report precision, recall, and raw counts because the sample is small.

2. **CHANGE:** Only apply canonicalizations whose equivalence is proved under the current Z3 encoding.

   - **Drop `kind: file` from extension-looking paths: unsafe.** `path` and `is_dir` are independent Z3 variables; extensions do not imply files. Directories such as `.config` or `release-1.0` also defeat the heuristic.
   - **`X/` ↔ `X` + `X/**`: conditionally safe.** `X/` means the directory itself plus descendants. However, a slashless `X` is rewritten as `**/X`, so the proposed expansion additionally matches `X` at any depth. It is safe only where the generated regexes are actually equivalent—for example, normally with a rooted multi-segment path. Let Z3 prove this rather than using a string rewrite.
   - **Ignore `when_unmodeled` wording: only partly safe.** Presence must remain significant. More importantly, `agreement.py` currently merges every such condition in a rule into one shared fact, while clash checking gives each clause a fresh fact. That can create false equivalence when two clauses have different opaque conditions. Align these semantics or introduce reviewed shared condition IDs.
   - **Sorting: safe but accuracy-neutral.** Order is already irrelevant for union/conjunction lists and `same_meaning` already uses Z3. Sorting helps reproducibility and diffs, not scores.

Add property tests asserting `same_meaning(before, after)` for every canonical rewrite.

3. **CHANGE:** Recommended order:

   1. Build and adjudicate the dev set; establish error categories and single-run baselines.
   2. Run the cheap non-thinking-mode A/B on a fixed dev subset.
   3. Fix deterministic semantic gaps: partial translations, “nothing left” handling, `when_unmodeled` identity, and defensible named-target relations.
   4. Add an atomic requirement inventory with source spans and a deterministic coverage check: every atom must be translated, marked unmodeled, or explicitly left out. This is the most promising missing lever for whole-rule accuracy and clash recall.
   5. Test three-run voting last. Keep it only if it improves adjudicated accuracy—not merely agreement. Treat no majority as abstention/ambiguity evidence.

For clash recall, separately measure failures caused by status routing, missing atoms, wrong fields, and solver expressiveness; otherwise improvements will be hard to attribute.