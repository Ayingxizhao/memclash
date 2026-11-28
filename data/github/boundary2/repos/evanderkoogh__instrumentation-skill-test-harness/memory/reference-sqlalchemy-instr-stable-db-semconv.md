---
name: reference-sqlalchemy-instr-stable-db-semconv
description: "A newer opentelemetry-instrumentation-sqlalchemy release emits stable DB semconv; the beaverhabits pin (0.49b2) only lagged — upgrade, don't waive"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3e877124-06e5-4378-8ee5-17e3ca5e1663
---

`opentelemetry-instrumentation-sqlalchemy` **does** emit the stable DB semantic conventions
(`db.system.name`, `db.query.text`, `db.namespace`, `server.address`/`server.port`) in a newer
release — Erwin confirmed this (2026-07-02).

The beaverhabits checkout was pinned at `0.49b2`, which still emits the pre-stable names
(`db.system`, `db.name`, `db.statement`, `net.peer.*`, `net.transport`) and ignores
`OTEL_SEMCONV_STABILITY_OPT_IN`. That is a **stale pin, not a library incapacity** — upgrading the
instrumentation dependency is the correct fix for the beaverhabits `current_semconv` /
`weaver_live_check_db` failures. Do NOT reach for a `db` waiver here.

Instance of the general rule in [[feedback-verify-compliance-impossible-before-waiver]].
Contrast with realworld-go, whose GORM plugin genuinely lags (has `APP_WEAVER_WAIVERS="db"`) —
but even that should be re-checked against newer releases before treating the waiver as permanent.
