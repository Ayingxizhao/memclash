# 0005. Find git rules with keywords OR an LLM question; estimate misses by sampling

Date: 2026-11-19. Status: Accepted.

## Context
Translating every rule of a large folder is costly, and most rules are not about git. A git rule
the filter drops can never be checked, so the filter must miss as little as possible.

## Decision
A rule is kept if either test says yes: a regular expression of git and GitHub words, or a short
LLM yes/no question with no folder context ("if unsure, answer true",
`prompts/git/git_filter.md`). Misses are estimated by reading a random sample of rejected rules
by hand: 0 git rules in n read gives an upper bound of about 3/n at 95% (rule of three).

## Consequences
- Large folders: 677 rules, 212 kept; 0 git rules in a random sample of 120 rejected rules, so the
  miss rate is below about 2.5%.
- Each test caught rules the other missed (the LLM caught "unpushed", "cloning", "refetch"; the
  keywords alone flagged rules the LLM correctly rejected), so both are kept.
