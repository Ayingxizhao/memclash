# Method audit (2026-11-22, after the final evaluation)

Question from the author: is the method wrong, or did we overfit the dev set, or are the
samples unrepresentative? Literature: `method_audit_codex.md`, `method_audit_claude.md`.

## Offline analyses (no LLM calls)

1. **Label-noise ceiling.** Two independent labellers (Claude, Codex) agree on 67% of the
   frozen rules (Z3 equivalence), status 87%. The model scores 48-56% against either
   labeller (final 51% vs the settled labels). Exact-match accuracy cannot be read on a 0-100%
   scale: about two thirds is the human level here.
2. **The two sets differ.** Both oversample keyword rules (80% vs 39% in the pool of 1,287).
   Frozen: 8 of 30 rules hand-picked because they are in known clashes; 10 marked ambiguous
   (labeller disagreement, settled by the author). Dev: random only; 1 ambiguous after
   adjudication by principle; only 10 rules in scope (6 in the iteration split).
3. **Where the test errors are.** Final method on the frozen set: random clear rules 73%
   (baseline 75%), known-clash rules 25-42%, random ambiguous rules 17%. Dev iteration set:
   73%. On comparable rules (random, clear) dev and test agree; the overall test score is pulled
   down by 18 hard or ambiguous rules that dev hardly has.
4. **Where the dev gain came from.** Dev, same v2.1 labels: +18 points (95% CI +5 to +35),
   from 7 rules, mostly rules about earlier steps (after a build, after editing a file) and a
   conjunction of files: the v2.1 features. The frozen set has few such rules. Test: +2 points
   (95% CI -6 to +10).
5. **Task-level check.** On the 88 same-folder pairs of the frozen rules, pair verdicts from
   translations agree with verdicts from labels 99% of the time, with 0 false flags; but only 2
   pairs clash by the labels, too few to measure recall. Most translation errors do not change
   any pair verdict.
6. **Scoring that accepts either labeller's reading** (frozen set): one-step 56%, final 62%. On
   the 17 in-scope rules only: one-step 39%, final 53%, +14 points (95% CI +2 to +25); strict
   single label: +6 (CI -2 to +16). Much of the "no transfer" came from strict single-label
   scoring of defensible readings.

## Small paid pilots (total about $0.15)

7. **Dev validation split** (10 dev rules never used, 4 in scope): one-step 63%, final 67%
   (clear rules 70% -> 74%). The +18 on the 20 iteration rules shrinks to about +3 on unseen
   rules from the same draw: part of the dev gain was tuning to those rules.
8. **Precommitted 20-pair comparison** (10 clashes: 7 planted, 3 real; 10 hard compatible
   pairs; gold fixed before running; one run each):

| Method | Clashes found (of 10) | False alarms (of 10) |
|---|---|---|
| Current (rule alone, two-step, Z3), run 1 | 5 | 1 |
| Current, any of 3 runs | 7 | 1 |
| Direct LLM judge (both rules + ADR 0003 definition) | **10** | **0** |
| Joint translation (each rule with the other shown) + Z3 | 4 | 0 |

   Caveats: 20 pairs, mostly planted and textually obvious; one run; the direct judge has to see
   every pair (n² calls), so on a real folder it needs a candidate step; its precision on a real
   folder's 435 pairs is unmeasured.
