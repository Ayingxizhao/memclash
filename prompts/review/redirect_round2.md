Round 2. Read your own answer in docs/review/redirect_research_codex.md first. Work read-only; no
paid calls; do not open data/gold/labels_*, frozen_*, held-out folders.

The advisor's constraint is firm: the talk needs at least one POSITIVE result against a fair
baseline; a pure failure study is "not presentable". Claude verified these papers:
- Arbiter (arXiv 2603.08993, 2026): LLM-only multi-model scouring of 3 vendor system prompts,
  no solver, no baseline, no precision numbers.
- WIRE (arXiv 2605.27784, Purdue 2026): SAT only nominates candidate rule pairs; LLM judges;
  measures agent behaviour: 64.6% of witnessed trials violate at least one rule. No LLM-only
  baseline for detection.
- Solver-Aided Verification of Policy Compliance in Tool-Augmented LLM Agents (arXiv
  2603.20449, UW 2026): NL policy -> SMT-LIB (human-guided), Z3 gates each tool call on
  tau2-bench airline; baseline = same agent without checker; fewer invalid write calls.
- Also seen (not verified): Agent-C (2512.23738, SMT temporal runtime checks), AgentSpec
  (2503.18666), PCAS (Datalog policy compiler), VEPA (2610.12813).

Questions (concise, concrete, honest):
1. Which direction most plausibly gives a positive, fair head-to-head win in one week with our
   data? Consider especially RUNTIME ENFORCEMENT: given the saved translations of our 84 real
   rules (git/file/task vocabulary maps onto agent tool calls), check proposed agent actions
   against the folder. Baseline: an LLM (DeepSeek and Codex) given the whole folder judging
   each action "allowed / violates rule X". Metrics: violation recall/precision, per-action
   cost and latency, determinism across repeats, and explanation (which rule, witness). Why
   would the LLM lose (many rules in context, subtle path/branch globs, cost per action at
   scale) and where would Z3 lose (translation errors; we can report both auto-translated and
   human-validated rule sets)? Is this fair or rigged? Design it: materials (Codex writes
   N actions per rule from natural tool-call shapes, labels independently), arms, fixed win
   conditions, budget (DeepSeek <= $0.05; whole-folder call ~$0.02-0.03 each, so per-action
   LLM judging is expensive; propose batching or a subset).
2. Compare it with: (a) incremental auditing cost, (b) Codex's benchmark/failure study plus
   translation-agreement abstention, (c) LLM-flag then Z3/witness verification. For each give
   probability of a real positive win and what the win would be.
3. Recommend a final story combining the clash-detection results (honest negative, as
   motivation: "detecting clashes is a reading problem") and the positive result. Title, 3
   sentences, and the slide order (6-8 slides).
4. List what is still missing or risky.
