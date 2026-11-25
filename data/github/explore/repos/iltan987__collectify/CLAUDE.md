# Collectify — Agent Context

Workspace-wide context for agents working in this repository. Per `.specify/memory/constitution.md` Principle V, all durable agent memory lives in `.claude/memory/` (not in per-user paths). This file is the top-level pointer that Speckit commands and the harness read.

## Active feature

<!-- SPECKIT START -->
- Feature: `002-pagination-filtering`
- Plan: [`specs/002-pagination-filtering/plan.md`](./specs/002-pagination-filtering/plan.md)
- Spec: [`specs/002-pagination-filtering/spec.md`](./specs/002-pagination-filtering/spec.md)
- Research: [`specs/002-pagination-filtering/research.md`](./specs/002-pagination-filtering/research.md)
- Data model: [`specs/002-pagination-filtering/data-model.md`](./specs/002-pagination-filtering/data-model.md)
- Contracts: [`specs/002-pagination-filtering/contracts/openapi.yaml`](./specs/002-pagination-filtering/contracts/openapi.yaml)
- Quickstart: [`specs/002-pagination-filtering/quickstart.md`](./specs/002-pagination-filtering/quickstart.md)
<!-- SPECKIT END -->

## Constitution

See [`.specify/memory/constitution.md`](./.specify/memory/constitution.md) for the five non-negotiable principles. Key operational reminders:

- **Phased gates** — every phase boundary ends with `pnpm --filter functions run lint && build && test` green, then **propose** a commit message and **wait** for the user's approval. Never `--no-verify`.
- **Verify libraries** — before invoking any third-party API from memory (Express 5, firebase-admin v13, firebase-functions v7, zod v4, express-rate-limit v8, vitest v4), check via `context7` or `node_modules/` first.
- **Delegate interactive steps** — `firebase login`, `gcloud auth login`, `firebase init`, enabling billing, real deploys: ask the user to run them and return the output.
- **Prefer official CLIs** — `pnpm add|remove|update`, `firebase deploy`, `firebase emulators:start`, etc. Do not hand-edit `package.json` / `pnpm-lock.yaml`.
- **Shared memory only** — new agent memory goes in `<repo>/.claude/memory/`, indexed in `.claude/memory/MEMORY.md`. No writes to `~/.claude/projects/.../memory/`.
- **No co-author trailers** — commit messages never include `Co-Authored-By` or agent-attribution footers.

## Repo shape

- Root is a pnpm workspace (`pnpm-workspace.yaml`) with a single package: `functions/`.
- Runtime: Node 24, TypeScript ^6, Express ^5, Firebase Functions ^7, Firebase Admin ^13. Tests use Vitest ^4 + Supertest + `firebase-functions-test`.
- Firebase config: `firebase.json` (Firestore `(default)` db in `nam5`; emulators on Auth:9099, Firestore:8080, Functions:5001). Firestore rules are at `firestore.rules`.
- Spec-kit feature workflow is tracked under `specs/<NNN-short-name>/`, indexed from this block.

## Project memory

See `.claude/memory/MEMORY.md` for the durable memory index.
