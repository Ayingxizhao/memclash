---
name: plans-dont-state-push-status
description:
  "A plan never says whether its work is pushed; that changes outside the plan and goes stale."
metadata:
  type: feedback
---

**Do not write "pushed", "not pushed" or "locally only" into a plan.** Whether a commit is on a
remote is a fact git holds, and it changes without the plan being edited, so the plan's copy goes
stale and misleads.

**Why:** Mike's words of 2026-10-12: "Plans should not state wether the work is pushed or not, it's
not maintainable." The page-types plan said its work was unpushed after it had shipped as `v0.1.4`.

**How to apply:** record what was done and the commit it is at. Whether to push still waits for
Mike's word, but a plan line asks for that action; it does not keep a record of push status.
Answer "is it pushed?" from `git ls-remote` when asked. See [[derive-dont-maintain]] and
[[msb-stitt-push-policy]].
