## 1. Is the method wrong?

Not fundamentally. Z3 can give an exact answer **about the translations it receives**. The weak link is semantic translation and the assumption that rules can be interpreted independently.

Known failure modes include:

- **Lost scope or conditions.** “For non-code changes” may apply to every clause, not just the nearest action. Your R20 false alarm is a textbook example.
- **Incomplete decomposition.** Conjunctions, exceptions, temporal order, “only after,” and implicit prerequisites are easily omitted or assigned to the wrong clause. This matches R8, R13, R14, path-list, and earlier-step errors.
- **Unaligned symbols.** Independent translations may give two names to the same condition, or one name to different conditions. ADR 0004 explicitly acknowledges this blind spot.
- **Context loss.** Definitions, headings, tool equivalence, priorities, and exceptions may live elsewhere in the folder. Your nine tool-choice misses and the backlog/dev-bot cases are outside the fixed ontology.
- **Representation limits.** A solver cannot recover distinctions absent from the vocabulary. Formal methods literature distinguishes translation correctness from solver correctness.
- **Higher-order conflicts.** Some conflicts arise only from three or more requirements. A requirements-NLI study found pairwise NLI inadequate for these “compositional conflicts.” [Fazelnia et al.](https://arxiv.org/abs/2405.05135)
- **Stochastic formalization.** Semantically different outputs from the same model/input are expected; formal-translation evaluation research explicitly treats autoformalization as nondeterministic. [∀uto∃∨∧L, ICLR 2025](https://aair-lab.github.io/Publications/autoeval_iclr25.pdf)

Nearly all apply here. The 0–1 false alarms are encouraging, but translation accuracy near 51%, large run variance, and only 6–10 in-scope rules per split mean the current system is better described as a **high-precision candidate generator for a narrow vocabulary**, not a reliable complete clash detector.

A better-supported architecture is hybrid:

1. Retrieve potentially related rules.
2. Interpret each candidate pair jointly, aligning actors, actions, conditions, exclusions, and priority.
3. Use Z3 where the joint representation fits the ontology.
4. Have an LLM or human verify the resulting witness against the original text.

ALICE follows a related pair-level hybrid: it separately compares variable identity, action incompatibility, condition equivalence, and condition co-occurrence. On controlled automotive requirements it outperformed an LLM-only baseline, though its authors explicitly warn about small-data overfitting and limited statistics. [Gärtner & Göhlich 2024](https://link.springer.com/article/10.1007/s10515-024-00452-x)

Direct NLI is worth benchmarking, but not adopting on faith: one requirements study found it better than ChatGPT yet still low-performing across domains. ContraDoc likewise reports that direct LLM detection struggles with nuanced, contextual contradictions (**abstract-only evidence**). [ContraDoc](https://aclanthology.org/2024.naacl-long.362/) Retrieval specialized for contradiction can outperform ordinary similarity search, but its evidence is from argument/fact-retrieval datasets rather than policies (**abstract-only for present purposes**). [SparseCL](https://proceedings.mlr.press/v267/xu25s.html)

I am unsure whether joint translation or direct pair judgement will win on this dataset; the literature does not settle that specific comparison.

## 2. Is the evaluation wrong?

Exact Z3 equivalence is a valuable **strict diagnostic**: it avoids penalizing harmless syntactic differences and tests complete formal meaning. Similar semantic-equivalence checking is used when the target meaning is generated from an unambiguous grammar. [∀uto∃∨∧L](https://aair-lab.github.io/Publications/autoeval_iclr25.pdf)

It is not a fair sole accuracy measure against one uncertain human label. With only 20/30 agreement, “wrong” mixes together:

- genuine model errors;
- annotation errors;
- defensible alternative interpretations;
- vocabulary-induced approximations.

The 67% agreement is **not a mathematical performance ceiling**—models can exceed inter-annotator agreement—but it is strong evidence that the reference is noisy or the task underspecified. [Richie et al. 2022](https://aclanthology.org/2022.bionlp-1.26/) NLI research shows that disagreement often persists with more annotators and reflects plausible interpretations rather than disposable noise. [Pavlick & Kwiatkowski 2019](https://aclanthology.org/Q19-1043/), [ChaosNLI](https://aclanthology.org/2020.emnlp-main.734/)

Use:

- two independent labels plus adjudication by a third person;
- `clear`, `ambiguous`, and `outside-vocabulary` strata;
- acceptance of either adjudicated formalization when both readings are defensible;
- clause-level precision/recall and coverage, alongside whole-rule equivalence;
- translation accuracy conditional on being in scope;
- pair-level clash precision, recall, F1, and false-positive rate as the primary end-task metrics.

Report per-run results and the three-run union separately. “Any of three” improves recall but gives every pair three opportunities to become a false positive; it should not be compared with a single-run baseline without qualification.

## 3. Dev → test transfer

All three explanations contribute, but they explain different things.

**Sampling mix strongly explains the absolute test score.** Dev had roughly 2/30 ambiguous rules, while test had 10/30. Test accuracy was 67% on clear rules and 20% on ambiguous ones; that mixture yields almost exactly 51%.

**Overfitting explains the missing improvement.** Clear-test accuracy remained 67%, despite several iterations and a dev rise from 55% to 73%. Thus, composition explains why test is low, but not why development gains failed to transfer.

**Label noise widens uncertainty.** With 30 independent rules, approximate 95% Wilson intervals are about 56–86% for 73% and 34–68% for 51%. Repeated runs on the same rule are not 90 independent observations; confidence intervals should cluster by rule, and preferably by source folder.

A sound design would use at least 60 development rules, a 30–50-rule validation set for method selection, and about 100 untouched test rules. Split by folder, not rule, and stratify by action family, scope status, ambiguity, length, and single- versus multi-clause structure. Label with two readers and adjudicate before seeing predictions. If that scale is impossible, use leave-one-folder-out validation and present wide paired bootstrap intervals rather than a single accuracy number. Maintain a separate balanced clash diagnostic set because naturally occurring clashes are too rare for stable recall estimates.

## 4. Cheap pilots

1. **No-call stratified reanalysis.** For every existing dev/test rule, tabulate baseline versus final correctness by clear/ambiguous, in/out of scope, action family, clause count, and folder. Post-stratify dev to the test mixture. Use paired McNemar tests and a rule-cluster bootstrap for the change. This separates mixture effects from genuine transfer failure.

2. **No-call translation-error simulation.** From independently reviewed error categories, replace erroneous model translations with the adjudicated translation one category at a time—scope, omitted clause, condition identity, action ontology, priority/context. Rerun Z3 and measure marginal recovery of planted and real clashes plus new false alarms. This identifies whether better translation could rescue the architecture or whether vocabulary limits dominate.

3. **Precommitted 20-pair comparison.** Select 10 positive pairs and 10 hard negatives, mixing planted pairs, known real clashes, and the false-alarm probe. Blindly adjudicate them first. For each pair, make one short direct-verdict call and one joint-translation call followed by Z3—about 40 calls, comfortably below $0.20 at the logged rates. Compare recall, precision, paired disagreements, and condition/action alignment against the existing independent-translation result. Do not tune after seeing these outcomes.

- The solver is not the main problem; semantic translation and ontology coverage are.
- Independent translation loses shared scope, condition identity, priority, and folder context.
- Exact equivalence is useful diagnostically but inadequate as the sole score against one uncertain label.
- Test composition explains much of 51%; non-transfer on clear rules is evidence of dev overfitting.
- The most informative next test is a small, blinded comparison of independent, joint-pair, and direct pairwise methods.