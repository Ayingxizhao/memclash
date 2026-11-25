# Runtime enforcement: results (2026-11-24)

Preregistration: `docs/review/enforce_prereg.md` (frozen by hash in
`data/runs/natural/enforce_freeze.sha256` before any arm ran; not yet committed).
Scores: `data/runs/natural/enforce_judge/scores.json`; script `pipeline/rules/enforce_score.py`.

## Material
- 19 eligible real rules (4 folders with actions), 84-rule folders shown to the LLM arms.
- 114 actions: 76 invented (set A) + 38 log-grounded (set B). 60 break a rule, 54 are allowed.
- Labels: Claude + Codex independently, user settled 2 of 114. 10 borderline actions.

## Main result (all 114 actions; violation precision / recall / F1)

| | No human help | One human review |
|---|---|---|
| LLM alone, DeepSeek | A1: 0.98 / 0.93 / **0.96** | A2: 0.97 / 1.00 / **0.98** |
| LLM alone, Codex x3 | A1: 0.95 / 0.98-1.00 / **0.97-0.98** | A2: 0.89-0.97 / 0.98-1.00 / **0.94-0.98** |
| LLM + Z3 | B1: 0.97 / 0.50 / **0.66** | B2: 0.95 / 0.58 / **0.72** |

Same picture on set A, set B, and without borderline actions (B2 F1 0.66 / 0.83 / 0.74).

## Decisions (fixed rules)
- **Q1 (no help): LLM wins.** Z3 F1 0.66 vs every LLM run >= 0.96.
- **Q2 (equal help): LLM wins.** Z3 F1 0.72 vs every LLM run >= 0.94.
- **Operation win: not met.** It needs Z3 within 0.05 F1 of the best LLM run; the gap is 0.26.
- **Q3 (descriptive):** review gain is larger for Z3 (B2 - B1 = +0.06 F1) than for DeepSeek
  (A2 - A1 = +0.02); Codex shows no gain (spread across runs is larger than the gap).

## Why Z3 loses
- Every Z3 miss comes from a rule it cannot check: R362, R74, R20, R21, R363, R273, R147, R146
  were judged "can't express" or have only unknown conditions (switched off). Z3 never
  mis-checked a rule it could express.
- Precision is high (0.95-0.97). False blocks: A66 (restarting Redis hits "restart needs
  approval", R217) and, in B2 only, A02 (user asked to see the server: implicit permission).
  Both come from Claude's chosen translation of R217 during review.
- Automatic translations (B1) also miss on name mismatch: R217 start ("start the RDForward
  server process" vs the name list) and R386 (no "running" in run 1).

## Exploratory (not preregistered): only actions whose broken rules Z3 can check
83 actions, 29 violating. B2: 0.93 / 0.97 / 0.95; B1: 0.87 F1; DeepSeek A1 0.98, A2 0.97;
Codex 0.89-0.97. On this subset Z3 with review is within 0.05 of the best LLM run, but the
subset was chosen after seeing results, so this is a hypothesis for a future test, not a claim.

## Cost and speed per 114 actions
| | Time | Money | Repeat agreement |
|---|---|---|---|
| Z3 | 0.5-0.6 s | $0 | identical by construction |
| DeepSeek (4 batched calls) | 171-221 s | about $0.01 per arm | 1 run each |
| Codex (4 calls per run) | about 1-2 min per run, in parallel | free plan | A1 113/114, A2 108/114 identical across 3 runs |
Z3 one-time cost: translation (saved from Part 1) + one review session + a name list.
DeepSeek spend for this experiment: $0.02 (balance $1.02 -> $1.00).

## Caveats
- Codex wrote the actions, labelled them, and is a judged arm: this can favour Codex. DeepSeek is
  independent of all three and still scores F1 0.96-0.98.
- Actions are written to be clear cases; labels agreed 112/114. Clear cases favour the LLM less
  than the scale and messiness of real traffic would.
- 19 rules, 114 actions: talk-level evidence, no significance claims.

## One-line summary
On real rules and realistic actions, an LLM judging each action from the English rules beats
translation + Z3 (F1 0.96-0.98 vs 0.66-0.72); Z3 is exact, free and instant on the rules it can
express, but only about half of the violations fall under such rules.

## Secondary arm (preregistered, run after the main arms): Codex with the full folders
Codex x1 judged the same 114 actions with the full original folders (119-394 rules).
- Against the main (84-rule) key: P 0.69, R 1.00, F1 0.82. All 27 extra flags cite rules
  outside the 84-rule set, which the key never covered.
- Claude and a fresh Codex labelled those 261 (action, rule) pairs (`full_pairs_*.json`). Both
  agree 19 of the 27 actions really break a full-folder rule (e.g. A27 push without approval,
  R72; A45 tests not asked for, R394; commits without re-reading house rules, R60); 8 stay
  ambiguous (mostly R322 "planning only in this session").
- Against this extended key (8 ambiguous excluded, 106 actions): full-folder Codex P 1.00 R 1.00
  F1 1.00; Z3 B2 F1 0.60; Codex with the 84-rule set 0.85; DeepSeek A1 0.82.
- Caveat: the extension only checks rules the full-folder judge itself cited, so it cannot find
  that arm's own misses; this favours the full-folder arm. Treat as an upper bound.
- Reading: real folders hold several overlapping rules per action (e.g. 5 commit-approval
  rules); the 84-rule sample understates what applies. A bigger folder did not hurt Codex here.
