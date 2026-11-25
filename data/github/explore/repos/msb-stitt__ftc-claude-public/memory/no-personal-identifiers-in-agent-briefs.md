---
name: no-personal-identifiers-in-agent-briefs
description:
  "Every research agent's brief says to put no email address or other personal identifier in any
  request, query string or header."
metadata:
  type: feedback
---

A research agent's brief says: do not put the user's email address or any personal identifier in
any request, query string or header.

**Why:** on 2026-10-16 a research agent sent Mike's email address to the Unpaywall API in a query
string, twice, taking it from the `userEmail` its session context carries. Claude Code's docs name
no setting that turns that context off. Mike asked for the line to be standard the same day.

**How to apply:** every brief to an agent that may reach the web, research agents above all. See
[[instructions-state-facts-not-importance]] for the rest of a brief's register.
