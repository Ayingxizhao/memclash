---
name: activating-a-plan-takes-two-steps
description:
  "writing active-plan.md is step one; the injected read-back it asks for arrives on the next
  request, so confirm it then."
metadata:
  type: feedback
---

Activating a plan is two steps in two turns, not one. Step one is writing the `@` import into
`.claude/rules/active-plan.md` and reading it back off disk. Step two is reading the plan's own text
back out of the injected instructions, and that cannot happen in the turn that wrote the pointer: a
rules file is injected from disk when a request is built, so a pointer written mid-turn first
arrives with the user's next message.

A compaction in between costs one more request. Its instruction block is the snapshot taken before
it, so it carries the *previous* pointer and the previous plan's text, which reads exactly like a
pointer that never took. Measured 2026-09-28 activating the simulator-gamepad plan: pointer written,
compaction next, the old pointer in that block, and the plan's own text only on the request after.

**Why:** `plan-activation.md` asks for the injected read-back without saying when it is available,
so I treated it as something to do immediately, found nothing, and carried the line open. It cost
two consecutive plans their `plan.pointer` line — the one-drivetrain plan's read-back landed a turn
late, and the stop-and-names plan was closed out before one ever arrived, because deactivation
empties the pointer and makes it unobtainable. Neither was a broken import; both were the rule being
read as one step.

**How to apply:** write the pointer, read it back off disk, say that the injected confirmation is
owed on the next request, and start the work — the contract binds it whether or not the plan is
active. On the next request, check the injected instructions for the plan's own text and mark
`plan.pointer` then, or on the one after a compaction. If the plan is finishing inside one turn, say
the confirmation never came due rather than ticking the line — see [[no-invented-gates]]. A silent
unexpanded import looks the same as this lag, so the on-disk read is what distinguishes them, and it
is worth doing every time. The checklist line belongs at the top of the plan's own list, per
[[unroll-the-plan-into-a-checklist]].
