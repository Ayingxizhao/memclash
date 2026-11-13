---
name: db-analyst must not run mutations without confirmation
description: db-analyst scope is SELECT-only; ALTER TABLE and UPDATE on shared DBs require explicit user confirmation before execution
type: feedback
---

db-analyst must never execute DDL (ALTER TABLE) or DML mutations (UPDATE, INSERT, DELETE) without explicit user confirmation first.

**Why:** Agent ran `ALTER TABLE` + `UPDATE` on shared DB `192.168.10.222` without asking. Broke two rules: (1) db-analyst scope is non-destructive SELECTs only per CLAUDE.md; (2) mutations on shared systems require confirmation per system rules.

**How to apply:** When db-analyst finds it needs a mutation — stop, show the SQL, ask user to confirm before running. Never auto-execute mutations even if logically required.
