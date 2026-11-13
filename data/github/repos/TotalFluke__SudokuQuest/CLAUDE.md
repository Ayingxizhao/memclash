# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SudokuQuest is a browser-based puzzle game in which many sudoku — classic and variant (Thermometer, Kropki) — are overlaid on one plane to form a single large **quest**. Neighbouring puzzles share cells; solving one puzzle fills in the shared cells of the next and so reveals where the quest continues. Quests can branch. The project builds both the **player game** and the **setter tooling** (solver, uniqueness verification, browser editor) needed to author quests. See `spec/overview.md` for the full picture and `plans/roadmap.md` for the PoC sequence.

The project is **client-only**: Svelte 5 (runes) + TypeScript + Vite, no backend. Puzzle logic lives in a pure TypeScript engine (`src/engine/`) with the Svelte UI as a thin shell over it.

## Quick Start

Requires Node.js ≥ 24.

```bash
npm install
npm run dev        # dev server on http://localhost:5173
```

A checkout under `.claude/worktrees/` (an agent worktree) serves on its own port
in 5200–5499 instead, so parallel runs don't collide — see `spec/development.md`.

## Commands

```bash
npm run dev          # Vite dev server
npm run build        # Production build to dist/
npm run preview      # Serve the production build
npm run check        # svelte-check + tsc type checking
npm run test         # Vitest in watch mode
npm run test:unit    # Vitest, single run
npm run test:e2e     # Playwright e2e tests (starts the dev server itself)
npm run test:all     # Unit + e2e, single run

# Run a single unit test file
npx vitest run src/engine/grid.test.ts

# Run a single e2e test
npx playwright test e2e/app.spec.ts
```

First e2e run may need `npx playwright install chromium`.

## Pre-Commit Requirements

**IMPORTANT**: Before committing code, all of these MUST pass:

```bash
npm run test:all && npm run build && npm run check
```

`test:all` is Vitest unit tests then the Playwright e2e suite; report both counts. The line that proves each ran is Vitest's `Tests  N passed` and Playwright's `N passed`. Never pipe a gate through `tail` without `pipefail`, since a piped failure reads as success. The first e2e run in a fresh environment may need `npx playwright install chromium`.

These gates are also recorded in `.claude/project-profile.md` (`## Gates`),
which the `workflow` plugin's skills read. Change both together.

## Project Structure

- `src/engine/` — pure TypeScript puzzle engine: types, grid helpers, constraints, solver, quest overlay model, generation. **No DOM or browser APIs here.** Densest unit-test coverage. All randomness goes through a seeded RNG (never `Math.random`), so generation and any test that depends on it are reproducible from a seed.
- `src/setter/` — setter-side logic that is not needed by the player (given minimisation, quest verification reports). Still pure TypeScript.
- `src/save/` — persistence (browser storage, quest export/import as JSON).
- `src/ui/` — Svelte components: the board, the quest map, the player and setter surfaces.
- `src/theme/` — design tokens (`tokens.css`); components consume tokens, never hardcode colours.
- Unit/component tests are colocated `*.test.ts` files under `src/`; e2e tests live in `e2e/*.spec.ts`.
- `public/quests/` — shipped quest JSON files (see `spec/engine/puzzle-format.md`).

## Specification (`spec/`) — Authoritative

The `spec/` directory is the **authoritative specification** for this project. The implementation conforms to the spec, not the other way around. Start at `spec/README.md` for the document map.

Key rules:

- **Status markers**: every spec document is marked Stable, Draft, or Exploratory. Stable and Draft sections are binding; Exploratory sections (and `spec/game/ideas.md`) are not.
- **Code/spec divergence is a bug**: if the implementation must deliberately diverge, update the spec in the same change. Never let them drift silently.
- **Rationale lives in ADRs**: `spec/decisions/` records why choices were made and the alternatives considered. The spec states only the outcome.
- **No progress tracking in spec/**: execution state belongs in `plans/`; history belongs in git.

When implementing anything, read the relevant spec documents first and conform to them. If a task requires changing the spec, make the spec change part of the task.

## Plans Workflow (`plans/`) — Execution, not authority

Plans are short-lived execution documents: they describe *how and when* a slice of work gets implemented. Plans must conform to the spec in `spec/`; if a plan requires a spec change, update `spec/` as part of the plan. Durable design content (requirements, contracts, schemas, decisions) belongs in `spec/`, not in plans.

`plans/roadmap.md` lists the intended order of plans and is updated as plans land.

Plans are stored in the `plans/` directory. When asked to start a new plan:

1. Create a new directory under `plans/` using a short descriptive name (e.g., `plans/search-index/`)
2. Create two files in that directory:
   - `plan.md` - The detailed plan with goals, approach, an `## Estimate` section, and implementation steps (organised into phases; one phase = one atomic commit)
   - `progress.md` - Track progress, completed items, blockers, and notes as work proceeds

### Every Plan Carries an Estimate

`plan.md` has an `## Estimate` section stating how long the plan takes to run unattended through `/workflow:implement` — Claude doing the work, not the user. Two parts:

- **Per phase**, one bucket: `minutes` (under 15), `~1 h`, `~half a day` (2–4 h), `~a day` (4–8 h), or `days`. Beside the bucket, name every single action expected to exceed 30 minutes of wall clock — a long test or measurement run, a rerun loop — with its own figure and the timeout it runs under. No long action is left unbounded.
- **Overall**, one bucket for the whole plan, on a line that starts `Overall:`, and a note if a phase must serialise on a shared resource (an exclusive resource in `.claude/project-profile.md`'s `## Parallelism`), since that stretches the wall clock when plans run in parallel.

Precision is not the point; relative order of magnitude is. The user calibrates against actuals over time, so when a phase closes, `progress.md` records its actual wall clock beside the estimate. Before estimating a long action, read the newest actuals in `plans/*/progress.md` rather than guessing. `/workflow:progress` sums the unticked phases into its *Est. remaining* column and `/workflow:implementall` sizes its waves from these sections; a plan without one shows up there as a guess.

### Keeping Plans Updated

**IMPORTANT**: Update `progress.md` incrementally as work proceeds, not just at the end. After completing each significant step or making a decision:

1. Mark the item complete in `progress.md`
2. Add any notes, blockers discovered, or scope changes
3. If scope expands significantly, update `plan.md` to reflect new work

This creates a clear audit trail and helps resume work after interruptions.

### Write Plans Against the Anticipated State

When drafting a plan while sibling plans are mid-`/workflow:implement`, target the state **after** those plans land, not current `master`. Read the other directories under `plans/` and the unmerged `implementations/*` branches first (`/workflow:progress` lists them), and say in `plan.md` which in-flight work you assumed.

Keep each plan narrow even when that leaves the project temporarily incomplete. A plan sized to keep everything working at every commit has to absorb every cross-cutting concern its neighbours are already handling, and wide plans merge badly. If a change breaks something that is another plan's remit, record it in `plan.md` as an accepted intermediate state rather than raising it as a blocker or widening scope. Plans whose scope changes the same feature's behaviour (one engine rule, UI surface or spec section) must not share a wave, because two incompatible shapes for one thing are a product decision; `/workflow:implementall` runs such plans one after the other, so partition work to avoid it.

Narrow has a number: aim for **at most six phases and roughly 3,000 changed lines** per plan. Plans of that size run through `/workflow:implement` in under an hour; plans of 8–16 phases have taken two to five hours each and caused most of the merge conflicts. When review of a finished branch produces follow-up work, file it as a **new plan** rather than appending phases to the running one — the second round merges on its own and doesn't hold the first hostage.

### Finalizing Plans

**IMPORTANT**: The final steps of any plan should always be:

1. **Write tests for the new functionality** — engine logic gets colocated Vitest unit tests, from a fixed seed for anything generated; UI flows get component and/or Playwright e2e coverage (`.claude/project-profile.md`, `## Test conventions`).
2. **Get the new tests passing.**
3. **Run the full quality gates**: `npm run test:all && npm run build && npm run check` — all must pass.
4. **Commit and push** — via `/workflow:finalise`.
5. **Merge to `master`** — via `/workflow:merge`. A plan run through `/workflow:implement` lands on an `implementations/<plan-name>` branch in its own worktree and is never merged automatically; merging is a separate, explicit step after the branch has been reviewed. `/workflow:implementall` is the one exception: asked to clear the whole backlog, it merges each branch as its plan finishes, without a review.

This ensures every plan results in verified, working code that's safely stored in version control.
