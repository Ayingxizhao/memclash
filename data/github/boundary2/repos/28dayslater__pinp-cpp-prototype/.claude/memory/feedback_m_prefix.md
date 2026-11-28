---
name: m_ prefix for private class members only
description: Use m_ prefix for private/protected class members; never on struct fields
type: feedback
---

The `m_` prefix is acceptable for private and protected members of a `class`. Never use it on `struct` fields — structs have public data by convention and `m_xxx` looks wrong there.

**Why:** Structs are value/data types; the prefix implies encapsulation that isn't present.

**How to apply:** Check every `m_` usage — if it's on a `struct` field, drop the prefix. Only `class` private/protected members may carry `m_`.
