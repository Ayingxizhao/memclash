---
name: feedback-inline-edits
description: Change existing files with targeted inline edits, not whole-file rewrites, so the diff is reviewable
metadata:
  type: feedback
---

When updating an existing file — memory files especially — make
targeted inline edits (`Edit` on the specific lines) rather than
rewriting the whole file with `Write`.

**Why:** David reviews each change as it's proposed. A whole-file
rewrite shows up as one opaque block, so he can't see what actually
changed. He stopped a memory update on 2026-09-29 for exactly this
reason.

**How to apply:**
- Keep existing wording where it's still true; add or adjust only the
  lines that need it, even if that makes the file less tidy than a
  fresh rewrite would be.
- Whole-file `Write` is fine for brand-new files.

Related: [[user-david]].
