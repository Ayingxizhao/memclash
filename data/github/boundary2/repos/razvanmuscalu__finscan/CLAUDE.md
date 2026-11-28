# CLAUDE.md

Guidance for Claude Code (claude.ai/code) when working with this repo.

## Communication Style — Caveman Ultra (Always)

All responses and file edits (prompts, identities, feedback, history, notes) use caveman ultra:

- Drop: articles (a/an/the), filler (just/really/basically/actually/simply), pleasantries, hedging
- Abbreviate: DB/auth/config/req/res/fn/impl
- Strip conjunctions; arrows for causality (X → Y)
- One word when one word enough; fragments OK
- Technical terms exact; code blocks unchanged
- Pattern: `[thing] [action] [reason]. [next step].`

Exception: security warnings, irreversible action confirmations, multi-step sequences where fragment order risks misread — write clearly, then resume caveman.

## Finance/Trading Topics — Research First, Always

User is engineer, finance-novice. Any topic touching finance, trading, investing, markets, portfolio, risk, instruments, strategies, indicators, macro:

- WebSearch for current/empirical claims; Context7 for library/API docs
- Assume nothing from training data — markets, regs, libs change fast
- Cite sources
- Translate findings to plain language; no jargon stacking
- Challenge user's ideas with researched counter-evidence; don't rubber-stamp guesses
- Insufficient research → say so, don't fill gaps

## Token Cost — Minimise at All Times

- **Never spawn subagents to read files.** Use Read tool directly. Subagents start cold, re-pay full system prompt, inflate every subsequent turn.
- **Never re-read file already read in same session.** Reference earlier read instead.
- **Read only what you need.** Use `offset`/`limit` on large files; don't read entire files when only section is relevant.
- **Keep responses short.** No preamble, no trailing summaries, no restating what was just done.
- **Prefer `grep`/`find` over Explore agents** for any search expressible as command.

## Pipelines — Default Edit Target

Repo has two worktrees:

- `~/Personal/GitHub/finscan-demo/` (primary, branch `main`) — **demo**. Default edit target.
- `~/Personal/GitHub/finscan-live/` (worktree, branch `live`) — **live**. Frozen between promotions.

Operate in primary unless user explicitly invokes promotion ritual. Never edit files inside `finscan-live/` directly — live tree advances only via `git merge --ff-only main` during promotion. Plist + prompt edits go in primary first. See `AGENTS.md` "Pipelines" + `docs/promotion.md`.

## Primary Reference

**Read `AGENTS.md` first** — canonical coding guide: project overview, full command reference, code style rules, testing patterns, metrics pattern, concurrency guidance.

For deeper context, read relevant file in `docs/` before any non-trivial task:
- `docs/architecture.md` — system diagram, component map, data flow, key patterns
- `docs/workers.md` — every in-process Go worker: schedule, inputs, outputs
- `docs/agents.md` — every Claude-loop agent (scheduled loops, critics, tooling)
- `docs/database.md` — all tables, columns, migrations
- `docs/config.md` — env vars, `workers.json`
- `docs/skills.md` — inventory of `.agents/skills/`, mapped to subsystems they shadow

## Downstream-impact check (before non-trivial changes)

Code lives in `internal/`, `cmd/`, `python/`, `pkg/`. Downstream artifacts that mirror code assumptions live elsewhere and silently rot:
- `.agents/agents/*/prompt.md` + `sub-prompts/` — critic + trader prompts often reference package names, struct fields, schedules
- `.agents/skills/*/SKILL.md` — operational skills cite file paths, table names, config keys
- `.launchd/jobs/*.plist` — schedules, env, log paths
- `docs/` — see list above

Before non-trivial code changes, grep these dirs for the symbols/paths/concepts you're about to touch:
```
grep -rln <package_or_symbol_or_path> .agents/ .launchd/ docs/
```
Review every hit. Update what's stale in the same commit. Use `docs-update` skill for structured doc refresh.

## Commands

```bash
make app-ci        # Full CI: tidy → build → vet → test → lint (run before every commit)
make app-tidy      # go mod tidy
make app-build     # go build ./...
make app-vet       # go vet ./...
make app-test      # go test -count=1 -race ./...
make app-lint      # golangci-lint run ./...

# Run a single test
go test -count=1 -race -run TestFunctionName ./path/to/package/

# Run a specific job locally
make app-job JOB=<name>
make app-job JOB=<name> AS_OF=2026-04-01T20:00:00Z

# Docker Compose
make compose-up
make compose-down
make compose-logs
make compose-app-restart
```

Pre-commit hook (`make setup` installs it) enforces `make app-ci` before every commit.

