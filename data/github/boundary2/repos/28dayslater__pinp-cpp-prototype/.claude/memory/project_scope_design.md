---
name: Sema/diagnostics foundations — completed
description: What was built in the semantic-analyses-foundations branch (merged to main)
type: project
---

Branch `semantic-analyses-foundations` merged to main 2026-03-30.

## What landed

- `ast.hh` / `parser.hh` split (was `interp.hh`); `parser.cc` (was `interp.cc`)
- `source_location.hh`: `SourceLocation{line, col}` and `SourceRange` on every AST node and statement type
- `SimpleAssign`: tuple → named struct
- `diagnostics.hh/cc`: `DiagConsumer` (abstract), `TextDiagConsumer` (stderr), `DiagnosticsEngine` (routes + tracks count + throws)
- `sema.hh/cc`: `Sema` pass invoked between parse and codegen; recursive visitor over all node/stmt types
- `ForRange` promoted to first-class type with `int64_t` bounds, `SourceLocation`
- `Sema::check_range()`: empty range and bad step ranges are errors

**Why:** Clang-style architecture — source locations → diagnostics → sema → codegen.
**How to apply:** Next sema checks go in the appropriate `Sema::check()` overload.
