---
name: self-verify-ci-work
description: For CI/workflow work, trigger the live run and verify it yourself before reporting done — and don't re-ask about setup steps the user already confirmed
metadata:
  type: feedback
---

During the cloud-agent-runner build (2026-08-15, session `e6470b0a`), the
GitHub Actions workflow needed ~6 rounds of live-only fixes, each discovered by
the **user** pasting failure logs back. They eventually said: *"would it be
possible for you to run the tests yourself, your work has a lot of errors and I
don't want to catch them all myself. I would assume you would prefer to show me
your best work AFTER verifying it too."* Separately, when asked again about a
setup step already done: *"I did the branch protections the first time, I'm not
stupid."*

**Why:** GH-Actions-shaped work can't be gated locally, so "gates pass" means
nothing until a real run succeeds; using the user as the test harness reads as
unverified work. And re-asking about confirmed steps reads as not listening.

**How to apply:** for any change to `.github/workflows/` or CI-adjacent
scripts, trigger a real run (e.g. `npm run agent`, a `workflow_dispatch`, or a
push that exercises it) and read its logs yourself before declaring the work
done. Track which setup steps the user has confirmed (branch protections,
repo settings, secrets) and don't re-ask;
verify server-side via `gh` if confirmation is really needed.
