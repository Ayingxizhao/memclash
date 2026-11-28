---
name: Lean prompt edits — no change history
description: When editing agent prompts in .agents/, write current-state instructions only; never embed why-changed narratives
type: feedback
originSessionId: ed5dc8b0-3c4e-4f59-9dad-fc8ba8a51a89
---
When editing prompts/instructions/sub-prompts/etc. in `.agents/agents/*`, write instructions as if the current state is the only state.

- Do NOT add sentences like "previously we had X, now we have Y", "this replaces the old Z", "recently split into A and B", or "we moved from N traders to 1".
- Do NOT add migration notes, deprecation markers, or "(was: ...)" parentheticals.
- Just describe what the current state of affairs is NOW. Git history is the change log.

**Why:** User observed I repeatedly bake change-rationale into prompts. Bloats tokens (these prompts are read every loop run), drifts as state moves further from the "recent change", noise that hides real instructions.

**How to apply:** On every prompt edit, scan the diff before saving — strip any sentence that only makes sense relative to a prior state. Keep only forward-looking imperatives.
