# Studies: plans and results

Each study has a plan fixed before its runs (prereg) and a results file. Later changes are logged
in the results file or the study's `changes.log`.

| Study | Plan | Results | Result in one line |
|---|---|---|---|
| Finding clashes in real memory folders | — | `natural_findings.md` (details: `experiment_log.md`, section N) | 56 repos, 12 with a clash, 42 clashes; 5 of the 22 labelled clashes fit Z3's logic; an LLM reading the whole folder finds more |
| Stopping rule breaks, all action rules | `enforce_prereg.md` | `enforce_results.md` | F1 on 334 actions: Z3 0.78, DeepSeek 0.87, Haiku 0.85 |
| Rules Z3 can express, round 1 | `boundary_prereg.md` | `boundary_results.md` | Built the 25-rule set the live gate holds |
| Rules Z3 can express, round 2 | `boundary2_prereg.md` | `boundary2_results.md` | F1 on 101 actions: Z3 0.97, DeepSeek 0.90, Haiku 0.89 |
| Live gate with Claude Code | `hidden_rules_prereg.md` | `hidden_rules_results.md` | 8 of 30 runs with rules loaded broke a rule; gate flagged 8 of 8, blocked 4 of 4 live, 0 false flags |

The whole-folder clash check (`pipeline/rules/group.py`, covers clashes among three or more
rules) gives the timing in `natural_findings.md`; measured costs are in `experiment_log.md`.

## Where the data and code are
- Data: `data/runs/natural/` (clashes, all-rules test, round 1), `data/runs/boundary2/` (round 2,
  clash timing), `data/runs/hidden_rules/` (live gate).
- Code: `pipeline/rules/`; tests in `tests/rules/`.
- Prompts: `prompts/rules/`, `prompts/review/`.
