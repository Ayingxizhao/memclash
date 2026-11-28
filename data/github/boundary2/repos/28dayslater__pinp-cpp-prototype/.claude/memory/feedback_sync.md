---
name: feedback_sync
description: Do not push to GitHub unless user says "sync"
type: feedback
---

Do not push to GitHub unless the user explicitly says "sync" (or equivalent).

**Why:** User wants control over when code goes remote.

**How to apply:** Commit freely, but never run `git push` unless the user asks to sync.
