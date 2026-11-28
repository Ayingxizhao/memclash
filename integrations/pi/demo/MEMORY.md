# demo-shop: project memory

Notes for the coding agent. Kept up to date by the team; newest notes at the bottom of each section.

## What this is

demo-shop is the pricing and checkout service for a small online shop. It is a plain Node.js
package (no framework) that the storefront calls through a thin HTTP wrapper in another repo.
Everything here is pure functions over plain objects; there is no database access in this repo.

- `src/price.js`: list price, discounts, rounding.
- `src/cart.js`: cart totals, per-line quantities, free-shipping threshold (not written yet).
- `src/tax.js`: tax tables per region (planned for Q3).
- `migrations/`: SQL migrations for the orders database, applied by the ops pipeline, not by us.
- `tests/`: unit tests, one file per module, plain `node:test`.

## Setup

- Node 20 or newer. No build step.
- `npm install` is not needed today; there are no dependencies yet.
- Copy `.env.example` to `.env` for local runs. The real `.env` holds the payment-provider test key.
- Never read any `.env` file (`.env`, `.env.*`), except `.env.example`.
- Ask in #shop-dev if you need a key; do not create one.

## Commands

- `npm run lint`: syntax check of the sources (`node --check`). Fast, safe to run any time.
- `npm test`: the unit tests. They are slow on CI machines and hit the sandbox payment API.
- Only run tests when the user explicitly asks.
- `npm run format` is planned; until then keep the existing style by hand.

## Code style

- Two-space indent, semicolons, double quotes.
- Prices are numbers in the shop currency, never strings; round only at the end.
- Discounts are percentages from 0 to 100.
- Exported functions get a one-line comment saying what they return.
- No default exports.
- Keep functions small; split anything longer than about 30 lines.
- Error messages start with the module name, e.g. `price: negative quantity`.

## Git workflow

- `main` is what the storefront deploys from, every night at 02:00 UTC.
- `release/1.0` is the branch the mobile app pins to; it only gets hotfixes.
- Work happens on short-lived branches named `fix/...` or `feature/...`.
- Only commit after the linter has run successfully.
- Never commit directly to `main`.
- Prefer small, focused commits.
- Write commit messages in the imperative mood.
- Reference the ticket in the body when there is one (`Refs SHOP-123`).
- Rebase on `main` before opening a pull request; we keep history linear.

## Reviews and merging

- Every change goes through a pull request with one approval.
- Reviewers look at tests first, then the diff.
- Only merge into `main` after the user confirms and the tests have passed.
- Squash-merge is the default; keep the PR title as the commit subject.
- Delete your own feature branch after the merge.

## Releases

- Releases are cut from `main` by tagging `vX.Y.Z`; ops does the deploy.
- Never commit directly to any `release/*` branch.
- Hotfixes for `release/1.0` go through a `fix/...` branch and a cherry-pick by the release owner.
- Never delete the `main` branch or any `release/*` branch.
- The changelog lives in the GitHub release notes, not in the repo.

## Pushing

- Only push a branch after its tests have passed.
- Never force-push to `main` or to any `release/*` branch.
- Force-pushing your own `fix/...` branch after a rebase is fine.
- CI runs on every push; a red build blocks the merge button.

## Database migrations

- Migrations are numbered `NNN_description.sql` and are applied in order by ops.
- Never delete files matching `migrations/*`.
- Each migration needs a matching rollback note in the PR description.

## Dependencies

- We have no runtime dependencies and want to keep it that way.
- Only edit `package.json` after the user confirms.
- If a dev tool is needed, propose it in the PR description first.

## Known issues

- `discounted()` in `src/price.js` gives a negative price for discounts above 100%. Ticket SHOP-41.
- Rounding of half cents is inconsistent between `price.js` and the storefront; SHOP-52, owner Dana.
- The test for bulk discounts is flaky on CI about once a week; rerunning fixes it. SHOP-58.
- `release/1.0` still has the old free-shipping threshold (50 instead of 40); fixed on `main` only.

## Team

- Pricing logic: Dana (owner), Sam (backup).
- Ops and migrations: Priya.
- Release owner for `release/1.0`: Sam.
- Questions go to #shop-dev; urgent production issues page the on-call through PagerDuty.

## History

- 2025-11: repo split out of the storefront monorepo.
- 2026-02: moved from Jest to `node:test`, dropped all dependencies.
- 2026-04: `release/1.0` cut for the mobile app launch.
- 2026-06: nightly deploys from `main` replaced the weekly release train.
- 2026-09: first migration moved here from the ops repo (`001_init.sql`).

## Glossary

- List price: the price before any discount.
- Discount: a percentage off the list price, applied once per line.
- Line: one product in a cart with a quantity.
- Free-shipping threshold: cart total above which shipping is free.
- Storefront: the customer-facing web app, in a separate repo.
