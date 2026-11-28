---
name: FIXME deferral policy
description: How to handle code quality issues noticed outside current iteration scope
type: feedback
---

When a code quality issue is noticed mid-iteration:
- If the offending code was **not touched** by the current iteration: add a detailed `// FIXME:` comment and defer the fix to a future branch.
- If the offending code **was added or modified** by the current iteration: fix it immediately (it's in scope).

**Why:** Keeps branches focused; avoids scope creep while still tracking technical debt.

**How to apply:** Before fixing anything flagged as a quality issue, check git blame / the current diff to determine if the code belongs to this iteration or predates it.
