# 0003. A clash means no single action satisfies both rules; "may" is a strong permission

Date: 2026-11-19. Status: Accepted.

## Context
Labelling showed that readers used different meanings of "clash". Two candidates:
1. "Following one rule can break the other." Taken literally, almost every pair clashes through
   details neither rule mentions (for example the timing of "prune after each clone batch").
2. "In some situation, no single action satisfies both rules." This is the standard meaning of
   inconsistency, and Z3 can answer it exactly.

Under (2), the reading of "may" decides pairs such as "create PRs with MCP" vs "you may also
create PRs with gh-cc-var". In deontic logic (the logic of obligation and permission), von Wright
separates a weak permission (merely not forbidden) from a strong permission (explicitly stated
by the rules). Vranes (2006) argues that a norm conflict covers obligation vs prohibition,
obligation vs permission not to act, and prohibition vs permission. Norm-conflict checkers in
multi-agent systems (Vasconcelos, Kollingbaum & Norman, 2008) also treat permission vs
prohibition as a conflict.

## Decision
Two rules clash if, in some situation the rules name, no single action satisfies both. The
words that set a rule's force are read as follows:

| Words | Meaning | Clause |
|---|---|---|
| must, always, do X | obligation | `must_do` |
| never, don't, avoid | prohibition | `never` |
| may, it's fine to, permit | strong permission: the action must stay possible | `may_do` |
| only if, not without, before X do Y | conditional obligation | `only_if` |

An explicit "may" in a memory rule is a strong permission, because the rule states it. "Use M
for X" read together with "use G for X" is a clash when the agent uses one tool per task
(indirect conflict: it depends on knowing that the two options exclude each other, and that,
for example, a lookup is a kind of read).

## Consequences
- An exception written as a permission ("you may skip dev-bot testing for test-only PRs")
  clashes with the rule it excepts. This is intended: the agent must know which rule wins.
- The checker already treats `may_do` as a strong permission.
- Sources (abstracts and summaries only, to be read in full before citing): Vranes 2006, EJIL
  17:395; Vasconcelos, Kollingbaum & Norman 2008, JAAMAS; Torres da Silva et al. 2015 on
  indirect conflicts; von Wright 1951/1968 via secondary sources.
