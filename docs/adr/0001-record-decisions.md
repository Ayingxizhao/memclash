# 0001. Record decisions as ADRs

Date: 2026-11-19. Status: Accepted.

## Context
The project changed direction several times (general method, one fixed format for every rule,
git-only method). The reasons were spread across chats and notes, which makes them hard to
defend in the talk and report.

## Decision
Every decision that changes what we measure or how we measure it gets a short ADR in
`docs/adr/`: Context, Decision, Consequences. A changed decision gets a new ADR that supersedes
the old one.

## Consequences
The report's method section can be written from these files. Each ADR must stay short and in
plain words.
