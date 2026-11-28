---
name: Semantic optimisation passes
description: When a second semantic optimisation is added, extract str-concat and all such passes into a dedicated pass layer
type: project
---

The str-concat chain optimisation (collect_str_parts / emit_str_concat_n) currently lives inline in emit(BinOpNode). This is acceptable while it's the only semantic optimisation.

**Why:** When a second semantic optimisation is added, having them scattered across emit() methods becomes hard to reason about and test. A dedicated pass layer (between sema and codegen) makes the boundary explicit.

**How to apply:** At the point a second semantic-level transformation is introduced, extract all such logic into a separate AST rewrite pass (e.g. a `SemanticOptPass` that runs after sema and before codegen). The str-concat flattening should be the first thing moved there, likely introducing `StrConcatNode` into the AST at that point.
