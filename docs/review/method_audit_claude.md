# Method audit: rule-by-rule translation + Z3 clash check

**How to read the sources.** For most papers I read only the abstract or a search summary, and these are marked **[abs]**. For WIRE I read most of the full HTML. I also used the repo's own offline analysis in `/Users/yingxizhao/dev/cs2520/projects/docs/review/method_audit.md`, which the task did not list but which holds the facts below.

## 1. Is the method wrong?

The method is not wrong. "LLM formalizes, solver checks" is the main approach in recent work, and the closest paper does almost exactly what you do. That literature also names failure modes, and most of them show up in your logs.

**Closest work**
- **WIRE** (Yan, Chen, Zhang, arXiv 2605.27784; most of the full text read). It encodes each rule of an LLM prompt policy separately (`C_i = enc(rule_i)`) into clauses over a closed vocabulary with open arguments. Satisfiability checks then flag "hard collision" pairs.
  - Two differences from you. First, WIRE treats flagged pairs only as *candidates* and checks them against concrete situations. Second, it validates by blind human audit ("source-faithful": 93.8% of 80 rules), not by exact match to one label.
  - Its own stated limits are close to yours: missed rules, clauses that are too broad, and implicit exceptions or priorities.
- Other LLM + SMT work on requirements conflicts:
  - SAT-LLM (ASE 2024 NIER) [abs].
  - VeriMed (Hall & Eiers, arXiv 2605.13817) [abs]. It uses disagreement between independent formalizations, checked by SMT equivalence, as an ambiguity signal. That is the same idea as your "unstable candidate" flag.
  - ALICE (Gärtner & Göhlich, ASE journal 2024) [abs]. Formal logic + LLM detected 60% of contradictions and beat LLM-only.
  - LACE (arXiv 2505.23835) [abs]. NL access policies → JSON → Z3 conflict check.

**Known failure modes, and whether they apply to you**
1. **Losing scope or conditions when translating.**
   - Literature: LINC notes that anything lost in translation sends the solver to a wrong answer [abs]. PolicyLint (USENIX Sec 2019) found contradictions by extracting statements one at a time; follow-up work judged 56 of 80 and 79 of 86 of its flags to be false alarms, mainly from simplified statements and wrong "is-a" links [search summary].
   - Applies to you: yes. The E7 false alarm (R20 lost "non-code") and the ADR 0004 history (20 false clashes from dropped conditions) are this failure.
2. **Grounding: mapping words to shared names.**
   - Literature: VLTL-Bench (arXiv 2507.00877) [abs] reports near-perfect NL→LTL translation but a sharp drop once phrases must be mapped to the right names (propositions). "Syntax is easy, semantics is hard" (arXiv 2604.07321) [abs] reports the same gap.
   - Applies to you: yes. Two rules naming the same unexpressible condition get separate facts (ADR 0004 blind spot), and "map data" vs a named file is the same problem. This is the main cost of translating each rule alone, and it causes **misses**.
3. **Vocabulary coverage.** Applies to you: yes, and it is your biggest recall limit. On the large folders, 11 of 11 real clashes fell outside the git vocabulary (tool choice and similar). Pair-level LLM/NLI methods do not have this ceiling.
4. **Run-to-run variation.**
   - Literature: LINC takes a majority vote over sampled formalizations [abs].
   - Applies to you: yes (E6 gave 10/8/18 per run). Taking the union over runs raises recall but also raises false alarms. Codex already flagged this in consult 4.
5. **Pairwise NLI / LLM judging has its own failures.**
   - The NLI-for-requirements study (arXiv 2405.05135) [abs] says NLI "falls short in identifying compositional conflicts".
   - de Marneffe et al. 2008 [abs] found contradiction detection good on negation and antonymy and weak where deeper inference or world knowledge is needed.
   - ConInstruct (AAAI 2026) [abs] reports high F1 (DeepSeek-R1 91.5%) for spotting conflicting constraints in *one* instruction. That is easier than deontic clashes across a folder.
   - Your own README: the LLM judge misses about half the labelled dev conflicts.

**Is there a better-supported method?** I found no head-to-head study showing that rule-alone translation loses to joint-pair translation or to pure LLM judging on this kind of data. The best-supported design is a **hybrid**:
- the solver (or retrieval of related rules) proposes candidate pairs;
- each candidate pair is then **re-translated jointly**, so the two rules share names (fixes the grounding misses);
- an LLM or a concrete situation, as in WIRE, confirms the clash.

Your `pipeline/general/` (filter → judge → Z3) is already close to this. One caution: joint translation gives up the ADR 0008 guarantee that other rules cannot change how a rule is read. Keep the rule-alone pass as the first step.

## 2. Is the evaluation wrong?

Partly. Exact Z3 equivalence to one label is a fair *strict* measure, but it is mis-scaled when the two labellers agree only 67% of the time.
- **The human ceiling is about two thirds.** The model scores 48-56% against either labeller (offline analysis). So "51%" should be read against about 67%, not 100%.
- **Others use several references or a human audit.**
  - Plank 2022 (EMNLP) argues that single-label ground truth hides real human variation [abs].
  - WIRE uses a blind "faithful to the source" audit.
  - Autoformalization uses bidirectional-equivalence metrics (BEq / BEq+, ICLR 2025; Poiroux et al.) and checks them against expert labels [abs]. Even there, a failed check does not prove two statements differ.
  - Suggested measure: **accept a translation that is equivalent to either labeller's reading**, report human-vs-human agreement next to it, and keep strict exact match as a secondary number.
- **Your stated goal is about pairs, so the main measure should be about pairs.**
  - Pair verdicts from the translations agree with verdicts from the labels 99% of the time (88 pairs, 0 false flags). But only 2 of those pairs clash, so recall cannot be measured there.
  - Make pair-verdict precision and recall on planted plus real clashes the headline, and treat translation accuracy as a diagnostic.
- **Small check:** I found no report of whether "rule right" counts rules that are correctly marked not_in_scope. Only about 6-10 rules per split are in scope, so if they are counted they may push the score up. Report in-scope rules separately.

## 3. Dev → test transfer

Most of the gap is explained by **sampling (different mix)** together with **gains that target rule types only dev has**. Classic overfitting and label noise play smaller roles.
- **Comparable rules agree.** Random, clear rules score 73% on dev and 73% on test. The test total is pulled down by 8 hand-picked known-clash rules (25-42%) and 10 ambiguous rules (17%), and dev has almost none of either.
- **The dev gain comes from 7 rules,** mostly v2.1 features ("after a build", lists of files joined by "and"). Dev: +18 points (95% CI +5 to +35). Test: +2 (CI -6 to +10). This is feature-specific tuning, a mild kind of overfitting: the fixes are probably real but rare on the test set.
- **Label noise caps the level but does not explain the gap.** Both sets share the ceiling of about 67%.
- **The labelling protocols differ.** Dev disagreements were settled *by principle*: the same vocabulary principles the method was tuned to. Test disagreements were settled by the author and marked ambiguous. This alone could account for several points; I could not measure it.
- **The intervals are wide.** Test 15/30 has a 95% Wilson interval of about 33-67%. Dev about 15/20 is about 51-87%. Planted recall 15/20 is 53-89%. Zero false alarms in 20 planted cases only bounds the rate below about 15% (rule of three). Card et al. 2020 (EMNLP) show that such small comparisons are usually underpowered [abs].
- **I found no reported result for the 10-rule dev-validation split.** If it was never scored, the held-out step inside dev was skipped.

**A sounder design**
- Stratify both sets by the same factors (random vs known-clash, clear vs ambiguous, rule type).
- Score the dev-validation split before touching the test set.
- Report bootstrap CIs with rules as the unit (runs nested inside rules).
- Use about 60-100 rules per set if the aim is to detect a gap of about 15 points.

## 4. Cheap pilots (total cost ≤ $0.10)

1. **Scoring against several references and attributing errors (no LLM, $0).** Re-score the saved dev and test translations three ways:
   - "equivalent to either labeller" vs strict exact match;
   - in-scope rules only;
   - labeller B vs labeller A as the human baseline.

   Then, on the planted pilot plus the 4 real clashes, swap in hand labels for the translations ("oracle translation") and rerun Z3. Count the misses that remain: those come from the vocabulary, the rest from translation. This tells you whether the problem is the method or the measure.
2. **Dev-validation split, by stratum (about $0.03).** Run the frozen method once (3 runs) on the 10 dev-validation rules. Report scores by stratum next to the frozen set's random-clear stratum.
   - If validation matches about 73% on clear random rules, the sampling explanation holds.
   - If it drops toward test levels, the dev gain was overfitting.
3. **Joint-pair re-translation as a hybrid check (about $0.04-0.06, roughly 40 calls).** Take every expected planted pair that was missed (R13, R14, R8 and others), the 4 known real clashes, the probe false-alarm pair, and about 15 random non-clash pairs that share an action or target. Translate each pair *together* (shared names), run Z3, and compare recall and false alarms with the rule-alone results.
   - If joint translation recovers the grounding misses without new false alarms, use the hybrid (rule-alone pass to propose candidates, joint pass to confirm).
   - In the same calls, ask for a direct "clash / no clash" verdict to get an LLM-judge baseline on the same pairs.

## 5. Summary

- The method follows the most common published approach. WIRE (2026) is nearly the same design, but it treats solver flags as candidates and audits translations by hand.
- Your errors match the known failure modes: lost scope (false alarms), unshared names and the vocabulary ceiling (misses), and run variation. Translating each rule alone is the specific cause of the shared-name misses.
- Judge translation accuracy against the human level of about 67%. Accept either labeller's reading, and make pair-level clash precision and recall the main metric.
- The dev→test gap is mostly a difference in mix: random clear rules score 73% on both, and the dev gains target rule types the test set rarely has. The intervals are about ±17 points, so nothing here is settled.
- Next, run three pilots: free re-scoring with oracle translations, the unused dev-validation split (about $0.03), and joint-pair re-translation as a hybrid check (about $0.05).

**Sources:** [WIRE](https://arxiv.org/abs/2605.27784), [VeriMed](https://arxiv.org/abs/2605.13817), [SAT-LLM](https://conf.researchr.org/details/ase-2024/ase-2024-nier-track/20/Translation-Titans-Reasoning-Challenges-Satisfiability-Aided-Language-Models-for-De), [ALICE](https://link.springer.com/article/10.1007/s10515-024-00452-x), [LACE](https://arxiv.org/abs/2505.23835), [PolicyLint](https://www.usenix.org/conference/usenixsecurity19/presentation/andow), [PoliGraph](https://arxiv.org/pdf/2210.06746), [nl2spec](https://arxiv.org/abs/2303.04864), [VLTL-Bench](https://arxiv.org/abs/2507.00877), [Syntax Is Easy](https://arxiv.org/abs/2604.07321), [LINC](https://arxiv.org/abs/2310.15164), [Logic-LM](https://arxiv.org/abs/2305.12295), [NLI in RE](https://arxiv.org/abs/2405.05135), [de Marneffe 2008](https://aclanthology.org/P08-1118/), [ConInstruct](https://arxiv.org/abs/2511.14342), [BEq](https://arxiv.org/abs/2406.07222), [Plank 2022](https://aclanthology.org/2022.emnlp-main.731), [Card et al. 2020](https://aclanthology.org/2020.emnlp-main.745).
