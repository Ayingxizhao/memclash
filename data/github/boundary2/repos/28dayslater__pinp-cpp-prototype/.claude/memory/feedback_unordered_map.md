---
name: Use unordered_map for symbol tables
description: Symbol tables and similar name→value maps should use unordered_map, not map
type: feedback
---

Use `std::unordered_map` for all symbol tables (variable maps, function registries, etc.) going forward. Current code uses `std::map` in several places (e.g. `fn_meta`, `global_vars`, `global_str_vars` in `jit.hh`).

**Why:** Symbol lookup is a hot path; ordered traversal is never needed for name→value maps, so the O(1) average lookup of `unordered_map` is strictly better than `map`'s O(log n).

**How to apply:** Any new map keyed by string name (variable, function, type) should default to `unordered_map`. Existing `map` instances should be migrated opportunistically when touching the surrounding code.
