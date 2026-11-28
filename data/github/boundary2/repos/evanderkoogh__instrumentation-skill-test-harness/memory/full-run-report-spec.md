---
name: full-run-report-spec
description: "Spec for building a full HTML report of an instrumentation run from its Honeycomb telemetry — sections, order, and the data behind each"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 954050d9-7ec5-40cd-adcc-0b70b2fc2575
---

This is the STANDARD run-report format — use it by default whenever a report/overview of a run is requested (it supersedes the earlier call-table-only version). Produce ONE self-contained HTML file (inline CSS/JS, no external deps) built entirely from that run's telemetry in Honeycomb. Scope everything to the run via `gen_ai.conversation.id` = the runId (`<app>-<ISO timestamp>`); see [[observing-a-run]] for the three streams and [[genai-conventions-agent-telemetry]] for how the agent telemetry is shaped + which content lives in log events vs span attrs.

Sections, in this order:

1. **Run-level metrics** (top): wall-clock time spent, tokens used (in / out / cache-read / cache-write), total cost, and pass rate. Include the full per-criterion pass/fail table. Sources: `runs.jsonl` record (criteria, agent metrics, weaver) for the authoritative result; the `instrumentation-skill-harness` orchestration spans and the agent's `chat` spans / `api_request` events for token + timing rollups.

2. **Failure investigations**: for EVERY failed criterion, investigate what went wrong and WHY — root cause, not just the symptom. Read the relevant report (e.g. weaver `logs/<app>/weaver-report/live_check.json`), the failing telemetry, and the agent's own actions. Classify the cause: **skill defect** (fixable in the skill — e.g. a weaver registry that doesn't `import` upstream semconv → tens of thousands of `missing_attribute` violations), **upstream library lag** (not skill-fixable — e.g. SQLAlchemy pool metric emitting deprecated `state`/`pool.name`, ungated by the semconv opt-in), or **measurement artifact** (harness scoping issue). State which, with evidence.

3. **Skill-phase overview**: under the [[project-two-box-skill-model]] it's a **single agent** (no conductor/sub-agents), so trace the skill's own phases and hand-offs (e.g. gather → auto-instrument → export → enrich → weaver registry → prove → `otel-verification` skill → fix → hand back), and how many times the `otel-verification` skill was invoked. Derive from the ordering/timestamps of `execute_tool` (incl. `Skill`) spans.

4. **High-level actions** (longer form): a narrative of the high-level actions the agent took (what it explored, what it instrumented/changed, what it verified/found). Summarize from each `chat` turn's `gen_ai.output.messages` (the `reasoning`/`text` parts) + the tool calls it issued.

5. **Full call table**: every tool call AND every LLM call, chronological, each row with a short human-readable summary of what happened (LLM: the model's reasoning gist + decision; tool: what the command/edit/read did + its outcome). **Clicking a row expands it** to show ALL information for that call. NOTE the data model changed 2026-07-03 (see [[genai-conventions-agent-telemetry]]): telemetry is now custom in-process gen_ai spans, not the SDK's native export. A "turn" = one `chat` span; its content is on `gen_ai.output.messages` (this turn's thinking+text+tool_calls) and `gen_ai.input.messages` (the tool_results it consumed) — there are no more `api_request_body`/`api_response_body` log events. Tool input/output live on the `execute_tool` span as `gen_ai.tool.call.arguments` / `gen_ai.tool.call.result` (no more `full_command`/`file_path`/`tool.output` span event). Sub-agent membership is the `gen_ai.agent.name`/span parent (`invoke_agent <subagent_type>`). (Implement expand with a tiny inline `<details>`/JS toggle — still no external deps.)

Practical: content attrs can be large — summarize in the row, keep full content in the collapsed detail. Write to `reports/agent-run-overview-<app>.html` (or similar). Per-app background agents that wait for the run to finish then build this are the working pattern (poll `tmp/.run.<app>.pid` disappearing as the finished signal).
