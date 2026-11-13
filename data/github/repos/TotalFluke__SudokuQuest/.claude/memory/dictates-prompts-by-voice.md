---
name: dictates-prompts-by-voice
description: The user dictates prompts by speech-to-text — read for intent, and confirm apparent negations rather than acting on them literally
metadata:
  type: user
---

Many of the user's prompts are **dictated**, not typed. They arrive with filler
words and spoken cadence (*"Um, I think any action that is not enabled should be
completely hidden… so, um, showing them all…"*) and occasionally with
transcription errors that invert the meaning.

A confirmed case: after a plan revision the user said *"That's not fine. Um, can
you use the implement skill to implement this plan?"* — the second half approves
the plan, so the negation contradicted it. Asking a single clarifying question
established it was a slip; the intended word was *"That's fine."*

**Why:** taken literally, one mis-transcribed word sends a whole plan phase down
the wrong path. The filler and self-correction are noise; the intent is usually
clear from the rest of the turn.

**How to apply:** read dictated turns for intent and ignore the disfluencies —
don't quote them back or treat a restart as a change of mind. When a negation or
odd word **contradicts the rest of the same turn**, treat it as a likely
transcription artifact: ask one targeted question naming the specific decision at
stake before proceeding, rather than either acting literally or silently assuming
the opposite. When it reads as a genuine objection with no contradiction, take it
at face value.
