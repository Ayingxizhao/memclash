---
name: msb-stitt-push-policy
description:
  "Claude works and pushes only in github.com/msb-stitt (signed in as msb-stitt via gh); MikeStitt
  and spiresfrc9106 are fetch-only"
metadata:
  node_type: memory
  type: project
---

Copied on 2026-10-03 from the `configure-computer` project's memory, `msb-stitt-push-policy.md`.

As of 2026-10-01, all of Claude's work lives in the msb-stitt GitHub account: ftc-claude (private)
and public forks of ftc31459-26-27-biobuzz, corbelsflightlog and stick-e-bot. Mike and others pull
from msb-stitt into MikeStitt or spiresfrc9106.

In each clone, `origin` is msb-stitt. `upstream` (MikeStitt) and `spires` (spiresfrc9106) are
fetch-only; their push URL is the placeholder `DISABLED-push-only-to-msb-stitt`. Claude may push to,
and change the GitHub settings of, msb-stitt only.

As of 2026-10-02 the workspace is ~/projects/ftc-claude, with the subprojects ftc31459-26-27-biobuzz
(two z's is the correct season spelling), corbelsflightlog and spiresRobot2026 inside it.
stick-e-bot is at ~/projects/stick-e-bot.

**Why:** Mike's plan: review the work on msb-stitt before it's promoted.
**How to apply:** Never add a push URL for any account other than msb-stitt. Push only when Mike
asks (ftc-claude's constitution says the same). Related: [[commit-identity]],
[[read-project-rules-before-acting]].
