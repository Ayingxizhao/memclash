---
name: feedback-verify-compliance-impossible-before-waiver
description: "Before recommending a weaver/semconv waiver, prove the app genuinely cannot comply — upgrading the instrumentation library is usually a valid fix"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3e877124-06e5-4378-8ee5-17e3ca5e1663
---

Before recommending Erwin add a semconv/weaver waiver (e.g. `APP_WEAVER_WAIVERS`), first
double-check it is **genuinely impossible** for the app to comply. Do not conclude "library
limitation → waiver" from the pinned version alone.

**Why:** waivers hide a real gap and are a last resort. A version pin lagging the spec is not the
same as the library being incapable — a newer release often adds stable-semconv support or honors
`OTEL_SEMCONV_STABILITY_OPT_IN`. Recommending a waiver when a version bump would fix it teaches the
skill to give up instead of upgrading.

**How to apply:** when instrumentation emits deprecated/old semconv, check whether a **newer version
of the instrumentation library** emits the stable conventions (or gains the opt-in) before proposing
a waiver. Upgrading the dependency is a valid, preferred compliance strategy. Only after confirming
no released version can comply is a waiver the right call.

Concrete instance (2026-07-02 beaverhabits run): I said `opentelemetry-instrumentation-sqlalchemy
0.49b2` "physically cannot" emit stable DB semconv and floated a `db` waiver like realworld-go's.
Wrong framing — the pin was just old; upgrading the library was the valid fix I skipped.

Relates to [[feedback-no-scoring-changes-without-permission]] (still: never edit scoring config on
my own initiative — this adds that even *recommending* a waiver requires ruling out an upgrade first).
