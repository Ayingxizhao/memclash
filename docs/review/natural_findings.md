# Finding clashes in real memory folders: results

Data: `data/runs/natural/`, `data/runs/boundary2/` (timing). Details: `experiment_log.md`
section N. Clash definition: `docs/adr/0003-clash-definition.md` (two rules in one repo's memory
that no single action can both follow).

## Question
When a rule is added to memory, does it clash with the rules already there? Z3 checks the
translated rules; the baseline is one LLM call that reads the whole folder in English.

## Findings
1. **Real clashes exist.** 56 repos checked, 12 had at least one clash, 42 clashes in all.
2. **Most real clashes do not fit Z3's logic.** The 22 clashes labelled in detail (two AI
   reviewers and the author), by type:

   | Type | Clashes | Fit Z3's logic |
   |---|---|---|
   | Which tool or command to use | 12 | 0 |
   | A plan step vs a standing rule | 4 | 2 |
   | Where files go | 2 | 2 |
   | Allowed vs forbidden | 2 | 1 |
   | A setting's value | 2 | 0 |
   | **Total** | **22** | **5** |

3. **An LLM reading the whole folder finds more real clashes than Z3.** On the pairs with saved
   translations, Z3 found 1 of 2 clear clashes with 1 false alarm; the whole-folder LLM found
   2 of 2 with none.
4. **Z3 loses on translation, not on solving.** Its errors: a dropped "may" (R24/R156), a target
   with no file path ("map and player data", R60/R213), a lost scope ("non-code changes", the
   R20/R74 false alarm).
5. **"Is this a clash?" is often a judgement call.** Typical disagreements: a specific rule that
   refines a general one, a preference vs an allowance, a permission that can be obtained first.

## Speed and cost (same memory: 51 rules, the largest translated folder)
| | Time | Money |
|---|---|---|
| Z3, add 1 rule (translate it, then check all rules together) | ~14 s | ~$0.001 |
| Z3, first check (translate every rule, then check) | ~1 min | ~$0.04 |
| DeepSeek 4.1 Flash, every check (re-read every rule) | ~3 min | ~$0.02 |

The Z3 check of all 51 rules together took 6.3 s (`group_timing.json`); it covers clashes among
three or more rules, not only pairs (`pipeline/rules/group.py`). Pair checks: median 5 ms over
4,139 same-folder pairs (`clash_timing.json`). `~` marks estimates: LLM output scaled from an
84-rule whole-folder call (47k output tokens) at about 160 tokens/s, and billed cost.

## Limits
Clashes were found by LLM screens, so recall over all pairs is unknown. Labels are two AI
reviewers and the author. Small samples.
