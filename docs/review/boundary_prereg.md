# Boundary stress test: preregistration (2026-11-24, frozen by hash before any action exists)

Follow-up to `docs/review/enforce_results.md`; design from `docs/review/enforce_next_codex.md`.
The first study's result stays reported unchanged. This is a NEW study with a narrower claim.

## Claim tested
For rules that are already compiled and validated in the fixed git/file/task vocabulary, does
Z3 decide difficult boundary actions more accurately than an LLM reading the same rules in English?
Not a claim about enforcing arbitrary English rules (coverage is reported beside every score).

## Rules (mechanical, no hand picking)
1. Codex judged all 1,287 real rules with the eligibility test (`prompts/review/enforce_select_full.md`): 86 eligible.
2. Codex translated the 86 (`prompts/review/boundary_translate.md`).
3. Fixed filter: status ok; only `never` / `only_if`; no `when_unmodeled`; compiles -> 47.
4. Claude and a fresh Codex each judge whether each translation is exact for every single action
   (`prompts/review/boundary_review.md`). A rule is kept only if BOTH say exact. No adjudication
   (the one human is away); exclusions and reasons are published.
Funnel reported: 1,287 -> 86 -> 47 -> 25 kept (Claude 40 exact, Codex 26, both 25; Codex found that `after` sees only the newest step of a kind, which breaks most "X before Y" rules). Below the 30 target: we continue and report coverage, as fixed beforehand.

## Actions
A fresh Claude helper (no access to translations, checker output, earlier results or LLM
prompts) writes 6 actions per kept rule from the English rule, the vocabulary field list and the
name list: exact boundary violation; adjacent allowed case; path/glob or exception pair member;
near-identical path or branch; one-step history violation; closest allowed history case. It must
not write cases meant to trick an LLM. Actions are shuffled and given neutral ids.

## Labels
A second fresh Claude helper and a fresh Codex label every action independently from the English
rules of its folder (kept rules only, same set every arm sees). Agreement = gold. Disagreements
are "ambiguous": excluded from the primary score, reported, and scored both ways as sensitivity.
Mechanical labels from the translations are a diagnostic only, never gold.

## Arms (all see the same kept rules of the action's folder and the same events)
- Z3: validated translations, `pipeline/rules/enforce.py` unchanged.
- Codex x3, one batched call per folder, prompt `prompts/review/enforce_judge.md` unchanged.
- DeepSeek x1 (official API), same prompt and batching.

## Measures
Violation precision / recall / F1; exact broken-rule-set accuracy; results by action category;
repeat agreement; time and cost; coverage (kept / 1,287). 95% intervals by bootstrap over rules
(all actions of a rule resampled together), 2,000 draws, seed 2520.

## Win rule (fixed)
Z3 wins on accuracy only if ALL hold: F1 at least 0.05 above EVERY single LLM run; precision no
lower than the best LLM run; exact-set accuracy higher than every LLM run; and the rule-clustered
95% lower bound of (Z3 F1 - best LLM run F1) is above 0. Otherwise: tie or LLM win, reported
plainly. No substitute cost win.

## Budget and order
DeepSeek: one scored run, batched per folder, hard stop $0.08; balance recorded before and after.
Codex free. Order: review -> freeze this file and rules -> actions -> labels -> freeze actions and
labels -> run arms -> score. No change to rules, translations, prompts, checker or labels after
any arm runs; crash or format fixes are logged.
