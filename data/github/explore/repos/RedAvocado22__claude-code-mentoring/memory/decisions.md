---
name: decisions
description: "All technical decisions — why this approach, what the trade-offs are. Read when you need context on a past decision."
metadata:
  type: project
---

Last updated: [date]

---

<!-- 
Format for each entry:
## [YYYY-MM-DD] Decision Title — short summary

**Decision:** What was decided.

**Why:** The reason — constraint, requirement, or technical insight that drove the choice.

**Trade-off:** What you gave up. Be honest here.

**Applies to:** Which services/modules this affects.
-->

## [YYYY-MM-DD] Example: Snapshot data at the time of action

**Decision:** When [entity] transitions to [state], snapshot [data field] from [service] and store it in [table].

**Why:** Protects immutability invariant. If the source data changes later, the record still reflects the value at the time of the action.

**Trade-off:** Two copies of the data. Accepted — the source-of-truth copy in [service] can change, but this snapshot must not.

**Applies to:** [List affected services/modules]

---

## [YYYY-MM-DD] Example: Gateway injects user context as headers

**Decision:** API Gateway extracts user identity from JWT and injects it as HTTP headers (`X-User-Id`, `X-User-Roles`, etc.) to downstream services. Gateway strips the `Authorization` header before forwarding.

**Why:** Downstream services don't need to re-validate JWT — single validation point at Gateway. Services receive clean, trusted context.

**Trade-off:** Downstream services fully trust Gateway. If Gateway is bypassed, no auth. Accepted — defense in depth is added via per-service SecurityConfig.

**Applies to:** All downstream services

---

<!-- Add your actual decisions below this line -->
