## Blunt conclusion

There is no defensible, preregistered slice in the existing data where the end-to-end Z3 pipeline beats the strongest whole-folder LLM baseline. There is one post-hoc sliver where it beats Codex but only ties DeepSeek. The most credible one-week opportunity is a frozen, large-folder test of subtle path/branch scopes—the part of the formal vocabulary where exact pattern algebra should genuinely help.

## 1. What the existing data show

- **Natural 84-rule folders:** On the original adjudication, Z3 found 1/3 clashes with one false alarm; Codex and DeepSeek each found 3/3 with zero false alarms. Under the later final labels, one of those three, R60/R213, became ambiguous, leaving Z3 at 1/2 clear clashes versus the whole-folder screens at 2/2. The Z3 miss and false alarm were translation failures, not solver failures. See [score.json](/Users/yingxizhao/dev/cs2520/projects/data/runs/natural/score.json) and [natural_findings.md](/Users/yingxizhao/dev/cs2520/projects/docs/review/natural_findings.md:9).

- **Fully translated three-rule groups:** Only G5, G7, and G9 fully translated. On this post-hoc slice, Z3 found 1/3; strict Codex found 0/3; DeepSeek found 1/3. Thus Z3 beats Codex by one but ties DeepSeek. This slice was noticed after seeing translation and detection results, so it cannot support a confirmatory claim. Overall, preregistered results were Z3 1/8, DeepSeek 5/8, strict Codex 2/8, all with zero control-group false alarms. [Experiment log G](/Users/yingxizhao/dev/cs2520/projects/docs/review/experiment_log.md:189).

- **False alarms:** The planted-pair pilots often had zero false alarms, but so did the LLM. The preregistered 435-pair precision probe was worse for Z3: two flags, both false, or 2/435 flagged and precision 0/2. On natural pairs Z3 had one false alarm while the subset LLM screens had none. There is no precision advantage.

- **Stability:** Z3 itself is deterministic conditional on a translation, but the end-to-end pipeline is not. Pilot runs found 10, 8, and 18 of 20 pairs in E6; after the final correction they found 9, 12, and 7, with only 3/20 found in all three runs. Whole-folder stability was not measured with repeated same-model runs; the two different LLMs shared only 4 of 15 flags. Therefore neither side has established end-to-end stability. [Experiment log](/Users/yingxizhao/dev/cs2520/projects/docs/review/experiment_log.md:92).

- **Folder-size effect:** Codex missed R60/R213 at full size after finding it in the 84-rule subset. But R60/R213 is ultimately labelled ambiguous, and it is only one size-transition observation. The 200-pair probe found 3 additional possible clashes, extrapolated to roughly 73 with a very wide 15–210 interval, but it used one Codex judge and was not adjudicated. More importantly, those examples concern command/tool choices outside the formal vocabulary. This establishes that one-pass LLM recall is imperfect, not that Z3 would recover the misses.

- **Vocabulary ceiling:** Only 5/22 clear full-folder clashes were judged expressible in the current vocabulary. The model covers git/file actions, fixed task kinds, paths, branch globs, booleans, and one level of prior actions. It does not cover most tool/command choices, numeric values, semantic file groups such as “documentation files,” tags, or deep temporal chains. [vocab.py](/Users/yingxizhao/dev/cs2520/projects/pipeline/rules/vocab.py).

So: **no existing result satisfies the advisor’s requirement**.

## 2. Best prospective regimes

### A. Large folder with many subtle, in-vocabulary clashes

This is the best bet.

Why an LLM may fail: whole-folder detection is a retrieval problem over quadratic pairs. Existing evidence already shows imperfect full-size recall, low overlap between two LLM screens, and an estimated reservoir of missed clashes.

Why Z3 may succeed: after each rule is translated independently, it exhaustively checks every relevant pair. Restrict the new material to operations actually covered—git, file actions, fixed tasks, paths, branches, and one-level ordering. Do not include tool names, values, tags, file-type semantics, or deep chains.

Cheap preregistered design:

- Reuse the 84 rules and saved translations from the group benchmark.
- Add 24 new natural-style rules: 12 clash cases and 12 matched compatible controls.
- Have Codex write them from independently sampled semantic specifications, using wording modeled on natural rules. The writer must not see checker output.
- Freeze rules, labels, prompt, seed, translator version, and method hash before translating.
- Run three fresh Codex whole-folder passes and one DeepSeek pass with the strongest prompt, plus the frozen translator/Z3 pipeline.
- Cost: approximately $0.019 for 24 translations plus $0.02–0.03 for DeepSeek: about $0.04–0.05.

Fixed win condition: count every translation failure as a Z3 miss. Claim a win only if Z3 finds at least 10/12 clashes, every single LLM run finds at most 8/12, and Z3 has no more than one control false alarm and no more false alarms than any baseline.

Threat: this is an in-vocabulary constructed benchmark and therefore favorable to Z3. Defuse it by saying exactly that, matching natural-rule wording, deriving cases before running either method, including hard controls, and reporting natural versus constructed results separately.

### B. Exact path and branch-pattern scope

This is the clearest reasoning advantage, but a narrower claim.

Why an LLM may fail: nested globs, exclusions, directory-versus-file scope, and overlapping branch patterns require exact set-intersection reasoning. Small wording differences such as `docs/`, `*.md`, `docs/**`, or `release/*` can reverse the answer.

Why Z3 may succeed: this is implemented directly using regex intersection and complement. `*`, `?`, `**`, directory recursion, basename-at-any-depth behavior, exclusions, and branch globs are explicitly supported by [patterns.py](/Users/yingxizhao/dev/cs2520/projects/pipeline/rules/patterns.py).

Test:

- Generate eight clashes and eight matched controls from a seeded pattern-relation generator.
- Separately ask Codex to render the abstract relations as natural memory rules; adjudicate ambiguous renderings before method runs.
- Embed them among the saved natural distractors.
- Use three Codex runs and one DeepSeek run.

Fixed win condition: Z3 at least 7/8 clashes, each LLM at most 5/8, with at most one false alarm and no more than the LLMs. Translation failures count as misses.

Threat: algorithmically generated glob cases plainly favor a symbolic method. This is acceptable only as a narrow claim—“exact scope relations”—not as general memory-clash superiority.

### C. Incremental folder updates

This is the best operational argument, but less likely to produce a raw-accuracy headline.

Why the LLM may fail: after every added rule, a plain baseline rereads the entire folder and may return a different incomplete list. Cost and context grow with the folder.

Why Z3 may succeed: translate the new rule once and compare it deterministically against cached translations. Marginal translation is about $0.0008 per rule versus roughly $0.02–0.03 for another whole-folder call—a nominal 25–37× paid-cost difference.

Test 12 sequential additions to the saved 84-rule folder. Predefine all clashes induced by each addition, give the LLM the favorable prompt “focus on conflicts introduced by the new rule,” and run three free Codex sequences plus one DeepSeek final snapshot.

Fixed win condition: Z3 must recover at least two more induced clashes than the best complete Codex sequence, have no more false alarms, and demonstrate at least a 10× marginal paid-cost advantage. Treat the DeepSeek endpoint as a sanity check, not an equivalent sequence unless budget permits every update.

Threat: caching gives Z3 an architectural advantage. That is the point of this deployment regime, but the claim must be about incremental auditing, not general reasoning accuracy.

Do not spend the week on deeper three-rule chains. The current checker explicitly does not model deeper prior-step chains, and the already favorable Codex-authored benchmark produced 1/8. [group.py](/Users/yingxizhao/dev/cs2520/projects/pipeline/rules/group.py).

## 3. Ranking

1. **Large folder containing subtle in-vocabulary scope clashes:** best chance of a real accuracy win and the strongest presentation.
2. **Dedicated path/branch-pattern benchmark:** highest probability of a solver win, but narrowly synthetic.
3. **Incremental updates:** strongest cost and determinism story; weaker chance of proving higher raw accuracy.

Recommendation: combine the first two into one frozen 108-rule test—84 saved natural rules plus 24 path/branch/file/task rules. Do not modify the translator or checker after predictions. If it fails the fixed win condition, stop trying to claim superiority.

## 4. Honest framing

**Title:** *When Solver-Checked Memory Audits Help: Exact Scope at Scale, with Translation as the Bottleneck*

The original broad comparison favored a single whole-folder LLM: it found more planted pairs and three-rule clashes than our translation-plus-Z3 pipeline. We therefore preregistered a narrower regime—large folders containing exact path, branch, file, and task scopes—where exhaustive symbolic checking has a principled advantage. The result shows whether that advantage survives end-to-end translation errors; outside this fixed vocabulary, direct LLM review remains stronger.

Do not claim that Z3 generally beats LLMs, improves natural-folder recall, certifies the original English folder as clash-free, or is end-to-end deterministic. At most, it certifies the supplied translations and may win on a preregistered, explicitly narrow scope-at-scale regime.