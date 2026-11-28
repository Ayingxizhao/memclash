---
name: genai-conventions-agent-telemetry
description: "How the harness captures the instrumentation agent's own telemetry as gen_ai spans in Honeycomb (in-process custom instrumentation built from the SDK message stream)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 954050d9-7ec5-40cd-adcc-0b70b2fc2575
---

The instrumentation agent's own behavior is captured as a gen_ai agent timeline in Honeycomb (dataset `<app>-instrumentation`). As of 2026-07-03 this is **custom in-process instrumentation**, NOT the SDK's native OTel export.

**How it works now (`src/agent-tracing.ts`):**
- The SDK's native export is OFF — `src/instrumentation.ts` no longer sets `CLAUDE_CODE_ENABLE_TELEMETRY` / `OTEL_*` / `OTEL_LOG_*`. There is **no agent-telemetry collector** and no `claude_code.* → gen_ai.*` remap (deleted `collector.agent.template.yaml`, `harness.sh` agent_collector fns, `startAgentCollector`/`stopAgentCollector`, the `HARNESS_COLLECTOR_ENDPOINT` plumbing).
- `createAgentTrace()` builds a real gen_ai span tree from the `query()` message stream (fed every event via `onMessage`) and exports straight to Honeycomb with its own `NodeTracerProvider` + OTLP exporter, authenticated by `HARNESS_INGEST_KEY` from inside the agent container. `end()`/`shutdown()` force-flush (replaces the old 3s sleep).
- **Trace shape:** root `invoke_agent <app>-instrumentation` (init→result) → one `chat <model>` span per turn → `execute_tool <name>` children. Sub-agent turns nest under an `invoke_agent <subagent_type>` span that hangs off the spawning `Task` `execute_tool` span. Parenting is derived from `parent_tool_use_id` on forwarded sub-agent messages — which requires **`forwardSubagentText: true`** on the query (else sub-agent text+thinking are not forwarded).
- **Content (delta strategy):** each `chat` span carries its own `gen_ai.output.messages` (this turn's thinking→`reasoning` part, text→`text` part, tool_use→`tool_call` part) + `gen_ai.input.messages` = the tool_results received since the previous turn. Full initial prompt lives once on the root. All content is JSON strings on span attrs.
- **conversation.id = the harness runId** (resource attr `gen_ai.conversation.id`), plus `harness.run_id`, `app`, `skill.*` — so agent telemetry, app telemetry, and the run record all key off the same value.
- Traces only — native metrics/logs are gone. `runs.jsonl` token/cost is unaffected (computed in-process from the `result` event, see [[full-run-report-spec]]).

**gen_ai semconv facts (verified against the semantic-conventions-genai repo; the conventions MOVED there from the main semconv repo):**
- Message-part discriminators: `text`{content}, `reasoning`{content}, `tool_call`{id,name,arguments}, `tool_call_response`{id,**response**} (the field is `response`, not `result`).
- `execute_tool` span attrs: `gen_ai.tool.name` / `.call.id` / `.type` / `.call.arguments` / `.call.result` (arguments & result are type `any` → JSON string on spans).
- `gen_ai.provider.name=anthropic` (NOT the deprecated `gen_ai.system`). Chat span attr set matches the repo's `reference/scenarios/claude-agent-sdk/data.json`.
- Anthropic stop_reason → gen_ai FinishReason: end_turn/stop_sequence/pause_turn→stop, max_tokens→length, tool_use→tool_call, refusal→content_filter.

`src/agent-tracing.ts` is baked into the image → rebuild after editing (see [[rebuild-images-after-harness-change]]). To look at a run's data, see [[observing-a-run]].
