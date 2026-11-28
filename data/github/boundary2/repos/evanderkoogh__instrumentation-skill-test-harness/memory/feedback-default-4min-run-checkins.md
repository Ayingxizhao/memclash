---
name: feedback-default-4min-run-checkins
description: "What a \"test run\" defaults to — parallel, all apps, 4-minute check-in cadence"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ae4a27c8-e829-435c-804a-cdcbf98786ae
---

Erwin's default shape for a **"test run"**: `run.ts all --parallel` (every app under `apps/`, concurrently) with a **4-minute progress check-in cadence**. When he says "do a test run" or "run it" without qualifiers, use these defaults; he only names an app/model/flag when he wants to deviate.

- **Scope:** all applications (`all`), not a single app.
- **Concurrency:** `--parallel`.
- **Model:** whatever he specifies for that run (no standing default); ask/keep last if unstated only when it matters.
- **Cadence:** check progress every ~4 minutes until every app completes, without being re-asked each time.
- Always wrap in `caffeinate -dimsu` (see [[run-under-caffeinate]]).

**Why:** He repeatedly launched parallel all-app runs and repeatedly asked for a 4-min cadence; making both the default removes the repeated asks.

**How to apply:** Launch the run in the background under caffeinate, then poll progress and schedule a ~240s wakeup to re-check, repeating until all apps finish; then report the combined pass/fail summary. 240s keeps the prompt cache warm (<5 min).

**Each check-in should give an overview of what's happening now + anything interesting in the last few minutes** — not just "still running." Combine:
- Local: `tmp/run-progress.<app>.log`, PID files, `docker ps`/`docker stats` (liveness), `logs/<app>/`.
- **Honeycomb telemetry for active runs** (team `otel-test`, env `claude-skill-test`): query the `<app>-instrumentation` stream (agent behavior, `gen_ai.*`) scoped by `harness.run_id`/`gen_ai.conversation.id` to see what the agent is actually doing right now — recent tool calls, which files it's editing, whether it's verifying, errors. See [[observing-a-run]] for the runId scheme and all three streams.

Surface notable things: phase transitions, errors/retries, what the agent is currently working on, cost/token burn.
