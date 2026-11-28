---
name: Next iteration scope (near-code improvements)
description: Issues #1–#4 from near-code-improvements.md are the planned iteration targets
type: project
---

The following items from `near-code-improvements.md` are the scope of upcoming iterations, in priority order:

1. **Scope duplication** — unify Sema::Scope and Codegen::Scope traversal logic (`src/sema.hh:53`, `src/codegen.hh:16`)
2. **Parser state stack fragility** — wrap parallel call stacks into a single struct, add consistency assertions (`src/parser.hh:19–31`)
3. **Magic operator chars** — replace `char op` on BinOpNode with a named `enum class BinOp` (`src/sema.cc:83`, `src/codegen.cc:502`)
4. **codegen.cc size** — split 1,044-line file into expr/stmt/strings sub-files and document invariants

**Why:** Identified by architectural review as correctness risks (1, 2) and maintainability blockers (3, 4).

**How to apply:** When the user asks to start the next iteration, expect these to be the candidates. Do not jump to other features without addressing these first.
