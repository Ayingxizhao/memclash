---
name: Infinite loop style
description: Use do { ... } while (true) for all infinite loops, not while(true) or for(;;)
type: feedback
---

All infinite loops (exited via `break` or `return`) must use `do { ... } while (true)`.

**Why:** Consistency and readability. The user prefers this form over `while (true)` and `for (;;)`.

**How to apply:** Any time an infinite loop is needed, write `do { ... } while (true);`. Never use `while (true)`, `while (1)`, or `for (;;)`.
