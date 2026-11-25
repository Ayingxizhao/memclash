## 1. Prior art for the vocabulary

| System | Actions and targets | Conditions | Conflict resolution |
|---|---|---|---|
| **Claude Code permissions** | Rules are `Tool` or `Tool(specifier)`: `Read(path)`, `Edit(path)`, and command-text `Bash(...)`. `Edit` covers built-in file-writing tools; `Read` denies also block writes on the same path. File targets use gitignore-style patterns: rooted, home-relative, or working-directory-relative; `*` stays within a segment and `**` crosses directories. Bash uses textual `*`, not path-aware matching. | Three effects—`allow`, `ask`, `deny`—plus permission modes. Some rules can test one top-level tool parameter. | Evaluation is **deny, then ask, then allow**, regardless of specificity. Negated path patterns can carve exceptions only within the same source and in order. [Claude Code permissions](https://code.claude.com/docs/en/permissions) |
| **Codex sandbox/approvals** | Fixed capability modes: `read-only`, `workspace-write`, and `danger-full-access`; workspace mode has explicit writable roots and a separate network switch. The unit is a command/tool call, with filesystem and network boundaries enforced outside the model. | `approval_policy` is `on-request`, `never`, or granular by prompt category. Approval decides whether an attempted escalation pauses; it does not itself enlarge the sandbox. | Managed requirements restrict available modes; a deny from managed or local policy can win. This is capability intersection, not “most-specific path rule.” [Official OpenAI configuration reference](https://developers.openai.com/codex/config-reference) |
| **`.gitignore`** | Controls whether untracked paths are ignored. Patterns are directory-relative; `/` anchors, a trailing `/` denotes a directory, `*` excludes `/`, and `**` spans directories. | No actors or runtime conditions. `!` re-includes, except that a file cannot be re-included beneath an excluded parent directory. | Source precedence applies; within one level, the **last matching pattern wins**. Already tracked files are unaffected. [gitignore](https://git-scm.com/docs/gitignore) |
| **`.gitattributes`** | Assigns attributes such as `text`, `diff`, and `merge` to paths. It mostly uses gitignore matching, but forbids negative patterns and directory matches are not recursive without `/**`. | Each attribute is set, unset, assigned a string, or made unspecified. | Later matching lines override earlier ones **per attribute**; nearer and repository-specific sources have precedence. [gitattributes](https://git-scm.com/docs/gitattributes) |
| **GitHub rulesets / branch protection** | Fixed operations and requirements include creation, update, deletion, force-push, PR/status-check requirements, and push restrictions on file paths. Branch and path targets use `fnmatch`; `*` does not cross `/`. Metadata restrictions may use RE2 regexes. | Target includes/excludes, actor/role/app bypass lists, required reviews, checks, deployments, and similar fixed predicates. | All matching rulesets and branch protection are aggregated; the **most restrictive** version applies. Rulesets have no priority. [Ruleset layering](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets), [target syntax](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository) |
| **Cedar** | Every request has a typed `principal`, `action`, and `resource`. Scope uses equality or hierarchy membership rather than arbitrary command parsing. A schema fixes entity/action types and attributes. | Boolean `when` and `unless` expressions over principal, resource, action, and request context. | Default deny; at least one permit is required, and **any matching forbid overrides permits**. Cedar therefore cannot directly represent this project’s strong permission or “must do.” [Cedar policy syntax](https://docs.cedarpolicy.com/policies/syntax-policy.html) |
| **AppArmor** | File rules attach `r`, `w`, append, execute, mmap, lock, and link permissions to absolute path expressions. Its AARE glob syntax distinguishes files and directories; write currently implies creation, deletion, chmod, and chown. | Profiles identify the program/actor; `owner` restricts a rule to files owned by the process identity. Ordinary Unix discretionary permissions must also allow access. | Profiles are allowlists/default-deny; explicit deny rules subtract permissions and take precedence over allows. [AppArmor rule basics](https://apparmor-documentation-c38b15.gitlab.io/documentation/getting-started/rules-basics/), [core policy reference](https://apparmor-documentation-c38b15.gitlab.io/documentation/in-depth/profiles/core-policy-reference/) |
| **POSIX/Linux ACLs** | Per-file/inode `read`, `write`, and execute/search permissions for the owner, named users, owning group, named groups, and others. There are no globs. | Effective UID, group memberships, and an ACL mask. Default directory ACLs affect newly created children. | A fixed lookup order selects owner, named-user, group, or other entries; the mask limits named-user/group grants. It is neither deny-wins nor last-match. [acl(5)](https://man7.org/linux/man-pages/man5/acl.5.html) |

The recurring design is a fixed request tuple, a deliberately limited matcher, and an explicit combining algorithm. None asks a solver to infer that an arbitrary tool spelling means “delete.”

## 2. Fixed or extensible schema?

Use a **fixed, versioned schema**, with extensibility only in opaque names such as paths, actor IDs, branch names, and activity IDs.

Exact checking requires fixed meanings for action subsumption (`force_push` is a push), path intersection, and which facts describe the environment rather than an agent’s choice. Three-run agreement also becomes uninterpretable if translations can invent `remove_tree`, `purge`, and `erase` as unrelated actions or invent logically equivalent predicates.

Prior art supports this choice: GitHub, Cedar, ACLs, and AppArmor fix the action/permission vocabulary; their extensibility is principally in resource names and attributes. Even Rego-like open predicates would merely move semantic translation into relation-name invention.

New concepts should be added through reviewed schema versions, not free-form relation types. Preserve `when_unmodeled`, but give repeated unmodeled phrases a canonical shared ID when possible.

## 3. Concrete schema proposal

Retain `never`, `only_if`, `must_do`, and strong `may_do`. Add these fixed actions to the existing Git actions:

- File: `read`, `create`, `modify`, `move`, `delete`, `repo_include`, `repo_remove`.
- Workflow: `test`, `build`.

`modify` means content or metadata modification, **not move/rename**. `move` has both `source_path` and `path` (destination). Directory creation/deletion uses the same actions with `kind: directory`; a bulk deletion is evaluated once per matched descendant. Do not make `write` an action: translate it deterministically to `create`, `modify`, or both when genuinely ambiguous.

`repo_include(path)` means the path is present in the resulting committed tree, not merely that `git commit` was invoked. Thus:

- “keep `vendor/` out of git” → `never repo_include vendor/**`;
- “`vendor/cmake` stays committed” → `must_do repo_include vendor/cmake/**`;
- “remove it from git” → `must_do repo_remove`.

This makes repository membership conflict-checkable while leaving the existing `commit` command action available for rules about committing, approval, or sequencing.

Paths are normalized repository-relative POSIX strings. Use one matcher only:

- exact literal, or glob where `*` excludes `/`, `?` matches one non-`/` character, and `**` crosses directories;
- directory targets canonicalize to `dir/**`;
- a target is `{include: [...], exclude: [...]}`.

Do **not** permit gitignore-style `!` or order dependence. Exceptions go into `exclude`, which denotes set subtraction.

Fixed fields should be:

```text
action, path, source_path, kind(file|directory), branch,
actor, activity, suite, user_asked, user_approved,
activity_running, after_change, tests_passed, when_unmodeled
```

`actor` is an exact opaque ID or one of `agent`, `user`, `any`; “only by agent X” becomes an `only_if` requiring that actor. Activity names are opaque: “not while X runs” is a `never` clause with `activity=X, activity_running=true`. “Tests only when asked” is `only_if test -> user_asked`; “always run all tests after a change” is `must_do test, suite=all, after_change=true`.

For Z3, use finite enumerated sorts for `Action` and `Kind`; strings for paths, actors, branches, suites, and activity IDs; and Booleans for conditions. Compile globs to Z3 regular languages and targets to `union(include) \ union(exclude)`. Encode action groups as fixed disjunctions. Situation variables such as `user_asked`, `after_change`, and `activity_running` are world facts; path, action, and actor are event fields. `must_do` requires an event in every named situation; `may_do` requires each explicitly permitted action to remain satisfiable; `never` and `only_if` constrain events.

Keep unexpressible: natural-language purposes (“when appropriate”), arbitrary tool choice, causal claims, deadlines, counts/sequences beyond one named predecessor, simultaneous multi-file atomicity, file contents except fixed booleans, and semantic relationships among opaque activities. Temporal rules such as “until,” “eventually,” or “while two processes overlap” need a later trace model.

## 4. Literature on conflict detection

- **Al-Shaer, Hamed & Boutaba (2005), “Conflict Classification and Analysis of Distributed Firewall Policies.”** Detects shadowing, correlation, generalization, redundancy, and irrelevance by overlap and order of packet predicates; ours additionally has obligations and strong permissions. [Full paper](https://rboutaba.cs.uwaterloo.ca/Papers/Journals/2005/Ehab05.pdf)
- **Fisler et al. (2005), “Verification and Change-Impact Analysis of Access-Control Policies.”** Margrave translates XACML/RBAC policies to decision diagrams for property queries and semantic differencing; ours compares independently translated natural-language norms and includes `must_do`. [Paper page](https://static.cs.brown.edu/~sk/Publications/Papers/Published/fkmt-verif-change-impact-xacml/)
- **St-Martin & Felty (2016), “A Verified Algorithm for Detecting Conflicts in XACML Access Control Rules.”** Proves in Coq an algorithm finding overlapping permit/deny rules; ours uses solver witnesses and treats explicit permission-versus-prohibition as a reportable clash. [Full paper](https://www.site.uottawa.ca/~afelty/dist/cpp16.pdf)
- **Turkmen et al. (2017), “Formal Analysis of XACML Policies Using SMT.”** Encodes XACML, combining algorithms, non-Boolean attributes, and properties such as separation of duty in SMT; ours has a smaller language but an uncertain LLM translation front end. **Abstract only inspected.** [Article](https://doi.org/10.1016/j.cose.2017.01.009)
- **Vasconcelos, Kollingbaum & Norman (2009), “Normative Conflict Resolution in Multi-Agent Systems.”** Uses unification and constraint solving for overlapping prohibitions versus obligations or permissions; this is closest to the project’s strong-permission semantics, though ours fixes the domain vocabulary. [DOI](https://doi.org/10.1007/s10458-008-9070-9)

## 5. Risks

Translations will still diverge on action force (“can” as permission versus ability), path scope, whether “write” includes creation, directory-versus-contents readings, actor identity, exceptions, and whether a phrase is a condition or rationale. Clause splitting is another risk: one conjunction and two independent obligations are not equivalent.

Reduce this with a decision table, canonical directory and glob forms, no optional synonyms, explicit defaults, sorted/deduplicated lists, and deterministic rewrites for “keep out of git,” rename, and approval. Reject internally unsatisfiable translations. Compare normalized meanings, including each obligation separately; an `Or` of all `must_do` clauses can incorrectly erase the difference between one obligation and several.

Three-run semantic agreement shows repeatability under the schema and prompt. It does **not** show correctness against the English, coverage of omitted concepts, soundness of the clash definition, or external validity on unseen folders. High agreement can simply mean a stable shared mistranslation.

- Fix actions, fields, glob semantics, and combining semantics in code.
- Extend only opaque entity names; version reviewed additions to the vocabulary.
- Keep rename separate from edit and model repository membership explicitly.
- Compile positive include/exclude path sets to Z3 regexes; avoid ordered negation.
- Report translation agreement alongside human accuracy and expressibility coverage.