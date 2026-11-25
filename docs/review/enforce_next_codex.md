## 1. Is the “unfair” concern valid?

Yes—as a concern about the estimand, not the validity of the result.

The original test measured the end-to-end pipeline: English rule → translation → available vocabulary → runtime verdict. Under that question, unsupported conditions must count as misses, exactly as preregistered. The result remains:

> On this real-rule population, direct LLM judgment beat translation + Z3, largely because the symbolic representation lacked coverage.

The concern is valid in two narrower senses:

- The experiment says little about accuracy after a policy has been successfully compiled and validated.
- There is tension between the preregistered eligibility criterion—rules expressible in the vocabulary—and the finding that every miss involved an inexpressible or unknown condition. Audit and explain how those rules passed screening; do not silently redefine eligibility.

Legitimate now:

- Run and report the already-preregistered full-folder secondary arm as secondary.
- Present the 83-action formalizable subset explicitly as exploratory.
- Preregister a new experiment with a conditional claim about validated, compilable policies.
- Improve the vocabulary in a separately versioned future system.

Not legitimate:

- Remove unsupported rules or revise translations and rescore the original comparison as though it were the same test.
- Promote the exploratory subset to the original primary result.
- Change labels, win thresholds, or the meaning of “eligible” after seeing outcomes.

## 2. One follow-up experiment

### Candidate stressors

| Candidate | Expected LLM effect | Expected solver effect | Rigging risk |
|---|---|---|---|
| Full 119–394-rule folders | More retrieval/distractor errors | Essentially unchanged | Moderate: asymmetrical context burden |
| Many compilable rules per check | More retrieval and rule-confusion errors | Small scaling cost, same semantics | Moderate |
| Exact globs, exceptions, histories, near-identical paths | Boundary and consistency errors | Strong if encoding is correct | Moderate, but defensible for enforcement |
| Adversarial/distractor-heavy actions | Likely substantial degradation | Little degradation | High |
| Long sequences | Context and state-tracking errors | Current checker loses information except the newest step of each kind | High and technically premature |
| Mixed folders | Scope/source confusion | Stable with correct namespaces | High unless mixed-folder operation is real |

### Pick: compiled-policy boundary stress test

Honest claim:

> For prevalidated policies expressible in the fixed git/file/task vocabulary, symbolic checking is more accurate than repeatedly interpreting the policy on difficult boundary actions.

This is explicitly not a claim about general English-rule enforcement.

**Rules.** Before action generation, mechanically take every saved rule satisfying all of these conditions:

- Translation status is `ok`.
- Every decisive clause is `never` or `only_if`.
- It uses only fields and values in `vocab.py`.
- It has no `when_unmodeled`, skipped state, `must_do`, or other unchecked condition.
- It compiles successfully.

Then validate each translation against its English rule before actions exist. Keep every rule passing this fixed test—no hand-picking by prior performance. Publish exclusions and reasons. Target at least 30 rules; if fewer qualify, report that coverage limitation and continue without lowering the criterion.

**Actions.** Create six per rule:

- exact boundary violation;
- adjacent allowed boundary;
- glob/path exception pair;
- near-identical path or branch pair;
- one-history-step violation;
- closest allowed history case.

A fresh Claude session writes them from the English and structured-event schema. It is blind to translations, checker output, prior action-level results, and LLM prompts. It may not deliberately write “trick the LLM” examples. Shuffle actions and include multiple-rule cases naturally.

**Labels.** Project author and a fresh Codex label independently from the English rules before any arm runs; adjudicate disagreements without seeing translations or arm outputs. Preserve ambiguous cases and exclude them from the primary score by a preregistered rule—not case-by-case. Also compute mechanically expected boundary labels as a diagnostic, not gold truth.

**Primary arms.**

- Validated translations + Z3.
- Codex, three independent runs, given the same complete selected-rule set and clarified English.
- DeepSeek, one run, same rules, events, prompt, and batching.

Diagnostics:

- Frozen automatic translations + Z3.
- One Codex run given only the gold-relevant rule, separating retrieval from boundary reasoning.
- The previously preregistered 119–394-rule-folder arm remains attached to the original study, not this primary comparison.

**Measures.**

- Violation precision, recall, and F1.
- Exact broken-rule-set accuracy.
- Paired accuracy on allowed/forbidden boundary twins.
- Results by path/glob, exception, and history category.
- Repeat agreement, latency, and cost.
- Coverage: qualifying rules divided by all candidate rules.

Use rule-clustered bootstrap intervals so six correlated actions do not masquerade as six independent rules.

**Win rule.** Validated Z3 wins on accuracy only if:

- Its violation F1 is at least 0.05 above every individual LLM run;
- its precision is no lower than the best LLM run;
- it has higher exact-rule-set accuracy than every LLM run; and
- the rule-clustered 95% bootstrap lower bound for its F1 difference against the strongest LLM run is above zero.

Otherwise report a tie or LLM win. Do not substitute a cost win.

**Budget.** Batch DeepSeek into at most two calls with a hard stop at **$0.08**; one scored run only. Codex runs are free. Record balance before and after. Freeze rules, translations, actions, labels, prompts, scorer, exclusions, seeds, and the budget before any arm runs.

This design favors the solver’s intended domain, but it is not disguised: coverage is reported, the LLM sees the same narrowed policy, and the claim is conditional on successful compilation.

## 3. Presenting both results in one talk

Use one question with two stages:

1. **Can we automatically enforce arbitrary real instruction-folder rules?**  
   No: LLMs scored 0.96–0.98 F1 versus 0.66–0.72 for translation + Z3, because vocabulary coverage failed.

2. **Once a policy is known to be compilable and validated, which runtime checker handles exact boundary cases better?**  
   Present the new preregistered result, whatever it is.

Call the exploratory 0.95 result the observation that motivated the second hypothesis, not evidence proving it. Show a denominator funnel:

> all real rules → syntactically actionable rules → compilable rules → validated compiled policies.

That makes the changed population visible and prevents the follow-up from looking like a replacement result. The overall conclusion can be:

> LLMs are better readers of broad natural-language policy; solvers may be better executors of a narrower compiled policy.

## 4. Anything missed

- Audit why nominally eligible rules later proved unexpressible; that is an important screening or specification failure.
- `enforce.py` deliberately treats unknown conditions as false and skips obligations/state clauses. These are coverage limits, not ordinary solver errors.
- Validate event normalization separately: a correct solver over incorrectly parsed paths or tasks is still wrong operationally.
- Freeze exact glob and path semantics; human and implementation interpretations can differ.
- Score multiple simultaneous violations as sets, not only binary decisions.
- Report rule coverage beside accuracy. “99% accurate on 20% of policies” is incomplete.
- Avoid having the judged model generate all actions if possible; the proposed independent author reduces that leakage.
- Preserve the original frozen hash and distinguish the unrun preregistered secondary arm from the newly preregistered follow-up.