---
name: Prefer string_view over string
description: Use std::string_view instead of std::string wherever ownership is not required
type: feedback
---

Prefer `std::string_view` over `std::string` wherever the data is not owned by the object holding it.

**Why:** Zero-copy, no heap allocation. Particularly valuable for token text (lexeme slices into the source buffer) and any API that only reads a string without storing it long-term.

**How to apply:** Default to `std::string_view` for function parameters, token fields, and any struct member that references data owned elsewhere. Only use `std::string` when the object must own its own copy of the string.
