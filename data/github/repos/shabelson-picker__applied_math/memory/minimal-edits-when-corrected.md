---
name: minimal-edits-when-corrected
description: When the user points at something, change only that thing — no surrounding rework or audits
metadata:
  type: feedback
---

When the user points at a specific line, cell, or sentence, **edit exactly that and stop.**
Do not rewrite the surrounding table, rename variables for consistency, add explanatory
callouts, or grep for similar cases elsewhere.

**Why:** rework costs the user time — re-reading a whole rebuilt section to find the one
change they asked for, and re-checking things that were already fine. Their words:
"if I didn't give notes — it's probably fine." Silence on a passage is approval of it.

**How to apply:**
- One pointed-at item → one edit. Re-render, report in a line or two.
- If fixing it *requires* a wider change, say so in one sentence and ask first — don't just do it.
- If a nearby problem is spotted, mention it; do not fix it unasked.
- Applies to [[ds-class-cheatsheet]] and [[aofa-course]] documents especially, where a full
  re-render + verify cycle follows every edit.
