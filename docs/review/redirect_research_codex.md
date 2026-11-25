## Bottom line

Do not spend the remaining week trying to show that Z3 beats an LLM. Your evidence says the opposite end to end, and changing the solver will not repair omitted permissions, lost scope, or an inadequate vocabulary.

The strongest defensible project is a benchmark and failure study of conflict auditing in real coding-agent instruction folders:

- Direct whole-folder review is the strongest baseline.
- Formal checking is exact only after a faithful translation.
- Most real clashes—17/22 in your adjudicated candidate set—are outside the current schema.
- Z3 remains useful for producing checkable witnesses, runtime enforcement, and possibly selective auditing, but not as evidence that the English files are consistent.

I read the cited papers in full unless explicitly marked otherwise. I did not inspect the prohibited gold, frozen, or held-out paths.

## 1. Closest related work

### Directly related agent-instruction studies

The closest paper I found is **WIRE: Profiling Witnessed Within-Policy Instruction Collisions in LLM Agents** (arXiv preprint, 2026). It extracts 276 rules from six public prompt policies, encodes them, uses satisfiability to nominate 170 collision pairs, constructs concrete co-governance witnesses, and measures how agents resolve them. Crucially, it does **not** treat the symbolic result as proof of an English contradiction; the solver is a candidate filter, and final evaluation returns to the original rule text and observed behavior. Its human audit reports 95.0% faithful extraction and 93.8% faithful encoding—much higher than your roughly 51% frozen translation accuracy—making your translation-bottleneck result an interesting contrast. [WIRE, arXiv, 2026](https://arxiv.org/pdf/2605.27784)

**ConInstruct: Evaluating Large Language Models on Conflict Detection and Resolution in Instructions** constructs 864 conflicts across content, keyword, phrase, length, format, and style constraints. DeepSeek-R1 reaches 91.5% conflict-detection F1, although inter-type conflicts are harder, and even strong models often silently satisfy only part of a conflicting request rather than alerting the user. This supports your strong direct-LLM baseline, but its conflicts are controlled user instructions, not persistent repository rules. [ConInstruct, AAAI, 2026](https://ojs.aaai.org/index.php/AAAI/article/download/40356/44317)

There is now substantial empirical work on real context files:

- **Agent READMEs** analyzes 2,303 `AGENTS.md`, `CLAUDE.md`, and Copilot files from 1,925 repositories. Test procedures occur in 75.9%, implementation details in 70.8%, and architecture in 68.1%; security and performance rules are much rarer. It studies content and maintenance, not semantic conflicts. [Agent READMEs, preprint, 2025/2026 revision](https://arxiv.org/pdf/2511.12884)
- **Toward an Evidence-Based Template for Agent Instruction Files** analyzes 3,387 files across four formats. Among 386 manually inspected corresponding-section pairs, 16.1% contain *divergent guidance*. This is the most relevant evidence that real cross-file inconsistency exists, though “divergent” includes complementary or agent-specific instructions and is broader than logical clash. [Evidence-Based Template, arXiv preprint, 2026](https://arxiv.org/pdf/2611.02383)
- **What Open-Source Projects Tell Their Coding Agents** analyzes 341,852 statements from 22,854 repositories. It provides a large taxonomy and warns that model annotators agreed more with each other than with the human reviewer. It does not check conflicts. [Census of AGENTS.md and CLAUDE.md, arXiv preprint, 2026](https://arxiv.org/pdf/2610.31715)
- **When Instruction Files Go Stale** evaluates three real stale instructions using 732 agent trajectories. Agents followed relevant stale guidance and recovered locally but never repaired the instruction; one stale test command added roughly two tool calls. This suggests that contradictions are only one form of instruction debt—staleness and disagreement with the repository may be more common and operationally measurable. [When Instruction Files Go Stale, arXiv preprint, 2026](https://arxiv.org/abs/2611.09802)
- A controlled ablation over 17 real tasks and 288 runs found no measurable correctness improvement from context files for either Claude Code or Codex. This reinforces the need to measure behavior rather than assuming that a textual clash necessarily affects the agent. [Do Context Files Help Coding Agents?, REALM/ACL, 2026](https://aclanthology.org/2026.realm-1.5/)

Therefore, do **not** claim “first empirical study of agent instruction files” or “first within-policy conflict detector.” A narrower novelty claim may survive: *a benchmark and comparative study of semantic clashes specifically in coding-agent repository memory folders, including direct-LLM and formalization-based baselines*. I would still phrase this as “to our knowledge,” not “the first.”

### Requirements, policies, and norms

**SAT-LLM** is almost your method: ChatGPT translates requirements to first-order logic and an SMT solver checks multi-requirement inconsistencies. On a 55-requirement Broker dataset with deliberately added composite conflicts, it reports precision 1.00, recall .83, and F1 .91 versus ChatGPT’s .85/.31/.46. Its authors explicitly identify accurate NL-to-FOL translation and real-world evaluation as unfinished work—the precise failure your project exposes. [Translation Titans, Reasoning Challenges, ASE NIER, 2024](https://www.researchgate.net/publication/383395498_Translation_Titans_Reasoning_Challenges_Satisfiability-Aided_Language_Models_for_Detecting_Conflicting_Requirements)

**ALICE** decomposes controlled-language automotive requirement comparison into seven semantic questions concerning variables, actions, conditions, and co-occurrence. It reports 99% accuracy, 94% precision, and 60% recall on heavily imbalanced real requirement sets, versus zero recall for an old GPT-3 direct baseline. Its controlled, atomic requirements are much easier to formalize than unconstrained memory Markdown. [Automated Requirement Contradiction Detection Through Formal Logic and LLMs, Automated Software Engineering, 2024](https://link.springer.com/article/10.1007/s10515-024-00452-x)

**PolicyLint** detects positive/negative privacy-policy statements while reasoning over an automatically constructed ontology. It found candidate contradictions in 14.2% of 11,430 app policies and manually inspected 510. This is a strong methodological analogue: domain ontology, large corpus, candidate-generation pipeline, manual validation, and an explicit taxonomy—without claiming that every formal match is a real-world failure. [PolicyLint, USENIX Security, 2019](https://www.usenix.org/conference/usenixsecurity19/presentation/andow)

Access-control verification has long encoded already-structured policies into SAT or SMT. XACML work proves the encoding sound and returns requests witnessing overlaps; AWS’s Zelkova compares IAM-policy behavior and reports `unknown` for unsupported constructs or timeouts. These successes depend on the input already having formal semantics, unlike Markdown instructions. [Formal Analysis of XACML Policies Using SMT, Computers & Security, 2017](https://www.sciencedirect.com/science/article/pii/S0167404817300135); [Semantic-Based Automated Reasoning for AWS Access Policies Using SMT, FMSE, 2018](https://d1.awsstatic.com/Security/pdfs/Semantic_Based_Automated_Reasoning_for_AWS_Access_Policies_Using_SMT.pdf)

Norm-conflict and deontic-logic work supplies appropriate concepts—obligation versus prohibition, permission versus prohibition, exceptions, priorities, and contrary-to-duty rules—but normally assumes norms are already formalized. ASP is particularly natural for defaults and exceptions. This work informs your taxonomy; it does not solve semantic parsing from natural memory files.

## 2. What “LLM alone versus tool+LLM” papers usually test

| Paper | Comparison design | Claimed advantage |
|---|---|---|
| **Logic-LM** | Standard prompting and chain-of-thought versus LLM translation plus domain-specific symbolic solvers on five logic datasets | Mean accuracy gain of 39.2 points over standard prompting and 18.4 over CoT; solver-error-driven syntactic refinement. [Findings of EMNLP, 2023](https://aclanthology.org/2023.findings-emnlp.248/) |
| **SatLM** | CoT and imperative program-aided LMs versus declarative specification plus solver on eight reasoning datasets | Better accuracy on search-heavy problems; correctness relative to the parsed specification; selective accuracy through rejecting malformed or unsatisfiable translations. [NeurIPS, 2023](https://papers.nips.cc/paper_files/paper/2023/file/8e9c7d4a48bdac81a58f983a64aaf42b-Paper-Conference.pdf) |
| **LINC** | Direct answers, logical scratchpads, CoT, and LLM-to-FOL plus Prover9 | Large gains on synthetic deep ProofWriter; roughly tied with CoT on expert-written FOLIO; complementary errors. Translation loses implicit facts and predicate distinctions. [EMNLP, 2023](https://aclanthology.org/2023.emnlp-main.313/) |
| **NL2TL** | Direct GPT translation versus proposition extraction plus lifted temporal-logic translation | More than 95% exact translation in three domains and better scaling with the number of propositions, but after training on a large domain-oriented corpus. [EMNLP, 2023](https://aclanthology.org/2023.emnlp-main.985/) |
| **SAT-LLM** | Direct ChatGPT versus ChatGPT-to-FOL plus SMT on a small requirements set | Higher precision/recall, especially for composite conflicts. Translation and real-world generalization remain open limitations. [ASE NIER, 2024](https://www.researchgate.net/publication/383395498_Translation_Titans_Reasoning_Challenges_Satisfiability-Aided_Language_Models_for_Detecting_Conflicting_Requirements) |

The recurring setup is: same or comparable LLM, direct/CoT/program baseline, frozen datasets with exact answers, and accuracy or F1 as the primary metric. Stronger papers additionally report executable-translation rate, abstention coverage, error categories, depth-stratified performance, robustness, and cost.

### Claims your evidence can honestly support

- **Raw accuracy:** No hybrid improvement. Whole-folder LLM wins on planted pairs, groups, and natural pairs.
- **Deep/compositional reasoning:** No. Z3 found 1/8 three-rule groups; the pipeline cannot claim a depth advantage.
- **Faithfulness:** Only “solver-faithful to its translation.” You cannot claim fidelity to the English.
- **Abstention/selective accuracy:** Not yet. Translation disagreement caught only 4/10 ambiguous frozen rules with precision .33.
- **Witnesses/explanations:** Potentially yes. Z3 can return a concrete conflicting branch/path/task situation. You still need humans to rate whether witnesses are faithful and useful.
- **Robustness:** No end-to-end robustness claim. Translation runs varied dramatically; repeated whole-folder LLM stability was not measured.
- **Cost:** You have useful accounting, but currently no demonstrated cost advantage. One folder-level call appears cheaper than many translations, and the triple scan took nine hours.
- **Scale:** No. You processed 1,287 rules with the LLM baseline, while formal triple checking at 64 rules was already impractical.
- **Certification:** Only of the fixed formal representations—not the original files.
- **Negative/scientific result:** Yes: realistic semantic translation and vocabulary coverage can erase the advantages reported on controlled reasoning benchmarks.

## 3. Is Z3 the right solver?

Yes—for the current vocabulary. Replacing it is unlikely to change accuracy because your observed failures occur before solving.

| Alternative | Better fit when… | Assessment here |
|---|---|---|
| **Z3/SMT** | Strings, integers, Booleans, set intersections, path/branch patterns, and existential witnesses coexist | Best current fit. Mature, automatic, and already validated by tests. Keep it. |
| **Datalog/Soufflé** | You need fast relational closure, dependency propagation, or candidate filtering over many rules | Easier to scale and explain for monotone relations, but awkward for permissions, defaults, exceptions, complements, and existential string-pattern overlap. Useful as a prefilter, not a replacement. [Soufflé documentation](https://souffle-lang.org/docs/home/) |
| **ASP/clingo** | Rules contain defaults, exceptions, priorities, defeasible permissions, or alternative acceptable worlds | Semantically attractive for norms and three-rule interactions. Harder for exact paths/globs, and answer-set semantics will require careful explanation. It still consumes mistranslations. |
| **Prolog** | Rapid interactive prototyping and human-written rule bases matter more than complete automated analysis | Easy to prototype; operational semantics, negation-as-failure, termination, and debugging make it a weaker research verifier. |
| **Deontic reasoner** | Obligation, prohibition, permission, priority, and contrary-to-duty behavior are the central contribution | Better conceptual vocabulary, thinner tooling and benchmarks. Risks turning one week into a logic-semantics project. |
| **SAT/MaxSAT** | Everything is finite/Boolean, or you want minimal correction sets and “fewest rules to relax” | SAT can be faster; MaxSAT could produce useful repair suggestions. Encoding strings and patterns manually removes Z3’s main convenience. |
| **Alloy** | Small bounded relational models and readable counterexamples are more important than unbounded claims | Excellent for demonstrations and bounded witnesses, but bounded analysis adds another qualification and does not fix translation. [Applications and Extensions of Alloy, MSCS, 2013](https://research.google/pubs/applications-and-extensions-of-alloy-past-present-and-future/) |
| **NuSMV/LTL** | Conflicts concern histories: “after,” “until,” “eventually,” repeated tool calls, or lifecycle states | The right direction for a runtime protocol model, but substantially more modeling is required. Current clashes are mostly static choice/scope conflicts. [NuSMV overview paper](https://nusmv.fbk.eu/papers/sttt_j/html/index.html) |
| **Cedar** | You can redesign agent rules as typed authorization policies over principals/actions/resources | Strong validation and analyzability; its analyzer itself compiles to SMT. Too authorization-specific for coding conventions and task ordering. [Cedar, OOPSLA, 2024](https://arxiv.org/abs/2403.04651) |
| **Rego/OPA** | The goal is runtime decisions over structured JSON tool events | Practical for enforcement, but conflict priority is author-defined; it is not automatically a semantic contradiction detector. [OPA policy language](https://www.openpolicyagent.org/docs/policy-language) |
| **Lean/Dafny** | You need machine-checked metatheory or verified monitor implementation | Massive overkill. Dafny itself ultimately uses Z3; Lean requires proof engineering. Neither repairs NL formalization. [Dafny reference](https://dafny.org/latest/DafnyRef/DafnyRef.html) |

The nine-hour triple scan is an implementation/search-space problem, not evidence that SMT is intrinsically wrong. Cheap fixes include indexing by action/target before solving, incremental solver contexts, caching pair compatibility, and asking the solver for inconsistent subsets rather than enumerating every triple. Datalog could help implement that indexing; ASP or MaxSAT could search conflict sets directly. None would raise recall beyond the translation/vocabulary ceiling.

## 4. One-week directions

| Rank | Direction and defensible claim | Existing evidence | Cheapest useful experiment | Main risk |
|---:|---|---|---|---|
| **1** | **Benchmark/failure study:** real coding-agent files contain diverse candidate clashes, but unconstrained translation is the dominant failure mode and direct folder review is a strong baseline | 1,287 rules; 43 adjudicated candidates; 22 clear candidate clashes; taxonomy; planted pairs/groups; translation labels; costs | Have two humans independently relabel the 43 candidates and the three probe discoveries, blind to method. Release source snippets, labels, ambiguity reasons, taxonomy, and all method predictions. Report *candidate-conditioned yield*, not prevalence. | The 43 were generated by model screens, so they cannot estimate population prevalence or recall. Five folders are small. |
| **2** | **Translation reliability/selective formalization:** formal checking is useful only on rules whose translations pass a reliability gate | Three translations for 84 rules; two-labeller translation labels; large run variance | Test whether cross-run semantic agreement, status, omitted-requirement count, or vocabulary-fit predicts translation correctness. Report coverage versus accuracy/AUROC and choose a frozen abstention threshold. | Existing instability had weak ambiguity precision; the signal may be poor. Still valuable as a negative result. |
| **3** | **Witnessed auditing:** solver flags are hypotheses with reproducible witnesses, not final contradictions | Z3 already produces conditional situations; one natural TP and one scope-loss FP expose both outcomes | For every existing Z3 flag plus matched LLM-only flags, generate a compact witness packet: original rules, activating state, incompatible actions. Blind humans rate validity and usefulness. Compare precision before/after source-text verification. | Very few natural in-vocabulary positives; statistical claims will be narrow. WIRE already establishes the general architecture. |
| **4** | **Runtime monitor:** a validated formal subset can deterministically block prohibited tool actions | Existing formal vocabulary maps directly to git/file/task events | Manually validate 10–20 formal rules, replay planted compliant and violating tool traces, and report enforcement accuracy, latency, and concrete explanations. Use Rego or the current Z3 code; do not retrain the translator. | This becomes a systems demo, not evidence that automatic English translation works. Coverage will be intentionally limited. VEPA provides a current formal-guardrail precedent. [VEPA, arXiv, 2026](https://arxiv.org/pdf/2610.12813) |
| **5** | **Incremental auditing:** cached translations make adding one rule cheaper than repeatedly rereading a folder | Saved translations and cost record | Add rules sequentially; measure new-rule translation cost, candidate pairs, solver time, and flags. Compare with a direct LLM prompt explicitly focused on conflicts introduced by the new rule. | An architectural cost win is likely, but accuracy may still favor the LLM. |
| **6** | **Broader formalism or vocabulary** | Only 5/22 natural clashes fit now | Do not attempt this before Dec. 1 | Expanding tools, numeric values, file layout, defaults, and temporal chains will enlarge the translation problem and invalidate frozen evaluation. |

I would combine directions 1 and 2: publish the benchmark/failure analysis, with translation agreement evaluated as a possible abstention signal. Direction 3 makes a good demo slide but should not be the headline.

## 5. Recommendation

**Proposed title:**  
**What Breaks Rule-Clash Auditing in Coding-Agent Memory? A Benchmark and Failure Study**

**Three-sentence pitch:**  
Coding agents increasingly rely on persistent natural-language rule files, but we find that detecting contradictions in them is primarily a semantic retrieval and translation problem, not a constraint-solving problem. Across real folders and controlled conflict sets, a direct whole-folder LLM outperforms an LLM-to-Z3 pipeline, while only 5 of 22 adjudicated real candidate clashes fit the pipeline’s fixed git/file/task vocabulary. We release a labeled benchmark, clash taxonomy, formalization annotations, repeated translations, and cost/error analysis showing where symbolic witnesses remain useful and where they must abstain.

That is a positive contribution because it answers a real design question and contradicts the easy assumption—encouraged by controlled benchmarks such as SAT-LLM and Logic-LM—that attaching a solver automatically improves reliability.

## Things the team may be missing

- **Human ground truth is now essential.** Claude plus Codex is not a substitute for two human annotators, especially with only 27/43 model agreement and one non-blind labeler.
- **You do not have a prevalence estimate.** The 22/43 figure is yield among LLM-nominated candidates. The 200-pair probe is restricted to pairs sharing at least two words and has only one judge.
- **The comparison changes two variables.** The direct model sees the rules jointly; the formal pipeline translates each independently. The result establishes that joint context matters, not purely that “LLM reasoning beats Z3.”
- **Define refinement versus contradiction.** Many disagreements concern a specific exception to a general rule, strong versus weak permission, priorities, or rules applying to mutually exclusive situations. Your labeling guide should state how these are treated.
- **Separate textual clash, activatable clash, and behavioral failure.** WIRE’s distinction is useful: two rules may look incompatible, may co-govern a constructed state, and may or may not cause the agent to violate either rule.
- **Measure duplicate and near-duplicate rules.** They distort pair counts and folder-level recall, as R74/R152 already demonstrated.
- **Normalize cost and latency by task.** Report folder size, tokens, dollars, wall time, failed calls, retries, and whether cached translations are reused.
- **Report uncertainty, not just fractions.** Results such as 2/2 natural pairs and 1/8 groups are descriptive, not stable population estimates.
- **Do not tune again on the planted benchmark.** Preserve the held-out materials for the presentation or omit a confirmatory claim.
- **Do not lead with three-rule reasoning.** With 1/8 recall and nine-hour runtime, it is presently a failure analysis, not a capability.
- **Preserve the negative result.** It is the most credible part of the project: formal solvers certify representations, and realistic semantic parsing determines whether those certificates mean anything about the source text.