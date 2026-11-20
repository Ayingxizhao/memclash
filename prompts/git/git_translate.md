You translate ONE rule from a coding agent's memory folder into a fixed model of git
operations. Other rules of the folder are shown only so you understand the project; translate
only the RULE. Do not judge whether it agrees with other rules. Follow the steps below in
order, and make every choice the way the steps say, even if another reading seems possible.

## The model

Each git operation is described by these fields:

| Field | Type | Meaning |
|---|---|---|
| `cmd` | list of names | which operation (names below) |
| `branch` | glob | branch the operation writes to (merge target, pushed branch, deleted branch) |
| `file` | glob | path of a file the operation commits |
| `has_secret` | true/false | that file contains real credentials (keys, passwords, tokens) |
| `min_files`, `max_files` | integer | number of files the operation touches |
| `after` | list of names | the operation comes right after this operation |
| `after_branch` | glob | branch of that earlier operation |
| `user_asked` | true/false | the user explicitly asked for this operation |
| `user_confirmed` | true/false | the user approved this operation |
| `files_shown` | true/false | the agent showed the user the files involved |
| `secrets_checked` | true/false | the agent checked the staged files for secrets |
| `tests_passed` | true/false | the tests passed before the operation |
| `admin_bypass` | true/false | the operation bypasses branch protection (e.g. `--admin`) |
| `in_worktree` | true/false | the operation is done inside a separate git worktree |

Operation names: `commit`, `push_branch`, `push_delete`, `force_push`, `local_merge`,
`pr_create`, `pr_merge`, `branch_create`, `branch_delete`, `checkout`, `pull`, `rebase`,
`reset_hard`, `cherry_pick`, `fetch`, `worktree_add`, `worktree_remove`.
Group names: `push` = push_branch, push_delete, force_push; `merge` = local_merge, pr_merge;
`any_branch_delete` = branch_delete, push_delete; `any` = every operation.

Clause types:
- `never` + `where`: operations matching `where` must not happen.
- `only_if` + `where` + `needs`: operations matching `where` may happen only if `needs` holds.
- `must_do` + `where`: the agent must perform an operation matching `where`.
- `may_do` + `where`: the rule explicitly permits an operation matching `where`.
Any clause may also carry `"when_unmodeled": "<situation>"` (see Step 5).

## Step 1: Is the rule about git?

The rule is about git if it says what the agent does with commits, pushes, merges, branches,
pull requests, pulls, rebases, resets or cherry-picks, or what may go into the repository
("never commit X", "store X in version control").

It is NOT about git if it is only about: how code is written (for example how code reads
credentials, or hardcoding values in source code), which tool or version to use, which task
to do next, how to run tests, or style. Then return `{"fits": false, "reason": "..."}` and stop.

## Step 2: Split the rule into single requirements

Write down each separate requirement. A list ("no stale branches, no credentials, tested
code") gives one requirement per item. "Delete the branch locally and on the remote" gives two
requirements (local delete, remote delete). Drop any requirement that is not about git and
name it in `left_out`. If a requirement is a vague goal with no concrete git operation
("keep things tidy", "work incrementally"), drop it and name it in `left_out`. If nothing is
left, return `{"fits": false, "reason": "vague"}` and stop.

## Step 3: Pick one clause type per requirement

Use the first line that matches:
1. "you may", "it is fine to", "it is allowed/permissible to", "can" -> `may_do`
2. "never", "do not", "don't", "avoid", "no X" -> `never`
3. "before X, do Y", "X only if/when Y", "do not X without Y", "only X when Y" -> `only_if`
   (X goes in `where`, Y goes in `needs`). If Y is a git operation ("before creating a branch,
   check out main"), write it as `needs: {"after": [Y]}`. Never put `cmd` inside `needs`.
4. "after X, do Y", "always do Y", "do Y", "skip Y and do X" -> `must_do`

"(Preference)" in front of a rule does not change anything; translate it like any rule.

## Step 4: Pick the operations (`cmd`)

| The rule says | Use |
|---|---|
| push (any push, no detail) | `push` |
| delete the remote branch, `git push origin --delete` | `push_delete` |
| force push, `--force` | `force_push` |
| merge, merge into main (no detail) | `merge` |
| `gh pr merge`, merge the PR, the PR is merged | `pr_merge` |
| create a PR, open a pull request, `gh pr create` | `pr_create` |
| delete the branch (no place named) | `any_branch_delete` |
| delete the branch locally, `git branch -d` | `branch_delete` |
| commit, store in the repository / version control, add to git | `commit` |
| create a branch, `git checkout -b` | `branch_create` |
| switch to a branch | `checkout` |
| fetch, refetch, `git fetch` | `fetch` |
| create a worktree / remove a worktree | `worktree_add` / `worktree_remove` |

Use only the operations the rule names. Do not add pushes because a commit is usually pushed.

## Step 5: Fill in only the fields the rule states

| The rule says | Field |
|---|---|
| a named branch (main, master, release/x) | `branch` (or `after_branch` if it belongs to the earlier operation) with that exact name |
| "the feature branch", "the branch", "the PR branch" | no branch field |
| a named file or pattern | `file`, written exactly as named; add `*` only if the rule says "any file starting with" or uses `*` |
| a named folder ("files in dist/") | `file: "dist/*"` |
| credentials, secrets, API keys, tokens, passwords | `has_secret: true` |
| "fewer than N files" / "at most N files" / "more than N files" | `max_files: N-1` / `max_files: N` / `min_files: N+1` |
| confirm, approve, get approval, ask the user | `user_confirmed: true` |
| show the files, show the file list | `files_shown: true` |
| "confirm which files", "confirm the files" | `user_confirmed: true` and `files_shown: true` |
| check / verify / scan for secrets | `secrets_checked: true` |
| tests pass, tested code | `tests_passed: true` |
| only when the user asks | `user_asked: true` |
| `--admin`, bypass branch protection | `admin_bypass: true` |
| "after X" | `after: [X]` (operation names from Step 4) |
| skip / bypass / without Y, "immediately" when the rule mentions approval | the field for Y set to `false` |

Leave out every field the rule does not state. Never guess a branch name or file pattern.

Conditions the model cannot express. If a requirement applies only in a situation that no
field above can describe ("in the local clones", "during a backlog sweep", "when the PR is
wedged", "for UI changes"), keep the clause and add `"when_unmodeled": "<that situation>"`.
Never drop such a condition: a rule without its condition would apply everywhere. Other parts
the model cannot express (which tool to use, the commit message format, "small focused PRs")
are simply named in `left_out`.

Two fixed patterns:
- "Before committing, verify that no X is staged" -> `only_if` commit needs
  `secrets_checked: true`, AND `never` commit with X.
- "Commit only Y" (Y a file) -> `may_do` commit `file: Y`, plus whatever the rule forbids.

## Step 6: Check your answer

- Every name is from the tables above. Every field you wrote is stated in the rule.
- Each requirement from Step 2 has exactly one clause.
- Parts you dropped are named in `left_out`; conditions you could not express are in
  `when_unmodeled`, not dropped.

Return JSON:
{"fits": true, "steps": "<one short line per step>", "clauses": [...], "left_out": "<text or empty>"}

## Examples (made-up rules)

RULE: "After a release is tagged, delete the release branch locally and on the remote."
{"fits": true, "steps": "1 git. 2 local delete; remote delete. 3 must_do x2. 4 branch_delete, push_delete. 5 no branch name given; 'after a release is tagged' has no operation name, left out.", "clauses": [
 {"type": "must_do", "where": {"cmd": ["branch_delete"]}},
 {"type": "must_do", "where": {"cmd": ["push_delete"]}}],
 "left_out": "after a release is tagged (tagging is not in the model)"}

RULE: "Never push to master without the user's approval and passing tests."
{"fits": true, "steps": "1 git. 2 one requirement. 3 'do not X without Y' -> only_if. 4 push. 5 branch master; approval; tests.", "clauses": [
 {"type": "only_if", "where": {"cmd": ["push"], "branch": "master"}, "needs": {"user_confirmed": true, "tests_passed": true}}],
 "left_out": ""}

RULE: "Before every commit, make sure no API keys are staged."
{"fits": true, "steps": "1 git. 2 one requirement. 3 fixed pattern 'verify no X is staged'. 4 commit. 5 API keys -> has_secret.", "clauses": [
 {"type": "only_if", "where": {"cmd": ["commit"]}, "needs": {"secrets_checked": true}},
 {"type": "never", "where": {"cmd": ["commit"], "has_secret": true}}],
 "left_out": ""}

RULE: "It's fine to merge a PR with only docs changes right away, without asking."
{"fits": true, "steps": "1 git. 2 one requirement. 3 'it's fine to' -> may_do. 4 merge the PR -> pr_merge. 5 docs -> file docs/*? not named as a path, left out; without asking -> user_confirmed false.", "clauses": [
 {"type": "may_do", "where": {"cmd": ["pr_merge"], "user_confirmed": false}}],
 "left_out": "only docs changes (no file path given)"}

RULE: "During a hotfix, push straight to main without opening a PR."
{"fits": true, "steps": "1 git. 2 one requirement. 3 'do Y' -> must_do. 4 push. 5 branch main; 'during a hotfix' cannot be expressed -> when_unmodeled; 'without opening a PR' has no field, left out.", "clauses": [
 {"type": "must_do", "where": {"cmd": ["push"], "branch": "main"}, "when_unmodeled": "during a hotfix"}],
 "left_out": "without opening a PR"}

RULE: "Before starting a feature branch, fetch origin."
{"fits": true, "steps": "1 git. 2 one requirement. 3 'before X, do Y' with Y an operation -> only_if, needs after. 4 branch_create; fetch. 5 nothing else stated.", "clauses": [
 {"type": "only_if", "where": {"cmd": ["branch_create"]}, "needs": {"after": ["fetch"]}}],
 "left_out": ""}

RULE: "Keep the history clean and never commit generated build files in dist/."
{"fits": true, "steps": "1 git. 2 'keep the history clean' vague, dropped; never commit dist/. 3 never. 4 commit. 5 file dist/*.", "clauses": [
 {"type": "never", "where": {"cmd": ["commit"], "file": "dist/*"}}],
 "left_out": "keep the history clean (vague)"}

RULE: "Read the database password from an environment variable, never hardcode it."
{"fits": false, "reason": "about how code reads credentials, not about git"}
