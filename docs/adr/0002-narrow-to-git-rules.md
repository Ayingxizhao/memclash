# 0002. Narrow the exact method to git rules and a fixed git model

Date: 2026-11-19. Status: Accepted.

## Context
Translating any memory rule into logic was unreliable: one fixed format for every rule found 0 of
10 labelled conflicts (`gate_v1/`). Tools that check rules exactly work on structured subjects
(config files, access policies such as Cedar), where the vocabulary is fixed in advance.

## Decision
For the exact method, handle only rules about git. A fixed git model
(`pipeline/git/git_check.py`) lists the operations (commit, push, merge, ...) and the facts
about them (branch, file, user asked, tests passed, ...). An LLM translates each rule alone into
clauses over this model; Z3 checks every pair of rules in a folder.

Cedar itself is not used: it decides at run time whether one request is allowed, has no notion
of "must do", and lets "forbid" always win over "permit", so it cannot express the clashes we
look for.

## Consequences
- Z3's answer is exact for what the model can express.
- Anything outside the model is invisible to the checker: tool choice (MCP vs CLI), words such as
  "backlog sweep" or "firmware". On the large folders, all 11 reference clashes fall outside the
  model (see ADR 0006), so the model must grow (for example a tool field) or the limit must be
  stated.
- Rules that are not about git are handled by the general method, not by this one.
