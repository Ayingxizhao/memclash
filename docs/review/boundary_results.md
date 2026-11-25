# Boundary stress test: results (2026-11-24)

Preregistration: `docs/review/boundary_prereg.md` (hashes `boundary_freeze1.sha256` before
actions, `boundary_freeze2.sha256` before any arm). Scores: `data/runs/natural/boundary_judge/`.

## Funnel (coverage)
1,287 real rules -> 86 eligible (Codex screen) -> 47 pass the mechanical filter after Codex
translation -> 25 kept (Claude and a fresh Codex both judge the translation exact) = 1.9% of all
rules. Codex rejected most "X before Y" rules: `after` sees only the newest step of a kind, so
"build before commit" fails if anything ran in between (a vocabulary flaw worth fixing).

## Material
150 actions (6 per rule, by a fresh Claude helper blind to translations): 25 per category.
Labels: a fresh Claude helper and a fresh Codex agree exactly on 143; 7 ambiguous (excluded).

## Results (143 actions; violation precision / recall / F1; exact rule-set accuracy)
| Arm | P | R | F1 | Exact set |
|---|---|---|---|---|
| Z3, frozen run | 1.00 | 0.83 | 0.91 | 0.92 |
| Z3, after logged format fix | 1.00 | 1.00 | 1.00 | 1.00 |
| DeepSeek x1 | 1.00 | 1.00 | 1.00 | 1.00 |
| Codex run 1 / 2 / 3 | 1.00 / 0.97 / 1.00 | 1.00 | 1.00 / 0.99 / 1.00 | 1.00 / 0.99 / 1.00 |

Rule-clustered bootstrap, Z3 F1 minus best LLM run (DeepSeek): frozen -0.09 [95% -0.19, -0.02];
after fix 0.00 [0.00, 0.00].

## Decision (fixed rule)
**Not met: tie at best.** The rule needs Z3 at least 0.05 above every LLM run; the LLMs are at
1.00, so no Z3 result could win. Frozen run: LLM wins. After the format fix: exact tie.

## Logged format fix (allowed by the preregistration; made after the run)
Codex's translations wrote some paths as a single string (`"path": ".env"`) instead of a list.
`model.py` then read the string letter by letter, so "never edit .env" never matched (12 misses,
all on `.env` / `MEMORY.md`). Also, event paths like `./.env` were not cleaned the way rule
patterns are. Fix: `model._paths` (string -> list) and `enforce._clean` (drop `./`); new test
`test_string_path_and_dot_slash`; all 200 tests pass. Rerunning the first study's Z3 arms with the
fix changes 0 of 114 decisions there (its translations already used lists).

## What it shows
- When rules are compiled and validated and actions are clear to a careful reader, both sides are
  perfect: the test has no headroom, so it cannot separate them. Z3's only errors were a checker
  format bug, i.e. Z3 is exactly as good as its plumbing.
- The LLMs did not slip on near-identical paths (`.env.local`, `docs/MEMORY.md.bak`), branch
  look-alikes, or history cases at this size (8-13 rules per folder, 36-78 actions per call).
- Z3 keeps its operational edge: 1.4 s for 150 actions, $0, identical every run; DeepSeek took
  145 s; Codex varied on 1-2 actions across runs.

## Spend
DeepSeek balance $0.98 before and after (about $0.01). Part 2 total so far: $1.02 -> $0.98.
