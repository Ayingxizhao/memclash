# Three-rule clash test: preregistration (2026-11-23, before any result)

Question: when a clash needs three rules together, does the set-level Z3 checker
(`pipeline/rules/group.py`) find it more often than an LLM reading the folder?

## Material
- 16 groups of three rules written by Codex (`prompts/review/group_bench_write.md`), 8 clash
  (every pair compatible, the three together not) and 8 look-alike controls. Claude does not
  edit them. Codex's stated situation is the reference; Claude and a fresh Codex check each
  group's label before any method runs; disputed groups are reported and excluded.
- Host folder: the 36 real QuagKhai rules (saved translations, real distractors). The 48 test
  rules are added with new ids, shuffled: 84 rules, 95,284 triples.

## Arms
1. **Z3 group checker**: test rules translated once (two-step v2.1, DeepSeek, run=1); host
   rules use saved run 1. Every triple is scanned (`scan_triples`); a flagged triple counts.
2. **DeepSeek whole-folder** (one call, `prompts/rules/folder_group_judge.md`, asks for pairs
   or larger groups).
3. **Codex whole-folder**, same prompt, blind (free).
4. Reference only: **Codex shown each group alone** (free), to see whether the LLM can judge a
   group when it is pointed at it.

## Measures
- Groups found: a reported clash whose rule set equals a clash group, or contains it with at
  most one extra rule.
- False alarms: reported clashes on control groups; other reported clashes are listed and
  adjudicated (Claude + fresh Codex) as real host clashes, ambiguous, or false.
- Z3 coverage: how many clash groups survive translation (all three rules `ok` and in scope).

## Decision rules (fixed now)
- "Z3 beats the LLM on three-rule clashes" only if Z3 finds at least 2 more clash groups than
  BOTH whole-folder LLM arms, with no more control false alarms than either.
- If the LLMs match or beat Z3, report that plainly. If translation drops a group, count it as
  a Z3 miss.
- One run per arm. No tuning of prompts, translator or checker after seeing results; fixing a
  crash or a format error is allowed and logged.

## Budget
Translation of 48 rules, two steps, one run (~100 calls) plus one whole-folder call: about
$0.04-0.05 at off-peak prices. Balance before: $1.15.
