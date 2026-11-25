# Fixed vocabulary for git and file rules (joint draft, v2)

Status: draft for the user; Codex reviewed v2 in round 5 (`vocab_review_codex_r5.md`), and
its text changes are applied. v1 was agreed by Claude and Codex in four rounds
(`docs/review/vocab_review_codex_r1.md` to `_r4.md`). v2 applies the two critical reviews
(`docs/review/attack_review_claude.md`, `docs/review/attack_review_codex.md`) and the user's
scope choice: git plus basic file rules; the file part is dropped if its results are poor.

## Idea in one paragraph

Every rule is translated into the same small set of words. The list of actions, the list of
conditions and the way path patterns match are written in code and do not change during the
experiment. The translator may only fill in names: paths, branch names, task names, process
names. If a rule needs a word that is not on the list, it is marked unmodeled instead of
inventing a new word. Every item below has a source: git's own definitions, prior art, or
rules seen in the data (counts are rough keyword counts over the 60 survey folders).

## 1. Rule types (unchanged)

| Type | Meaning |
|---|---|
| `never` | an action matching `where` must not happen |
| `only_if` | an action matching `where` may happen only if `needs` holds |
| `must_do` | some action matching `where` must happen |
| `may_do` | an action matching `where` is explicitly allowed and must stay possible |
| `must_hold` / `never_hold` | a repository state must be true / must be false at the end (section 7) |

Any clause may carry `when_unmodeled: "<situation>"` (ADR 0004).

## 2. Actions

One action operates on one target; `move` additionally names its destination.

| Family | Actions | Source |
|---|---|---|
| git | commit, stage, push_branch, push_delete, force_push, local_merge, pr_create, pr_merge, branch_create, branch_delete, checkout, pull, rebase, reset_hard, cherry_pick, fetch, worktree_add, worktree_remove | git commands; all but `stage` already in the checker |
| files | `read`, `create`, `edit` (change content of an existing file), `move` (rename or move; old path stops existing), `delete` | Claude Code Read/Edit/Write, AppArmor, POSIX |
| running | `run` with a `task` (below) | survey: tests 8 folders, lint/format 8, publish/release 7, migrations 6, deploy 5, build 3, restart 3 |

`task` is one of a short fixed list: `test`, `build`, `lint`, `format`, `deploy`, `migrate`,
`publish`, `restart`. Any other task is `other:<exact text>` and matches only identical text.
A rule about running anything leaves `task` out.

Groups (git only, as now): push, merge, any_branch_delete, any. There are no file groups:
a rule that covers several file actions lists them (`cmd: [create, edit]`).

## 3. Fields

**What the action is** (the agent chooses the action, so these are part of it):

| Field | Kind | Meaning | Source |
|---|---|---|---|
| `cmd` | name or group | which action | |
| `path` | target (section 4) | file or folder acted on; for `move`, the old path | prior art |
| `dest_path` | target | for `move`, the new path | survey: move/rename rules in 3 folders |
| `kind` | `file` or `dir` | the path is a file or a folder | "no subfolders" rules |
| `task`, `suite` | name; `all` | which task; which tests (`all` = full suite) | "run all tests" rules |
| `branch` | glob | branch written to (as now) | git |
| `has_secret` | yes/no | the file holds real credentials | tuning rules |
| `user_confirmed` | yes/no | the user approved this action; the agent can ask | tuning rules |
| `files_shown`, `secrets_checked`, `admin_bypass`, `in_worktree`, `min_files`, `max_files` | as now | | taken from rules in the tuning data |

**What the situation fixes** (the agent cannot change it). When either rule of a pair
mentions one of these, the checker tries every case the two rules tell apart: both yes/no
values, and every inside/outside region of the named patterns.

| Field | Kind | Meaning | Source |
|---|---|---|---|
| `user_asked` | yes/no | the user explicitly asked for this action | tuning rules |
| `tests_passed` | yes/no | tests passed before the action | tuning rules |
| `after` | one yes/no per action | that action happened at some earlier point; several can be true. It does not mean "right after" | as in the checker now |
| `after_branch` | glob | branch of that earlier action | tuning rules |
| `running:<name>` | yes/no per name | process `<name>` is running; names match only if identical | survey: 6 folders |

Cut from v1: `actor` (one survey folder at most).

## 4. Path patterns

- Paths are relative to the repo root, with `/` and no leading `/`.
- `*` matches inside one folder level, `?` matches one character (not `/`), `**` matches any
  depth. This is the common wildcard subset of gitignore, GitHub rulesets and Claude Code
  permissions; the folder and bare-name rules below are our own fixed choices. Branch globs
  use the same meanings.
- A folder `X/` becomes `{include: ["X", "X/**"]}` in code: the folder itself and everything
  in it.
- For paths only, a name with no `/` (`server-world.dat`) matches at any depth: it becomes
  `**/server-world.dat`. A branch name like `main` stays exactly `main`. Code does this, not
  the translator.
- A placeholder filling one folder level (`XX-name`, `<id>`) becomes `*`.
- A target is `{include: [...], exclude: [...]}`: in the include patterns, minus the exclude
  patterns. Use `exclude` only for an exception written in the same rule ("never commit
  vendor/ except vendor/cmake"). An exception in another rule stays a separate rule.
- No `!` and no "last match wins": the order of patterns never matters.

## 5. Translation choices

Each row describes a **meaning**, not an exact phrase. The quoted English is an example; any
wording with the same meaning gets the same translation. Whether the translator does this the
same way each time is what the three-run agreement measures; the hand-checked sample checks
that it is right.

### 5a. Definitions (one reading, from what the words mean)

| Meaning (example wording) | Translation |
|---|---|
| X must not be in the repo ("keep X out of the repo") | `never_hold in_repo:X` |
| X must be in the repo ("X stays committed", "X must be in git") | `must_hold in_repo:X` |
| take X out of the repo ("remove X from git", "untrack X") | `never_hold in_repo:X` |
| stage X / never stage X | `must_do stage path:X` / `never stage path:X` |
| commit only when asked (no path) | `only_if commit needs user_asked` |
| edit or modify X (change what is in an existing file) | `edit` |
| don't create subfolders in X (any depth) | `never create path:X/** kind:dir` |
| don't create folders directly in X (one level only) | `never create path:X/* kind:dir` |
| run tests only when asked | `only_if run task:test needs user_asked` |
| always run all tests after a commit | `must_do run task:test suite:all after:commit` |
| with the user's approval / permission | `needs user_confirmed` |
| when the user asks / explicitly requests | `needs user_asked` |
| not while X runs | `never ... where running:X` |
| you may / can / are allowed to X | `may_do` (always strong permission, ADR 0003) |
| a group of files with no pattern ("player data", "generated files") | unmodeled, unless the folder gives the pattern; `when_unmodeled` is for unknown situations, not unknown targets |

Cut from v1: "X is gitignored" (git ignore rules do not affect files already tracked, so it
does not mean "not in the repo"); "copy S to D" (not one action; now unmodeled).

### 5b. Words to watch (read from context, flag if unclear)

These words often carry more than one meaning. The translator picks the meaning only when the
rule's own text makes it clear. If it does not, the translator writes `unclear: "<word>"`
and the rule is **excluded** from checking. The report lists every excluded rule and the
word, so the ambiguous choices stay visible.

| Word | Possible meanings |
|---|---|
| "write X", "save X" | create; edit; either |
| "add X" | create a file; edit a file; `git add` (stage) |
| "delete X" | delete; also moving X away |
| "remove X" | delete; move away; take out of git; remove content inside a file |
| "change X" | edit only; any file action |
| "touch X" | edit; any file action; the Unix `touch` command |
| "never commit X" (with a path) | don't commit changes to X; X must not be in the repo |
| "after a change" | after an edit; after any file action; after a commit |

Other words the translator cannot read one way are flagged the same way. The list is fixed
during a run and only changes between versions.

Lists are sorted and duplicates removed. Each `must_do` is its own clause: "must do A and B"
is two clauses, "must do A or B" is one clause with `cmd: [A, B]`.

## 6. Not expressible (marked unmodeled)

- Which files belong to a named group ("map data") unless the folder spells out a pattern.
- File contents beyond the yes/no fields ("only formatting changes"); copying with the same
  content.
- Action counts and longer time orders ("at most twice", "for a week", "until",
  "eventually", "right after"); `after` only says whether a named action happened earlier.
  Atomic multi-file changes.
- File modes (`100755`), symlinks and their targets, commit-message contents, which command
  form was used for staging (`git add -A` vs names).
- Purposes and judgment ("when appropriate", "if it makes sense").
- Which tool is used (MCP vs CLI), who performs the action, and whether two process or task
  names are the same thing.

## 7. Repository state

`in_repo:X` is a state, not an action: the path X is tracked in the repository at the end.
Git defines this state ("tracked"). A rule can require it (`must_hold`) or forbid it
(`never_hold`). Two rules clash if one requires and the other forbids it for overlapping
paths, in a situation both cover ("vendor/cmake stays committed" vs "keep vendor/ out of the
repo"). The checker does not link state to actions in this version: a rule about the
`commit` action and a rule about `in_repo` are not compared.

For checking, the solver picks one concrete path: `must_hold` and `never_hold` clash when one
path matches both targets. This is reported as its own verdict, **state conflict**, because
ADR 0003 defines clashes over a single action; amending ADR 0003 instead is open (section 9).

## 8. Changes needed in the checker and the prompt

1. Enumerate every situation field named by either rule (today "push only when asked" vs "the
   final step pushes to main" wrongly passes). Add this pair as a test.
2. Agreement check compares each `must_do` on its own (today "A and B" equals "A or B").
3. Compile `*`, `?`, `**` with the section 4 meanings, including the folder rule and the
   path-only bare-name rule (today `*` crosses folders).
4. A target is `in some include AND NOT in any exclude`.
5. Add the file actions, `stage`, `run` with `task`, and the fields in section 3.
6. Add `must_hold` / `never_hold` on `in_repo` (section 7).
7. Report `may_do` vs `never` / `must_do` pairs as their own category, "exception (needs a
   priority rule)", next to plain clashes.
8. Report rules excluded as `unclear`, with the word.
9. Prompt: `after` means "at some earlier point", not "right after"; running commands are now
   in scope (Step 1 says tests are not); one prompt for git and file rules, in separate
   sections.

## 9. Points still open

1. Decided (user): the translator no longer sees the folder's other rules. It sees only the
   rule, its file name and its section heading. Reason: other rules can make it soften a rule
   to fit them, hiding clashes. Rules that become unclear without context are counted.
2. Claims: say "solver-checked" (exact only with respect to the translations), not "exact".
3. Final test: the held-out rules were chosen by a git filter, so the held-out claim stays
   git-only; file rules are reported on the survey folders (agreement and hand check).
4. Decided (user): state conflicts are a separate verdict; ADR 0003 is not changed.
5. Decided (user): accept that "never commit vendor/" vs "vendor/cmake stays committed" is
   excluded as unclear unless the text says what "never commit" means.
