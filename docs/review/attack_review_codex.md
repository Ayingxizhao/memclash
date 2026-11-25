## 1. Attack surface

Ranked by likely damage:

1. **The advertised git-and-file system does not yet exist.** The draft lists seven substantial checker changes, while the code and prompt still implement the older git-only vocabulary.  
   **Smallest change:** Present and evaluate the git-only system on Dec 1; label file rules as future work.

2. **The current checker misses basic conditional clashes.** It enumerates situation fields mentioned by the clause under test, not fields introduced by the other rule; therefore “push to main” can appear compatible with “push only when asked.”  
   **Smallest change:** Implement draft change 8.1 and add this exact regression test. Until then, remove “exact” and “checks every clash” from claims.

3. **The held-out test may not test the new scope.** ADR 0007 describes only 52 “git-looking” held-out rules; it does not establish that file rules or running-command rules were selected and labelled.  
   **Smallest change:** Keep the final-test claim git-only. I am unsure whether the unseen labels already cover file rules.

4. **Recall is only as good as a possibly incomplete reference.** The documented large-folder reference reviews pairs proposed by two readers, not every pair; pairs both readers miss are treated as negatives. The held-out labelling procedure and number of positive clashes are not documented here.  
   **Smallest change:** Report “recall against this reference,” the number of positive pairs, annotator disagreement, and how candidate pairs were produced. Do not call it ground truth.

5. **“One action” is too narrow for several vocabulary features.** Copying, sequences, and two required actions cannot be judged as one event; conversely, `repo_include` and `repo_remove` could both happen at different times rather than clash.  
   **Smallest change:** Limit the claim to incompatible constraints on the same atomic operation or explicitly defined repository state. Cut copy and opposite-action clashes for this presentation.

6. **Strong permission will look like a false positive.** Most programmers will read “you may skip testing for docs changes” as an exception to a general testing rule, not as a contradiction with it. The cited sources have only been read through abstracts or summaries.  
   **Smallest change:** Call these “interactions requiring precedence,” report permission-versus-ban separately, and delete claims that this is the standard definition until the sources are read.

7. **The agreement measurement is currently misleading.** `same_meaning` combines all `must_do` clauses with OR, so “must do A and B” can equal “must do A or B.” Translation is also not truly “one rule alone” because every other folder rule is supplied as context.  
   **Smallest change:** Remove folder context and compare normalized clause multisets. If that is not done, report only raw field/clause agreement and call the runs context-order repetitions.

8. **Tests and builds look cherry-picked.** Tests occur in 8 survey folders and builds in 3, while omitted lint/format, release, migration, deploy, and restart rules occur just as often or more often.  
   **Smallest change:** Replace both with the generic `run` design in section 4, or cut running commands entirely.

Given the nine days remaining, scope reduction is safer than implementing the full draft and producing an untested “final” system.

## 2. Unjustified parts

Several core git and file actions are ordinary meanings and are defensible: commit, stage, push, merge, branch operations, read, create, edit, move, and delete. Push and merge groups are also reasonable.

The following need revision or removal:

- **`repo_include` is a state, not an action.** “Must be in the repository” can justify a repository-state predicate, but not an event named `repo_include`. Either model it explicitly as state or cut the `repo_include`/`repo_remove` opposite-action check.

- **“Never commit X” does not always mean “X must not exist in the repository.”** It can mean do not include X in a new commit, or do not modify an already tracked X. Do not collapse these readings automatically.

- **“X is gitignored” does not mean X is absent from the repository.** Git’s ignore rules do not affect already tracked files. Cut this equivalence.

- **“Always run tests after a change” is not captured by “some change happened earlier.”** The latter has no immediacy or causal meaning. Cut this row unless the temporal meaning is defined.

- **Copy is not atomic.** Decomposing it into read plus create/edit contradicts the one-action model and loses the essential same-content relation. Cut it.

- **The agent-choice/situation division is partly arbitrary.** `has_secret` and `kind` are properties of the target, not choices. `files_shown`, `secrets_checked`, and approval are facts that the agent may influence, but treating them as freely selectable can hide obligations. Reclassify or avoid claims based on that distinction.

- **`min_files`/`max_files` lack demonstrated need.** Cut them unless observed rules or held-out labels depend on them.

Most of the multiple-meaning table is not justified as fixed semantics:

- `delete` does not ordinarily include move.
- `touch` does not reliably mean read, edit, or every file action.
- `remove` means `repo_remove` only with explicit git context.
- `change` need not include deletion.
- “add a line,” “add a file,” and `git add` are normally distinguishable from context.
- Treating “may” as either strong permission or no clause is a project policy choice, not lexical fact.

For Dec 1, cut the exhaustive-reading feature. Translate contextually clear uses; mark genuinely unclear cases as excluded and report their count.

## 3. One prompt or two?

Use **one prompt and one shared vocabulary**, with compact git, file, and running sections.

A split requires a router that can itself make errors, and mixed rules such as “never commit `.env`” are exactly where routing is hardest: they concern a path, repository state, and a git operation. Translating them twice creates duplicate or inconsistent clauses; choosing only one prompt loses information. Separate prompts also make cross-family clashes and three-run agreement harder to interpret.

One shared representation does not automatically solve cross-family clashes. The checker must explicitly define relations such as staging a path versus committing it, or editing a file versus its repository inclusion. Do not claim those clashes are covered merely because both families share a prompt.

Control prompt length by removing long examples and unjustified ambiguity tables, not by introducing routing. Report agreement overall and separately for git-only, file-only, and mixed rules.

## 4. Running commands

Replace `run_tests` and `run_build` with:

```text
cmd: run
task: <opaque exact name>
```

A rule about any run matches by omitting `task`. Named tasks match only identical names. Unnamed or ambiguous tasks become unmodeled.

This covers tests, builds, deploys, migrations, linting, formatting, publishing, releases, and restarts without inventing a task taxonomy. It also removes the obvious selection-bias attack. Exact matching will miss aliases such as `db:migrate` versus “migrations,” but that is a clear, conservative limitation and preferable to unsupported semantic guessing.

## Summary

- Cut the Dec 1 claim back to the implemented and held-out-tested scope.
- Fix situation enumeration before making any exactness claim.
- Describe results against a fallible reference, not ground truth.
- Use one shared prompt; mixed rules make routing a new source of error.
- Replace test/build actions with `run` plus an exact opaque task name.