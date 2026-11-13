# Code Improvement Log

## Lesson: Do not treat approval `target_status` as generic core enum

**Problem:**
When asked to seed `core.approval_module_config` rows, I assumed `target_status` must come from `core.approval_status_enum` (because that was the column's PG type). I proposed narrowing the user's intended values (`WAIT_RECEIVE`, `WAIT_DELIVERY`) down to intersection with core enum (`APPROVED`), which lost the real semantic meaning.

**Solution:**
`target_status` is the **next-step label on the target table**, not a generic approval outcome. The approval consumer is status-only; it writes `target_status` literally into `<target_table>.<status_column>`. Valid labels therefore come from the target table's enum (e.g. `warehousing.item_transfer_status_enum`), not `core.approval_status_enum`. Column type must allow any label (now `varchar(50)`).

**Pattern:**
- Before trimming a user's value to satisfy a schema constraint, ask whether the constraint itself is wrong.
- For cross-module config fields, trace where the value is consumed. If the consumer uses it as raw text to another column, value domain = that other column's enum, not the origin column's enum.
- Schema fix (column type change) is on the table when the constraint contradicts real domain.

---

## Lesson: submitItemTransferRequestAction called wrong repository (skipped approval)

**Problem:**
`submitItemTransferRequestAction` (table-column DRAFT submit) called `submitItemTransferRequestRepository` which directly sets `status = "WAIT_DELIVERY"`, bypassing `WAITING_ON_APPROVAL` and never creating the approval record. Activity log showed `WAITING_ON_APPROVAL` but DB wrote `WAIT_DELIVERY` — silent contradiction.

Additionally, `editItemTransferRequestAction` had `generateSeriesNumber` gated on `status === "WAIT_DELIVERY"` — so the series number was never generated from the form path (form submits with `WAITING_ON_APPROVAL`).

**Solution:**
- `submitItemTransferRequestAction`: call `editItemTransferRequestRepository({ ...requestTransform, status: "WAITING_ON_APPROVAL", actionBy })` — this creates the approval record inside the transaction.
- `editItemTransferRequestAction`: gate condition corrected to `inputData.status === "WAITING_ON_APPROVAL" && prevData.status === "DRAFT"`.

**Pattern:**
- For table-column DRAFT → WAITING_ON_APPROVAL submit: ALWAYS call `edit<X>Repository` with `status: "WAITING_ON_APPROVAL"` — this is the only repo path that creates the approval record.
- `submit<X>Repository` is ONLY for APPROVED → FINAL_STATUS (called from `publish<X>FromApprovedAction`).
- `generateSeriesNumber` gate in `edit<X>Action` MUST be `WAITING_ON_APPROVAL && prevData === DRAFT`, never the final status like `WAIT_DELIVERY`.

---

## Lesson: submitPurchaseReceiptAction missing actionBy caused approval_id not created

**Problem:**
`submitPurchaseReceiptAction` (table-column DRAFT submit) spread `parent` into `updatePurchaseReceiptRepository` without overriding `actionBy`. `parent.actionBy.updatedBy` = previous updater (possibly null). The repository's employee lookup used that null/wrong user → `createBy: ""` → approval creation failed or created with missing employee data → `approvalId` never set on header.

**Solution:**
Pass `actionBy` explicitly as an override in the spread: `{ ...parent, items: child, status: "WAITING_ON_APPROVAL", transactionDate: now, actionBy }`.

**Pattern:**
- When building DTO from `mappingDataToDtoAction` (or any entity-to-DTO transform), always override `actionBy` with the current caller's `actionBy` before passing to the repository. Never rely on stored `updatedBy` for the current user identity.

---

## Lesson: CASE...WHEN in sql`` templates must CAST numeric values

**Problem:**
Passing bare values into a CASE...WHEN `sql` tagged template expression for a `numeric` column — e.g. `THEN ${item.density ?? null}` or `THEN ${String(item.qty)}` — causes PostgreSQL to infer the CASE result type as `text`. PostgreSQL then rejects assignment to a `numeric` column with: `column "xxx" is of type numeric but expression is of type text`.

**Solution:**
Always wrap numeric values with `CAST(... AS NUMERIC)` inside CASE...WHEN `sql` templates:
```ts
sql`WHEN ${table.id} = ${item.id} THEN CAST(${currency(value ?? 0).toString()} AS NUMERIC)`
```

**Pattern:**
- Never use `THEN ${item.field ?? null}`, `THEN ${String(item.field)}`, or `THEN ${item.field.toString()}` when the target column is `numeric`.
- Always use `THEN CAST(${currency(value ?? 0).toString()} AS NUMERIC)` for every numeric column in a CASE...WHEN bulk UPDATE.
- In `.values()` / `.set()` direct assignments, `currency(value ?? 0).toString()` is sufficient — no CAST needed there.

---

## Lesson: Never write a direct status update to APPROVED in a repository

**Problem:**
An `else` block in `editItemTransferReceiveRepository` directly set `status: "APPROVED"` on the header record when `approval.create()` returned falsy. This bypassed the approval service entirely — the record would jump from `WAITING_ON_APPROVAL` to `APPROVED` without any real approval ever occurring.

**Solution:**
Remove the `else` block entirely. When `approval.create()` returns falsy (e.g. no approval config found), the status should remain `WAITING_ON_APPROVAL` as set on the header — it is not the repository's job to resolve that case by auto-approving. Status transitions to APPROVED must only happen via the external approval service callback, never via a direct DB write in an edit or submit repository function.

**Pattern:**
- Approval status transitions are owned by the approval service. Repository edit functions may set `WAITING_ON_APPROVAL` (to trigger approval creation), but must NEVER set `APPROVED` directly.
- The `if (approvalData)` guard in the approval creation block must have no `else` branch. If approval creation fails silently, leave the record in `WAITING_ON_APPROVAL` — do not compensate with a direct status flip.
- `APPROVED` is a status that must only arrive from the external approval service writing back to the module.

---

## Lesson: CASE...WHEN sql templates must CAST timestamp values

**Problem:**
Passing bare values into a CASE...WHEN `sql` tagged template expression for a `timestamp with time zone` column — e.g. `THEN ${item.expiredDate ?? null}` — causes PostgreSQL to infer the CASE result type as `text`. PostgreSQL then rejects assignment to a `timestamp with time zone` column with: `column "xxx" is of type timestamp with time zone but expression is of type text`.

**Solution:**
Always wrap timestamp values with `CAST(... AS TIMESTAMPTZ)` inside CASE...WHEN `sql` templates:
```ts
sql`WHEN ${table.id} = ${item.id} THEN CAST(${item.expiredDate ?? null} AS TIMESTAMPTZ)`
```

**Pattern:**
- Never use `THEN ${item.field ?? null}` when the target column is `timestamp with time zone`.
- Always use `THEN CAST(${item.field ?? null} AS TIMESTAMPTZ)` for every timestamp column in a CASE...WHEN bulk UPDATE.
- `CAST(NULL AS TIMESTAMPTZ)` is valid PostgreSQL — null is preserved correctly.
- In `.values()` / `.set()` direct assignments, bare string/Date values are sufficient — no CAST needed there.
- Same principle as numeric CAST: any CASE...WHEN expression must explicitly CAST to match the target column type.
## Note: employee.repository.ts uses bare `throw error` throughout (pre-existing convention)

**Context (task 18476):**
A code-reviewer flagged that `findemployeeByUserAccountIdRepository`'s catch block does `throw error` (bare re-throw) instead of `throw new GlobalError("KEY")`. CLAUDE.md Rule 3 forbids `throw new Error(...)` — not bare `throw error`.

**Finding:**
ALL functions in `shared/repositories/employee/employee.repository.ts` consistently use bare `throw error` in their catch blocks. This is a file-wide pre-existing convention. It does not violate Rule 3 (which forbids constructing `new Error(...)`). Bare `throw error` simply re-throws whatever was caught.

**Decision:**
Do not change the newly added `findemployeeByUserAccountIdRepository` catch block — it matches the file-wide pattern. Do not refactor the entire file (out of scope). `EMPLOYEE_NOT_FOUND` exists in `shared/error/messages/hr.message.ts` if a specific GlobalError is ever needed for a "not found" guard in this function.

**Pattern:**
- Before flagging a catch block, distinguish `throw error` (re-throw — acceptable) from `throw new Error(...)` (construction — forbidden).
- Scope repo fixes to the function added in the current task; do not refactor the whole file.
