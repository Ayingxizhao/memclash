# Making rule translation reliable without patching the prompt

## 1. What others do

The common pattern in the work I found: let the LLM produce the formal form, then use **code, a solver, or more samples** to check or choose the result. People do not keep adding instructions to the prompt.

| Technique | What it does | Evidence | Cost |
|---|---|---|---|
| **Sub-translations** (nl2spec) | The LLM breaks a requirement into pieces, each with its English fragment and its formula. People fix the pieces, not the whole formula. | Codex got 44% right on its own and 86% with user edits, on only 36 requirements. The 86% needs a human. [arXiv 2303.04864](https://arxiv.org/abs/2303.04864), [full text](https://ar5iv.labs.arxiv.org/html/2303.04864) | 1 call plus human time |
| **Modular pipeline** (Lang2LTL) | Separate steps: find the referring phrases, ground them, then translate a "lifted" template. | Works zero-shot in 21 cities. [arXiv 2302.11649](https://arxiv.org/abs/2302.11649) (abstract and summary only) | Several calls |
| **Fixed pattern catalogue** (NL2LTL) | The model maps text onto a set of known templates (DECLARE). | Demo paper only, no strong accuracy claim. [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/27068), [GitHub](https://github.com/IBM/nl2ltl) (abstract only) | 1 call |
| **Solver error feedback** (Logic-LM) | The solver's error message is sent back so the model can repair its formula. | It raised how often formulas were valid, but accuracy moved only about −1.2 to +2.6 points. GPT-4 dropped on 2 datasets. The authors say a valid formula is not necessarily a correct one. [full text](https://ar5iv.labs.arxiv.org/html/2305.12295) | 1–3 extra calls |
| **Voting over samples** (LINC; self-consistency) | Sample K translations (LINC uses 10), run each through the prover, take the majority answer. | LINC: a 15.5B model beat GPT-4 with chain-of-thought on ProofWriter; more samples helped weaker models most. [arXiv 2310.15164](https://arxiv.org/abs/2310.15164). Self-consistency: +18 points on GSM8K. [arXiv 2203.11171](https://arxiv.org/abs/2203.11171) | K times the calls |
| **Declarative spec plus solver** (SatLM) | The LLM writes constraints and the solver does the reasoning. | +23% over program-aided LMs on a hard GSM subset. [arXiv 2305.09656](https://arxiv.org/abs/2305.09656) (abstract only) | 1 call |
| **Grouping candidates by solver equivalence** (Li et al. 2024) | Generate many formalizations. The prover groups the logically equivalent ones, the biggest group wins, and candidates are also turned back into English and compared to the source. | +7.8% and +10.7% with GPT-4. [arXiv 2410.20936](https://arxiv.org/abs/2410.20936) (abstract and summary only) | K calls plus K back-translations |
| **Round-trip check** (Amrollahi et al. 2026; Round-Trip Critique for SQL) | Formal → English → formal again, then test whether the two formal versions are equivalent. | The authors warn that both versions can agree and still both be wrong. [arXiv 2604.25031](https://arxiv.org/abs/2604.25031), [VLDB](https://www.vldb.org/pvldb/vol19/p3732-alrashed.pdf) (summaries only) | 2 extra calls |
| **Execution voting for SQL** (C3, CSC-SQL) | Group SQL candidates by the result they return and vote. CSC-SQL revises the top two groups and votes again. | CSC-SQL: +0.7 to +5.5 points over plain voting on BIRD; plain majority is sometimes wrong. [C3](https://arxiv.org/pdf/2307.07306), [CSC-SQL](https://arxiv.org/abs/2505.13271) (abstract and summary only) | K calls |
| **Policy text to access-control languages** (RAGent, Prose2Policy, XACML pipeline) | Pull out structured policy parts first, then convert them with code; RAGent adds a verify-and-refine step. | I did not find strong formal verification results. [RAGent](https://arxiv.org/abs/2409.07489), [Prose2Policy](https://arxiv.org/abs/2603.15799), [XACML](https://scitepress.org/PublishedPapers/2025/133572) (abstracts only) | Several calls |
| **Checking fact by fact** (FActScore) | Split a text into atomic facts and check each one separately. | Widely used for checking facts; I found no use of it for translation coverage. [arXiv 2305.14251](https://arxiv.org/abs/2305.14251) | 1–2 calls |
| **Constrained decoding** (Outlines, XGrammar) | The output is forced to fit a grammar or schema. | It guarantees layout only, not meaning. [XGrammar](https://arxiv.org/abs/2411.15100), [vLLM blog](https://vllm.ai/blog/struct-decode-intro) | About free |
| **Format limits** ("Let Me Speak Freely") | Strict JSON can hurt reasoning. Answering in plain language first and converting after helped. | [arXiv 2408.02442](https://arxiv.org/abs/2408.02442) | 1 extra call |
| **Ambiguity** (AmbiEnt) | Tests whether models notice when a sentence has two meanings. | Humans judged GPT-4's disambiguations correct only 32% of the time, so the model's own "this is unclear" call is weak evidence. [arXiv 2304.14399](https://arxiv.org/abs/2304.14399) | — |
| **LLM judges** | When a model grades its own output, it tends to prefer it. | [arXiv 2404.13076](https://arxiv.org/abs/2404.13076). A 2026 paper says part of this effect is a measurement artifact: [arXiv 2601.22548](https://arxiv.org/abs/2601.22548) (abstracts only) | — |
| **SymbolicAI** | A framework that uses LLMs as parsers inside symbolic workflows. It is not a reliability method as such. | [arXiv 2402.00854](https://arxiv.org/abs/2402.00854) (abstract only) | — |

Lessons from the evidence:
- Solver feedback fixes syntax, not meaning.
- Voting fixes random noise, not mistakes the model makes every time.
- Constrained decoding only fixes layout, which you have already solved.

## 2. Fit to your pipeline

Useful facts from the repo:
- `translate_all` already runs 3 times per rule.
- `agreement.same_meaning` already uses Z3 to test whether two translations mean the same.
- `left_out` is a single free-text field.
- The model is DeepSeek with strict tool mode.

**A. Voting by Z3 equivalence (Li et al. / LINC style)**
- *Change:* sample K = 3–5 translations. Group them with `same_meaning` and keep the biggest group. If there is no majority, mark the rule "unstable" rather than picking one at random.
- *Helps with:* #4 (wording differences across runs, such as `files_shown` present in one run only). It helps #3 if "unclear" is a minority answer.
- *Cost:* K calls per rule. You already make 3, so this is about 0 extra.
- *Measure:* accuracy on the hand-labelled rules for majority vote vs a single run, and the share of rules with no majority.
- *Will NOT fix:* errors every sample makes (#1 and #2 may be like that).

**B. Two steps with a coverage check (nl2spec / FActScore style)**
- *Change:* split the one call into two fixed questions:
  1. Step 1 tool `list_requirements` returns atomic requirements, each with an exact quote from the rule.
  2. Step 2 translates and tags every clause with a requirement id.
  3. Code then checks that every requirement id maps either to a clause or to a `left_out` entry, and that the quotes together cover the important words of the rule.
  4. Turn `left_out` into a list of {requirement id, reason from a fixed set such as "vague" or "no vocabulary"}.
  5. A failed check uses your existing single retry, with a message the code generates.
- *Helps with:* #1 (a dropped requirement becomes visible) and #2 ("no stale branches" becomes a listed requirement that must be translated or explicitly marked "vague").
- *Cost:* about 2 calls per rule.
- *Measure:* the rate of dropped requirements on labelled rules, before vs after.
- *Will NOT fix:*
  - Step 1 itself missing a requirement. You can vote on step 1 as well.
  - A wrong but complete translation.

**C. Enumerated readings for "unclear"**
- *Change:* when the status is `unclear`, code builds one candidate translation for each listed meaning of the word (the table in section 5 already lists them). A separate fixed question then asks which readings the whole sentence allows, as a multiple choice. If Z3 says the allowed readings are equivalent, or only one is allowed, the rule is accepted instead of marked unclear.
- *Helps with:* #3. "Add … to version control" should leave only the `git add` reading.
- *Cost:* 1 extra call, only for rules marked unclear.
- *Measure:* precision and recall of "unclear" against the labels.
- *Will NOT fix:* #1, #2 or #4. AmbiEnt shows models are weak at this kind of judgement, so it needs measuring.

**D. Back-translation (formal → English, then compare)**
- Use a different model for the English step and the comparison.
- *Helps with:* #1 and #2 as a **flag**, not a fix.
- *Cost:* 2 calls.
- *Risk:* both directions can agree and still be wrong (Amrollahi et al.). An English-to-English comparison by an LLM is soft.
- It is weaker than B, because B's check is plain code.

**E. Second model as checker**
- It is mostly useful when the checker comes from a different model family, because of self-preference bias.
- Same coverage as D, and the check is just as soft.

**F. Solver feedback loop**
- Your solver only sees well-formed translations, so following Logic-LM it would catch almost nothing here.
- Exception: a cheap Z3 sanity check (is a rule contradicting itself? is a clause empty?) could catch some errors. I am unsure how many.

**G. Plain language first, then fill the format**
- Does not fit well. Your problem is meaning, not layout, and option B already gives a free-text first step.

## 3. Recommendations for Dec 1

1. **Z3-equivalence voting (A).** This is mostly done already, so do it first.
   - *Show:* accuracy and agreement for one run vs the majority of 5, on the labelled set and on pairs of rephrased rules.
   - *Will NOT fix:* errors the model makes every time, i.e. likely #1 and #2.
2. **Requirement list plus coverage check in code (B).** This targets your two worst errors, and the check is ordinary code, which is easy to defend in a report.
   - *Show:* counts of dropped requirements (#1) and of concrete parts wrongly marked vague (#2), before vs after, on the same rules and the same model.
   - *Will NOT fix:* requirements that step 1 misses, wrong mappings, or the over-cautious "unclear" problem (#3).
3. **Enumerated readings for unclear (C).** Only if time allows.
   - *Show:* precision and recall of "unclear" against the labels.
   - *Will NOT fix:* #1, #2 or #4.

Run them as an ablation: baseline, +A, +B, +A+B. Report each failure type separately, plus calls and tokens per rule. Report the four problem cases separately too, because tuning on them is exactly what you want to avoid.

I am not sure how often each error appears outside your pilot. The pilot is small, so give confidence intervals.

## Summary
- Layout tools (strict mode, grammars) are already solved for you and cannot fix meaning errors.
- Solver error feedback mostly fixes syntax. Logic-LM's accuracy gains were small.
- Voting with Z3 grouping (A) is nearly free in your pipeline and targets wording differences (#4), but not errors every run repeats.
- A requirement list plus a coverage check in code (B) is the best general fix for dropped parts (#1) and concrete parts called vague (#2).
- Measure everything as an ablation against the labelled rules, by failure type and cost; treat back-translation and LLM checkers as flags only.
