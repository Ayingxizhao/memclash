---
name: Prefer concrete types; avoid unknown/any/never and eslint-disable
description: User dislikes unknown/any/never in type annotations and dislikes eslint-disable comments; only use them when genuinely required, and never pair an `any` with an eslint-disable
type: feedback
---

Avoid `unknown`, `any`, and `never` in type annotations by default — reach for a concrete type first. Do not silence lint rules with `// eslint-disable`.

**Why:** The user said "I don't like `unknown`, `any`, `never` in general" and, in the same 2026-04-22 exchange, "similarly, avoid eslint-disable. i don't like that as well." They accept broad types when structurally unavoidable — e.g. a generic Express middleware whose return type widens `RequestHandler` generics so downstream controllers can narrow `ReqQuery` to a Zod-parsed type — but they do **not** accept `any` plus an eslint-disable pragma as a shortcut. When concrete types won't fit, use `unknown` (accepted by the lint config) rather than `any`.

**How to apply:**
- When tempted to write `unknown` / `any` / `never`, first ask whether the function actually uses the full shape. If it only reads a subset of fields, type the parameter to that subset. Example from this repo: `getUid(req: { user?: { uid?: string } })` is cleaner than `Request<Record<string, unknown>, unknown, unknown, unknown>`.
- If a broad type is genuinely required, prefer `unknown` over `any` so no eslint-disable is needed. In this repo the validate middleware uses `RequestHandler<Record<string, unknown>, unknown, unknown, unknown>` for exactly this reason.
- If keeping a broad type, leave a short comment explaining why so the choice doesn't look lazy on later reads.
- Never introduce `// eslint-disable…` to silence a rule — fix the underlying type/design instead.
