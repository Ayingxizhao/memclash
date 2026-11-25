## 1. When hybrids beat an LLM alone—and when they do not

All results cited here come from full text; none are abstract-only.

**Logic and reasoning.** Logic-LM translates a problem into logic, invokes an appropriate solver, and falls back to chain-of-thought when formalization fails. Across ProofWriter, PrOntoQA, FOLIO, Logical Deduction, and AR-LSAT, accuracy averaged 39.2 points above standard prompting and 18.4 above chain-of-thought. Gains were largest on nonlinear or deeper reasoning; solver-error self-refinement increased executable translations by about five points, but often fixed syntax rather than meaning. Its synthetic datasets were much easier to translate than expert-written FOLIO and LSAT questions. [Logic-LM](https://aclanthology.org/2023.findings-emnlp.248/)

SatLM compared declarative translation plus Z3 with direct prompting, chain-of-thought, and program-generating LMs over nine arithmetic, logic, and synthesis datasets. It usually won on accuracy—for example, 69.4% versus 46.5% CoT on GSM-SYS and 99.7% versus 80.1% on ProofWriter. More relevant here, it could abstain on malformed, ambiguous, or unsatisfiable translations: selective accuracy was 77.1% versus 45.2% for the program baseline on GSM-SYS and 89.9% versus 73.7% on CLUTRR. [SatLM](https://papers.nips.cc/paper_files/paper/2023/file/8e9c7d4a48bdac81a58f983a64aaf42b-Paper-Conference.pdf)

LINC compared direct answers, a logical scratchpad, CoT, and LLM-to-FOL plus Prover9. It strongly won on deep synthetic ProofWriter problems—GPT-4 LINC was 26 points above CoT—but on expert-written FOLIO GPT-4 CoT and LINC were roughly tied, with CoT slightly higher, 75.3% versus 72.5%. Translation lost implicit facts and sometimes collapsed distinct predicates. The two methods’ errors were unusually complementary. [LINC](https://aclanthology.org/2023.emnlp-main.313/)

Later evidence is less flattering. On five newer open models, LINC lost to CoT on every full-FOLIO comparison. It was nevertheless more stable under counterfactual word substitutions: under 5-point accuracy changes, versus usually over 10 for neural methods. Thus formalization can improve invariance and auditability without improving raw accuracy. [Bansal et al.](https://aclanthology.org/2025.alta-main.1/)

**Temporal logic and policy translation.** NL2TL’s modular pipeline—atomic-proposition extraction followed by a trained lifted temporal-logic translator—exceeded 95% exact accuracy on three domains, versus ad-hoc GPT-4 direct translation at 62%, 87%, and 84%. Direct GPT-3 accuracy collapsed as propositions increased, while the modular model remained near 95%. This was trained on a large, partly synthetic and human-corrected corpus, so it supports decomposition and vocabulary normalization, not zero-shot Z3 superiority. [NL2TL](https://aclanthology.org/2023.emnlp-main.985/)

For access control, Code4Policy’s typed schema and few-shot examples achieved roughly 0.98–1.00 relation F1 where a plain-language prompt was near zero. However, evaluation used LLM-synthesized policy corpora, and the authors still require expert validation. This supports narrow schemas and examples, but not a solver advantage on natural documents. [NIST/Code4Policy](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=958734)

**Requirements and norms.** ALICE decomposed automotive requirement comparison into seven semantic questions. On 1,071 real controlled-language pairs it reported 99% accuracy, 60% recall, and 94% precision, versus GPT-3 alone at 97%, 0%, and 0%; on 3,916 pairs its precision was 86%. The data were highly imbalanced, the direct baseline is obsolete, and the authors warn about limited statistics and overfitting. [ALICE](https://link.springer.com/article/10.1007/s10515-024-00452-x)

Classical norm work uses unification and constraint solving for obligation–prohibition and permission–prohibition conflicts, including indirect conflicts induced by domain relations. It supplies the right conceptual machinery but no LLM baseline or modern precision/recall evidence. [Vranes](https://ejil.org/pdfs/17/2/80.pdf), [Kollingbaum et al.](https://www.iiia.csic.es/media/filer_public/53/6a/536a89c9-be92-4790-bd0a-f30d49944bff/iiia-2007-1636.pdf)

**Instruction conflicts.** Direct models can already be strong. ConInstruct reports conflict-detection F1 of 91.5% for DeepSeek-R1 on constructed instructions, but inter-constraint conflicts were harder, and even the best model explicitly acknowledged conflicts in only 45% of cases. Prompting it to request clarification increased false alarms on compatible instructions. [ConInstruct](https://arxiv.org/abs/2511.14342) Instruction-hierarchy training improves obedience under system/user/tool conflict, but this is conflict resolution through training—not solver-based detection—and does not establish a hybrid advantage. [Instruction Hierarchy](https://arxiv.org/abs/2404.13208)

The pattern is clear: hybrids win when translation is constrained and inference is long, exact, or compositional. They often do not win when semantic parsing is harder than the inference itself.

## 2. Improvements ranked for this project

1. **LLM verification of every Z3 flag and witness.** Show the two source rules, ADR definition, and Z3’s concrete conflicting situation. Ask whether the conditions really can co-occur, the actions are genuinely exclusive, and no scope or exception was lost. This directly targets the observed false alarm and preserves an auditable witness.

2. **Model-neutral retrieval followed by direct pair judgment; use Z3 as supporting evidence.** The internal pilot is stronger evidence for this than any external paper. It also avoids quadratic LLM use while allowing recovery of clashes missed by independent translation.

3. **Abstain on LLM/Z3 disagreement.** Send disagreements to a person and report coverage plus selective accuracy. SatLM provides especially direct support for this design.

4. **Use the three saved translations as an ensemble.** Predefine majority vote for final Z3 flags and the union only as a high-recall candidate generator. Do not present “any of three” as a normal single-run score.

5. **Targeted refinement only.** Normalize equivalent actors, actions, tools, scopes, and conditions across saved translations; ask for refinement only when Z3 produces a parse error, ambiguity, or implausible witness. Logic-LM suggests solver feedback helps executability, but I am unsure it will repair your more important semantic omissions.

## 3. Claims the results do and do not support

**Can claim:**

- On the fixed 20-pair diagnostic, the one-run direct judge made 0 errors; independent translation plus Z3 made 6 errors in run 1, or 4 using a three-run union.
- Joint access to both rules and the clash definition is promising and corrected important failures of independent interpretation.
- Z3 gives deterministic conclusions and inspectable witnesses **conditional on the translations**.
- The current method may serve as a narrow candidate generator or secondary consistency check.
- The result motivates a hybrid pipeline and a larger natural-pair test.

**Cannot claim:**

- That LLM-plus-Z3 beats an LLM alone; this test showed the reverse.
- That the direct judge is perfect, generally superior, or reliable at natural clash prevalence.
- That the method has 70% recall: “any of three” is not one deployable run.
- That either approach has demonstrated low false-alarm rates over whole folders.
- That Z3 makes the end-to-end result faithful when the formalization is wrong.
- That the method is stable, scalable, production-ready, or validated on broad real conflicts.
- That planted, textually obvious clashes estimate real-world performance.

## 4. Fair fixed next test for about $0.03

Freeze the following before any new labels or predictions:

- **18 natural pairs:** use folders absent from the 20-pair pilot. Apply one model-neutral candidate rule—shared action/object terms or manually specified synonym groups. From six folders select one high-ranked, one middle-ranked, and one random eligible candidate. Do not select using Z3 or an LLM verdict.
- **6 subtle planted clashes:** one each involving shared scope, exception, temporal order, strong permission, synonym/tool equivalence, and mutually possible conditions.
- **6 hard compatible controls:** minimal counterparts using disjoint scope, explicit exception, compatible ordering, weak/non-exclusive choice, genuinely different actions, and mutually exclusive conditions.

Do not replace natural pairs if few prove positive; that prevalence is itself evidence. Blind and shuffle all 30.

Create reference labels first in a fresh Codex session, without translations or method outputs. Mark `clash`, `compatible`, or `ambiguous`, with an explicit witness. A human should adjudicate ambiguities and all later disagreements; otherwise Codex judging Codex labels is circular.

Compare:

- Codex direct judge, one run;
- DeepSeek direct judge, one run;
- saved-translation Z3 run 1;
- three-run Z3 majority and union;
- Z3 flag accepted only when the direct judge validates its witness;
- abstention when direct judge and Z3 majority disagree.

Report TP/FP/FN/TN, precision, recall, F1, false-positive rate, abstention coverage/selective accuracy, results separately for natural/planted/compatible strata, saved-run agreement, and exact paired disagreements. Report candidate-stage recall as unmeasured.

Precommit interpretation:

- Direct judgment is supported only if **both** LLMs beat Z3 run 1 overall and on natural pairs.
- Witness verification is useful if it removes at least one false alarm while losing no more than one true clash.
- Complementarity is useful if the union recovers at least two true clashes with at most one added false alarm.
- Stability is supported only by strong agreement among saved runs; one DeepSeek run says nothing about DeepSeek stability.
- Improvements confined to planted pairs support only a diagnostic claim, not real-folder effectiveness.

- The honest story is “precise formal checking after uncertain semantic translation,” not “formal reasoning beats LLMs.”
- Solver hybrids excel when parsing is narrow and reasoning is deep.
- Your direct judge result is meaningful but far too small and artificial for a general claim.
- The best immediate architecture is retrieval, direct pair judgment, Z3 witness, then abstention or review.
- A frozen 18-natural/12-controlled test can distinguish that story for almost no cost.