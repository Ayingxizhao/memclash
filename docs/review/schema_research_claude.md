# Schema research: one fixed format for git and file rules

Reviewer: Claude (independent). Read: README, ADR 0002–0004, `pipeline/git/git_check.py`,
`prompts/git/git_translate.md`. Not read: `data/gold/`, `labels_*`, the Codex report.
One local check was run with the existing checker (no LLM call), reported in 3.6.

## 1. Prior art for the vocabulary

| System | Actions | Target matching | Conditions | Conflict resolution |
|---|---|---|---|---|
| Claude Code permissions ([docs](https://code.claude.com/docs/en/permissions)) | tools: `Read`, `Edit` (covers every built-in write tool; `Write(..)` paths are not matched, use `Edit`), `Bash(cmd prefix *)`, `WebFetch(domain:..)` | Read/Edit paths use **gitignore syntax** with four anchors (`//abs`, `~/`, `/settings-root`, `./cwd`); bare names match at any depth; `*` = one segment, `**` = any depth; `!` negation carves out of earlier deny rules from the same source. Bash: literal prefix + `*` wildcard, after splitting `&&`, `;`, `|` | none in the rule itself; modes (plan, auto, bypass) and hooks | **deny, then ask, then allow; first match in that order; "specificity doesn't change the order"**. An allow can't carve an exception out of a deny |
| Codex sandbox + rules ([approvals](https://learn.chatgpt.com/codex/agent-approvals-security), [rules](https://learn.chatgpt.com/codex/rules)) | sandbox modes `read-only` / `workspace-write` / `danger-full-access`; approval `on-request` / `never` / `granular`; command rules decide `allow` / `prompt` / `forbidden` | writable roots (workspace, /tmp); `.git`, `.codex`, `.agents` protected read-only recursively; `prefix_rule(pattern=[argv tokens])` | `match`/`not_match` example tests checked at load time | **most restrictive wins** (`forbidden > prompt > allow`), per part of a split compound command |
| gitignore ([docs](https://git-scm.com/docs/gitignore)) | one: "untracked file is ignored" | `*` and `?` stop at `/`; `**/`, `/**`, `a/**/b`; trailing `/` = directory only; leading or middle `/` anchors to the file's directory | none | **last match wins** within a file; deeper files override shallower; `!` re-includes, but **not under an excluded parent directory**; tracked files are not affected |
| gitattributes ([docs](https://git-scm.com/docs/gitattributes)) | per-attribute set / unset / value / unspecified | gitignore patterns, but **negation forbidden** and a directory pattern does not recurse (use `dir/**`) | none | later line overrides earlier, per attribute |
| GitHub rulesets ([about](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets), [rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)) | restrict creations / updates / deletions, block force pushes, require PR, require status checks, linear history, signed commits; push rules: restrict file paths / extensions / size | `fnmatch` on branch, tag and file paths (`test/demo/**/*`); file-path exceptions also fnmatch | **bypass actors** (roles, teams, apps) | rulesets have no priority; all apply; **most restrictive version** of the same rule wins |
| AWS IAM ([eval logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)) | `service:Action` strings | ARN with `*`, `?` | `Condition` operators on context keys | default deny; **explicit deny overrides allow**; boundaries and SCPs intersect |
| Cedar ([syntax](https://docs.cedarpolicy.com/policies/syntax-policy.html), [operators](https://docs.cedarpolicy.com/policies/syntax-operators.html)) | `action == / in [..]` with action groups via `in` | entity hierarchy (`resource in Folder::"x"`), `like` with `*` only (no regex) | `when` / `unless` boolean expressions over typed context | default deny; **forbid always overrides permit** |
| OPA/Rego ([docs](https://www.openpolicyagent.org/docs/policy-language)) | whatever the policy defines | any built-in (string, glob, regex) | arbitrary Datalog-like rules | none built in: incremental rules are OR-ed; a complete rule with two values is a **runtime conflict error**; `else` gives order; `default` gives fallback |
| AppArmor ([apparmor.d(5)](https://manpages.ubuntu.com/manpages/noble/man5/apparmor.d.5.html)) | `r w a l k m` + exec modes `ix px cx ux` | `*` (no `/`), `**`, `?`, `[..]`, `{a,b}`; **trailing `/` needed to match a directory** | `owner` qualifier (euid = file owner) | `deny` rules exist; the man page I read does not state the precedence (I believe deny wins, not verified) |
| SELinux file contexts ([Fedora wiki](https://fedoraproject.org/wiki/SELinux/ManagingFileContext), [semanage-fcontext(8)](https://www.man7.org/linux/man-pages/man8/semanage-fcontext.8.html)) | labels a path; allow rules are on types | full POSIX regex | none on the path rule | policy rules: **most specific** (longer string, has type); local rules: first match, newest first (sources disagree) |
| POSIX ACL ([acl(5)](https://www.man7.org/linux/man-pages/man5/acl.5.html)) | `r w x` | one inode (plus default ACL for new entries in a directory) | identity: owner, named user, group, other; mask caps | **fixed check order, first matching class decides**, else deny |

What this shows for us:
- Every system fixes the action list in code; only Rego leaves it open, and Rego is the one
  with no built-in conflict semantics.
- File targets are almost universally gitignore/fnmatch globs where `*` stops at `/` and `**`
  crosses it; regexes appear only in SELinux.
- Conditions are a small fixed set of typed context keys (IAM, Cedar), or identity classes
  (ACL, rulesets' bypass actors, AppArmor `owner`).
- All of them **resolve** conflicts by a combining rule (deny wins, most restrictive, last
  match, most specific). We must **detect** them, so we should not import any combining rule:
  an exception ("vendor/cmake stays committed") must stay visible as a clash with the general
  rule, consistent with ADR 0003.

## 2. Fixed or extensible schema?

Recommendation: **fixed in code** (actions, groups, fields, glob semantics), with one
controlled opening: **free condition names** that are shared across rules after normalization.

Reasons:
- Exact checking needs known semantics. Zelkova and Cedar's analyzer are exact because the
  language is closed (Cedar's paper presents analyzability as a design goal that limits
  expressiveness). An open relation set ("A implies B", supplied by the LLM) brings back the
  `verify_pair.py` problem: the answer is only as good as the LLM's relation facts.
- Measurable agreement needs a closed vocabulary. `same_meaning` compares formulas; with an
  open list of action names, two runs that write `remove_file` vs `delete` disagree for a
  naming reason, not a meaning reason, and Z3 cannot tell.
- The open part that is unavoidable is the name of a process or condition ("while the server
  runs", "during a backlog sweep"). Treat those as uninterpreted booleans keyed by a normalized
  name, so two rules that name the same condition share one fact. This also fixes the ADR 0004
  blind spot. It does not require understanding tool names, only string equality.

## 3. Concrete schema proposal

### 3.1 Actions and groups (one event = one action on one path)

| Family | Atomic actions | Groups |
|---|---|---|
| file | `read`, `create`, `write` (change content, incl. append and overwrite), `rename` (source path), `delete` | `modify` = create, write, rename, delete (like Claude Code's `Edit` and Codex `workspace-write`); `remove` = delete, rename (the old path stops existing) |
| git (existing) | commit, push_*, merge, branch_*, ... | as now |
| git on paths | `commit` (existing, `path` = committed file), `untrack` (`git rm --cached`, or removing from the index) | none |
| run | `run_tests`, `run_build` | `run` = both |

Choices, with my uncertainty:
- "edit X" maps to `write` only; "change/modify/touch X" maps to `modify`. Rename is in
  `modify` and `remove` but not in `write`, so "never edit config.json" does not forbid
  renaming it. This is a judgment call; POSIX treats rename as a directory write, Claude Code
  treats all as `Edit`.
- **"keep X out of git"** = `never commit path:X` (canonical form; the prompt fixes it).
  Adding X to `.gitignore` is a `write` on `.gitignore` and need not be modelled.
- **"X stays committed"** = `never untrack path:X` plus `may_do commit path:X` (strong
  permission: committing changes to X must stay possible). Then "never commit vendor/**" vs
  "vendor/cmake/** stays committed" clashes by glob overlap, as intended.
- `read` is included because "never read .env" vs "load .env to check keys" is a real pair,
  and every prior-art system has it.

### 3.2 Fields

| Field | Sort | Who fixes it | Notes |
|---|---|---|---|
| `cmd` | Int (enum index) or Z3 enum datatype | agent | as now |
| `path` | String | agent | glob target; replaces `file` |
| `is_dir` | Bool | agent | for "no subfolders" / "create dir X/" |
| `actor` | String, equality only | world | `"self"` unless named; "only the release agent may X" = `only_if cmd X needs actor:"release-agent"` |
| `user_asked` | Bool | **world** | the user explicitly asked |
| `user_confirmed` | Bool | agent (it can ask) | approval / permission |
| `tests_passed` | Bool | world | as now |
| `after` | Bool per action | world | add `modify` as an "after" value: "after a change, run all tests" |
| `running` | Bool per normalized name | **world** | "not while the server runs" = `never ... where running:"server"` |
| `has_secret`, `branch`, ... | as now | | |

### 3.3 Glob semantics (what Z3 needs)

Adopt gitignore/fnmatch semantics, the same as Claude Code's Read/Edit rules and GitHub push
rules:
- Paths are repo-relative, no leading `/`. Directories are written `dir/**` (gitattributes
  style), never `dir/`.
- `*` = `Star(seg)` where `seg = Intersect(AllChar, Complement(Re("/")))` (or
  `Range` pieces): one segment. `**/` = `Option(Concat(Star(AllChar), Re("/")))`; trailing
  `/**` = `Concat(Re("/"), Plus(AllChar))`. `?` = one `seg` char.
- A pattern with no `/` matches at any depth: `server-world.dat` becomes `**/server-world.dat`
  (gitignore rule). The normalizer, not the LLM, applies this.
- **No `!` negation.** Exceptions are separate clauses, so they show up as clashes.
- Note: the current `glob_re` maps `*` to `Full` (crosses `/`). Changing it changes branch
  matching (`feat/*` vs `feat/a/b`); GitHub's fnmatch `*` also does not cross `/`, so the
  change is consistent, but the selftest should be rerun.

Example: "objects are game/objects/XX-name.c, no subfolders" =
`never create where path:"game/objects/*/**"` plus `never create where is_dir:true,
path:"game/objects/*"`; "create game/objects/XX-name/" = `must_do create is_dir:true
path:"game/objects/*"` (the `XX-name` placeholder becomes `*`, a fixed prompt rule). Clash.

"delete all map and player data" (`must_do delete path:"<unknown>"`) vs "never delete
server-world.dat without permission": the first rule has no path pattern the model can use,
so it needs `when_unmodeled`/a named class ("map data"). This pair is **not exact-checkable**
unless the folder states which files are map data; say so rather than guess.

### 3.4 Clause types

Keep `never`, `only_if`, `must_do`, `may_do`, `when_unmodeled` unchanged. No new types.

### 3.5 What stays unexpressible

Which files count as "player data" or "generated"; counts and order beyond one `after` step;
time ("for a week"); content of a change ("only formatting"); tool choice (MCP vs CLI);
process identity beyond string equality ("the dev server" vs "npm run dev" stay different).

### 3.6 A gap I found in the current checker

`situations()` enumerates only fields the tested clause itself names. World facts named only
by the *other* rule stay free, so the solver can pick them. I ran (no LLM):

```
only_if push needs user_asked:true   vs   must_do push branch:main   -> compatible
```

That is the README's own example ("never push without an explicit ask" vs "the final step
pushes to main"), and it should be a conflict. Fix: split fields into world-fixed and
agent-chosen, and enumerate every world field (`user_asked`, `tests_passed`, `running:*`,
`actor`, `after`) named by **either** rule. `user_confirmed` stays agent-chosen, because the
agent can ask. Please verify against the existing test runs before relying on this.

## 4. Literature on conflict detection

1. Al-Shaer, Hamed, Boutaba, Hasan, "Conflict Classification and Analysis of Distributed
   Firewall Policies", IEEE JSAC 23(10), 2005
   ([pdf](https://rboutaba.cs.uwaterloo.ca/Papers/Journals/2005/Ehab05.pdf)). Classifies
   shadowing, correlation, generalization, redundancy between ordered 5-tuple rules. Ours has
   no order and no single allow/deny effect; obligations (`must_do`) have no firewall
   counterpart. *Read the abstract and first page only.*
2. Fisler, Krishnamurthi, Meyerovich, Tschantz, "Verification and Change-Impact Analysis of
   Access-Control Policies" (Margrave), ICSE 2005
   ([page](https://cs.brown.edu/~sk/Publications/Papers/Published/fkmt-verif-change-impact-xacml/)).
   XACML to decision diagrams; property checks and semantic diff of two policy versions. Its
   semantic diff is close to our `same_meaning`; it does not handle obligations. *Summary only.*
3. Hu, Ahn, Kulkarni, "Discovery and Resolution of Anomalies in Web Access Control Policies",
   IEEE TDSC 10(6), 2013 ([pdf](https://cse.buffalo.edu/~hongxinh/papers/TDSC2013.pdf)).
   BDD-based segmentation of XACML rules into conflict and redundancy regions. Same "find the
   overlapping region" idea as our witness; their rules come pre-structured, ours come from an
   LLM. *Abstract only.*
4. Backes et al., "Semantic-based Automated Reasoning for AWS Access Policies using SMT"
   (Zelkova), FMCAD 2018 ([pdf](https://cs.utexas.edu/~hunt/FMCAD/FMCAD18/papers/paper3.pdf)).
   Encodes IAM policies (including `*` wildcards as string constraints) into SMT and checks
   "is A at most as permissive as B". Closest technically to ours (SMT + string globs); it
   compares permissiveness, not obligation vs prohibition. *Abstract and summaries only.*
5. Vasconcelos, Kollingbaum, Norman, "Normative conflict resolution in multi-agent systems",
   JAAMAS 19(2):124–152, 2009 ([dblp](https://dblp.org/rec/bibtex/journals/aamas/VasconcelosKN09)).
   Detects prohibition vs obligation/permission overlap on first-order norms with constraints,
   then resolves by curtailing. Ours is the same deontic notion, but rules come from free text
   translated one at a time. *Citation and secondary summaries only; not read.*
6. Cutler et al., "Cedar: A New Language for Expressive, Fast, Safe, and Analyzable
   Authorization", OOPSLA 2024 ([arXiv](https://arxiv.org/abs/2403.04651)). Argues for a
   closed language so analysis is sound and complete. Supports our "fixed schema" choice.
   *Abstract only; I did not confirm the SMT details.*

## 5. Risks

What will make 3 runs disagree even with a fixed schema:
- **Group vs atom choice**: `write` vs `modify`, `delete` vs `remove`, `push` vs `push_branch`.
  Fix: a word-to-name table in the prompt (as for git) and canonicalize after parsing.
- **Glob spelling**: `vendor/`, `vendor/*`, `vendor/**`, `**/vendor/**`. Fix: normalize in
  code (strip `./`, `dir/` → `dir/**`, no-slash → `**/x`); `same_meaning` then compares
  regex languages, so equal spellings agree anyway, but different ones don't.
- **Optional fields** (`is_dir`, `actor:"self"`, `user_confirmed:false` for "immediately").
  Each optional field is a coin flip. Fix: defaults in code, fewer fields, and a rule "omit
  unless the rule states it".
- **Splitting**: one clause vs two ("keep out of git" as never-commit only, or also
  never-untrack). Fix: fixed patterns for common phrases, like the existing two.
- **`when_unmodeled` text**: free text that differs per run. Under the proposed shared names,
  `"during sweep"` vs `"backlog sweep"` become different facts. Fix: normalize (lowercase,
  stem) and compare names only through a small synonym step, or exclude these from agreement
  and report them separately.
- **`fits` borderline** (is "run tests only when asked" a git/file rule?). Fix: a separate
  filter decision, measured on its own.

What agreement shows and does not show:
- It shows **stability**: the translator gives the same meaning each time, so clash verdicts
  will not flip between runs.
- It does **not** show **correctness**: three runs can agree on the same wrong reading
  (dropped condition, wrong group). Agreement is an upper bound on trust, not a measure of it.
- Because runs share the prompt and model, agreement is inflated relative to an independent
  translator. Rewording pairs (already in `consistency`) and a small hand-checked sample of
  translations are needed to measure correctness.
- Agreement is measured per rule; a clash depends on two rules, so per-pair verdict stability
  (run the check on each of the 3 translation sets) is the number that matters for results.

## Summary

- Prior art (Claude Code, Codex, gitignore, GitHub rulesets, IAM, Cedar, AppArmor, ACL) fixes
  actions in code, matches files with gitignore/fnmatch globs (`*` one segment, `**` any
  depth), and *resolves* conflicts (deny wins / most restrictive / last match); we must
  *detect* them, so no combining rule and no `!` negation.
- Use a fixed schema: file actions `read, create, write, rename, delete` with groups
  `modify` and `remove`, git `commit`/`untrack` on a `path`, `run_tests`/`run_build`; fields
  `path`, `is_dir`, `actor`, `user_asked`, `user_confirmed`, `after`, and shared named
  `running:*` conditions. Same four clause types.
- "Keep out of git" = never commit; "stays committed" = never untrack + may commit; Z3 needs
  String paths with segment-aware regex globs, booleans, and an enum for actions. Class words
  ("map data") stay unexpressible.
- Bug found with the current checker: "push only if the user asked" vs "must push to main" is
  reported compatible, because world facts named only by the other rule are left free; enumerate
  world fields named by either rule.
- Run-to-run agreement measures stability, not correctness; reduce disagreement with
  code-side canonicalization of globs and groups and fewer optional fields, and also report
  per-pair verdict stability plus a hand-checked sample.
