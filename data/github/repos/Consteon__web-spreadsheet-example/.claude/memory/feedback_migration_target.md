---
name: Always confirm migration target database before running
description: Never assume the target database — always ask the user which DB to run migrations against before executing
type: feedback
---

Always confirm the exact target database with the user before running any SQL migration or destructive DB operation.

**Why:** Ran migration against `adfood` (wrong DB) before rolling back and applying to `db_analyst` (correct DB). User explicitly stated the target — do not infer or assume from `.env` or prior context.

**How to apply:** When a migration needs to be run, if the user specifies a database name, use exactly that. If there is any ambiguity (e.g., connection error, DB not found), stop and ask the user to clarify — do not try alternate databases on your own.
