---
name: parser-rewrite branch status
description: Active branch replacing PEGTL+grouper pipeline with a recursive-descent parser; tracks what is done and what remains
type: project
---

Active branch: `parser-rewrite`

**Why:** Replace the PEGTL action-based parser and grouper pre-pass with a hand-written recursive-descent parser (rd-parser.hh/cc). Cleaner architecture, easier to extend, grouper eliminated.

**Completed:**
- Full RD parser implemented (all expressions, statements, control flow, f-strings, arrays)
- Grouper (grouper.hh/cc) removed
- grammar.hh stripped to tokenisation reference only
- parser.hh/parser.cc gutted to empty stubs (still compiled — see open items)
- RD parser wired into JIT pipeline (jit.cc uses Lexer + Parser directly)
- repl.cc rewritten: completeness detection delegates to Parser in interactive mode via IncompleteInputError
- Multi-line argument lists and parameter lists handle Newline/Indent/Dedent inside open parens
- Type-cast calls int()/float()/str() recognised in parse_primary()
- PinpState extracted from PinpJIT: all accumulated interpreter state (fn_meta, global_vars,
  global_str_vars, live_globals, counters, scratch_str, diags) lives in PinpState owned by main.cc
- PinpJIT is now a pure compilation engine; eval()/eval_program() take PinpState & as first arg
- fn_meta, global_vars, global_str_vars, live_globals migrated to unordered_map/unordered_set
- Lexer::tokenize(bool interactive=false): interactive mode skips EOF Dedent injection so the
  parser can signal IncompleteInputError for incomplete blocks (REPL completeness check)
- TestJIT wrapper in test-helpers.hh: bundles PinpJIT + PinpState, exposes old single-arg interface

**Open items:** none — branch is ready to merge.

**How to apply:** When resuming work, pick up from the open items above.
