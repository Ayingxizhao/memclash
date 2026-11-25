# CLAUDE.md

Guidance for AI coding tools working in this repo. Structure follows Anthropic's recommended CLAUDE.md layout; sections are filled as we decide them.

## House rules (always apply)

The few rules that must survive long, complex sessions. Re-read before writing a DECISIONS entry or committing.

- **DECISIONS.md = decisions, in discussion voice.** A paragraph or two per decision: who proposed it, the push-back, where it landed, the trade-off. Not a spec dump, not a work log, not a bullet list of what the code does. Keep it concise.
- **Small components, no giant files.** Split the frontend into focused component files — reusable ones in `src/components/`, page-specific ones in a colocated `_components/` folder. `page.tsx` composes; it doesn't hold many components. Never let one file grow into a pile of components.
- **Approval gates.** Never commit, push, or delete a branch without an explicit user "go". Code on its own branch; docs/non-code can commit on the current branch.
- **Right-sized, no over-engineering.** Smallest change that fully does the task. Don't add shared constants / config / indirection for values that are fixed requirements (e.g. the 2/1 image caps).
- **Never touch `.env`.** Don't read or edit the user's `.env`. Communicate config only via `.env.example` or chat.
- **Docs move with the work.** Update `DECISIONS.md`, `docs/plan.md`, `docs/tasks.md`, `TESTING.md` as part of the change, not as an afterthought. When a real test run changes, refresh the `TESTING.md` count/report.

## Project overview

Web app: turns a book's text into character portraits and one chapter illustration via the Gemini API. Five user-driven steps, run one at a time by the user: Style → Characters → Portraits → Chapters → Illustrations. Scope is bounded on purpose — max 2 adult characters, max 1 chapter, enforced server-side.

Two modes, chosen up front and **locked when Style runs**: **Auto** (the server picks the top characters/scene — the original behaviour) or **Selection** (the user picks which characters/chapter to illustrate from a model-proposed candidate pool). A **no-content guard** stops non-book / too-short text (no characters or chapters found → delete and start over).

## Tech stack

- **Next.js** — full-stack (frontend + API route handlers), one framework for both. Chosen because the scope is bounded; a single framework is enough, no separate frontend/backend services.
- **Gemini API** — text model + Nano Banana image model, via the Interactions API (chained by `previous_interaction_id`) with File API upload for the book. JS SDK available (Next.js is JS); REST is the fallback. Model IDs: TBD.
- **Storage** — JSON files on disk (no DB). One file per entity type: `data/projects.json`, `data/users.json`; load → mutate object → serialize back (demo's pattern, swapped off localStorage to server disk). Lock on the file + atomic temp-write/rename. Images and book text are separate files under `data/`, referenced by path, served through our own API. See `DECISIONS.md`.

## Gemini API rules

- **Backend only.** Every Gemini call happens server-side. Never call Gemini from the client — protects the key and keeps the single-call guard in one place.
- **Official SDK.** Use the official Gemini SDK (JS, since Next.js is JS), not hand-rolled REST unless the SDK lacks an endpoint we need.
- **Send the book once, reuse the result.** Upload the book once (File API) and chain interactions by id (`previous_interaction_id`). Never re-send the full book text on later steps.
- **No auto-retry.** Never retry a failed Gemini call in a loop. Retries are user-triggered only.
- **Key in env var**, never committed. Ship `.env.example`.
- **Caps enforced server-side.** A finished project draws at most **2** character portraits + **1** chapter illustration — the hard, cost-bounding cap on *images* (each image is a paid request). In **Selection** mode the text step may propose a larger candidate *pool* (`CHARACTER_POOL` / `CHAPTER_POOL`, text-only and cheap) to pick from; **Auto** asks for only the capped count. Either way the backend caps the drawn images (`resolveSelection` slices to `MAX_CHARACTERS` / `MAX_CHAPTERS`) — never rely on the UI. The image caps are fixed literals, not tunables.
- **No-content guard.** If the text yields no characters/chapters, the step fails with a "delete this project / start a new one" message — there is no in-project recovery (you can't conjure characters a text lacks). Plus a length pre-check at project creation.

## Commands

> One command starts the stack, one runs the tests (§5.5). No Docker.

- One-command wrappers (bash; Git Bash on Windows): `./start.sh` · `./test.sh` (each runs `npm install` first; `start.sh` also creates `.env` from `.env.example` on first run, never overwriting an existing one)
- Start: `npm run dev` (after `npm install`) · Test: `npm test`
- Build: `npm run build` · Lint: `npm run lint`

## Code style

- **Semantic HTML + Tailwind together** — use meaningful elements (`header`, `nav`, `main`, `section`, `article`, `button`, ...) over `div` soup. Each element carries a **semantic class name** for its meaning/role (e.g. `retry-button`, `home-page`) **plus Tailwind utility classes** for styling. The semantic name conveys purpose and is a hook for advanced CSS when Tailwind isn't enough; Tailwind handles appearance. Both coexist on the same element; the semantic name is never appearance-based.
- **Semantic naming** — functions and variables named for what they do / represent. Well-known short forms are fine (`id`, `db`, `err`, `prev`, `tmp`); cryptic single letters are not (`u`→`user`, `p`→`project`, `c`→`chapter`, `i`→`index`).
- **Consistent naming convention** — names follow one consistent pattern across the codebase, not ad-hoc per function. Use a steady verb + noun set (e.g. `createProject`, `readProject`, `updateProject`, `saveProject`, `listProjects`, `deleteProject`; same shape for users). Implementation mechanics stay **out** of the name — a `saveProject` that writes safely is still `saveProject`, not `saveProjectWithoutCorruption`; the "how" (lock, temp-file swap) lives inside the function and is explained by a short comment. The name carries purpose; the comment carries mechanism.
- **Comments** — concise and direct. Lead with the block's main purpose (why it exists); mention how it runs only where non-obvious. No narrating the obvious.
- **Organized & reusable** — structured folder, code, clear module boundaries, factor shared logic into reusable helpers instead of copy-paste.
- **Least code, same result** — reach for the smallest solution that fully does the task. No abstractions for features we aren't shipping. Right-sized over clever.
- **Optimize** — remove dead code and needless work; keep hot paths (Gemini calls, polling, file I/O) lean. Optimize for clarity first, then cost.

## Testing

Kept simple and targeted — 3-day scope, no over-testing. No E2E.

- **Layers**
  - **Unit (backend)** — pipeline logic: step-order guard, no-duplicate (running step returns in-flight), retry (failed step retryable, others untouched), stuck recovery (running+stale → retryable), caps (>2 chars / >1 chapter refused).
  - **Integration (backend)** — happy-path run through all 5 steps with a **mocked Gemini** (no quota, no key, deterministic).
  - **Component (frontend)** — key states only: error+retry, empty list, in-progress naming the step.
- **Tools** — Vitest (runner for unit + integration), React Testing Library (components), Gemini SDK mocked in all tests.
- **TDD leash** — test-first on backend pipeline logic (pins behavior before AI writes code); test-after on frontend states.
- **Deliverables** — `TESTING.md` (what we test, what we skip, why) + a real test-run report.

## Repo etiquette

- **Every commit needs user approval** — docs and code alike. Stage/prepare, then wait for the go before committing.
- **Docs & non-code — commit on the current branch**, no new branch needed: documentation, decisions, planning notes, and other non-coding changes.
- **Code — on its own branch.** Never work code directly on `main`/`master`; check out a dedicated branch (feature, fix, or next phase) and commit there after approval.
- **Deleting a branch needs explicit approval** (like commit/push). Merged branches may be deleted once the user asks; never delete on your own initiative.
- **Pushing** to a remote needs approval regardless of what changed.

## Where the detail lives

- Roadmap / milestones: `docs/plan.md`
- Task checklist (tick as we build): `docs/tasks.md`
- Key decisions and AI overrides: `DECISIONS.md`
- Open / undecided questions: `docs/open-decisions.md`
- Testing approach and test report: `TESTING.md`
- Working context & preferences (memory): `.claude/memory/`
- Resume the project: `/resume` (`.claude/commands/resume.md`)

## Notes & warnings

- **Deliberately simple, local-only.** No Docker, no separate backend language or service — one Next.js app. This is a right-sized choice for a bounded 3-day assessment: simpler to run and test, one command each.
- **Accepted production limitation.** This shape does not target real production. Next.js alone, running the async step work in-process, would not hold up under production load — serverless handlers time out on long interactions, in-memory in-flight state is lost on restart or scale-out, and there is no durable job queue. A real deployment would need a proper background-job/queue layer and durable state. Out of scope here on purpose; documented as a known trade-off.
