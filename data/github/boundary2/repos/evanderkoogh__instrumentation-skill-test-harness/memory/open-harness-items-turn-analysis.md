---
name: open-harness-items-turn-analysis
description: Two harness items from the 2026-07-03 turn-reduction analysis — BOTH now resolved (2026-07-06)
metadata: 
  node_type: memory
  type: project
  originSessionId: 42c64023-14b2-4b95-a8e2-0a58b2bf8c57
---

From mining the `<app>-instrumentation` gen_ai spans of the 2026-07-03 batch for wasted turns
(see [[observing-a-run]] for how). The four skill-side fixes were shipped (otel-instrumentation
v0.2.4, otel-verification v0.2.1). Two items were **harness/measurement, not skill** — both now
resolved (2026-07-06):

1. **Dead verification sub-agent spawn on fable — MITIGATED.** beaverhabits' first `Task`/Agent spawn
   died in ~490ms with HTTP 400 `"thinking.type.disabled" is not supported for this model ... use
   "thinking.type.enabled" with budget_tokens`; it re-spawned and succeeded (~4-6 wasted turns).
   `claude-fable-5` rejects a `disabled` thinking config. Fix: `src/instrumentation.ts` query opts now
   set `thinking:{type:"enabled",budgetTokens:10000}` **only when the model matches /fable/i** (Opus/
   Sonnet keep their adaptive default — do NOT pin them to a fixed budget). Extend the guard if another
   model shows the same 400. Was intermittent (a plain re-spawn also cleared it), so this is a belt-and-
   suspenders preventive, not a proven deterministic root-cause fix. Requires a docker image rebuild to
   take effect ([[rebuild-images-after-harness-change]]).

2. **Measurement gap: Edit diffs + sub-agent prompt/result not on spans — RESOLVED by the in-process
   rewrite.** The gap was recorded against the OLD collector-remap telemetry (`claude_code.*`, only
   `file_path` survived). The same-day in-process rewrite (`src/agent-tracing.ts`, commit 03d839e)
   already captures all three: Edit diffs → `gen_ai.tool.call.arguments` = full `JSON.stringify(input)`
   (incl. `old_string`/`new_string`, un-truncated) on every `execute_tool` span; sub-agent/verification
   prompt → `invoke_agent` span `gen_ai.input.messages` (inline Skill verification is a `Skill`
   execute_tool span with the same arg capture); sub-agent final verdict → the Task execute_tool span's
   `gen_ai.tool.call.result`. No code change needed.

Turn-waste is ~15% of model turns; the verification sub-agent alone is ~25-30% of all turns (inherent
to the two-box design, not waste). Biggest recurring sinks were weaver run-once-vs-probe loops,
chasing out-of-scope/baseline failures, and reacting to BSP span-drops after a boot — all four fixed
in the skills.
