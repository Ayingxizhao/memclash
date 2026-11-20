You translate ONE rule from a coding agent's memory folder into a fixed model of git
operations. You see only this rule (and the folder's other rules for context). Do not judge
whether it agrees with other rules.

## The model

The agent performs git operations. Each operation is described by these fields:

| Field | Type | Meaning |
|---|---|---|
| `cmd` | list of names | which operation (see below) |
| `branch` | glob | branch the operation writes to (merge target, push branch, deleted branch) |
| `file` | glob | path of a file the operation commits, stages, pushes or merges |
| `has_secret` | true/false | that file contains real credentials (keys, passwords, tokens) |
| `min_files`, `max_files` | integer | number of files the operation touches |
| `after` | list of names | the operation comes right after this operation |
| `after_branch` | glob | branch of that earlier operation |
| `user_asked` | true/false | the user explicitly asked for this operation |
| `user_confirmed` | true/false | the user approved this operation (e.g. approved the file list) |
| `files_shown` | true/false | the agent showed the user the files involved |
| `secrets_checked` | true/false | the agent checked the staged files for secrets |
| `tests_passed` | true/false | the tests passed before the operation |
| `admin_bypass` | true/false | the operation bypasses branch protection (e.g. `--admin`) |

Operation names for `cmd` and `after`:
`commit`, `push_branch` (push commits to a branch), `push_delete` (`git push origin --delete`),
`force_push`, `local_merge` (local `git merge`), `pr_create`, `pr_merge` (`gh pr merge` or
merging a PR on GitHub), `branch_create`, `branch_delete` (local `git branch -d/-D`),
`checkout`, `pull`, `rebase`, `reset_hard`, `cherry_pick`.
Group names: `push` = every kind of push (push_branch, push_delete, force_push);
`merge` = every kind of merge (local_merge, pr_merge); `any_branch_delete` = branch_delete,
push_delete; `any` = every operation. A rule that says "push" or "merge" without narrowing
it means the group.

Globs: `*` matches any text. Write exactly what the rule says: `.env` matches only the file
`.env`; `.env*` also matches `.env.example`. A branch "main" is `main`; "a feature branch"
is `feat/*` unless the rule names a pattern.

## Clause types

A rule becomes one or more clauses:

- `never`: operations matching `where` must not happen.
  "Never commit credentials" ->
  `{"type": "never", "where": {"cmd": ["commit"], "has_secret": true}}`
- `only_if`: operations matching `where` may happen only if every field in `needs` holds.
  "Before any push, ask for confirmation" ->
  `{"type": "only_if", "where": {"cmd": ["push"]}, "needs": {"user_confirmed": true}}`
- `must_do`: the agent must perform an operation matching `where` (when the rule's situation
  arises). "After a merge to main, delete the branch" ->
  `{"type": "must_do", "where": {"cmd": ["any_branch_delete"], "after": ["merge"], "after_branch": "main"}}`
- `may_do`: the rule explicitly permits an operation matching `where`.
  "You may push without asking when only docs changed" ->
  `{"type": "may_do", "where": {"cmd": ["push"], "file": "docs/*", "user_confirmed": false}}`

In `must_do` and `may_do`, a check field set to `false` means the rule says to do the
operation WITHOUT that step ("skip confirmation", "merge immediately without approval").
Leave a field out when the rule says nothing about it. Use only the fields and names above.

If the rule is not about git operations (for example it is about coding style, a Python
version, or what to work on next), return `{"fits": false, "reason": "..."}`. If only part of
the rule is about git, translate that part and list the rest in `"left_out"`.

Return JSON:
{"fits": true, "clauses": [...], "left_out": "<part of the rule not translated, or empty>"}
