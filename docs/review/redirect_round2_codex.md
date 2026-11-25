## 1. Best direction: runtime enforcement

This is the most plausible one-week positive result. I would give it roughly:

- **80% chance of an operational win** on cost, latency, and determinism.
- **55–65% chance of an accuracy/F1 win** on a deliberately narrow, monitorable rule subset.
- **Low chance of winning end-to-end on all 84 rules**, because automatic translation remains the bottleneck.

The claim should be narrow:

> After policies have been compiled and validated, symbolic checking is better than repeatedly asking an LLM whether concrete tool actions comply with a large instruction folder.

That is different from claiming that Z3 understands the original English better.

### Experimental design

**Rule population**

Use the saved 84-rule folder, but define the primary evaluable subset before generating actions:

- Every prohibition or precondition expressible using the existing git/file/task vocabulary.
- Target 16–20 rules covering paths and exclusions, branch globs, confirmation, secrets, file counts, tasks, and one-step history.
- Exclude pure stylistic rules and unbounded obligations.
- A `must_do` rule is enforceable only over a trace with an explicit `task_end`; a single proposed action cannot reveal that an obligation will eventually be omitted.

Keep two formal versions:

1. **Frozen automatic translations:** the honest end-to-end arm. Preselect one saved run without viewing action results; report the other two as sensitivity analysis.
2. **Human-validated translations:** the deployable compiled-policy arm and best prospect for a positive result. Validation must finish before action generation.

**Actions**

Have Codex generate **four actions per selected rule**:

- One ordinary violation.
- One subtle boundary violation.
- One closest legal action.
- One exception or scope near-miss.

For 16 rules, that gives 64 actions: approximately 32 violating and 32 allowed. Codex sees the English rules and ordinary tool-call schemas, but not translations or checker output.

Represent actions as structured tool events, for example:

```json
{
  "cmd": "edit",
  "path": "docs/internal/plan.md",
  "branch": "release/1.4",
  "user_confirmed": false,
  "prior": [{"cmd": "run", "task": "test", "ok": true}]
}
```

Both methods receive exactly the same event. Do not mix raw shell-command parsing into the primary experiment; evaluate a raw-tool-call adapter separately.

Two people independently label each action against the English folder, including violated rule IDs. Adjudicate before running any arm. The generator should not supply the gold label.

**Arms**

- Z3 with frozen automatic translations.
- Z3 with human-validated translations.
- Codex with the complete folder, three independent repeats.
- Codex with only the selected rules, three repeats. This controls for the possibility that the “win” comes solely from burdening the LLM with irrelevant rules.
- DeepSeek with the complete folder, one batched run.

Ask each LLM for only:

```json
{"allowed": false, "rule_ids": ["R17"], "reason": "..."}
```

Batch all 64 actions into one DeepSeek request. Based on the existing folder calls, budget **$0.03–$0.05**. Do not claim DeepSeek repeat stability from one run; repeatability can be measured for Codex and the checker.

**Metrics**

- Violation precision, recall, and F1.
- Overall action accuracy.
- Exact violated-rule attribution.
- Human-rated explanation correctness: does the cited rule actually apply, and do the supplied action fields witness the violation?
- Cold-start compilation cost and time.
- Warm per-action median and p95 latency.
- Marginal dollars per 100 and 1,000 actions.
- Identical-decision rate across repeats.
- Abstention/unsupported-rule rate.

Report both cold-start and amortized cost. Excluding translation and human validation from the cost comparison would be misleading.

### Fixed win conditions

Pre-register two distinct possible positive claims:

1. **Accuracy superiority:** validated Z3 has at least 0.90 violation F1, exceeds every individual direct-LLM run by at least 0.10 F1, and has no lower violation precision.

2. **Operational superiority at comparable accuracy:** validated Z3 is within 0.05 F1 of the best LLM run, with at least 0.90 precision and recall, while being at least 10× faster and 10× cheaper marginally at 100 actions, with 100% deterministic decisions.

For the automatic arm, count every translation failure or unsupported rule as a miss or abstention—not as an excluded example.

### Why each side could lose

The LLM can lose because it must repeatedly retrieve the relevant rule among many distractors, calculate exact glob/path overlap, remain consistent across dozens of nearly identical actions, and pay the folder-context cost again. Your existing full-folder miss and low overlap between Codex and DeepSeek make this plausible.

Z3 can lose because:

- Automatic translations omit conditions or permissions.
- Only a minority of discovered natural clashes fit the vocabulary.
- Tool calls may not normalize cleanly into the event schema.
- Unknown conditions, priorities, and exceptions require semantics the checker does not possess.
- Single-action monitoring cannot enforce future obligations.
- A correct formal decision can still be wrong about the English source.

### Is it rigged?

It is fair **as a deployment comparison** if you disclose that the validated monitor received an up-front policy-compilation step and report that cost. It is not a fair comparison of unaided natural-language understanding.

The selected monitorable subset favors Z3, so the claim must explicitly be “runtime enforcement of compiled git/file/task policies,” not “general instruction compliance.” The filtered-rule Codex baseline is important: if Z3 beats only the whole-folder baseline, the win is retrieval/scale; if it also beats filtered Codex, exact symbolic scope reasoning is contributing.

This direction also overlaps substantially with the verified UW policy-compliance paper. Your differentiation is the coding-agent instruction-folder setting, the direct whole-folder LLM baseline, and the explicit comparison of automatic versus human-validated compilation—not runtime SMT enforcement itself.

## 2. Comparison with alternatives

| Direction | Probability of a presentable positive | Plausible win |
|---|---:|---|
| **Runtime enforcement** | **~80% operational; 55–65% accuracy** | Comparable or better violation detection, exact rule witnesses, deterministic sub-second decisions, and much lower marginal cost |
| **Incremental auditing** | ~70% cost win; ~25–35% accuracy win | Translate one new rule and compare against cached policies for a nominal 10–30× marginal-cost advantage |
| **Failure study + agreement abstention** | ~15–20% | Better selective accuracy after abstention—but current ambiguity detection has only 0.33 precision, so evidence is unfavorable |
| **LLM flags, then Z3 verifies** | ~50% on a validated subset; ~20–25% end-to-end | Higher precision and reproducible witnesses for formalizable flags, at the cost of capped recall |

Incremental auditing is a good backup operational experiment, but the comparison must give the LLM the favorable task “find conflicts introduced by this new rule,” not require it to rediscover every folder conflict. Its strongest likely result is amortized cost, not accuracy.

The abstention direction is scientifically useful but unlikely to satisfy the advisor: the existing agreement signal is weak, and a negative abstention result is still another failure result.

LLM-then-Z3 verification is useful when the relevant rules already have validated encodings. Z3 cannot verify whether a natural-language flag is correct merely by solving a possibly wrong translation. Its recall is also bounded by the LLM candidate stage and the current vocabulary—only 5/22 clear nominated clashes were in scope.

## 3. Recommended talk

**Title:**  
**From Reading Rules to Enforcing Actions: Where Solver-Checked Agent Policies Win**

**Three-sentence story:**  
Detecting clashes in coding-agent instruction folders is primarily a reading and semantic-coverage problem: direct whole-folder LLM review beat our automatic LLM-to-Z3 pipeline. Runtime enforcement is a different regime, because the question is no longer “do any two English rules conflict?” but “does this concrete structured action violate a compiled policy?” On the validated, monitorable subset, report the symbolic checker’s measured accuracy, deterministic witnesses, and amortized cost advantage—without extending that result to unsupported natural-language rules.

Use past-tense “wins” only after a preregistered condition is actually met.

**Seven-slide order**

1. **Problem:** persistent agent rules can disagree, and agents must also obey them at runtime.
2. **System and data:** 1,287 natural rules, the 84 translated rules, vocabulary, and evaluation methods.
3. **Honest negative:** whole-folder LLM beats automatic translation plus Z3 on clash detection.
4. **Why:** translation loss, 5/22 vocabulary coverage, and the distinction between English truth and solver truth.
5. **Pivot:** concrete runtime action checking; arms, action examples, independent labels, and fixed win conditions.
6. **Positive result:** accuracy, precision/recall, rule attribution, latency, cost break-even, and repeatability in one dashboard.
7. **Boundary and conclusion:** validated subset versus automatic translations; unsupported obligations and policies; “reading folders and enforcing compiled policies are different jobs.”

## 4. Missing or risky

- The current code checks rule compatibility; it is not yet a complete per-action policy monitor.
- Immediate checking naturally supports `never` and `only_if`; obligations require trace semantics and a terminal event.
- The concrete-event adapter could become the new translation bottleneck.
- Selecting only monitorable rules creates a narrow, favorable benchmark.
- Codex-generated actions may reproduce Codex’s own interpretation of the rules; human gold labels are essential.
- Human validation makes the strongest arm compiler-assisted, not fully automatic.
- Sixty-four actions support a talk-level comparison but only limited statistical claims.
- DeepSeek gets only one repeat under the stated budget.
- Batched LLM judgment is cheaper than literal per-action calls, but its latency is not equivalent to an online one-action-at-a-time service. Report both modeling assumptions.
- Some actions may violate multiple rules; gold labeling and scoring must allow a set of rule IDs.
- The human-validated checker might achieve only a cost/determinism win, not an accuracy win.
- The UW paper means “SMT runtime guardrails” is not novel by itself.
- The final positive must not erase the central negative finding: automatic semantic compilation remains unreliable.

I made no changes and did not open the prohibited data locations. I also did not create a Lavish HTML artifact because that would conflict with the read-only instruction.