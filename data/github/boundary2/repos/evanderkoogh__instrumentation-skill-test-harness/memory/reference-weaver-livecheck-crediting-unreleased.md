---
name: reference-weaver-livecheck-crediting-unreleased
description: "On released weaver (0.24.2, the harness version + latest as of 2026-07), NO registry-authoring form makes live-check credit standard semconv attributes without --include-unreferenced. The feature is unreleased (main)."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 30cd11f6-a60f-4ba7-b066-d6bd1a501eb5
---

**The core weaver limitation behind the `weaver_live_check_*` failures.** Verified empirically
2026-07-01 on BOTH host weaver 0.23.0 and the container's 0.24.2 (which actually scores; also the
latest GitHub release): a custom registry that declares `dependencies: [otel]` and then tries to
credit standard span attributes (`http.request.method`, `url.path`, `server.address`, `db.*`) via ANY
of these forms **still gets every standard attribute flagged `missing_attribute` at `live-check`**:

- `imports: {spans: [http.*]}` (also: glob is wrong — semconv span group ids are `span.http.*`)
- `imports: {spans: [span.http.*]}`
- `imports: {attribute_groups: [registry.*]}`  → resolves to `groups: []`
- explicit `groups: [{type: attribute_group, attributes: [{ref: http.request.method}]}]`
- a v2 `type: span` group with `ref:`s
- `--future` flag

The ONLY thing that credits them is **`--include-unreferenced`** — which, as of 2026-07-02, the harness
NOW sets as a temporary workaround (reversing the earlier no-flag posture; see
[[project-weaver-no-include-unreferenced]]). Remove it once #1267/#1442 ship.

**Why:** the weaver CHANGELOG shows the crediting behavior is **UNRELEASED** (on `main`, not in 0.24.2):
- PR #1267 (unreleased): "Support `imports` for all signal types **and public attribute groups** in v2
  registry." — released weaver's `imports` (v0.15.3, #769) covers only metrics/events/entities, NOT
  spans or attribute_groups, and http/url/server/db attrs live in attribute_groups carried by spans →
  no released path to reference them.
- PR #1442 (unreleased): "Change `--include-unreferenced` so that this is the same as creating a set of
  `import:` statements in the registry manifest." — i.e. on future weaver, a proper `imports:` block
  gives the same result as the flag, reconciling the no-flag posture with the mechanism.

**Consequence:** with released weaver + no `--include-unreferenced`, `weaver_live_check_*` is
**unpassable by any registry the agent could author** — the failures are a tooling/version limitation,
NOT an instrumentation-quality problem and NOT a fixable skill defect at this weaver version. This is
exactly why the harness now sets the flag (above): so the criteria measure real registry quality
instead of the crediting gap. The `main`
weaver docs (define-your-own-telemetry-schema.md, semconv-syntax.v2.md) describe the unreleased
behavior, so they read as if it should work. Path forward is a weaver upgrade to a build with #1267/#1442
(a measurement-fidelity harness change), then fix the skill's registry recipe (correct import targets)
to match. Related: [[reference-weaver-registry-import-syntax]], [[project-configurable-semconv-expectations]].
