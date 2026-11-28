---
name: project-two-box-skill-model
description: "The deliverable is two self-contained skills (the \"two boxes\") — no conductor agent, no instrumenter/verifier sub-agents, no weaver in the verifier."
metadata: 
  node_type: memory
  type: project
  originSessionId: f93dfb0c-4a5a-4da6-8fec-4d6e7fcb67f9
---

The instrumentation deliverable is a **two-box model** (agent-skill repo; spec in harness
`docs/observability-boxes.md`). This **supersedes** the older conductor/sub-agent design — the
`instrumentation-agent` conductor, the `otel-instrumenter` / `otel-verifier` sub-agents, and the
`otel-migration` skill were all removed. CLAUDE.md's "Reviewing a skill" section describes the
current model; this memory holds the durable lessons that aren't in the repo.

**The two skills:**
- **`otel-instrumentation`** ("make my app observable") owns the whole job end-to-end in one skill:
  gather → auto-instrument → export → enrich → **define a weaver registry (static)** → prove under real
  traffic → hand off to verification + fix → hand back. No sub-agents; the verification hand-off is the
  `otel-verification` **Skill** (same context), not a Task agent. The harness runs it non-interactively,
  so it must proceed autonomously from the preamble alone (no mid-run questions).
- **`otel-verification`** ("how good is it") is a **read-only judge**: queries Honeycomb via MCP, judges
  against current OTel semconv (`search_semconv`/`get_semconv_attribute`) + any org registry. It does
  **not** run the app, generate traffic, or stand up a collector/weaver.

**Weaver registry (skill step 5):** look for an existing registry in the repo first, reuse/extend it,
else create one; validate **statically** with `weaver registry check` (NOT live-check — the harness runs
live-check itself). A directory of group files is itself a valid registry — the **manifest is optional**
(weaver 0.23), and `docker/lifecycle.sh` discovers a manifest-less registry by a YAML with a top-level
`groups:` key. **But if a manifest IS written it MUST declare `schema_url` (or `schema_base_url` +
`semconv_version`)** — an incomplete `registry_manifest.yaml` makes weaver live-check die and the
criterion skip. This has been a recurring skill-quality defect worth watching.

**Durable lessons:**
- The verifier must use the **Honeycomb MCP only** — never hand-roll `curl` against the Honeycomb REST
  API, and don't infer auth from `~/.claude/mcp-needs-auth-cache.json`.
- The container's ingest key is `HARNESS_INGEST_KEY` (a collector example authing with
  `${HONEYCOMB_API_KEY}` will fail — that var isn't set in the container).

**Recurring skill-quality findings (next improvement targets, seen across apps — reverify, may be
addressed):** `current_semconv` fails when libs emit deprecated `db.*`/`enduser.*` names
(db.system→db.system.name, db.statement→db.query.text, db.name→db.namespace, enduser.id→user.id);
`env_var_output` fails when the handback omits `OTEL_EXPORTER_OTLP_ENDPOINT` +
`OTEL_SEMCONV_STABILITY_OPT_IN`.

See [[project-goal-portable-skills]], [[feedback-no-preamble-edits]], [[observing-a-run]],
[[rebuild-images-after-harness-change]], [[project_broadleaf_startup]].
