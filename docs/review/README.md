# Review folder: index of studies (2026-11-24)

Each study has a plan fixed before any run (prereg) and a results file. Nothing in a prereg was
changed after its runs; later fixes are logged in the results file or the study's `changes.log`.

## Part 2: enforcing rules on agent actions
| Study | Plan | Results | Result in one line |
|---|---|---|---|
| Main enforcement test (19 rules, 114 actions) | `enforce_prereg.md` | `enforce_results.md` | LLM wins: F1 0.96-0.98 vs Z3 0.66-0.72; every Z3 miss is a rule it cannot express |
| Full-folder arm (119-394 rules) | `enforce_prereg.md` (secondary arm) | `enforce_results.md`, last section | Bigger folders did not hurt the LLM; 19 extra flags were real breaks outside the sample |
| Boundary stress test (25 Z3-exact rules, 150 edge actions) | `boundary_prereg.md` | `boundary_results.md` | Tie at F1 1.00 after a logged format fix (frozen Z3 0.91); only 1.9% of rules qualify |
| Agent trial (Codex as a real agent, 21 of 70 runs) | `agent_trial_prereg.md` | `agent_trial_results.md` | Rule files cut breaks from 5/6 runs to 2/10; no forgetting seen in short tasks; gate flags 6/8 (7/8 after fix), never fired live |

Design notes for Part 2: `enforce_next_codex.md` (follow-up design after the main test),
`data/runs/agent_trial/review_codex.md` (Codex's review of the agent trial).

## Part 1: finding clashes between rules
Headline: one whole-folder LLM call finds as many or more clashes than translation + Z3 (paper
section 6.1). Plans and notes: `experiment_design.md`, `final_prereg.md`, `group_bench_prereg.md`,
`experiment_log.md`, `natural_findings.md`; vocabulary: `vocab_draft.md`, `vocab_review_codex_r*.md`,
`vocab_v2_1_rubric.md`; method audits and outside reviews: `method_audit*.md`, `*_codex.md`,
`*_claude.md`.

## Where the data and code are
- Data: `data/runs/natural/` (Part 2 studies 1-3), `data/runs/agent_trial/` (agent trial).
- Code: `pipeline/rules/` (`enforce*.py`, `boundary_*.py`, `trial_*.py`); tests in `tests/rules/`.
- Prompts: `prompts/review/`.
