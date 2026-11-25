1. **CHANGE — earlier-step details.** The idea is sound and general, but the proposed fields do not fully fix the cited build example.

Add `after_task` and `after_path`, with validation that:

- `after_task` accompanies an earlier `run`.
- `after_path` accompanies an earlier file action.
- Each describes the same earlier event selected by `after`, rather than merely some unrelated prior event.

Otherwise, with several prior actions, Z3 can satisfy `after: edit` using one event and `after_path: X` using another. The existing `after_branch` has the same latent correlation problem; copying its implementation would perpetuate it.

“Verify the build succeeds before committing” also needs success, not merely `after_task: build`. Either add a general `after_succeeded` field or explicitly leave success unmodeled. Encoding success in `when_unmodeled` weakens an `only_if`: it makes the whole restriction conditional instead of requiring success.

For labels:

- Preserve v2 labels and baseline scores unchanged.
- Write and preregister the v2.1 conversion rubric before running v2.1 translations.
- Relabel the dev set under that rubric, preferably independently and blind to model outputs.
- Create a separate v2.1 frozen-label artifact; never overwrite the original. Reviewers should see rule text and the v2.1 rubric, not baseline predictions or error reports.
- Treat results on the existing frozen rules as retrospective because they have already influenced the vocabulary. A clean confirmatory v2.1 claim requires a new untouched frozen sample.

2. **CHANGE — path-list splitting.** Splitting is right for explicit conjunctions such as “update A, B, C, and D,” including `may_do` under the project’s strong-permission semantics. It is wrong as an unconditional normalization of every multi-pattern list:

- “Create X or Y” requires one obligation over the union.
- “Create either X or Y, but not both” is not representable by splitting or by the current union.
- A list may simply describe one target class, such as several alternative spellings or patterns.

Keep path lists as OR and require the translator to emit separate clauses for conjunctions, or add an explicit `path_quantifier: "any" | "each"` and expand only `each`. Do not infer conjunction solely from list length. Commands should retain their present OR semantics.

**Adjudication review: CHANGE R80 and R133; AGREE on the other eight.**

- **R80:** four clauses are correct, but `when_unmodeled: "as part of the change"` treats a required timing relationship as an optional applicability condition. Use a genuine trigger such as “when making a change,” while recording “not as an afterthought” as unexpressible timing; I would not mark the action-list reading ambiguous.
- **R133:** the partial clause captures only “delete some branch.” The unmodeled text should preserve the universal requirement: every local branch other than `main`, in every fork. Current wording loses “all.”

R224, R47, R194 under v2, R101, R85, R30, R62, and R114 follow the stated v2 vocabulary and status policy.