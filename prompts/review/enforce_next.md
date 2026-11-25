You advise a research team. Work read-only; your final message is saved. No paid API calls.
Read: `docs/review/enforce_prereg.md`, `docs/review/enforce_results.md`,
`docs/review/redirect_round2_codex.md`, `pipeline/rules/vocab.py`, `pipeline/rules/enforce.py`.
Do not open files under `data/gold/`, any `frozen_*` file, or held-out folders.

Situation: a preregistered runtime-enforcement test found LLM judges (F1 0.96-0.98) beat
translation + Z3 (0.66-0.72); every Z3 miss came from rules the vocabulary cannot express. An
exploratory subset (actions whose broken rules Z3 can check) gave Z3 0.95 vs LLM 0.89-0.98.
The team lead feels the rule choice was unfair to Z3. We must NOT re-select rules after seeing
results and present that as the same test. The first result stays reported.

Answer, concisely, with sections:
1. Is the lead's "unfair" concern valid in any sense? What exactly is and is not legitimate now?
2. Design ONE follow-up experiment, preregistered before any run, where a solver plausibly
   wins on accuracy (not just cost), with an honest, narrower claim. Consider: the unrun
   secondary arm (LLM given full 119-394-rule folders); many more rules per check; harder
   actions (exact globs, path exceptions, long histories, near-identical paths); adversarial or
   distractor-heavy actions; long action sequences; mixed folders. For each candidate give the
   expected effect on each side and the risk of rigging. Pick one and specify: rules, actions
   (who writes them, blind to what), labels, arms, measures, win rules, budget (DeepSeek
   <= $0.08; Codex free).
3. How to present both results together in one talk without it looking like goalpost moving.
4. Anything we missed.
