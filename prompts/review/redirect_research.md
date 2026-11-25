You are a research advisor on a class project (presented Dec 1, about one week away). Work
read-only; your final message is saved. Use web search and read full papers where you can; mark
anything you only saw as an abstract. Do NOT open `data/gold/labels_*`, `frozen_*`, held-out
folders. No paid API calls.

Project so far: detect clashes between rules in coding-agent memory folders (CLAUDE.md, memory
files). An LLM translates each rule into a fixed git/file/task vocabulary, then Z3 checks pairs
and three-rule groups. Read docs/review/experiment_log.md, docs/review/natural_findings.md,
docs/review/win_regime_codex.md, docs/review/hybrid_lit_codex.md for results. Summary: a single
whole-folder LLM call matches or beats our pipeline everywhere (planted pairs 20/20 vs 15-18/20;
three-rule groups 5/8 vs 1/8; natural pairs 2/2 vs 1/2); only 5/22 real clashes fit the
vocabulary; translation is the bottleneck; triple scan takes 9 h at 64 rules. Assets we have:
1,287 real rules from 5 folders, saved translations (3 runs) for 84 rules, labelled natural
clash sets (43 adjudicated full-folder candidates), planted pair and group sets, two-labeller
translation labels, an LLM-cost record.

The advisor wants presentable results and is open to changing scope, what is checked, and
method. Research and answer, concisely, with citations (title, venue, year, link):

1. Related and similar studies: rule/instruction/memory conflict detection for LLM agents
   (agent memory, CLAUDE.md / AGENTS.md / .cursorrules, system-prompt conflicts, policy
   conflicts, requirements-conflict detection, norm conflicts, access-control policy
   verification, guardrail/spec consistency). Anything empirical about real agent rule files?
2. "LLM alone vs tool+LLM" papers: how they set up the comparison (baselines, datasets,
   metrics) and what they typically claim as the improvement or novelty (accuracy on deep
   reasoning, faithfulness, abstention/selective accuracy, witnesses/explanations, robustness,
   cost, scale, certification). Which of these claims could our data support honestly?
3. Is Z3 the right tool? Compare alternatives for this problem: Datalog/Souffle, Answer Set
   Programming (clingo) for defaults/exceptions/norms, Prolog, deontic logic reasoners, SAT/
   MaxSAT, Alloy, temporal logic/model checking (NuSMV, LTL), Cedar/Rego(OPA)-style policy
   languages with analyzers (Cedar has an SMT-based analyzer; Zelkova at AWS), Lean/Dafny. Which
   is more reliable or easier, and would any plausibly change our results (note our failures
   were translation, not solving)?
4. New directions that reuse our data and could produce a positive, defensible result in a
   week: e.g. reframe as a benchmark/dataset paper (first study of clashes in real agent memory
   folders, taxonomy, prevalence), LLM-flag + Z3/witness verification to cut false alarms,
   formalization as an auditing/abstention layer, use the solver to enforce rules at action
   time (runtime monitor over agent tool calls) rather than to detect clashes, incremental
   checking cost, translation-consistency as a signal. For each: claim, evidence we already
   have, what extra cheap experiment is needed (free Codex work; DeepSeek budget ~$0.05), risk.
5. Rank the directions and recommend one, with a title and 3-sentence pitch. Also list
   things the team may be missing.

Be blunt and concrete. If unsure, say so.
