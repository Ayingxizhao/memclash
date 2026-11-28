---
name: project-configurable-semconv-expectations
description: "weaver check split into http/db/other criteria + APP_WEAVER_WAIVERS to waive conventions an app's libs can't emit"
metadata: 
  node_type: memory
  type: project
  originSessionId: af33947f-24d8-479d-8f7a-c19091b1ff2d
---

Implemented 2026-07-01. Two related changes to the `weaver_live_check` scoring in `src/weaver.ts`,
so scores don't conflate a library limitation with a genuine instrumentation gap.

**Weaver criteria are split three ways.** `weaver.ts` buckets every live-check violation by
convention family and emits three criteria instead of one: `weaver_live_check_http` (http / url /
network / server / client / user_agent), `weaver_live_check_db` (`db.*`), `weaver_live_check_other`.
`http` and `db` gate independently (custom registry created + telemetry received + zero non-waived
violations in that bucket), so a library lagging one family fails only that bucket. Bucketing is
namespace-level (not per-attribute) to avoid overfitting. Buckets partition the authoritative
`statistics` total exactly; violations in stats but absent from `samples` (weaver truncation) go to
`other` so nothing is masked.

**UPDATE 2026-07-03: `weaver_live_check_other` is now INFORMATIONAL, not pass/fail.** It's reported
(ℹ️ icon) but excluded from the passed/total tally and the `run.criteria_*` span attrs — because the
`other` bucket is dominated by standard resource/SDK attributes (`service.*`, `telemetry.sdk.*`) and
other signal-less namespaces the app's libraries emit but can't reshape. Implemented via an optional
`informational?: boolean` on `CriterionResult` (evaluation.ts); weaver.ts sets it on the `other`
criterion; metrics.ts + run.ts skip informational criteria when counting. Same day, the skill's
`references/weaver-registry.md` gained a "Don't forget the resource attributes" note (import
`service.*`/`telemetry.*` via the `entities` signal) since those are always SDK-injected.

**Waivers, bucketed:** `APP_WEAVER_WAIVERS` in `apps/<app>/config.sh` — whitespace-separated
attribute-key / metric-name prefixes. `readWeaverWaivers` reads it; `tallyViolations` walks the
report's `samples` tree and, per bucket, subtracts violations whose `context.attribute_key` (or
`signal_name` for metrics) matches a waiver. A bare namespace waives the subtree (`db` → `db.*`,
emptying the db bucket). First user: `realworld-go` sets `APP_WEAVER_WAIVERS="db"` because its GORM
plugin (uptrace/opentelemetry-go-extra) still emits the old DB semconv.

**Eval-side only:** read only in the trusted eval step (`run-eval.ts` → `weaver.ts`), deliberately
NOT rendered into the agent prompt (would leak the scoring criteria).

**Why:** otherwise scores penalize apps whose deps lag the spec — noisy, unfair signal.

Documented in CLAUDE.md ("Adding a new app" + the structure list). Relates to the two-box
[[project-two-box-skill-model]] verification skill. Baked harness code, so needs an image rebuild
[[rebuild-images-after-harness-change]] to take effect in a run.
