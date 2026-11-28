---
name: feedback-no-preamble-edits
description: "Preamble = general framing + app facts only, never instrumentation how-to. Suggest-and-ask, never bake in. On an explicitly-requested edit, do exactly what was asked — no adjacent extras."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bd1ec468-6a77-45c8-94a7-5a1abd0f8b8a
---

The preamble is the shared, user-voice template `instrument-preamble.template.md` at the repo root
(rendered per app from `APP_*` facts in `config.sh` — there are no per-app preamble files). It may
contain **only** two kinds of content: (1) the general, app-agnostic framing of the instrumentation
task, and (2) the app-specific *facts* the agent needs to begin (what the app is, its
language/framework, the service name, how to reach it, the OTLP endpoint it exports to). It must
**never** contain instrumentation *instructions* — any guidance about *how* to instrument (techniques,
attribute choices, fixes, gotchas, "do X to avoid Y"). All such guidance belongs in the skill
(`agent-skill/honeycomb/skills/.../SKILL.md`).

You may **suggest** a preamble change and **ask for explicit permission**, but never add instrumentation
instructions to a preamble on your own — and if a "fix" really is instrumentation guidance, the answer
is to put it in the skill, not to ask to add it to the preamble.

**Scope discipline on an explicitly-requested edit:** when Erwin asks for a specific preamble change,
make *exactly* that change and nothing adjacent. On 2026-07-01 he asked to add the `otlp_endpoint` row;
I also filled the `honeycomb_ingest_key` row (reasoning "an endpoint needs a key") — he had **not**
asked for that and pushed back, so I reverted it. If a companion change seems warranted, call it out
and let him decide; do not fold it in. (He *later* explicitly asked to put both the Honeycomb endpoint
and ingest key back — so the current preamble does carry `%OTLP_ENDPOINT%` = the real Honeycomb
endpoint and `honeycomb_ingest_key` = `%API_KEY%`. The lesson is about the *unasked* first edit, not
the final state.)

**Why:** The deliverable is a **portable instrumentation skill**, not perfectly-instrumented sample
apps. The skill must carry all instrumentation guidance so that *the skill* is what gets evaluated.
Baking how-to-instrument hints into a preamble leaks app-specific answers, makes the app pass for the
wrong reason, and invalidates the test of whether the skill stands on its own. See
[[project-goal-portable-skills]].

**How to apply:** When a run surfaces something the agent should do during instrumentation (e.g.
"set service.name", "raise the BSP queue size", "disable the agent's self-telemetry"), generalize it
into the SKILL.md — never the preamble. Keep preambles to minimal app context + start-up facts only.
Harness config (`config.sh`) and evaluation (`evaluation.ts`, `EVALUATION.md`) changes are fine
without asking.
