---
name: background-work-must-be-tracked
description: "never chain or launch long work with `&` inside a Bash call; it dies with the shell and is invisible; use run_in_background"
metadata:
  node_type: memory
  type: feedback
---

In one session three long agent runs were queued as `(until ...; do sleep; done; run.sh ...) &` inside ordinary Bash calls. All three died when that shell exited: one output file stayed empty, two never started. The user saw only the monitors in the task list and asked why no fix round was running. The runs had been reported as "running" for over an hour.

**Why:** a job backgrounded with `&` belongs to the Bash call's shell, not to the harness. It is killed or orphaned when the call returns, and it never appears as a task, so neither the user nor the agent can see it die.

**How to apply:** every long or queued job goes through Bash `run_in_background: true` (or Monitor for streams), one tracked task per job. To run B after A, wait for A's completion notification and launch B then; do not build a waiter loop. Before telling the user something is running, confirm the process with `pgrep` or the task list. Related: the `jig:multitask` skill, [[keep-tool-output-small]].
