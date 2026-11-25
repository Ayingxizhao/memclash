# Review of the git + file rule checker (read-only)

I read the README, all ADRs, `docs/review/vocab_draft.md`, `pipeline/git/git_check.py` and `prompts/git/git_translate.md`. I did not open the held-out data or the labels, so anything I say about held-out clash counts is a guess.

## 1. What a grader will most likely attack (most damaging first)

**1. The final test may hold almost no clashes.** The 10 held-out folders have 52 git-looking rules. On the tuning folders, 212 git rules gave 11 reference clashes, and the checker found 0 of them. At that rate, 52 rules may hold 0 to 3 clashes, so any recall or precision number would rest on a handful of pairs.
- *Fix:* Lead with a number you can measure without many clashes: **coverage**, meaning the share of reference clashes the vocabulary can express at all. It needs no API calls, since the 11 tuning clashes can be counted by hand now. Report the held-out counts as raw counts ("x of y") with exact confidence intervals, and say plainly that the test is small.

**2. Adding file rules on Nov 22 breaks your own freeze rule (ADR 0007), the filter (ADR 0005) and possibly the labels.** The "52 git-looking rules" came from a git-only filter, and its miss-rate estimate covers git rules only. I am not sure whether the held-out clash labels cover file rules. If they don't, file-rule clashes there will have no reference.
- *Fix:* Write an ADR that freezes the vocabulary and prompt before the held-out run. Rerun the filter with file words and redo the hand sample of rejected rules. If the labels are git-only, narrow the held-out claim to git rules and report file rules as tuning-only.

**3. "Exact method" overclaims.** Z3 is exact only for the translated formulas. Your own research question says translation is the main error source.
- *Fix:* Rename it to "solver-checked". Add one sentence: "exact with respect to the translations; translation errors are measured separately."

**4. The clash definition counts intended exceptions as clashes.** ADR 0003 says "you may skip X for test-only PRs" clashes with "always do X". In the norm-conflict literature, a more specific rule overriding a general one (lex specialis) usually settles the conflict. A grader will say you are flagging rules the user meant to coexist. The ADR also admits the sources were read only as abstracts.
- *Fix:* Report a separate category, "exception (needs a priority rule)", instead of plain "clash". Read Vranes 2006 and Vasconcelos et al. 2008 in full before citing them.

**5. The vocabulary looks fitted to the data, and the reference used the same models that designed it.** Claude and Codex drafted the vocabulary, and the same two models were the readers who built the tuning reference (and Claude had seen the checker's output). Several fields (`in_worktree`, `admin_bypass`, `files_shown`, `secrets_checked`, `actor`, `running:<name>`) have no stated source. Modeling builds (3 folders) but not lint (8), publish (7) or migrations (6) does not match your own counts.
- *Fix:* Add a one-line source for every item: git or gitignore docs, a rule in the data, or prior art. Cut items with no source (see section 2).

**6. The documents contradict each other** (details in section 2):
- The 5b row for `may` lets "may" also mean "only describes what is possible". That contradicts ADR 0003's fixed strong-permission reading, and it would turn every "may" vs "never" clash into "depends on reading".
- The prompt defines `after` as "right after", but the code means "done at some earlier point".
- Prompt Step 1 says "how to run tests" is not in scope, but the new vocabulary includes running tests.
- Group names `write`, `change` and `remove` mean one fixed thing in section 2 and a list of readings in 5b.
- *Fix:* Fix each one now, before any translation run.

**7. Recall is low by design.**
- Each `when_unmodeled` condition gets a fresh unknown fact, so two rules naming the same condition ("during a sweep") can never clash (ADR 0004 admits this).
- Actor and process names match only if identical.
- Tool choice, which is behind 9 of the 11 tuning clashes, is out of scope.
- *Fix:* Narrow the claim to "few false clashes; recall limited to what the vocabulary can express", and report recall next to coverage. A cheap add: let rules share one fact when they use the identical condition text.

**8. Agreement is not correctness, and one scoring rule is undefined.** Three runs agreeing shows the translator is consistent, not that it is right. The hand check is done by one person, the author. The scoring of the "depends on reading" verdict is not decided in advance.
- *Fix:* Decide now how "depends on reading" is scored and report it both ways (counted as flagged and as not flagged). Give the hand-check sample size with a rule-of-three bound.

## 2. Parts that can't be justified

Each item below comes with whether to cut it.

- **"X is gitignored" means "X must not be in the repo": wrong by git's own docs.** The gitignore docs say files already tracked are not affected. *Cut this example*, or translate it as "never stage or commit X" (new files only).
- **5b `may` with the reading "only describes what is possible": contradicts ADR 0003.** *Cut `may` from 5b*; "may" always becomes `may_do`.
- **5b `touch` reading "read or edit": no source.** Neither the plain meaning nor the Unix `touch` command supports a read-or-edit middle reading. *Cut that reading* and keep "edit" and "any file action".
- **Groups `write`, `change`, `remove` share names with 5b ids that mean something else.** Group `remove` = move or delete, but 5b `remove` also includes `repo_remove`. *Rename the groups or drop them*: 5b already covers these words.
- **`repo_include` / `repo_remove` are listed as actions but are really states.** The draft says "one action = one operation", yet "must_do repo_include" asks for a state that may already hold. This is defensible (git docs define the "tracked" state), but the draft needs one sentence explaining it. Keep both. Opposite actions listing only this pair is fine if a sentence says why: create and delete can happen one after the other, while including and removing the same path cannot both end up true.
- **`actor` field: I found no source cited.** *Cut it* unless you can point to real rules ("only the release agent may push").
- **`running:<name>`, `dest_path`, `kind`, `suite`: keep only if a rule in the data uses them.** I am unsure; check the survey counts. `kind` (for "subfolders") and `suite: all` ("run all tests") look plausible. `dest_path` is only needed if rules about moving files exist.
- **`in_worktree`, `admin_bypass`, `files_shown`, `secrets_checked`, `min_files`/`max_files`:** these come from tuning rules. That is acceptable, but say so: "fields taken from rules in the tuning data".
- **`user_asked` (a fact of the situation) vs `user_confirmed` (something the agent can do): the split is defensible**, since the agent can ask but cannot make the user ask. Expect the translator to mix them up, so report agreement on this field separately.
- **5b `add`, `copy`, `delete`, `remove`, `change`: their readings follow plain meaning.** For `delete`, "delete or move" is fine because a move also makes the old path stop existing. `copy` is likely rare (I'm unsure), so cut it if no rule in the data uses it.

## 3. One prompt or two?

**Recommendation: one prompt, one vocabulary.**

- **Mixed rules are common in exactly this scope.** "Never commit .env" is both git and file. A split would have to route it or translate it twice.
- **A split adds a routing step**, which is a new error source that needs its own measurement, like the git filter in ADR 0005, and you have no time for that before Dec 1.
- **Cross-family clashes only work in one vocabulary.** "Never touch secrets/" vs "commit secrets/config" can only be checked if both rules share one action and path model. With two prompts, the two translations might name the same path in different ways.
- **Agreement is simpler to measure**: one translator, one comparison, no routing disagreement mixed in.
- **Prompt length is the real cost.** The current git prompt is about 1,700 words, and adding file rules may roughly double it. That is manageable. Keep one ordered table per family inside the one prompt, and keep the fixed examples.

## 4. Running commands

**Replace `run_tests` and `run_build` with one action `run` plus a task name. I am somewhat unsure about this.**

- **The counts don't support keeping only tests and builds.** Builds (3 folders) are as rare as server restarts (3) and rarer than deploy (5), migrations (6), publish (7) and lint (8). Note these are rough keyword counts per folder, not counts of real rules.
- **Fully free-text names would hurt agreement.** "npm test", "tests" and "pytest" would not match each other, so clashes get missed and the three runs disagree.
- **Middle option:** `run task:<name>`, where the translator picks from a short fixed list (test, build, lint, format, deploy, migrate, publish, restart). Anything else becomes `other:<exact text>`, matched exactly. Names match only if identical, like process names. This keeps `suite` for tests and costs one table row per name.
- **If time is short, cutting running entirely is also defensible.** Say "running commands is out of scope", and drop the `run_tests` rows and the `tests_passed` link to running.

## 5. Summary

- The biggest risk is a held-out test with too few clashes. Lead with coverage (no API cost) and report raw counts with intervals.
- Freeze the vocabulary in an ADR now. Redo the filter for file rules, or narrow the held-out claim to git rules only.
- Change "exact" to "solver-checked", and report "exception" pairs separately instead of as clashes.
- Fix the contradictions before running anything:
  - `may` in 5b
  - `after` meaning "right after" in the prompt
  - tests marked out of scope in the prompt
  - group names reused for 5b words
  - "gitignored" treated as "not in the repo"
- Use one prompt and one vocabulary. Replace the two running actions with `run` plus a fixed short list of task names, or cut running entirely.
