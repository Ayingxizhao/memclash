---
name: reference-weaver-registry-import-syntax
description: "Correct weaver registry manifest syntax for importing upstream semconv — use dependencies:/registry_path:, not registries:/url:, plus an app-specific schema_url. The wrong form fails silently."
metadata: 
  node_type: memory
  type: reference
  originSessionId: bd1ec468-6a77-45c8-94a7-5a1abd0f8b8a
---

To make a weaver custom registry import the upstream OpenTelemetry semantic conventions (so standard
attributes like `http.*`/`db.*`/`server.*` resolve during `weaver registry live-check`), the
`manifest.yaml` MUST use a top-level **`dependencies:`** list with `name` + `registry_path`:

```yaml
name: <service>-registry
schema_url: https://<your-app>/schemas/1.0.0   # app-specific host — NOT opentelemetry.io/schemas/...
dependencies:
  - name: otel
    registry_path: https://github.com/open-telemetry/semantic-conventions.git[model]
```

**The trap that caused this:** a `registries:`/`url:` block (what the skill used to say) is **silently
ignored** by weaver — and `weaver registry check` STILL PASSES — so semconv is never imported and
live-check flags every standard attribute as "does not exist in the registry." This silently inflated
the `weaver_live_check_http`/`_other` buckets across ALL harness apps; the telemetry was spec-compliant,
weaver just had nothing to compare it to. See [[project-configurable-semconv-expectations]].

Two rules:
- **`dependencies:` not `registries:`** (and `registry_path:` not `url:`).
- **schema_url must be app-specific**, not `https://opentelemetry.io/schemas/...` — pointing it at the
  upstream schema makes the app registry share the upstream's identity and weaver fails with a
  "circular dependency detected" error.

Verified empirically 2026-07-01 on weaver 0.23.0 (host) and 0.24.2 (container): with `registries:` the
resolved registry is ~657 B and `http.route` is absent; with `dependencies:` it is ~3.9 MB and
`http.route` resolves. Fixed in otel-instrumentation SKILL.md (agent-skill @ 00b2a99).

**Self-check with `--include-unreferenced` (matches the harness as of 2026-07-02).** The harness now
runs live-check **WITH** `--include-unreferenced` as a temporary workaround (see
[[project-weaver-no-include-unreferenced]]), so declaring `dependencies:` correctly is what matters:
the flag credits imported standard attributes even when the registry doesn't enumerate them. Mirror
the harness: self-check *with* the flag. (Before the flag was added, getting `dependencies:` right was
necessary but not sufficient — the registry also had to *reference* each emitted standard attr. Once
weaver ships #1267/#1442 and the flag is removed, that stricter requirement returns.)
