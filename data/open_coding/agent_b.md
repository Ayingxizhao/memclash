# Open coding — agent_b

## Coverage and method

Read all **31 markdown files in full**: 6 / 7 / 3 / 9 / 6, matching the supplied counts. Extracted **199 atomic rules** and manually considered all **5,455 within-folder pairs**, including same-file and index/file pairs. Scripts were used only for mechanical checks, not rule judgment. No other annotations, runs, cache, root CLAUDE.md, or network sources were consulted.

The JSON contains the full inventory and pair explanations. This report quotes the operative evidence for each recorded pair; ellipses only shorten displayed quotations. Counts below count **pairs**, not independent underlying incidents. Repeated formulations remain separate rule occurrences. Same behavior with unequal scopes is not automatically a duplicate; compatible specializations, explicit exceptions, and merely shared topics are excluded.

Descriptive project/user facts, frontmatter, rationale, and past mistakes were not extracted as rules. Agreed conventions, operative preferences, imperative headings, explicit permissions, and instructions under “How to apply” were included. A recommendation to question a constraint is not equivalent to a prohibition against changing a value.

## 1. Consteon/web-spreadsheet-example

**6 files; 68 rules; 2,278 pairs checked; 11 relations.**

- **R2 ↔ R53 — other, medium.** Index: “db-analyst scope is SELECT-only”; file: “db-analyst must never execute DDL (ALTER TABLE) or DML mutations (UPDATE, INSERT, DELETE) without explicit user confirmation first.” The index imposes an unconditional role boundary, while the file states a confirmation precondition. Whether confirmation expands the role is unspecified; the file does not explicitly permit mutations, so this is not a proven contradiction.
- **R2 ↔ R56 — other, medium.** “db-analyst scope is SELECT-only” / “ask user to confirm before running.” The application workflow contemplates running a mutation after confirmation without resolving the index's role restriction.
- **R53 ↔ R56 — duplicate, high.** “db-analyst must never execute DDL (ALTER TABLE) or DML mutations (UPDATE, INSERT, DELETE) without explicit user confirmation first.” / “ask user to confirm before running.” Both require confirmation for db-analyst mutations.
- **R53 ↔ R57 — duplicate, medium.** “db-analyst must never execute DDL (ALTER TABLE) or DML mutations (UPDATE, INSERT, DELETE) without explicit user confirmation first.” / “Never auto-execute mutations even if logically required.” Read in their confirmation workflow, both prohibit unconfirmed execution.
- **R56 ↔ R57 — duplicate, medium.** “ask user to confirm before running.” / “Never auto-execute mutations even if logically required.” Positive and negative restatements of the same confirmation requirement.
- **R7 ↔ R44 — duplicate, high.** “use async function not arrow” / “Regular `async function` (not arrow)”. Same referenced function-declaration requirement.
- **R10 ↔ R47 — duplicate, high.** “never copy nearby code” / “Never copy nearby modules as reference”. Same prohibition on using nearby modules as implementation references.
- **R28 ↔ R34 — duplicate, high.** “Status transitions to APPROVED must only happen via the external approval service callback, never via a direct DB write in an edit or submit repository function.” / “`APPROVED` is a status that must only arrive from the external approval service writing back to the module.” Same exclusive ownership of APPROVED transitions.
- **R8 ↔ R51 — duplicate, high.** “trust reference params” / “Follow its function signature, param types, and patterns exactly.” R51 is the atomic parameter-types component of the latter sentence; both require reference-defined parameter types.
- **R9 ↔ R63 — duplicate, high.** “use buildWorkspaceFilter” / “const baseWhereFilter = buildWorkspaceFilter(table, workspaceFilter);”. The file explicitly marks this code as Good instead of manual workspace filtering.
- **R12 ↔ R68 — duplicate, high.** “Never treat `target_status` as a generic approval state” / “Do not treat approval `target_status` as generic core enum”. Same prohibition on a generic approval-state interpretation.

**Important exclusions:** correcting an invalid stored value versus changing an incorrect configuration-column type concerns different schema objects, not opposing repair instructions. Numeric and timestamp CASE casts have distinct target-type scopes; direct-assignment permissions explicitly concern a different SQL context. Migration target confirmation and mutation approval are compatible, independent requirements.

## 2. M-Hernandez/setflow

**7 files; 24 rules; 276 pairs checked; 8 relations.**

- **R3 ↔ R16 — duplicate, high.** “never commit API keys, secrets, or credentials” / “Never commit API keys, secrets, passwords, tokens, or any credentials to the repo.” Same credential-commit prohibition.
- **R4 ↔ R17 — duplicate, high.** “use .env (gitignored) only” / “Always use .env files (gitignored)”. Same credential-storage convention.
- **R5 ↔ R7 — duplicate, high.** “delete local and remote feature branches after every merge to main” / “After every merge to main, delete the feature branch both locally and on the remote.” These atomic components both require local deletion.
- **R6 ↔ R8 — duplicate, high.** “delete local and remote feature branches after every merge to main” / “After every merge to main, delete the feature branch both locally and on the remote.” These atomic components both require remote deletion.
- **R2 ↔ R24 — duplicate, medium.** “get approval before git push or merge” / “always confirm files before push/merge”. The profile's imperative repeats the index's push/merge approval workflow.
- **R11 ↔ R9 — other, high.** “then switch to main” / “After `gh pr merge`, run `git branch -d <branch>`”. The stated sequence deletes the local branch before switching to main. If the feature branch remains checked out after merging, Git refuses deletion. This is an executable-sequence defect, not two logically incompatible obligations.
- **R10 ↔ R13 — other, medium.** “`git push origin --delete <branch>`” / “Always confirm with the user which specific files will be pushed or merged before running `git push`, `git merge`, or creating PRs.” Branch deletion is a push but pushes no files, leaving the confirmation payload poorly specified. Separate approval can still satisfy both.
- **R10 ↔ R14 — other, medium.** “`git push origin --delete <branch>`” / “Before any `git push` or `gh pr create`, show the user the list of changed files”. Deleting a remote branch has no changed-file list. Reporting an empty list and explaining the deletion avoids conflict, but the schema of the requested confirmation does not fit the operation.

**Non-rule observation, not counted as a pair:** the index says “issues #2 done, #3 in review, #4 and #5 next (can parallel)”; the progress file says “Phase 0 (Foundation) — **complete.** All 4 issues closed (#2-#5).” This is stale factual index metadata, not a conflict between extracted instructions.

## 3. MCMike0399/from-tcp-to-http

**3 files; 16 rules; 120 pairs checked; no relations found.**

There is **no MEMORY.md** in this folder; all three supplied markdown files were read. Direct tutoring and enforcement testing are compatible: one concerns assistance style, the other implementation validation. ThePrimeagen is described as historical inspiration, not a current instruction to recommend videos. Descriptive user-profile statements were not converted into additional agent instructions.

## 4. shabelson-picker/applied_math

**9 files; 73 rules; 2,628 pairs checked; 19 relations.**

- **R1 ↔ R51 — duplicate, high.** “when pointed at something, change only that” / “When the user points at a specific line, cell, or sentence, **edit exactly that and stop.**”. Same targeted-edit restriction.
- **R1 ↔ R56 — duplicate, high.** “when pointed at something, change only that” / “One pointed-at item → one edit.” Same restriction on change scope.
- **R51 ↔ R56 — duplicate, high.** “When the user points at a specific line, cell, or sentence, **edit exactly that and stop.**” / “One pointed-at item → one edit.” The application bullet repeats the main instruction.
- **R5 ↔ R70 — duplicate, high.** “don't re-debug launch.json” / “don't\nre-debug the launch.json.” Same prohibition for the known C-debugging freeze. Here `\n` marks the original line break.
- **R17 ↔ R32 — contradiction, high.** “Each module = my plain-text lecture notes (no LaTeX, see [[no-latex-explanations]]) +\n  a problem set with worked solutions.” / “Conventions in course notes: inline math `\( … \)`, display `$$ … $$`, single\n`$` literal”. **Situation:** write a mathematical formula in AofA lecture-note source for PDF rendering. The same file both bans LaTeX and prescribes it for these notes.
- **R17 ↔ R37 — contradiction, high.** “Each module = my plain-text lecture notes (no LaTeX, see [[no-latex-explanations]]) +\n  a problem set with worked solutions.” / “write its math in LaTeX from the start.” **Situation:** create Module 2 lecture-note mathematics. The all-module ban and Module 2 requirement cannot both be followed.
- **R17 ↔ R67 — contradiction, high.** “Each module = my plain-text lecture notes (no LaTeX, see [[no-latex-explanations]]) +\n  a problem set with worked solutions.” / “**those source files use LaTeX** (inline `\( … \)`,\ndisplay `$$ … $$`)”. **Situation:** author AofA lecture notes rendered to PDF. The dedicated memory requires LaTeX while the old course structure still bans it. Its explicit exception qualifies its own terminal rule, not the obsolete course-file ban.
- **R3 ↔ R67 — other, high.** “explain math in plain text” / “**those source files use LaTeX** (inline `\( … \)`,\ndisplay `$$ … $$`)”. The index omits the chat-only scope and PDF-source exception of the file it summarizes.
- **R4 ↔ R67 — other, high.** “never LaTeX” / “**those source files use LaTeX** (inline `\( … \)`,\ndisplay `$$ … $$`)”. Categorical index wording loses an explicit exception in the linked memory. Classified as index-summary drift rather than a separate chat/PDF conflict.
- **R7 ↔ R20 — override, medium.** “Teach everything from the ground up, self-contained and thorough — including\nprerequisites the book assumes (Big-O basics, combinatorics, probability, recurrences).” / “the sum-vs-integral bounding technique can be introduced as a\nrepurposing of something familiar rather than from zero”. **Situation:** introduce sum-versus-integral bounds using the learner's known integral test. The topic-specific permission relaxes the ground-up policy without a linked exception.
- **R10 ↔ R20 — override, medium.** “or lean on outside knowledge.” / “the sum-vs-integral bounding technique can be introduced as a\nrepurposing of something familiar rather than from zero”. **Situation:** reuse prior calculus knowledge to teach AofA bounds. The course calibration permits what the general stance prohibits. The first quotation is governed by “Don't” in its original sentence.
- **R8 ↔ R20 — override, medium.** “default to teaching, not assuming.” / “the sum-vs-integral bounding technique can be introduced as a\nrepurposing of something familiar rather than from zero”. **Situation:** choose the introduction to sum-versus-integral bounding. A specific calibration changes the default for this topic; no unavoidable conflict is asserted.
- **R14 ↔ R34 — override, high.** “**One module per chapter** (Module 1 = Ch 1 … Module 9 = Ch 9), following the book.” / “SYLLABUS.md and the module map still describe the book-chapter-per-module\nstructure and need rewriting against CLRS.” **Situation:** update the course structure after the August 29 primary-text change. The newer CLRS rewrite supersedes the retained Sedgewick-Flajolet mapping.
- **R14 ↔ R47 — override, high.** “**One module per chapter** (Module 1 = Ch 1 … Module 9 = Ch 9), following the book.” / “needs re-mapping onto CLRS after the 2026-08-29 text change.” **Situation:** update course/SYLLABUS.md. The cheatsheet memory carries the new mapping requirement while the old course rule remains.
- **R4 ↔ R32 — other, high.** “never LaTeX” / “Conventions in course notes: inline math `\( … \)`, display `$$ … $$`, single\n`$` literal”. The course rendering convention exposes the same missing medium qualification in the index.
- **R4 ↔ R37 — other, high.** “never LaTeX” / “write its math in LaTeX from the start.” The Module 2 instruction exposes the index's omitted PDF exception.
- **R4 ↔ R38 — other, high.** “never LaTeX” / “LaTeX math as `\( … \)` inline / `$$ … $$` display”. The cheatsheet explicitly says the linked no-LaTeX rule governs chat, not its files; the index fails to retain that qualification.
- **R50 ↔ R72 — other, high.** “proof practice per [[ds-formal-proof-practice]].” / “user wants proof practice each DS session”. Both reference the same practice, but `ds-formal-proof-practice.md` is absent from the nine-file input. Cadence survives in the index; the delegated procedure is unavailable.
- **R50 ↔ R73 — other, high.** “proof practice per [[ds-formal-proof-practice]].” / “simple formal English with articles”. The surviving index gives a language convention, but its missing referenced file prevents checking the full procedure.

**Important exclusions:** the dedicated no-LaTeX memory's chat/PDF split is an **explicit exception**, not itself a contradiction. DS versus AofA English-register instructions concern different teaching contexts. Targeted-edit rules explicitly instruct re-rendering and verification; “stop” is not treated as forbidding those steps. Opening a toolbox early need not mean creating it before friction occurs.

## 5. thesteve0/local-llm-benchmark

**6 files; 18 rules; 153 pairs checked; 3 relations.**

- **R1 ↔ R5 — duplicate, high.** “Use llama.cpp server metrics (API `timings`) for benchmark metrics, not GuideLLM client numbers” / “Use llama.cpp server metrics as the primary source of benchmark data, not GuideLLM client-side numbers.” Same primary metric source.
- **R1 ↔ R15 — duplicate, medium.** “Use llama.cpp server metrics (API `timings`) for benchmark metrics, not GuideLLM client numbers” / “Pull benchmark metrics from the llama.cpp `timings` object”. The serving memory repeats API-timings sourcing; its cross-reference supplies the primary-source context.
- **R5 ↔ R15 — duplicate, medium.** “Use llama.cpp server metrics as the primary source of benchmark data, not GuideLLM client-side numbers.” / “Pull benchmark metrics from the llama.cpp `timings` object”. Same sourcing instruction, with the implementation path in the latter.

**Important exclusions:** GuideLLM supplementary figures are explicitly permitted, not prohibited by the primary-source rule. Historical Ramalama labels are explicitly preserved; retaining them does not prescribe current Ramalama serving. User evaluation tendencies are descriptive, not an instruction to replace the scoring rubric.

## Cross-folder catalog

### Issue types

Names are inductive categories, not alternative names for the four supplied labels. Each pair appears in exactly one category here.

| Type | Definition | Pair count | Verbatim examples |
|---|---|---:|---|
| Repeated operative prescription | Multiple rule occurrences require the same behavior in the same scope, including index/file and within-file repetition. | 21 | “use async function not arrow”; “Regular `async function` (not arrow)” |
| Role boundary versus consent gate | An unconditional agent capability boundary coexists with a confirmation workflow whose effect on that boundary is unstated. | 2 | “db-analyst scope is SELECT-only”; “ask user to confirm before running.” |
| Unsafe procedural ordering | Individually feasible steps are ordered so that a realistic precondition blocks execution. | 1 | “After `gh pr merge`, run `git branch -d <branch>`”; “then switch to main” |
| Confirmation payload/operation mismatch | A generic approval rule requests a file-level payload for a Git operation that changes refs, not files. | 2 | “`git push origin --delete <branch>`”; “show the user the list of changed files” |
| Source-format migration residue | An obsolete document-authoring prohibition remains alongside incompatible rendering requirements for the same sources. | 3 | “my plain-text lecture notes (no LaTeX, see [[no-latex-explanations]])”; “write its math in LaTeX from the start.” |
| Exception lost in index compression | An index renders a medium-scoped rule categorical, omitting the linked file's explicit exception. | 5 | “never LaTeX”; “**those source files use LaTeX**” |
| Prior-knowledge calibration drift | Topic-specific permission to reuse prior learning relaxes a general self-contained/assume-nothing teaching stance without linking an exception. | 3 | “default to teaching, not assuming.”; “repurposing of something familiar rather than from zero” |
| Curriculum transition residue | New primary-text mapping instructions supersede a retained old textbook-based module rule. | 2 | “**One module per chapter** (Module 1 = Ch 1 … Module 9 = Ch 9), following the book.”; “needs re-mapping onto CLRS after the 2026-08-29 text change.” |
| Dangling procedural memory | An operative instruction delegates to a missing memory; only fragments of the procedure survive in an index. | 2 | “proof practice per [[ds-formal-proof-practice]].”; “simple formal English with articles” |

**Total: 41 pairs = 21 duplicate + 3 contradiction + 5 override + 12 other.** Several pairs share a single cause: the LaTeX migration, for example, produces both direct conflicts and compressed-index defects. These are not 41 independent incidents. The separate stale Setflow progress summary is factual drift and is not included in this total.

### Scope dimensions

Rough, overlapping incidence estimates across the 199 rules; these are manual coding ranges, not exact disjoint bins. Scope is often supplied by a section or file rather than repeated in every quotation.

- **Task/workflow:** roughly 100–120 rules — architectural-layer authoring, approval submission, migrations, tutoring, exam prep, benchmark reporting, harness building.
- **Tool/API or executable operation:** roughly 60–80 — Git/gh, codebase-onboard, repository APIs, CASE-WHEN SQL, PDF tools, cpptools, stream-test helpers, llama.cpp.
- **Communication/output medium and style:** roughly 45–60 — chat versus PDF sources, academic versus simple formal English, references, terse correction reports, inline comments.
- **File/project/module path:** roughly 40–60 — employee.repository.ts, course notes, DS cheatsheet, .env/.env.example, models/*.md, particular course modules.
- **Temporal/event sequencing:** roughly 35–50 — before mutation/push/commit, after merge/edit, until “skip,” when a module is reached, after a textbook change, historical result provenance.
- **Data type/state/domain:** roughly 25–40 — NUMERIC versus TIMESTAMPTZ, target-table enums, DRAFT/WAITING_ON_APPROVAL/APPROVED, environment credentials, server versus client metrics.
- **Actor, authority, or human consent:** roughly 20–30 — db-analyst/coder role, approval-service ownership, user-specified database, confirmation before execution or wider edits.
- **Language/runtime/environment:** roughly 10–20 — English/Hebrew, Java stream/thread constraints, Python interpreter, VS Code extension version and inherited environment.

### Hard-to-formalize rules

IDs are folder-local. Grouped entries identify each affected rule and the shared obstacle; this list concerns representation difficulty, not additional pair relations.

**Consteon**
- **R1, R12, R14, R16, R68:** “wrong schema,” generic-versus-module-specific meaning, and “real domain” require semantic/domain judgment; questioning a constraint is a deliberative step rather than a simple action prohibition.
- **R6, R8, R45–R52, R64:** “exactly” and reference precedence depend on retrieving the current external reference and interpreting its patterns/signature, not merely a fixed typed predicate.
- **R15:** tracing a consumer requires program/dataflow analysis and a stopping criterion.
- **R39–R43:** “newly added,” “current task,” acceptable rethrowing, and out-of-scope refactoring require change provenance and task boundaries. R41 also embeds permission/prohibition inside a distinction instruction.
- **R53–R57:** confirmation must attach to the particular mutation, not just any previous assent; “auto-execute” and “logically required” add interpretation.
- **R58–R62:** “exact target,” “any ambiguity,” and clarification/alternate-database behavior require interpreting user intent and error context.

**Setflow**
- **R1–R2, R13–R15, R24:** file-specific approval needs a stable proposal/approval identity; remote deletion shows why Git command names alone are insufficient.
- **R21:** “look like real credentials” is probabilistic and permits false positives; it is not just a known-secret lookup.
- **R22:** “~40 sets” is approximate, while “validate data quality” lacks a success threshold.

**TCP/HTTP**
- **R1:** preference strength differs from R3's absolute video prohibition; ranking alone does not encode that strength.
- **R5–R7, R9:** “direct,” “clearly,” “fast,” and “artificially” depend on teaching context and lack thresholds.
- **R8:** identifying primary sources is partly provenance/genre judgment.
- **R10:** “enforcement” versus mere correctness is an intensional property of a test suite.
- **R13–R15:** “like” leaves the prohibited wrapper set open; performance gates depend on workload/hardware; “rapid” connection cycles has no rate.

**Applied math**
- **R1–R2, R51–R56, R59–R62:** the pointed-at item, surrounding/nearby material, one “edit,” necessity of wider changes, and whether something was requested require discourse and document-boundary interpretation.
- **R6–R12:** “from the ground up,” self-contained, thorough, default assumptions, “outside knowledge,” and covering material “properly” are pedagogical judgments; “until skip” is a temporal/user-intent condition.
- **R15–R16, R20–R23:** friction, familiar knowledge, reteaching, “early,” and on-demand reference use need a model of learner state and preference strength.
- **R24–R25:** session duration is measurable, but session boundaries and an approximate six-month schedule are not simple timeless constraints.
- **R26–R30, R73:** precise/idiomatic academic English, genuinely advanced/confusable terms, prose simplification, proactive glossing, and simple formal English are graded linguistic judgments. The two registers also require retaining course scope.
- **R34–R37, R47, R49:** “next,” “resume,” “when reached,” and post-change remapping depend on evolving progress and instruction-version state.
- **R45–R46:** “~70 chars” is approximate and terminal rendering can change width; “wide” tables has no boundary.
- **R48:** choosing a representative small tree example requires mathematical relevance, not just substituting a number.
- **R50:** the delegated procedure is absent, so it cannot be fully encoded from these inputs.
- **R58–R59:** lines depend on wrapping and sentences on segmentation; the brevity constraints have different units.
- **R63–R68:** output-medium typing is straightforward, but recognizing mathematical explanation versus literal source/code and distinguishing LaTeX from Unicode/plain text can require content interpretation.
- **R69–R71:** recurrence of “the same” debugging freeze requires diagnosis; “first”/“second” actions require event order and remembered downgrade state.
- **R72:** “each DS session” needs a defined session boundary and persistent tracking.

**Local LLM benchmark**
- **R1, R5, R10–R11, R15:** primary versus supplementary data is a provenance/priority relation, not a blanket ban on client numbers.
- **R3–R4:** mechanical code restatement versus useful business intent requires semantic judgment, including accessibility context.
- **R16:** “historical” labels require measurement provenance and time, not replacing every occurrence of a serving-tool name.
- **R17–R18:** reasoning/planning versus code generation requires task decomposition; mixed requests may contain both kinds.

### Schema implications suggested by the observations

Preserve **output medium, operation subtype, actor authority, approval identity, temporal/version scope, and source/index provenance**. Keep explicit exceptions distinct from inferred overrides. Allow non-logical defects—missing referenced procedures and impossible step ordering—without forcing them into contradiction. Keep pair counts separate from deduplicated incident counts.
