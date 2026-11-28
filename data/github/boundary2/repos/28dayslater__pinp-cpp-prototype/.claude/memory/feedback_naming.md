---
name: Naming conventions — files and identifiers
description: Filenames use hyphens; all identifiers must be readable by a non-expert human
type: feedback
---

## Filenames

Use `-` (hyphen) instead of `_` (underscore) in all project filenames — specs, docs, and test `.cc` files (e.g. `0003-do.md`, `0003-do.cc`).

**Why:** User extended the convention from spec files to test files for consistency.

**How to apply:** Any new file in `specs/`, `tests/`, or elsewhere should use hyphens as word separators.

## Identifier readability

All identifiers — rule names, variables, functions, types — must be readable by an average human who is not a compiler expert. No unexplained abbreviations.

**Why:** The codebase should be approachable without domain knowledge.

**How to apply:**
- Write `str_literal` not `str_lit`
- Write `float_literal` not `float_lit`
- Write `lex_grammar` not `lg`
- When in doubt, use the full English word.
- Universally understood short forms are fine: `src`, `dst`, `buf`, `idx`, `pos`, `loc`, `op`, `lhs`, `rhs`.
