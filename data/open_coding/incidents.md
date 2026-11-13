# Incident-level comparison (non-duplicate issues)

Grouped by hand from `comparison.md` (automatic quote matching) plus both reports. An
incident = one underlying problem, possibly recorded as several pairs. Duplicates are
excluded (differences there are mostly segmentation/index-extraction policy).
`Adjudicate` = needs the third annotator's decision; agent_a gives a recommendation.

| # | Folder | Incident | agent_a | agent_b | Status / agent_a recommendation |
|---|---|---|---|---|---|
| I1 | Consteon | db-analyst "SELECT-only" vs mutations after user confirmation | contradiction (med) + index scope override | other (med) ×2 | **Agree issue.** Label: adjudicate (A: permission-vs-prohibition = contradiction; B: file never explicitly permits mutation) |
| I2 | Consteon | "fix the value, not the target enum" vs "schema fix is on the table" | contradiction (med) | excluded: different schema objects | Adjudicate. A concedes: B is right that R3 concerns the target table's enum, R6 the config column type → **drop** |
| I3 | Consteon | "always confirm target DB" vs "use the DB the user specified; ask only if ambiguous" | other (med) | excluded: compatible | Adjudicate. A leans **drop** (both followable) |
| I4 | Consteon | index calls the first lesson "latest" | other (high) | — | Adjudicate. Factual index drift; real but minor |
| I5 | Consteon | keep file-wide pattern vs "never copy nearby modules" | other (low) | — | A leans **drop** |
| I6 | setflow | auto `git push origin --delete` vs "confirm before any git push" | other (med) | other (med) ×2 | **Agree** |
| I7 | setflow | index "#4 and #5 next" vs file "#17 is next" | other (high) | noted as non-rule factual drift | **Agree it exists**; disagree whether it is a rule relation |
| I8 | setflow | `git branch -d <branch>` runs before "switch to main" (fails while branch is checked out) | — | other (high) | **B only.** A agrees it is valid (procedural defect, not a rule conflict) |
| I9 | setflow | commit `.env.example` vs "no .env files staged" | other (low) | — | A leans **drop** |
| I10 | applied_math | module notes "no LaTeX" vs LaTeX conventions / "write its math in LaTeX" / no-latex file's "source files use LaTeX" | contradiction (high) ×3 | contradiction (high) ×3 | **Agree** |
| I11 | applied_math | index "never LaTeX" drops the chat-only scope | contradiction (high) | other (high) ×4 | **Agree issue.** Label: adjudicate |
| I12 | applied_math | "one module per chapter" (Sedgewick-Flajolet) vs CLRS now primary | override (high) | override (high) ×2 | **Agree** |
| I13 | applied_math | "don't lean on outside knowledge" vs "repurpose something familiar" | contradiction (med) | override (med) ×3 | **Agree issue.** Label: adjudicate (A leans B's `override`: specific vs general) |
| I14 | applied_math | "lazy expansions only on friction" vs "build prerequisites explicitly" | override (med) | not addressed | Adjudicate |
| I15 | applied_math | "Resume at Module 1 §4" predates the re-pacing | other (med) | not addressed (listed as temporal/hard to formalize) | Adjudicate |
| I16 | applied_math | "simple formal English" vs "do NOT simplify the prose" | other (low) | excluded: different contexts | A concedes → **drop** |
| I17 | applied_math | `ds-formal-proof-practice.md` referenced but missing | other (high) | other (high) ×2 | **Agree** |
| I18 | applied_math | `aofa-course-teaching-stance.md` not in index | other (med) | — | Adjudicate (structural) |
| I19 | applied_math | index "built around Sedgewick-Flajolet" stale | other (high) | — | Adjudicate (index drift) |
| I20 | llm-benchmark | `[[user-hardware]]` link to a missing file | other (med) | — | Adjudicate (structural) |

Folder-level: both annotators find real problems in Consteon, setflow, applied_math and
none in MCMike0399 and llm-benchmark (apart from structure/duplicates). Agreement on that is 5/5.
