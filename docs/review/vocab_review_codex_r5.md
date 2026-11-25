## 1. Remaining issues

The checker’s current behavior differs from v2, but section 8 correctly identifies those implementation gaps. Do not describe v2 as implemented until they are completed.

Four specification issues remain:

- “One operation on at most one path” contradicts `move`, which has source and destination paths.
- ADR 0003 defines clashes over a single action; v2 additionally calls contradictory repository states clashes. The ADR must be extended or state contradictions given a separate verdict.
- `in_repo` lacks quantification for globs: whether `must_hold vendor/**` requires every matching existing path, at least one path, or a symbolic path witness.
- A named group such as “map data” cannot use `when_unmodeled`: that field represents an unknown situation, not an unknown target. Section 5a conflicts with section 6 here.

Strong `may_do`, separate obligations, and unclear-word exclusion are otherwise consistent with ADR 0003.

## 2. User examples under v2

| Example | Result |
|---|---|
| force push vs never force push | **Clash** |
| may delete merged branches vs never delete branches | **Clash**, reported as an exception/precedence interaction |
| never push without an explicit ask vs final step pushes to main | **Clash** in the `user_asked:false` situation |
| delete map data vs never delete `server-world.dat` | **Unmodeled**: membership in “map data” is unknown |
| object folder vs flat files/no subfolders | **Clash**: placeholder, directory kind, and depth rules suffice |
| never commit `vendor/` vs `vendor/cmake` stays committed | **Unclear-excluded** unless context establishes that “never commit” means repository absence; action-level commit and `in_repo` are intentionally unlinked |
| tests only when asked vs always run all tests | **Clash** in `user_asked:false` |
| If the latter says “after a change” | **Unclear-excluded** unless context resolves “change” |

Nothing dropped from v1 is needed to represent the examples that remain clashes.

## 3. Exact text changes

1. Replace “One action = one operation on at most one path” with:  
   **“One action operates on one target; `move` additionally names its destination.”**

2. Replace the named-group row in 5a with:  
   **“A group of files with no derivable pattern is unmodeled; do not use `when_unmodeled` for a missing target.”**

3. Add to section 7:  
   **“For state checking, the solver selects a concrete path. `must_hold` and `never_hold` clash when one selected path matches both targets.”**

4. Amend ADR 0003’s decision to cover both **action incompatibility** and **opposite final-state requirements**, or label the latter separately as `state_conflict`.

5. Replace “Same as gitignore, GitHub rulesets and Claude Code permissions” with:  
   **“This vocabulary uses the stated common wildcard subset; its folder and bare-name canonicalizations are defined below.”**