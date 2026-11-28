---
name: Worker vitest spawn EPERM in Codex Desktop sandbox
description: On Windows, Codex Desktop sandbox may block Node child_process.spawn and cause false-negative vitest failures
type: feedback
---

When running Worker tests in Codex Desktop on Windows, `npm test` / `vitest run` may fail with `spawn EPERM` before tests start.

**Why:** This can be caused by the Codex Desktop sandbox blocking Node `child_process.spawn()`, not by the Worker test code itself. In this repo, the failure was reproducible in Codex Desktop, while the same `cmd /c npm test` passed outside the sandbox.

**How to apply:** If Worker tests fail with `spawn EPERM` in Codex Desktop, first treat it as a sandbox/environment issue. Re-run `cmd /c npm test` outside the sandbox before concluding that Vitest, Vite config, or the test code is broken.
