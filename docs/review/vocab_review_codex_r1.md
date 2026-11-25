## 1. Rule types

**AGREE**

## 2. Actions

**CHANGE**

Replace the git-family row with:

```markdown
| git | commit, stage, push_branch, push_delete, force_push, local_merge, pr_create, pr_merge, branch_create, branch_delete, checkout, pull, rebase, reset_hard, cherry_pick, fetch, worktree_add, worktree_remove |
```

Replace “git (as now)” with “git” in that row only. Leave the remaining action and group tables unchanged.

Reason: `stage` is necessary for surveyed rules that distinguish staging from committing; the existing actions cannot express that distinction.

## 3. Fields

**CHANGE**

Replace the `after` row with:

```markdown
| `after` | one yes/no per action, plus `change` | whether that action occurred earlier; more than one value may be true |
```

Replace the paragraph introducing situation fields with:

```markdown
**What the situation fixes** (the agent cannot change it). When either rule of a pair
mentions one of these, the checker enumerates every truth region induced by both rules:
both Boolean values, equality to each named actor, an unnamed-other actor, and every
inside/outside overlap region of the named globs.
```

Replace the `actor` row with:

```markdown
| `actor` | exact opaque name, or `agent` (default) | who performs the action; names are compared only for exact equality |
```

Reason: “right after” contradicts the current checker’s deliberately non-immediate predecessor model, and infinite strings must be checked through finite equivalence regions rather than literally “every value.”

## 4. Path patterns

**CHANGE**

Replace the second through fifth bullets with:

```markdown
- Wildcards have gitignore/fnmatch meaning: `*` matches within one segment, `?` matches
  one non-`/` character, and `**` crosses directory boundaries. Branch globs use the same
  wildcard meanings.
- A folder target `X/` canonicalizes in code to `{include: ["X", "X/**"]}` so that the
  directory itself and everything below it are covered.
- For paths only, a pattern with no `/` (`server-world.dat`) matches at any depth and
  canonicalizes to `**/server-world.dat`. A branch name such as `main` remains exactly `main`.
- A placeholder occupying one path segment (`XX-name`, `<id>`) canonicalizes to `*`.
```

Reason: `X/**` alone does not match an operation on directory `X`, and bare branch names must not receive path-style any-depth expansion.

## 5. Fixed translation choices

**CHANGE**

Replace the three repository-membership rows with:

```markdown
| "never commit X" / "keep X out of git" / "X is gitignored" | `never repo_include path:X` |
| "X stays committed" | `must_do repo_include path:X` and `never repo_remove path:X` |
| "X must be in git" | `must_do repo_include path:X` |
| "remove X from git" / "untrack X" | `must_do repo_remove path:X` |
```

Add:

```markdown
| "stage X" | `stage path:X` |
| "keep X unstaged" / "never stage X" | `never stage path:X` |
| "copy S to D" | separate `read path:S` and `create path:D` clauses; content equality is unmodeled |
```

Reason: “stays committed” must conflict both with exclusion and removal; staging is not committing, while copying can be decomposed without adding another atomic action.

## 6. Not expressible

**CHANGE**

Replace the counts/order bullet with:

```markdown
- Action counts and longer temporal sequences ("at most twice", "until", "eventually");
  `after` records only whether a named action occurred earlier.
```

Add:

```markdown
- Exact content preservation across a copy, specific metadata values such as mode `100755`,
  symlink targets, commit-message contents, and whether staging used a particular command form.
- Deployment, service restart and arbitrary command execution; only tests and builds are
  workflow actions in this vocabulary.
```

Reason: these boundaries are required by surveyed rules and prevent translators from inventing unsupported fields.

## 7. Checker changes this list needs

**CHANGE**

Replace the numbered list with:

```markdown
1. Enumerate every situation field named by either rule, using finite equality and glob-overlap
   regions for actor and string fields.
2. Agreement compares each `must_do` separately; two obligations are not one disjunction.
3. Compile `*`, `?` and `**` with the section 4 meanings, including the folder-root
   canonicalization and path-only bare-name rule.
4. Compile a target as `union(include) AND NOT union(exclude)`.
5. Add the new actions, groups and fields; make `kind` an enum and actor names exact strings.
6. Enforce the fixed action-group expansions in code, including `stage` as atomic.
```

Reason: these are the minimum implementation requirements for the proposed text to have one exact Z3 meaning.

## Survey rules exposing missing concepts

- “Stage every commit by explicit file name; never `git add` a directory, `-A` or `.`.” — `JHU-PL-Lab__tola`. The `stage` addition covers the operation, but the exact command form remains unmodeled.
- “No symlink from the repo into the depot” — `sid597__Softland`. Symlink type and link target are missing.
- “Whenever a PR merges to `main`, do a fresh restart of BOTH `--dev` servers” — `tartale__actual-tools`. Process restart is outside the proposed workflow actions.
- “check git file modes (100755 for executables)” — `M-s-Tech4TIME__project-wolf`. Exact file-mode values are missing.

## Open points

- `repo_include` and `repo_remove` describe repository state but are encoded as actions. Without a final-state variable, `must_do repo_include X` and `must_do repo_remove X` may both be satisfiable as separate events. I do not see a short textual fix; the checker needs either final repository membership or an explicit incompatibility rule.
- I am unsure whether `after` is intended to mean “immediately previous” or merely “occurred earlier.” I selected the latter because that matches the current checker and lets multiple prerequisites coexist.