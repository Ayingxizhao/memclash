---
name: Branch focus discipline
description: Warn user when a requested change is unrelated to the current branch/feature
type: feedback
---

Keep branches focused on the current functionality. If the user asks for a code improvement unrelated to the branch being worked on, warn them before proceeding.

**Why:** Good development practice; mixing concerns makes history harder to read and review.

**How to apply:** Before implementing any change, check whether it belongs to the current branch's scope. If not, flag it and let the user decide.
