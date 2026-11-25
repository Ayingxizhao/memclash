# Memory Index

## TIER 1 — READ FIRST, EVERY SESSION
- [Mentoring Rules](mentoring_rules.md) — CRITICAL: interaction style, review protocol, what Claude must never do
- [User Profile](user_profile.md) — who you are, how you learn, known weak points, habits

## TIER 2 — PROJECT CONTEXT
- [Decisions](decisions.md) — technical decisions log: why this approach, what the trade-offs are
- [Dev Progress](dev_progress.md) — service/module status, what's done, what's next

## TIER 2.5 — FEEDBACK
- [Feedback Log](feedback_log.md) — loose feedback and confirmed patterns that aren't formal decisions or named mistakes

## TIER 3 — TRACKING
- [Recurring Mistakes](recurring_mistakes.md) — patterns that keep appearing, tracked by name and count

## SESSION UPDATE PROTOCOL
At the end of each session, update:
1. `dev_progress.md` — what was implemented, what remains
2. `recurring_mistakes.md` — increment count if you hit a known mistake
3. `feedback_log.md` — corrections or confirmed approaches that aren't full decisions
4. Create new files for important context not covered by the above

If you ran `/init-mentoring`, a `Stop` hook nudges this automatically after
turns that look save-worthy — but the hook only surfaces a reminder, it
never writes the file itself. This protocol is still what Claude follows
once nudged, and still applies in full at the end of any session regardless.
