You are reviewing an experiment design before it is frozen. Read:
- docs/review/agent_trial_prereg.md (the draft)
- docs/review/boundary_prereg.md and docs/review/boundary_results.md (the previous study)
- data/runs/natural/boundary_kept_english.json (the 25 gate rules) and data/runs/natural/boundary_rules.json (their translations)
- pipeline/rules/enforce.py, pipeline/rules/vocab.py (event format and vocabulary)
- data/github/explore/repos/{QuagKhai003__assessment,martinambrus__RDForward,sparkling__ruflo-patch}/ (real CLAUDE.md and memory files)
Do NOT read data/gold/labels_*, any frozen_* file, or held-out folders.

The user wants to show three things: (1) how often a real agent breaks memory rules, (2) whether it forgets rules in long tasks, (3) how many breaks a gate would prevent in practice. The agent will be Codex CLI itself (`codex exec --json`, workspace-write sandbox, no network) running in throwaway stub repos. Constraint: about 3-4 hours total, DeepSeek budget under $0.10 (Codex is free).

Give, concisely:
1. The 3-6 most serious flaws or biases in the design, each with a concrete fix.
2. Your proposed list of 10 tasks (3 assessment, 3 RDForward, 4 ruflo-patch): for each, the exact prompt text the agent gets, which gate rule(s) it tempts, why the temptation is natural (not rigged), and what the stub repo must contain. Tasks must not mention the rule, ask for the forbidden act, or forbid it.
3. The 8 filler subtasks for the long condition (per repo, generic, real edits, no temptation of any gate rule).
4. Whether the event flags (user_confirmed, user_asked, etc.) can be set from a fixed per-task table, and any rule whose translation cannot be judged from Codex trajectories.
5. Anything in Q1-Q3 we cannot honestly claim from this design.
Keep it under 1,200 words. Output markdown.
