# Project Memory

## Style
- [feedback_test_descriptions.md](feedback_test_descriptions.md) — Capitalise first char of TEST_CASE descriptions; exception: starts with a language keyword
- [feedback_naming.md](feedback_naming.md) — Filenames use `-` not `_` (e.g. `0003-do.md`)
- [feedback_spec_sections.md](feedback_spec_sections.md) — Spec files have [Human]/[AI] sections; write analysis under [AI]
- [feedback_no_param_letter_in_comments.md](feedback_no_param_letter_in_comments.md) — Don't write `M`/`F`/`B`/`V` in comments; spell out "the module", "the function", etc.

## C++ style
- [feedback_inline_methods.md](feedback_inline_methods.md) — Inline methods: ≤4 lines, no loops; else define in .cc
- [feedback_unordered_map.md](feedback_unordered_map.md) — Use `unordered_map` for all symbol tables; `map` is never needed for name→value lookups
- [feedback_method_spacing.md](feedback_method_spacing.md) — Empty line between every method in a class body
- [feedback_loop_style.md](feedback_loop_style.md) — Infinite loops: always `do { ... } while (true)`, never `while(true)` or `for(;;)`
- [feedback_string_view.md](feedback_string_view.md) — Prefer `std::string_view` over `std::string` wherever ownership is not required
- [feedback_m_prefix.md](feedback_m_prefix.md) — `m_` prefix only on private/protected `class` members; never on `struct` fields

## Changelog
- [feedback_changelog_milestones.md](feedback_changelog_milestones.md) — Version bumps tied to a GH milestone should link to it in the CHANGELOG entry

## Active branch
- [project_parser_rewrite.md](project_parser_rewrite.md) — parser-rewrite branch: RD parser replacing PEGTL+grouper; lists completed work and open items

## Next iterations
- [project_next_iterations.md](project_next_iterations.md) — Issues #1–#4 from near-code-improvements.md are the planned iteration targets (scope/parser/op-enum/codegen split); item #2 is now moot (old parser gone)

## Workflow
- [feedback_branch_policy.md](feedback_branch_policy.md) — Never commit directly to main; all changes (even chores) need a branch, merged only after user approval
- [feedback_branch_focus.md](feedback_branch_focus.md) — Warn user when a requested change is out of scope for the current branch
- [feedback_fixme_policy.md](feedback_fixme_policy.md) — Out-of-scope quality issues get a detailed FIXME comment and are deferred; in-scope issues are fixed immediately
- Always run `clang-format -i` on any C/C++ file after writing or editing it
- [feedback_no_autocommit.md](feedback_no_autocommit.md) — Do not auto-commit; wait for user to say so explicitly
- [feedback_formatting.md](feedback_formatting.md) — 100-column line limit (not 80)
- [feedback_workflow.md](feedback_workflow.md) — Red→Green→Refactor: tests first, then implement, then clean up together
- [feedback_sync.md](feedback_sync.md) — Only push to GitHub when user says "sync"; commit freely otherwise
- [feedback_commit_no_metrics.md](feedback_commit_no_metrics.md) — No benchmark numbers, binary sizes, or "N/N tests pass" lines in commit messages; those belong in the spec

## Build / environment
- [feedback_worktree_llvm_install.md](feedback_worktree_llvm_install.md) — New git worktrees of parserkg/ need `third_party/llvm-install/` symlinked from the canonical worktree; cmake silently falls back to system LLVM otherwise and link fails cryptically

## Design (pending implementation)
- [project_string_layout.md](project_string_layout.md) — 16-byte string struct with SSO + mutability flag; custom layout required for AOT compatibility

## Architecture
- [project_aot_compiler.md](project_aot_compiler.md) — Future AOT compiler alongside JIT; JIT stays for REPL/scripts; shared codegen must live on CodegenContext
- [project_scope_design.md](project_scope_design.md) — Sema/diagnostics foundations merged to main (2026-03-30): source locations, DiagnosticsEngine, Sema pass, ForRange

## Architecture (decisions)
- [project_todo_semantic_passes.md](project_todo_semantic_passes.md) — Second semantic optimisation triggers extracting all such passes (incl. str-concat) into a dedicated pass layer before codegen

## TODOs
- [project_todo_bootstrap.md](project_todo_bootstrap.md) — Automate LLVM submodule bootstrap before pinp goes public
- [project_todo_pinpstr_anon_union.md](project_todo_pinpstr_anon_union.md) — Name the union in PinpStr to fix -Wgnu-anonymous-struct; do at start of next strings iteration
