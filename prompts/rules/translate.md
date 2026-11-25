Translate ONE rule from a coding agent's memory folder into the fixed format below. You get the
rule and the name of the file it came from. Use only the names in this prompt. Never guess a
path, branch or name the rule does not state. Answer by calling the tool `record_translation`.
Every field of the tool must be filled; a field the rule does not state stays blank: `[]` for
a list, `""` for text, `"unstated"` for yes/no, `-1` for a number.

## 1. Status

- `not_in_scope`: the rule is not about git, files, or running a task (e.g. code style, which
  tool to use, how code reads credentials). Fill `reason`; leave `clauses` empty.
- `unclear`: nothing can be translated because a word the rule depends on has more than one
  meaning (section 5) and the rule's text does not say which. Fill `word` and `reason`; leave
  `clauses` empty.
- `ok`: at least one requirement is translated. Fill `reason`, `clauses` and `left_out`; a
  requirement that depends on an unclear word goes in `left_out` with that word.

`reason` is one short line.

## 2. Clauses

Split the rule into single requirements, one clause each. "Delete it locally and on the
remote" is two clauses. "Must do A and B" is two clauses; "must do A or B" is one clause with
`cmd: [A, B]`. The same holds for paths: a list of paths in one clause means any of them, so
"update A, B and C" is one clause per file. Drop vague parts ("keep it tidy") and name them in `left_out`. If nothing is left, return `not_in_scope` with reason "nothing left".

Pick the type with the first line that matches:
1. "you may", "can", "it is fine / allowed to" -> `may_do`
2. a path must or must not be in the repo ("X stays committed", "keep X out of the repo",
   "remove X from git") -> `must_hold` / `never_hold` with `where: {"in_repo": [X]}`
3. "never", "do not", "don't", "avoid", "no X" -> `never`
4. "X only if / only when Y", "do not X without Y", "before X, do Y", "when you do X, do it
   this way" -> `only_if`, X in `where`, Y in `needs`. If Y is an action, write
   `needs: {"after": [Y]}`.
5. "always do X", "do X", "after Y, do X" -> `must_do`, but only if the rule requires X itself
   to happen. A rule that only says how X is done, whenever it is done, is not `must_do`.

A condition no field can describe ("during a hotfix", "for UI changes") stays on the clause as
`"when_unmodeled": "<the condition>"`. Never drop it.

## 3. Actions (`cmd`)

| The rule says | `cmd` |
|---|---|
| commit | `commit` |
| stage, `git add` | `stage` |
| push (no detail) | `push` |
| push a branch / force push / delete a remote branch | `push_branch` / `force_push` / `push_delete` |
| merge (no detail) / merge locally / merge the PR | `merge` / `local_merge` / `pr_merge` |
| open a PR | `pr_create` |
| create / delete a branch locally | `branch_create` / `branch_delete` |
| delete a branch (no place named) | `any_branch_delete` |
| switch branch, pull, rebase, `reset --hard`, cherry-pick, fetch | `checkout`, `pull`, `rebase`, `reset_hard`, `cherry_pick`, `fetch` |
| create / remove a worktree | `worktree_add` / `worktree_remove` |
| read a file | `read` |
| create a file or folder | `create` |
| edit or modify an existing file | `edit` |
| rename or move | `move` (old path in `path`, new path in `dest_path`) |
| delete a file or folder | `delete` |
| run a task | `run`, with `task` |

`task` is one of: `test`, `build`, `lint`, `format`, `deploy`, `migrate`, `publish`, `restart`.
Anything else: `other:<exact words>`. A rule about running anything leaves `task` out.

## 4. Fields

Write only fields the rule states.

| Field | Value | Use for |
|---|---|---|
| `path`, `dest_path`, `path_except`, `in_repo` | list of paths as written | files or folders; `path_except` only for an exception in the same rule ("except vendor/cmake") |
| `kind` | `file` / `dir` | the rule says folder, directory, subfolder |
| `branch`, `after_branch` | exact name or glob | a named branch; `after_branch` if it belongs to the earlier action |
| `suite` | `all` | "all tests", "the full suite" |
| `after` | list of actions | "after X": X happened at some earlier point |
| `after_task`, `after_path`, `after_ok` | task name; list of paths; true/false | details of that same earlier step: the task of an earlier `run`, the path of an earlier file action, whether the earlier `run` succeeded ("after a successful build" -> `after: [run], after_task: build, after_ok: true`) |
| `running` | list of names as written | "while X runs" |
| `user_asked` | true/false | the user explicitly asked |
| `user_confirmed` | true/false | approval, permission, "ask the user first" |
| `tests_passed` | true/false | tests passed |
| `has_secret` | true/false | the file holds credentials, keys, tokens, passwords |
| `files_shown`, `secrets_checked` | true/false | the agent showed the files / checked for secrets |
| `admin_bypass`, `in_worktree` | true/false | `--admin` / inside a separate worktree |
| `min_files`, `max_files` | integer | "more than N files" -> `min_files: N+1`; "at most N" -> `max_files: N` |

Paths: write them as in the rule. Folder: end with `/`. A placeholder (`XX-name`, `<id>`)
becomes `*`. "Subfolders in X" -> `path: ["X/**"], kind: "dir"`; "folders directly in X" ->
`path: ["X/*"], kind: "dir"`. A named group with no path ("player data", "generated files")
is not a path: put it in `left_out`.

## 5. Words to watch

These words have several meanings. Use one only if the rule's own text makes it clear;
otherwise return `unclear` with the word.

| Word | Meanings |
|---|---|
| write, save | create; edit; either |
| add | create a file; edit a file; `git add` |
| delete | delete; also moving away |
| remove | delete; move away; take out of git; remove content inside a file |
| change | edit; any file action |
| touch | edit; any file action; the Unix `touch` command |
| never commit X (X a path) | don't commit changes to X; X must not be in the repo |
| after a change | after an edit; after any file action; after a commit |

The same applies to any other word you cannot read one way.

## 6. Examples (made-up). Shown with blank fields left out; in the tool every field is present.

FILE: git.md RULE: "Never push to main without the user's approval and passing tests."
{"status": "ok", "reason": "do not X without Y", "clauses": [{"type": "only_if", "where": {"cmd": ["push"], "branch": "main"}, "needs": {"user_confirmed": true, "tests_passed": true}}], "left_out": ""}

FILE: notes.md RULE: "Always write the summary to notes/today.md."
{"status": "unclear", "word": "write", "reason": "does not say whether notes/today.md is new or existing"}

FILE: style.md RULE: "Use tabs, not spaces, in Go files."
{"status": "not_in_scope", "reason": "code style"}
