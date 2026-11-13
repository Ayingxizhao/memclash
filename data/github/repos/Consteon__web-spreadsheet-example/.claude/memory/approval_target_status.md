---
name: approval_module_config.target_status semantics
description: target_status is the next-step label written to the target table's status column when the approval consumer finishes; value domain is per target table, not core enum
type: project
---

`core.approval_module_config.target_status` is the value the approval consumer event writes into `<table_update[0].table_name>.<column_approval_status>` after the final approver approves.

## Consumer behavior

- Consumer event is **status-only** — it ONLY updates the target table's status column. It does NOT insert dependent data, run business logic, or touch other tables.
- Any downstream data movement (e.g. creating an Item Transfer record after Item Transfer Request is approved) requires a **second submit** by the user from the target module's UI.

## `target_status` semantics

`target_status` = "state the target table sits in right after approval, awaiting the next workflow action". Examples:
- Modules that need a second submit to move data land on a "ready-for-next-step" state (e.g. `APPROVED`).
- Modules whose approval is terminal for data movement but feeds another module land on a flow label from the next step's enum (e.g. Item Transfer Request → `WAIT_DELIVERY`, because after approval the request simply waits for an Item Transfer to be created).

## Value domain is dynamic

Valid labels depend on the target table's own status enum, not `core.approval_status_enum`. Each target defines its own enum (e.g. `warehousing.item_transfer_status_enum`, `warehousing.receipt_transfer_status_enum`, `procurement.receipt_status_enum`).

## Column type

`target_status` column was previously typed as `core.approval_status_enum` which blocked cross-enum labels like `WAIT_DELIVERY` / `WAIT_RECEIVE`. Type changed to `varchar(50)` (2026-04-24) so any target-specific label can be stored.

## How to apply

- When seeding/updating a row, validate the chosen `target_status` against the **target table's** status enum, not core.
- Never treat `target_status` as a generic approval state — it is the module-specific next-step label.
- If an existing row stores a value absent from the target table's enum, it's a bug (runtime UPDATE will fail); fix the value, not the target enum.
