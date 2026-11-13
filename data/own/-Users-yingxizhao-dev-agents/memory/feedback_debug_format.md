---
name: feedback-debug-format
description: Debugging session format – Goal/Problem/How I Found It/Plan with bold topic sentences
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ff611b65-533f-4d36-b125-db48dbca3669
  modified: 2026-08-11T14:12:50.116Z
---

Format requirements for debugging sessions:
- Use `#` headers: Goal, Problem, How I Found It, Plan
- Bold topic sentence continues inline as the body (one idea per section)
- When the problem or plan changes mid-debug, explicitly re-state with Updated Problem / Updated Plan + note what changed and why
- Tell me the plan **before** running any command – never run first and explain after
- User asks follow-up if they want more detail

**Why:** Keeps debugging sessions scannable and lets the user track how the diagnosis evolved, consistent with [[feedback_response_format]] (bold-topic-sentence style) and CLAUDE.md's debugging rules (issue/fix/expected-behavior).

**How to apply:** Automatic for any debugging session. Always state the plan before executing any command.

Example:

# Goal
**Run `kc_setup.sh` to configure Keycloak.**

# Problem
**`kc_setup.sh` failed – Keycloak returned empty JSON on the admin token call.** Only one log line (Python JSON parse error), confirmed no RUNNING tasks for `keycloak-svc`.

# How I Found It
**Read container logs via `aws logs get-log-events`, then checked service status via `describe-services`.** Log stream name = `/ecs/<container>/<task-id>`, log group = `/ecs/<family>`.

# Plan
**Force new Keycloak deployment, wait for healthy, then re-run bootstrap.** `describe-services -> runningCount/failedTasks` tells me if it's stopped or crash-looping.

*(If plan changes mid-debug):*

# Updated Problem
**Keycloak is crash-looping due to missing env var, not a transient stop.** Found via `stoppedReason` showing OOM – not what I expected.

# Updated Plan
**Fix the env var in the task definition and redeploy before re-running bootstrap.**
