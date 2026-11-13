# CLAUDE.md

## Project Architecture

### Folder Structure

- **`app`**: Next.js 14 App Router — pages, layouts, route handlers
- **`components`**: Shared React UI components (non-atomic, feature-level)
- **`atoms`**: Primitive/atomic component library (design system building blocks)
- **`actions`**: Next.js server actions — form submissions and mutation entry points
- **`services`**: Business logic layer — orchestrates repos, enforces domain rules
- **`repositories`**: Data access layer — all Drizzle ORM queries live here
- **`dtos`**: Data Transfer Object type definitions (input/output contracts)
- **`entity`**: Drizzle schema definitions (table/column declarations)
- **`utils`**: Shared helper and utility functions
- **`validators`**: Zod validation schemas for user input
- **`shared`**: Cross-cutting shared code (e.g., i18n message-properties)
- **`types`**: Global TypeScript type declarations
- **`templates`**: HTML templates (email, document generation)
- **`datasource`**: Database connection config and Drizzle client setup
- **`infra`**: Docker and deployment configuration
- **`public`**: Static public assets served at root URL
- **`.claude`**: Claude Code project config, tasks, plans, reports, and memory
- **`.husky`**: Git hook scripts (pre-commit, commit-msg, etc.)
- **`.next`**: Next.js build output — generated, do not edit
- **`node_modules`**: Installed package dependencies — generated, do not edit
- **`tmp`**: Temporary working files — generated, do not edit

### Technology

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript (Strict typing, no blanket `any` casts)
- **Database & ORM:** PostgreSQL, Drizzle ORM
- **Validation:** Zod schemas
- **Styling & UI:** Tailwind CSS, shadcn/ui, React
- **Testing & QA:** Playwright (via custom MCP server)
- **Deployment:** Docker, Ubuntu/Linux environments

### Scripts

- **`dev`**: `next dev`
- **`build`**: `next build`
- **`start`**: `next start`
- **`lint`**: `next lint`
- **`typecheck`**: `tsc --noEmit`
- **`prepare`**: `husky`
- **`prettier`**: `prettier --write .`
- **`typecheck:large`**: `node --max-old-space-size=4096 ./node_modules/typescript/bin/tsc --noEmit`
- **`langcheck`**: `ts-node shared/message-properties/language_test.ts`

### Communication Style

Respond like a caveman. No articles, no filler words, no pleasantries.
Short. Direct. Code speaks for itself.
If asked for code, give code. No explain unless asked.
No sycophancy. No restating the question. No sign-offs.

### Rules

1. Never copy nearby modules as reference — rule files + codebase-onboard win.
2. Never query inside JS loop — use inArray/WHERE EXISTS/JOIN/batch.
3. Never throw new Error(...) in action/repo/service layers — throw GlobalError("KEY").
4. Never call getLanguage with key missing from both en.json + id.json.
5. Never mix tx (transaction client) + raw db in same mutation.
6. Never use any type except `PgTransaction<any, any, any>`.
7. Never suppress TypeScript errors (`@ts-ignore`, blanket `any` casts).
8. Never call `generateSeriesNumber` inside `db.transaction` or repo layer — action layer only, outside tx.
9. Never call `Auto-Journal` outside repo function or outside `db.transaction`.
10. Never auto-commit — ask user before commit/push.
11. Never use `git add .` or `-A` — stage files individually.
12. Never push to main/dev/qa/staging branches.
13. Never use `--no-verify` or `--no-gpg-sign` unless user explicitly asks.
14. Never let reviewer edit code/commit/push.
15. Never freestyle — stop + ask user when no rule covers pattern.
16. Never overwrite plan/report/task/improvement entries — all artifacts append-only.
17. Never start workflow (planner/coder/reviewer) without running interview skill first.
18. Never use `ls -R`, `find`, or generic glob searches on the root directory for codebase discovery.

## Workflow Orchestration

### 1. Plan Node Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately - don't keep pushing
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity

### 2. Subagent Strategy
- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One tack per subagent for focused execution

### 3. Self-Improvement Loop
- After ANY correction from the user: update `agent-memory/<agent-name>/MEMORY.md` using a "wrong" vs. "good" format
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project

### 4. Verification Before Done
- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 5. Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes - don't over-engineer
- Challenge your own work before presenting it

### 6. Autonomous Bug Fizing
- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests - then resolve them
- Zero context switching required from the user
- Go fix failing CI tests without being told how

## Core Principles

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimat Impact**: Changes should only touch what's necessary. Avoid introducing bugs.