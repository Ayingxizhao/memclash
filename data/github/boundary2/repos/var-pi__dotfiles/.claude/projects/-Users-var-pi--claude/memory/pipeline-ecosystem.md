---
name: pipeline-ecosystem
description: The three-altitude planning pipeline (3 skills + 2 cores + reader-profile + domain profiles + 6 subagents + git-guard hooks + 2 check scripts) and its design intent
metadata: 
  node_type: memory
  type: project
  originSessionId: 685a0512-e644-4ce1-b0c2-2b309b52e7f9
  modified: 2026-08-12T12:17:12.749Z
---

A planning/execution pipeline on the ladder **project → feature → commit** lives in
interconnected files under `~/.claude/`, each read by a different model:

- `skills/project-plan/SKILL.md` — the **project planner** (Opus 4.8). Top altitude: through-line,
  decomposition into features, repo architecture, risk register. Emits one **feature brief** per
  feature. Added 2026-07-17.
- `agents/project-plan-reviewer.md` — its **reviewer** subagent (Opus, xhigh). Persistent;
  resumed with its full transcript (its prior reviews) intact each round.
- `skills/feature-plan/SKILL.md` — the lead **planner** (Opus 4.8). Decomposes a feature
  into one commit plan per file — the contract surface, decisions, and test intent — reviewed as
  one set. (Was "two tiers"; collapsed 2026-07-22, see below.)
- `agents/feature-plan-reviewer.md` — the **reviewer** subagent (Opus, xhigh). Persistent
  session, resumed each round over the whole set until the architecture converges.
- `agents/commit-plan-implementer.md` — the **implementer** subagent (Sonnet, xhigh as of
  2026-08-05; the planner may override one commit to Opus). Executes
  one commit plan at a time — **writes the code bodies and derives the test bounds theory-first**
  (as of 2026-07-22; the plan no longer carries code or numbers). It **delegates all durable doc
  *authoring* to two Opus writer subagents** (below) while owning verify/stage/commit itself.
- `agents/feature-readme-writer.md` — the **feature-README writer** subagent (Opus, high), and since
  2026-08-08 the pipeline's only doc writer. Authors the feature's *outward-facing* `README.md`,
  whose subject is **the insight the work produced, not the implementation**; dispatched **last**,
  once every commit has landed green; synthesizes the whole feature (`git log` over its commits +
  code + tests + existing figures); does not stage/commit. Added 2026-07-18. *(A sibling
  `commit-doc-writer`, authoring a per-commit `docs/commits/` file, existed 2026-07-18 → 2026-08-08;
  see the retirement entry below.)*
- `hooks/pre-push` + `hooks/commit-msg` — the **pipeline guard** (POSIX sh). Marker-gated on
  `$GIT_DIR/CLAUDE_PIPELINE_ACTIVE` (or `$CLAUDE_PIPELINE` override): during a run they block every
  push and reject a degenerate commit message; inert otherwise, chaining to any repo-local hook.
  `hooks/pre-commit` survives as a chain-only shim that enforces nothing (see 2026-08-08). Armed by
  `hooks/pipeline-marker.sh` on the implementer's dispatch, via per-repo `core.hooksPath`.

Design intent: shared execution discipline lives once in the implementer's prompt; plans stay
lean. The planner pins the architecture — contracts, decisions, each test's intent/target/method —
and hardens it as one reviewed set; the **implementer writes the code bodies and derives the
numeric bounds theory-first**. The one human checkpoint is the plan approval (`ExitPlanMode`,
Phase 4).

**Two-tier planning collapsed (2026-07-22).** An earlier design had the planner complete "the two
deferred parts" (exact code + empirically-grounded bounds) just-in-time per commit in a "Tier 2,"
each reviewed before dispatch. Retired because pre-written code turns the implementer into a
transcriber that stops checking integration, drains context twice, and grounds "final" code in
not-yet-built infra; the real safety net is the pinned test *target* + the implementer's
verify/mutation/`/code-review` loop. *Rejected alt:* planner code for load-bearing commits only (a
fuzzy per-commit classification that keeps the machinery alive). Now: one planning pass → one
whole-set architectural review loop → a thin execution loop (dispatch → gate → halt).
feature-plan-reviewer is architecture-only, persistent across *rounds*. Bounds are **theory-first**
(analytic where the math gives one; measured ~3σ only for the constant it won't). Retired
vocabulary: "Tier 1/Tier 2", "the two deferred parts", "empirically-grounded test bounds" as the
default framing.

**Hooks (2026-07-22).** pre-commit now **exempts docs-only commits** (nothing staged outside
`README.md`/`docs/`), so the docs-only feature-README commit carries **no** `docs/commits/` doc and
no `commit-doc-writer` pass (still routed through the implementer, which commits it). pre-push
unchanged.

**Shared cores + meta-skill (2026-07-22).** `shared/reviewer-core.md` now holds the discipline both
reviewers share (independence, objective-list workflow, resumed-not-respawned, converge); each
reviewer file reads it at start and carries only its altitude-specific objectives.
`skills/pipeline-maintenance/SKILL.md` is a new meta-skill for **editing this ecosystem** — it
carries the map, the cross-file dependency graph (altitude contract, docs/commits path ownership,
git-guard quartet, reviewer-resumption, README routing, session boundary, shared cores), the
editing discipline, and a post-edit checklist. Invoke it before changing any pipeline file. (A
`writer-core.md` for the two writers was scoped but deferred — the two writers are more
differentiated and the overlap smaller; a candidate follow-up.) No global `~/.claude/CLAUDE.md`
exists, so truly-general one-line preferences stay inline rather than being centralized there.

**Altitude contract (2026-07-17).** Each rung owns exactly one thing and copies nothing from
another: project-plan owns philosophy/decomposition and must contain **no signatures, no stubs,
no tolerances**; feature-plan Tier 1 owns contracts; the implementer owns code; Tier 2
owns measured numbers. A copy upstream is not a head start — it is a competing source of truth
that drifts once the real one is decided. The motivating artifact was
`~/repo/pavliotis/.../pavliotis_ch1_project_plan_3.tex`, which reached down two altitudes (a
450-line Julia stub appendix + per-feature signature tables + invented tolerances).

**The project-plan → feature-plan handoff crosses a session boundary**, deliberately.
project-plan names the next feature and *stops*; the human starts each feature in a fresh
top-level session. Two reasons: (1) `ExitPlanMode` doesn't exist for subagents, so dispatching
feature-plan as one would silently delete the pipeline's only human gate; (2) a whole
project doesn't fit one context window, and an *in-session* gate doesn't help — it gates the
start without refilling the budget. The persisted plan in `docs/plan/`, not a live session,
carries state across the boundary. This is why a feature brief must be self-sufficient for a
cold reader.

Vocabulary collision to respect: a **feature brief** (project-plan's per-feature entry) is not a
**feature plan** (feature-plan's Tier 1 set of commit stubs). "Unit" is retired.

On 2026-07-16 these files were refactored for consistency/compactness under the operative-why
test — see [[editing-subagent-guideline-files]]. (The 2026-07-22 collapse above superseded the
Tier-2 machinery this era introduced.)

Also on 2026-07-16, six Claude Code features were wired in: Phase 1 delegates the fan-out
survey to the `Explore` subagent (planner still deep-reads what it carves up); Phase 4 approval
runs through plan mode / `ExitPlanMode`, reordered to persist-*after*-approve; Phase 5 arms the
git guard and sends a `PushNotification` on halt; a new **Phase 6** disarms the guard, notifies
"ready to push", and writes cross-feature learnings to memory (planner-writes-at-feature-end);
the implementer's empirical verification now routes through the `verify`/`run` skills.
Key finding that shaped the guard: **CC `settings.json` hooks did NOT fire on `Agent`-subagent
tool calls (GitHub #34692, closed "not planned"), and the harness runs each Bash call in a
fresh shell** — so a runtime env var can't gate the subagent, hence the repo-local marker file.
(**Half-superseded 2026-07-25:** hooks now *do* fire on subagent tool calls and carry
`agent_type` — see the harness-substitution entry below. The fresh-shell half still holds, which
is why enforcement stays at the git layer.)

**Self-compaction was removed (2026-07-18).** The reviewers and planner previously told the model
to run `/compact` on itself after each review. This can't work: `/compact` is a built-in
interactive command with **no tool behind it**, so no model can self-trigger it — it is not a skill,
and even the main-session model can't emit it as a command. (The original entry also claimed
subagents have no `Skill` tool; **that is false** — `Skill` is in their default pool. The `/compact`
conclusion stands for the other reason.) Confirmed empirically: sending `/compact` to a subagent via `SendMessage` arrives as
**literal wrapped text** (no `compact_boundary`, no token drop; the subagent just reads the string
"/compact"). It's also unnecessary for the reviewers — they run ~2–3 passes and are resumed with
their **full transcript intact** (prior reviews already in context), never nearing the ~95%
auto-compaction threshold, so a carry-forward recap would only duplicate context. Fix: reviewers
now rely on the persistent transcript; the two skills dropped the false "self-compacts / already
lean on resume" claim; the planner keeps a slimmed note that steers *auto-compaction (or the human
typing `/compact` at the REPL)* to preserve the decomposition/contracts/decisions. General fact
worth keeping: built-in slash commands like `/compact` are not model-invocable. (This entry once
claimed `code-review` and `verify` *were* invocable bundled skills — **no longer true**, see the
2026-07-25 entry.)

**Execution-tier tune-up (2026-07-24).** A retrospective on the `05-bm-scaling-limit` run (5
commits; implementer tier ~730k of ~1.25M subagent tokens) drove these changes:
- **One synchronous gated run.** commit-plan-implementer runs the verifying experiment in the
  foreground exactly once — no background monitors, no repeated "confirmation runs" (seeded +
  deterministic ⇒ a re-run only reproduces identical numbers at full cost). Biggest leak: the
  stall/re-run instinct was baked into the agent and ignored per-dispatch instructions.
- **Single verification owner (model a).** feature-plan Phase 5 gates on the implementer's own
  result (commit landed + `ALL GATES: PASS` in the returned log + cheap test suite) and does **not**
  re-run the heavy experiment as a second ground truth. Codified a **land-or-idle waiter** (one wait
  per commit; no reactive polling; judge stall-vs-legit-run by the effort estimate). *Rejected alt:*
  model (b) — implementer a pure coder, orchestrator owns the authoritative run + commit — rejected
  as too invasive (would rewrite git-guard/doc-staging ownership).
- **Per-commit effort estimate** (template §0, renamed "Dispatch & effort") **+ a Phase-4 Execution
  budget** section the operator approves. Primary purpose is **operator awareness** — a legit long
  commit isn't mistaken for a stall. Advisory by default; a **hard stop only when the planner can
  certify (~3σ) the pinned config suffices**, never a cap that could abort work at 80%. Costly
  statistical gates ship a **near-final starting config** in the plan so the run is a check, not a
  search.
- **Descriptive-message guard (new `hooks/commit-msg`).** Marker-gated like the others; rejects an
  empty/degenerate message (subject < ~15 chars, or subject-only with no body) during a run. The git guard is now a **quintet**
  (pre-commit + pre-push + commit-msg + Phase-5 arm/disarm + implementer conventions).
- **`CLAUDE.md` added to the pre-commit docs-only exemption** (file set now
  `README.md` / `CLAUDE.md` / `docs/`), so a pure docs commit touching CLAUDE.md no longer forces a
  disarm.
- **Phase 6 retrospective + improvement-inbox loop.** feature-plan emits an operator-facing
  token/workflow retrospective and appends suggestions to [[pipeline-improvement-inbox]];
  pipeline-maintenance reads that inbox first (new **Intake** step) and reconciles it — a new
  coupling in the meta-skill's graph.
- **Removed the Phase 3 `/compact` steering note** (the "2026-07-18 slimmed note" above is now gone
  entirely) — planner context peaked at ~33%, so it was dead weight.
- **commit-doc-writer** reinforced to foreground the design "war story" (iterations / rejected
  approaches) for load-bearing commits.
- **Deferred (in the inbox, with reasons):** standalone API-doc artifacts (contract surface already
  serves it), Explore on a cheaper model (~35k, right-sized, harness-controlled), a planner
  context-offload agent (context is a non-problem).

**Docs-readability overhaul + two new agents (2026-07-25).** Operator feedback on the Unit-5 README
and commit docs (too verbose, everything weighted equally, run-log content crowding out design
content) drove these changes:
- **`shared/writer-core.md` (new)** — the second shared core, for the two doc writers, mirroring
  `reviewer-core.md`. Owns: the **rushed-team-lead reader** model and its economics (operator reading
  time dominates this workflow and costs far more than agent tokens, so extra passes to compress are
  always a good trade); layering (front-load, `<details>` folds for opt-in depth, `<summary>` as a
  real title, never fold the essential, headings as a table of contents); signal hierarchy (bold the
  load-bearing term, blockquote callouts — **one or two per doc**); denser-form selection; the cut
  list; figure embedding + the self-explanatory bar; LaTeX/jargon style; weight calibration; handoff.
  Both writer files were rewritten to carry only their audience, sources, sections, and altitude.
  (The 2026-07-22 "writer-core deferred, writers too differentiated" note is now superseded — the
  scannability rules turned out to be identical for both.)
- **commit-doc-writer re-scoped to "the build and the approach."** Three exclusions, generalized from
  the operator's examples: **not the run log** (seeds, gate margins, re-run counts, review status —
  state the conclusion, fold the raw output), **not the development history** (a bug fixed mid-flight
  is invisible in the final design), **not the code's local traps** (those belong in a code comment,
  where the implementer is separately required to put them). "Code review" and "Deviations from plan"
  stopped being always-present sections. TL;DR hard-capped at ~5 lines / 3 bullets. New metric: the
  **unfolded surface** stays under ~150 lines regardless of weight — depth below a fold is free.
  "Open with the picture, then the mechanics" (generalized from the praised Donsker-first framing).
- **The war-story rule was over-applied and is now bounded.** 2026-07-24 told the writer to
  *foreground* the war story for load-bearing commits; every doc grew one. Replaced by **"the one
  interesting thing — at most one per doc, usually none,"** folded, qualifying only if it changed the
  design. This is the ecosystem's canonical example of the new maintenance rule below.
- **`agents/commit-code-reviewer.md` (new, Opus, read-only, one-shot).** **`/code-review` is no
  longer model-invocable** — in Claude Code 2.1.220 it is a user-triggered command that fails with
  `disable-model-invocation` for any agent. The pipeline had been running with **no** independent code
  review, visible only as an aside in a commit doc. The new agent restores the control: the
  implementer dispatches it over its own diff, it reports (no write tools) and never fixes. It
  deliberately does **not** read `reviewer-core.md` — that core assumes a session resumed across
  rounds, which a per-commit one-shot is not. The `verify`/`run` skills are likewise no longer
  guaranteed present; the implementer's empirical-verification rule is now phrased "use them if
  available, otherwise drive the flow directly."
- **`agents/pipeline-retrospector.md` (new, Opus).** feature-plan Phase 6 no longer writes its
  own run retrospective — it dispatches this agent, because the planner reviewing its own run is the
  author's account. It reads the run artifacts + the current ecosystem files, files proposals to
  [[pipeline-improvement-inbox]], and returns an operator-facing retrospective the planner relays
  **verbatim**. *Operator asked whether it should simply upgrade the pipeline itself; scoped to
  **propose-only** — it may write that one memory and nothing else.* Rationale: those files govern
  every future run and the run closes unattended, so an edit here would change pipeline behavior with
  nobody reading the diff. *Rejected alt:* auto-apply "low-risk" changes only — needs a
  risk-classification the agent must judge correctly, the same fuzzy per-case call the Tier-2
  collapse already rejected.
- **New maintenance rule: generalize the feedback, never transcribe it.** Operator feedback arrives
  as examples; the rule written must be the extracted principle. Corollaries now in the skill: praise
  for a device is not a mandate to use it everywhere; a rule stated as a **cap** ("at most one",
  "under ~150 lines") survives an eager agent, an encouragement ("foreground the …") does not.
- **New post-edit check: named capabilities still exist.** The harness changes underneath these
  files; verify a skill/command an agreement depends on against the session's available-skills
  listing before relying on it.
- New couplings in the maintenance skill's graph: the **independent code review** (implementer ↔
  commit-code-reviewer ↔ feature-plan ↔ feature-plan-reviewer) and the **doc-style contract**
  (the implementer's bundle must pass a *superset* and let the writer select, or it competes with the
  writer's agreement and wins by accident). The improvement-inbox loop now spans four places.

**Harness-substitution audit (2026-07-25, Claude Code 2.1.220).** Prompted by "has the harness grown
builtins that replace parts of this?". Three of these are corrections of harness facts the files
rested on — all three had failed *silently*, which is the generalizable lesson.
- **`reasoning_effort:` was never a real frontmatter key.** All seven agents carried it; the schema
  field is `effort:`. Frontmatter parses loose, so the key was dropped with no warning and every
  agent inherited the session's `effortLevel: high` — meaning the two "xhigh" plan reviewers had
  **never actually run at xhigh**. Renamed in all seven; operator chose to keep xhigh as designed.
- **Marker arm/disarm retired (`hooks/pipeline-marker.sh`, new).** Hooks now fire on subagent tool
  calls and `SubagentStart`/`SubagentStop` take an `agent_type` matcher, so the marker's lifetime is
  bound to a `commit-plan-implementer` dispatch via two `settings.json` wirings. feature-plan
  Phase 5/6 and the halt path no longer arm, disarm, or mention the marker. Gains: the operator's own
  push is never blocked between commits, and a halt cannot strand an armed marker. The git hooks
  **stay** as the enforcement — the git layer catches a commit by any route, a `PreToolUse` Bash
  matcher only catches one made through Bash. *Rejected alt:* `disallowedTools: Bash(git push:*)` on
  the implementer to replace `pre-push` — the frontmatter-parsing risk (it might resolve to removing
  `Bash` outright and break every dispatch) isn't worth duplicating a hook that already works.
- **Shared cores are now preloaded skills.** `shared/*.md` → `skills/reviewer-core/SKILL.md` +
  `skills/writer-core/SKILL.md`, `user-invocable: false`, listed in the four agents' `skills:`
  frontmatter, which injects the full body at startup instead of trusting a "read this file first"
  instruction the agent could skip. `shared/` is gone. Two constraints: a preloaded skill must **not**
  set `disable-model-invocation: true` (that also blocks preloading), and a missing core is skipped
  with only a debug-log warning — hence each core now opens by stating it is preloaded and what to do
  if it is absent.
- **`/verify` joined `/code-review` as user-triggered-only** (2.1.215); the implementer's empirical
  verification now names only `/run`.
- **Checked and rejected:** agent teams (experimental, off by default, explicitly worse than
  subagents for sequential/dependent work, much higher token cost); packaging the ecosystem as a
  **plugin** (plugin subagents silently ignore `hooks`/`mcpServers`/`permissionMode`, which would
  break the marker wiring, and skills get namespaced — the benefit is distribution, which the
  dotfiles repo already covers); `isolation: worktree` (commits would land in a throwaway worktree);
  `maxTurns` (could abort a legitimate long gated run); the builtin task list for Phase 5 (the
  persisted plan set is already that queue).

**Altitude re-cut + implementer promoted to Opus (2026-07-28).** Operator review of the `06-fbm`
artifacts, plus the five retrospector inbox items from that run (all shipped).
- **`commit-plan-implementer` is now Opus/high.** No non-Opus node remains. What this *retired* is
  the argument for handing over near-final configs ("so a weak implementer doesn't search"); the
  "guaranteed-sufficient hard stop" marker went with it, having never been used by any commit.
  Consequence for maintenance: `pipeline-maintenance`'s "calibrate by reader" rule no longer keys on
  model tier — it now keys on the *file's job* (checklist vs. judgment instrument).
- **Measurement splits by question, not by rung** — the session's central decision. The planner may
  run code at plan time, against **already-existing** infrastructure, for one purpose: certifying a
  gate **discriminates** and a negative control genuinely fails. It writes the **margin** ("a wrong
  exponent moves this by O(0.1)"); every `atol`/`rtol`/SE-multiple/sample size is the implementer's,
  theory-first. Template §6's columns are now *intent / target / method class / discrimination*.
  *Why not simply forbid planner numbers:* the measurement's real job is **timing and scope**, never
  capability — the circulant-margin measurement is what *created* `06-fbm`'s probe commit and
  corrected the project plan's risk line, and the implementer (reading one plan) structurally cannot
  check a control in the last commit against a kernel in the first. *Rejected alts:* (a) planner
  measures nothing — decomposition-changing findings would then surface as a halt during the last
  commit; (b) legitimize the status quo (any measured number, tolerances included, reviewer
  re-measures) — it is what produced the frozen expressions below, and made three passes measure the
  same quantities. Redundancy now collapses to one pass per question.
- **The plan states what a test must distinguish, never how it is written.** A `method` naming an
  expression, fixture, grid size, or loop is code. *Motivating evidence:* `06-fbm` commit 01 shipped
  a provably no-op `eigvals(Symmetric(Matrix(Σ)))` because simplifying it "would be an unrecorded
  override of a plan-pinned decision", and a plan-pinned PSD check had to be rewritten after
  contributing 82 % of the suite's assertions for something other than what its comment claimed. The
  matching half is the implementer's new **"plan-stated mechanics are yours"** (an expression in a
  plan is illustration, not a decision) and `feature-plan-reviewer`'s new converse duty: *fault a
  plan that contains* a body, mechanic, or tolerance — not only one that omits them.
- **Additive-only relaxed to planner-declared consolidation.** Template §3 → "Files & delta": a
  commit may declare what it alters, subsumes, or removes. The guarantee that makes it safe, stated
  identically in three files: **the existing test-set stays green *unmodified* in that commit**; a
  legacy test that must change is a *contract change* needing its own declared step, never a quiet
  edit inside the commit whose implementation that test guarded. The implementer's ban on
  *opportunistic* restructuring is untouched. This is the commit-altitude half of the
  `APPROVAL-GATED` brownfield inbox item; the feature-altitude half (deltas in project-plan's briefs)
  stays gated.
- **Four more inbox items shipped:** never return in a waiting state (implementer re-dispatches a
  silent child once, else proceeds recording the step as not-performed) with its upstream half in
  Phase 5 (*a dispatch returning without its commit landed is neither success nor failure* — verify
  the tree, resume that same session, don't halt and don't re-dispatch cold); negative controls must
  be **certified** to fail, not merely named; §7 pass conditions must name a known systematic bias as
  the first hypothesis *and* the parameters that must not move; §0 effort splits **agent wall-clock**
  from **compute** (only wall-clock supports a stall diagnosis — `06-fbm` derived "past ~10 min is a
  stall" from a sub-minute experiment while all six dispatches legitimately ran 12–32 min).
- **Writer rules restated as caps/bounds**, because each already existed as an encouragement and
  failed to bite: a fold buys opt-in, **not exemption** from structure or the cut list; `<summary>`
  under ~8 words; **≤ ~5 consecutive prose sentences** without a structural break (a multi-sentence
  bullet counts as prose); **one section, one object**; the stand-alone bar extends from figures to
  **tables and display blocks**; claim strength must match evidence *and stay consistent across the
  doc*; the **antithesis tic capped at one per doc** with the tell named (*was Y ever on the table?* —
  "the nugget is reported rather than assumed" says nothing). commit-doc-writer additionally: every
  item under a heading must be an **instance** of that heading (a padded section is worse than an
  absent one); mechanical "What changed" items get **one line**; a decision earns a row only if the
  rejected alternative was **genuinely tempting**; never compare the work against the plan; notes
  aimed at the next editor of a line are **code comments**. feature-readme-writer: **≤ ~6 lines** from
  title to the first concrete thing. *No rule was written from the operator's praise* — every praised
  device already followed an existing rule, and the war-story precedent is why.
- **New coupling registered:** the delta/consolidation shape (feature-plan §3 ↔ implementer ↔
  feature-plan-reviewer), plus the altitude contract now explicitly spanning five files (the
  reviewer enforces it, `PIPELINE.md` §3 mirrors it).

**Readability + invocation pass (2026-07-28, second session that day).** Operator feedback: the
descriptions read like abstracts, the meta-skill has no stated workflow, and starting
feature-plan required spoon-feeding it "read file X, plan unit Y" every time.
- **`pipeline-maintenance` gained a six-phase spine** (read feedback → read ground truth →
  synthesize + ask → plan & `ExitPlanMode` → implement + checklist → **`/dotfiles-sync` commit and
  push**). Its existing sections became the detail behind phases 1, 2 and 5. Two bounds written with
  the rules: the question round asks only where two readings give *materially different edits* and
  arrives **batched** (a ritual round trains the operator to skim the one that mattered), and Phase 4
  is the sole gate (nobody else reads this diff — the same reason the retrospector is propose-only).
- **Phase 6 is new and load-bearing.** The ecosystem is distributed through the `~/.dotfiles` bare
  repo, so an uncommitted edit is one machine's local divergence and every other session keeps
  running the old rules with nothing reporting it. Scope bound: commit **only this session's edits**,
  name anything else dirty and leave it, so `git log` on these files stays a record of *why the rules
  are what they are*. New coupling registered ("the sync step"): a rename of `dotfiles-sync`, or an
  untracked new ecosystem file, fails silently — post-edit check 6's exact mode.
- **Description convention, now an editing-discipline rule with a cap.** A `description:` states
  *what + when*, **never how**, at **~25 words / two sentences**; mechanism there is an abstract of
  the body that owns the rule, free to drift, and the operator reads it in the `/` menu. Two things
  survive the cut: the **nearest-neighbour** discriminator and any **caller instruction** ("one plan
  at a time", "read-only"). All eleven descriptions rewritten (7 agents, 4 skills + `dotfiles-sync`).
  *Deliberate deletion:* "persistent — resumed each round" left both reviewer descriptions; it was a
  fourth copy of a protocol already owned by feature-plan Phase 3, project-plan step 3, and
  `reviewer-core`, and the dispatcher is the file that already states it.
- **`## How you are invoked` on both planner skills.** p-a-d: fresh session, cwd is the project repo,
  operator hands *where the project plan lives* + *which feature* — resolve both before exploring,
  accept the operator's word for the feature ("unit" is retired in the files, not in their speech),
  and when it is ambiguous **list the briefs and ask** rather than guessing, since a wrong guess
  burns a session's context. project-plan: same shape plus the distinction that actually bites — **a
  path to an existing `docs/plan/` plan means correction mode, not a fresh plan**, because the two
  are indistinguishable at invocation and re-planning discards the decision records.

**Bare invocation + the project-state record (2026-07-28, third session).** The operator's
correction to the invocation sections written earlier the same day: they had assumed a plan path and
a feature name would be handed over, and ended with *"never plan a feature the operator did not
name."* **The intended model is the opposite — `/feature-plan` is called with no arguments at
all**, in the project repo. `docs/plan/` is a fixed convention it already knows, the project plan
carries the spine, and the project's `CLAUDE.md` carries the state, so the feature is derivable and
asking for it was the per-run friction.
- **The rule was reversed, not softened.** Now: derive the next feature from the record, **announce
  it in the first message and proceed** (Phase 4's `ExitPlanMode` already gates the choice, so a
  blocking question buys nothing an announcement doesn't), and stop to ask in exactly two cases —
  `CLAUDE.md` and the project plan **disagree**, or a feature is recorded **in progress** (resuming a
  half-built feature and starting a fresh one are different jobs). An operator-named feature still
  overrides, in whatever words they use.
- **The blocking gap this exposed.** `CLAUDE.md` was written **once**, at Phase 4, describing the
  *planned* work; `commit-plan-implementer` touches it only incidentally; **Phase 6 had no
  `CLAUDE.md` step at all.** Nothing recorded that a feature *landed*, so a halt at commit 3 of 6
  left a record indistinguishable from a clean finish — and a bare invocation would have walked past
  a half-built feature into the next one. Deriving is only safe once the record is bracketed.
- **The run is now bracketed in a pipeline-state block:** Phase 4 opens the feature (in progress +
  commit count), **Phase 5's halt path records where it stopped**, Phase 6 flips it to landed and
  names the next; `project-plan` step 4 seeds the block for a fresh project, since p-a-d reads a
  missing block as a broken record. The planner commits these itself as docs-only commits —
  `CLAUDE.md` is already in `pre-commit`'s exemption set. *The halt write is the one to defend in
  any future compaction:* it fires unattended, and it is the only thing separating a half-built
  feature from a finished one.
- **`project-plan` leads with the convention** rather than with what it was handed: the plan lives at
  `docs/plan/`, and **what is on disk picks the mode** — a plan already there means correction mode.
  Same rationale as before (the two modes are indistinguishable at invocation and re-planning
  discards decision records); only the trigger moved from *a path you were given* to *what you find*.
- **New coupling — the project-state record**, spanning five places (project-plan step 4, p-a-d
  Phases 4/5/6, p-a-d's invocation) plus `pre-commit`'s exemption. Its failure mode is not an error
  but a plausible wrong feature. The **session boundary** coupling was updated to say what crosses
  it is written, not spoken.

**Visual map added (2026-07-25).** `~/.claude/PIPELINE.md` — Mermaid diagrams (end-to-end lifecycle
with both human gates and the session boundary; the implementer's inner loop as a sequence diagram;
the guard's branch logic; the improvement loop) plus the altitude-contract table, the artifact-path
table, a file index (model/effort/reads/dispatches), and a symptom→owning-file troubleshooting
table. Written because orientation is the one thing 13 agent-facing files could not provide: each is
prose for an agent about to act, so the *shape* of the whole — who dispatches whom, where the two
human gates sit — was legible nowhere. Markdown+Mermaid chosen over an HTML artifact so it lives
beside the files it documents, rides the dotfiles repo, and stays greppable. **Constraint that makes
it safe: pointer-only.** It names the owning file for every rule and states none itself; nothing may
be recorded only there, since a rule in a file that governs nothing is still read and obeyed and then
drifts. Registered as a coupling ("the visual map") in the maintenance skill's graph and in post-edit
checklist #7, because a mirror with no authority goes stale silently and a stale diagram is worse
than none — it is trusted at a glance.

**FOSS-survey items shipped (2026-07-28, second session that day).** Three of the five
`APPROVAL-GATED` inbox items from the 2026-07-25 survey were approved and built; two the operator
deferred (behavioural regression tests via `promptfoo`; a Semgrep pass beside the code review —
note Semgrep is not believed to support Julia, so that one needs a fact checked before reopening).

- **Feature-altitude brownfield delta** — completes the item whose commit-altitude half shipped
  earlier the same day. project-plan's brief gains field 8 **Delta** (`none — new ground` when it
  only adds, so an absent line cannot read as "nobody considered it"), `project-plan-reviewer` gains
  a **Declared deltas** objective, and feature-plan Phase 2 gains **carry a brief's delta down
  into the set**. Two bounds keep it from reaching down a rung: a brief **names modules, never
  signatures**, and it must **name every shipped guarantee it intends to break** — that break is
  exactly what the commit-altitude "existing test-set stays green *unmodified*" guarantee cannot
  cover, so it needs its own declared migration step. *Why the bounds and not just the field:*
  without them the brief re-specifies the replaced surface and becomes the competing source of
  truth the altitude contract exists to prevent.
- **`skills/handoff-core/SKILL.md` — the third preloaded core.** Owns all four agent-to-agent
  bundle field sets (code-review, commit-doc, feature-README, retrospective) plus a two-part
  protocol: the **sender writes every field including `none`**, the **receiver names any gap in its
  handback and proceeds** (never stalls — same principle as the implementer's *never return in a
  waiting state*). The two halves are a matched pair: without explicit `none` the receiver cannot
  tell a dropped field from a genuine nothing, so the check has nothing to bite on. *Why a core
  rather than a required-fields list in each agreement (the original proposal):* enforcement at
  both ends means both ends need the list, and a list in two files is the drifting-restatement
  defect. The sending and receiving agreements now only **name** a bundle. Boundary held
  deliberately: the core says what must *reach* an agent, never what its artifact contains — the
  **superset rule** stays with the doc-style contract. Harness constraint found and verified
  against the published field tables: **`skills:` is a subagent-only frontmatter key**, so
  `feature-plan` (a skill) cannot preload the core and invokes it via the `Skill` tool at
  Phase 6 instead. Writing it exposed a live drift that vindicated the item: `pipeline-retrospector`
  claimed the improvement-inbox path "is in your bundle" while the planner's list never carried it
  — now a declared field.
- **`skills/pipeline-maintenance/validate-config.sh` (new, POSIX sh).** The mechanical half of
  post-edit check 6. Checks frontmatter keys against the published field tables, that every
  preloaded `skills:` entry resolves and does not set `disable-model-invocation` (which would block
  its own preload), that each agent's `name` matches its filename, and that `settings.json`
  Subagent matchers and command paths still resolve. **Unknown key ⇒ warning; unresolvable
  reference ⇒ error (exit 1)** — because the field lists are transcribed from docs that move, so
  the validator can be the stale party. Verified against a fixture carrying all five historical
  failure modes. Two triggers, no background automation: post-edit check 6 (drift you introduce)
  and **feature-plan Phase 1** (drift the *harness* introduced with nobody editing a file —
  the `reasoning_effort` mode). *Rejected alt:* a `SessionStart` hook — it fires in every unrelated
  repo, and a warning seen 40 times a week stops being a warning. It cannot check whether a named
  capability is still *invocable*; that half of check 6 stays human.
- New couplings registered in the maintenance skill: **the handoff bundles** and **the config
  validator**; the delta/consolidation coupling now explicitly spans the feature altitude too.

**Measurement, tier split, per-session dispatch, ladder rename (2026-08-05).** Triggered by operator
asks about cost, pacing and naming; reframed by one finding that made most of them answerable.

- **Every cost figure the ecosystem had ever produced was wrong by ~170×.** The only number an agent
  can see is `totalTokens` on an Agent tool result, which **excludes cache reads** — and cache reads
  are 60–95% of a run. `07-sde-bridge`'s six implementer dispatches reported 1.31M; the transcripts
  say 222M. Measured truth: `06-fbm` 122.5M/$114, `07-sde-bridge` 478.8M/$445. Every prior
  retrospective, and the tuning done from them, argued against fiction. Fixed by
  **`skills/pipeline-maintenance/pipeline-stats.py`** (reads `projects/<slug>/<session>.jsonl` plus
  the `<session>/subagents/` tree, which carries `agentType`/`parentAgentId`/`spawnDepth` and full
  per-turn usage) plus the new [[pipeline-metrics]] memory. The bundle now carries **session ids, not
  token counts** — deliberately, so a wrong number cannot travel by narration. *Registered as the
  **measurement loop** coupling, spanning five places.*
- **Cost scales as ~turns^1.56** (R²=0.948, n=7), not linearly — so turn count is the lever and model
  tier the smaller one. Spend also concentrates hard: 2 of 8 commits were 60% of the implementer
  tier, the cheapest 3%. Both facts are why the tier decision below is *per commit*.
- **Implementer split by commit weight:** frontmatter `model: sonnet`, `effort: xhigh`, with the
  planner marking `model: opus` on commits carrying load-bearing mathematics (template §0). *Why
  xhigh:* `effort: high` was a **Sonnet-era holdover** — the 2026-07-28 Opus promotion changed
  `model:` and never revisited `effort:`. *Empirical anchor:* `06-fbm` ran the implementer on
  Sonnet 5 at 93 turns/commit and 35% of run cost; `07-sde-bridge` on Opus 5 at 217 turns/commit and
  60% — confounded by feature size, but it rules out the worry that Sonnet needs more turns.
  *Break-even:* Sonnet stops paying only past **+39% turns**. **Found and fixed while doing it:** §0
  had offered a per-commit **effort** override since 2026-07-24 — the Agent tool takes `model` only,
  so that half had never been deliverable.
- **Dispatch is now one commit per session.** Phases 1–4 run once; Phase 5 runs per session and
  stops. *Why:* the unattended chain accumulated 346 coordinator turns and 20% of `07-sde-bridge`'s
  cost, and a usage limit hitting mid-chain interrupted the run at an arbitrary point. The state
  block gains a **plan-set path** field — without it a fresh session can name the right commit and
  still not find its plan. "A feature is in progress" flips from a stop-and-ask to *the* resume path;
  the remaining stop-and-ask is *in progress but the plan set is missing*. Guard untouched: the
  implementer is still a subagent, so both `settings.json` matchers still fire.
- **Opus-5 re-baseline of the implementer.** The agreements were written for Opus 4.8. Deleted the
  verification scaffolding the current models perform unprompted (it is a *delete*, not a rewrite —
  telling these models to verify causes over-verification with no capability gain); capped review
  re-dispatch at **one**; added the **marginal-gate protocol** (diagnose the mechanism before
  touching a number — enlarging an ensemble makes a *biased* gate worse, and one feature's three
  marginal gates each needed a different response); added a scope bound against unrequested helpers
  and abstractions.
- **Ladder rename:** `master-plan` → `project-plan`, `plan-and-dispatch` → `feature-plan`,
  `master-plan-reviewer` → `project-plan-reviewer`, and this memory → `pipeline-ecosystem`. The
  *agents* were already systematic (`<rung>-<artifact>-<role>`); only the skills were inconsistent.
  **`commit-plan-implementer` deliberately keeps its name** — the git guard's two matchers key on it
  and it appears in shipped `docs/commits/` files, so renaming would break the record for no
  operator-facing gain. Timing chosen because the roadmap had just closed: no run in flight, no new
  artifact carrying a retired name.
- **The improvement-inbox loop had broken.** `07-sde-bridge`'s retrospector filed six well-argued
  proposals to a **project-local** memory file the maintainer never reads. Fixed with an absolute
  fallback path and an explicit "never create a second inbox"; the six items were merged into the
  global file and shipped.
- **Deduplicated the generated-artifact bar**, which was stated four times (implementer,
  `commit-code-reviewer`, `writer-core`, [[figure-legibility-requirements]]). The implementer owns it
  because it owns the generating; the others name it and add only their own act. *Registered as a
  coupling.*
- **Considered and rejected (2026-08-05, first session):** turning the two doc writers into skills invoked by the implementer
  (the operator's token-saving hypothesis). Measured the opposite — a writer subagent runs at
  1.3–3.7M cache-read against the implementer's 250–350k context, so inlining the same work would
  cost ~3.5× more *and* lose the fresh-context read of the diff. Also rejected: a new specialist
  agent (nothing a generic agent does is expensive enough to justify the preload + coupling —
  `Explore` just needed routing to Sonnet), and having the implementer write memories (one per
  commit is the war-story failure mode again). **Condensation was measured, not assumed:** the
  implementer's agreement is ~2% of its own dispatch cost, so condensation buys precision, not
  tokens — it was scoped to the dedup above rather than a global squeeze.

**Foreground dispatch — the stall machinery was treating a symptom (2026-08-05, second session).**
Triggered by an operator ask about two verification articles plus a sweep of recent Claude Code
releases. The articles taught little; the harness sweep found the root cause of a defect the
ecosystem had been patching for two features.

- **The finding.** Since **Claude Code v2.1.198** subagents **run in the background by default**; a
  background result arrives as a completion notification in a *later* turn, so a dispatching agent's
  turn can end while its child still works, and the result surfaces to whoever is listening. **No
  agreement in the ecosystem mentioned this.** Evidence from the actual transcripts (166 `Agent`
  dispatches in the `pavliotis` project): the main session dispatched the implementer in the
  foreground **40 of 41** times, but the implementer — one level down, where the agreements were
  silent — backgrounded **9 of 22** `commit-code-reviewer` dispatches, plus doc- and README-writer
  calls. The dates settle it: the three `rib=UNSET` nested dispatches are **2026-07-26** (`06-fbm`)
  and the eleven `rib=true` ones are **2026-07-29 → 08-04** (`07-sde-bridge`) — precisely the two
  features whose retrospectives produced *never return in a waiting state* (2026-07-28) and the
  late/misrouted-result merge rules (2026-08-05). The pipeline had written recovery machinery for
  the documented behaviour of a parameter nobody was setting.
- **The fix, stated once.** `handoff-core` gains a **sender: dispatch in the foreground** rule
  (`run_in_background: false`) as the first half of its protocol — it is squarely "what must *reach*
  an agent", and every handoff in the pipeline is sequential and dependent, so the default buys
  nothing. `commit-plan-implementer` and `feature-plan` Phase 5 beat 1 only **name** it; the planner
  needs its own copy because `skills:` is subagent-only and a skill cannot preload a core.
  **The recovery machinery was deliberately kept** — a background dispatch can still slip through,
  and the rules cost little. *Generalizable lesson:* the symptom ("a child that never reports") was
  diagnosed twice from inside the run, where the cause is invisible; it was only visible by grepping
  the `Agent` tool inputs in the transcripts. Prefer the transcripts over the agreements when a
  dispatch misbehaves.
- **Nesting depth registered as a dependency.** The pipeline requires depth ≥ 2 (session →
  implementer → reviewer/writers). The default was **1** until **v2.1.219** raised it to 3, and
  `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` can restore it. At the limit the harness **withholds the
  `Agent` tool** rather than erroring, so the failure mode is an implementer that quietly writes its
  own commit doc and skips its independent review. `validate-config.sh` cannot see this.
- **Both of the above are now one coupling** in `pipeline-maintenance` — *the dispatch shape* — and
  two `PIPELINE.md` troubleshooting rows.
- **The articles.** The *agentmarketcap* post (Opus 4.7, April 2026, third-party) claims models now
  self-verify — which is what the Opus-5 re-baseline above already concluded when it **deleted** the
  verification scaffolding. It confirms a decision rather than proposing one; its one unadopted idea
  ("capture uncertainty signals before completion") was declined as ceremony, since declined findings
  and plan deviations already ride the handback. Anthropic's *verification loops as skills* post
  reframes the `APPROVAL-GATED` deterministic-checks inbox item — **the loop is the skill, not the
  tool**, which dissolves the Semgrep/Julia blocker. Left gated at the operator's instruction, with
  the reframe and its altitude question annotated in [[pipeline-improvement-inbox]].
- **Harness sweep, checked and rejected (2026-08-05):** `fallbackModel` (a silent downgrade on a load-bearing-math
  commit is worse than a visible halt); dynamic workflows (rejected for the same reason as agent
  teams — this work is strictly sequential); `/goal` (fights one-commit-per-session); Artifacts for
  `PIPELINE.md` (the markdown-beside-the-files rationale stands); `Agent(model:opus)`-style
  permission rules (the git layer catches a push by *any* route, a tool matcher only through Bash —
  unchanged since 2026-07-25); `/usage` per-subagent attribution (`pipeline-stats.py` measures
  better). `validate-config.sh` was **not** stale — its field lists already carried `background`,
  `context` and `isolation`. Noted for the operator: 2.1.221/222 exist and fix subagent `model:`
  override handling.

**The project plan gained a writing discipline (2026-08-06).** Operator feedback: the project
planner "has to learn a thing or two from other writers — folds are welcome, low noise/high signal
is a mantra to take seriously, good structure is always welcome; not poetic but precise, we are
doing science here." The gap was real and total: `writer-core` gives the two doc writers a full
craft agreement, and **`project-plan` had none** — it specified what the plan must *contain* and
nothing about how it reads. Measured in the artifact (`~/repo/bip-lab/docs/plan/bip-lab.md`, 719
lines): **zero** `<details>` folds; brief F5 at ~85 lines against an agreement saying "each field is
a line or two"; four invented sub-headings replacing field 2; the `X, not Y` cadence ~6×.

- **New section `## How the plan reads`** in `project-plan`, every rule a cap. Its operative why is
  the **two readers that fail differently**: the human at the approval gate, where noise costs
  attention, and a **cold `feature-plan` session** that reads one brief and acts on it, where
  ambiguity costs a misplanned feature nothing downstream catches. Rules: every line must change
  what a reader does; structure is navigation (enumerable ⇒ table, one section one object); **fixed
  fields stay fixed** — more room means a fold, never an invented sub-heading, because a cold
  planner must land on field 8 without reading 1–7 and the reviewer checks field by field;
  **unfolded surface capped at ~25 lines per brief / ~1 screen per section** with depth below a fold
  free; a fold buys opt-in, not exemption, and nothing essential goes in one (*at the approval gate
  there is no fold to open*); precise-not-literary with the antithesis cadence capped at one per
  plan. Two clauses pre-empt the obvious objections — a folded passage is still plain text to the
  cold planner reading the file, and a `.tex` plan's equivalent is an appendix.
- **The cap is safe to state hard because of its pairing with the fold.** It can only relocate
  content, never strip it — which is what let this be written as a cap rather than the encouragement
  that has failed every previous time (2026-07-28).
- **`project-plan-reviewer` gained a *Legibility* objective**, phrased as **fault the form as you
  would the content** (same shape as "fault a delta that names a signature"). Without it the rule is
  obeyed on run one and gone by run three, and the author is structurally the last person who can
  see the defect — prose reads clearly to whoever just wrote it.
- **Registered as a coupling: *the artifact-craft rules*, split by artifact, not by principle.**
  `writer-core` owns the doc writers' statement; `project-plan` owns the plan's; neither may be
  rewritten to cover the other's artifact, and a change to a shared principle checks both.
  *Rejected alt (a):* point `project-plan` at `writer-core` — it is model-invocable, but a skill
  cannot preload a core, half of it does not apply (figures, handoff), and its **LaTeX ban directly
  contradicts** `project-plan` step 4's `.tex` permission. *Rejected alt (b):* a fourth shared core
  — one consumer does not justify the preload and the coupling.
- **Deliberately not extended down a rung** (operator-confirmed): a commit plan is read only by the
  implementer and the reviewer, agents that read linearly, so folds and scannability buy nothing
  there. `PIPELINE.md` got one troubleshooting row; the §3 altitude table was left alone, since
  that column is content ownership and form is not altitude.

**Implementer flipped to Opus, Fable rejected, map rewritten (2026-08-07).** Operator upgraded Pro →
Max x5 and asked three questions: use Fable anywhere, promote the implementer, bump effort.

- **`commit-plan-implementer` is Opus/xhigh again, and the marker inverted.** Template §0 now names
  `model: sonnet` as a **downgrade** for a commit carrying *no new load-bearing mathematics and no
  novel contract* (scale-up, plumbing, mechanical extension). *Why:* the 2026-08-05 Sonnet default
  was a cost decision, and 5× limits removed the constraint; Opus 5's advantage concentrates on
  multi-file/refactor work and narrows on easy single-turn edits, which is exactly the implementer's
  split. Not derivable from the rows — 93 turns/commit (Sonnet, `06-fbm`) vs 217 (Opus,
  `07-sde-bridge`) is confounded by feature size — so this is recorded as a **preference call**, to be
  judged by the next [[pipeline-metrics]] row.
- **The generalizable half: whichever way the marker points, the skipped marking is the free one.**
  Under Sonnet-default, omitting `opus` was visible; under Opus-default, omitting `sonnet` costs
  nothing and *reads as caution*, so an unmarked set silently runs everything at the default and the
  discrimination dies. `feature-plan-reviewer`'s objective was therefore re-pointed and given a cap
  ("on a set of four or more, no `sonnet` mark at all is a finding"). Registered in the coupling: a
  future flip must move that objective with it.
- **Fable 5: rejected, not deferred-by-omission.** *Operator's reason:* Opus 5 trumps Fable on almost
  all fronts at half the price ($5/$25 vs $10/$50 per MTok); revisit at the next Fable release. Two
  facts worth not rediscovering: `fable` **is** a valid `Agent`-tool model alias in 2.1.222 (the
  blocker was never mechanical), and Fable is metered *separately from plan limits* — a per-model
  allowance with a usage-credits path behind it. *A correction worth keeping:* the maintainer first
  argued against Fable **from that metering**, reading strings in the CC binary as evidence the
  operator was constrained; they were evidence a mechanism exists, nothing more. A mechanism is not a
  measurement. The surviving argument is different and unresolved: published guidance says prompts
  written for prior models are *often too prescriptive for Fable and reduce its output quality*, and
  these ~3,400 lines are exactly that shape — so re-opening means an A/B with scaffolding removed,
  not a frontmatter edit. `pipeline-stats.py` gained a `claude-fable-5` price row anyway, because
  `DEFAULT` is Opus-priced and would silently halve the cost of any hand-run Fable dispatch.
- **`commit-code-reviewer` high → xhigh** — the only effort change. It is the pipeline's sole
  independent code review, its job is squarely coding/agentic judgement (where xhigh is the documented
  setting), and it now reviews Opus-written diffs. The plan reviewers stay xhigh (`max` is documented
  as prone to overthinking); the writers and retrospector stay high. *Noted, not changed:*
  `settings.json` carries `effortLevel: high`, which is what every main-session skill actually runs at.
- **New bound: the implementer delegates to exactly three agents.** Opus 5 reaches for subagents
  markedly more readily than the model that agreement was tuned for, and the implementer *is* a
  delegating node. It may now dispatch only `commit-code-reviewer`, `commit-doc-writer`, and
  `feature-readme-writer`; verification is never delegated. Operative why (measured 2026-08-05): a
  child runs at 1.3–3.7M cache-read against the implementer's own 250–350k context.
- **`PIPELINE.md` rewritten** — 289 → ~208 lines, nine sections to eight. Fixed staleness that had
  survived two sessions: the implementer labelled "Opus high" (wrong on both counts since
  2026-08-05), Phase 5 described as walking the whole set, and a verified-against line for 2.1.220.
  Merged the artifact-path table into the file index, dropped the four-box improvement-loop diagram,
  and cut prose that restated an adjacent table. Three diagrams survive. **The ~130-line target was
  missed and the estimate is the lesson:** it was formed by costing prose, but 35 of the file's lines
  are table rows carrying one fact each, and those are the part a human actually uses. Cutting to 130
  would have meant deleting reference rows, not tightening writing.

**`docs/commits/` retired; the commit message is the deliverable; the README re-aimed at insight
(2026-08-08).** Two operator `.todo.md` items, worked together because they are the same question:
what each written artifact of a feature is *for*.

- **The `docs/commits/` file and `commit-doc-writer` are gone.** The operator's reasoning: the doc
  and the commit message explained the same increment twice, the doc cost an Opus dispatch per code
  commit, and the review surface they actually use is `git log`. **The message is now an increment's
  only durable explanation**, and the standard moved into `commit-plan-implementer` → *Write the
  commit message*: subject; a body covering what was built / why this approach / what the tests pin /
  the evidence, **capped at ~15 lines** with most commits far under; plain text, no Markdown. The
  retired agent's four exclusions were sound and carried over almost verbatim — **not the run log,
  not the development history, not a comparison against the plan, not the code's local traps** — plus
  the rejected-alternative bar (a rejection nobody would have chosen is not a decision).
- **The altitude call: §8 pins the staging set and nothing else.** It previously pinned "the exact
  staging and the full commit message". A message written at plan time states *intent*, not what
  landed, and the implementer transcribes it — the same defect as a pre-written code body one rung
  down, now landing on the one artifact the operator reads. `feature-plan-reviewer` gained the
  converse duty (a drafted message in §8 is a finding, same shape as an expression in a `method`
  column). *Rejected alt:* a dedicated commit-message writer subagent — it re-adds most of the token
  spend this change removes, since a child runs at 1.3–3.7M cache-read against the implementer's own
  250–350k (measured 2026-08-05).
- **`hooks/pre-commit` was reduced to a chain-only shim, not deleted** — the trap worth not
  rediscovering. `pipeline-marker.sh` sets `core.hooksPath` with `git config --local` and never
  unsets it, so every repo that has ever run the pipeline looks there for its hooks from then on;
  deleting the file would silently stop running that project's own `pre-commit`, forever, with
  nothing reporting it. The **docs-only exemption** vocabulary (`README.md`/`CLAUDE.md`/`docs/`) is
  retired everywhere it appeared.
- **`hooks/commit-msg` was deliberately *not* strengthened**, though it is now the only guard on what
  a commit says. A hook measures length, and length is not quality: raising the thresholds buys
  padding rather than explanation. Both the hook and the implementer now say the check is a **floor,
  not the standard**. The git guard is a **quartet** (marker + its 2 wirings + pre-push + commit-msg).
- **`writer-core` retired and folded into `feature-readme-writer`.** Losing `commit-doc-writer` left
  it with one consumer, which is exactly the test that kept a fourth core from ever being built:
  *one consumer does not justify the preload and the coupling.* The pipeline now has two cores
  (`reviewer-core`, `handoff-core`) and one doc writer.
- **The README's subject is now the insight, stated as three hard exclusions** (operator: "not
  implementation level information… taken to relative extreme"): **no component/module inventory, no
  API/parameter/configuration reference, at most one runnable block** and only to make a claim
  reproducible. *The operative why is exclusivity, and it is what makes the rule generalize:* the
  README is the **only** artifact that can carry the feature's insight — a commit message explains
  one increment and cannot see across the set, the code says what it does and never what it showed,
  the tests pin behaviour and not meaning. Anything else a README holds duplicates something that
  already exists somewhere better. Paired with a guard against the obvious over-correction: insight
  is *specific*, so vagueness is not the compliant form.
- **Handoff bundles: four → three.** The commit-doc bundle is gone; the feature-README and
  retrospective bundles now carry the feature's **commit range** in place of the docs path, since
  `git log` is where per-increment explanation lives.
- **`pipeline-stats.py` keeps `commit-doc-writer` in `TIER_ORDER` on purpose** — features measured
  before this date have a real tier under that name, and dropping it would sort those rows to the end
  of every historical report.
- **Unmeasured, like the Opus flip before it.** Expected direction is one fewer Opus dispatch per
  code commit plus a shorter artifact; whether that shows up is the **next [[pipeline-metrics]] row's**
  job to say, not this entry's.

**`reader-profile` — the calibration layer (2026-08-08, second session that day).** The operator
delivered a finished reader profile (what may be assumed unexplained for them as reader, standing
notation, where to spend words, and a **no-verdict clause**) with an instruction to wire it into
seven consumers. Two of the seven were wrong, both verified against ground truth rather than memory:

- **`commit-doc-writer` was named as its "primary customer"** — retired six hours earlier, in the
  session recorded directly above. Its consumer slot was already covered by `commit-plan-implementer`,
  which now owns the commit message. *Generalizable:* a document written against the ecosystem goes
  stale between drafting and wiring; check the roster, not the draft.
- **`skills:` in a skill's frontmatter was the specified mechanism for the two planner skills** — it
  is **subagent-only**. Re-verified today against the published tables (`/docs/en/skills` frontmatter
  reference has no `skills:`; `/docs/en/sub-agents` defines it as "preload into the *subagent's*
  context"), so the 2026-07-28 finding still holds. A `skills:` block in a `SKILL.md` parses, is
  dropped, and the skill runs uncalibrated — the `reasoning_effort:` mode. Fixed by the existing
  `handoff-core` precedent: **four agents preload, two skills invoke** via the `Skill` tool, each
  carrying the "you cannot preload it" why so a later edit does not convert it back.
- **`validate-config.sh` was the file that should have caught this and only warned.** `skills:` in a
  `SKILL.md` is now a hard **error** naming the workaround. This deliberately breaks the validator's
  standing rule (*unknown key ⇒ warning, because the validator can be the stale party*) — the
  distinction that licenses it is **known-invalid vs. merely unlisted**. Also refreshed `SKILL_FIELDS`
  against today's table (`when_to_use`, `metadata`, `license`, `compatibility` were missing and
  warned spuriously); `AGENT_FIELDS` checked and still exact.
- **Two scope rules were added that the delivered draft did not have, and they are the load-bearing
  part.** (a) It governs **shipped artifacts only** — not review findings, handbacks or the
  retrospective. §6 forbids most of a review finding's vocabulary (*critical*, *the key gap*,
  *subtle*), so a reviewer reading it as a style constraint files a weaker finding and **nothing
  reports it**; the file now says that for the plan reviewers it is a *checking standard*. (b) **An
  artifact's own agreement wins on audience** — `feature-readme-writer` writes for a newcomer, bans
  LaTeX and requires every symbol defined, all of which flatly contradict the profile's
  assume-silently ledger and `$\mathcal X$` notation. §2/§3 yield there; **§1.3, §1.4, §5 and §6
  never yield**, because they are honesty rules rather than audience calibration. Stated as a named
  precedence order and mirrored by name in `feature-readme-writer`, since a collision left to
  judgement is resolved two ways on two runs. *Rejected alts:* dropping the writer from the list (it
  would lose the no-verdict clause, which applies regardless of who reads); re-aiming the README at
  this reader (reverses the same-day insight decision).
- **Not a `-core`, deliberately.** A core is discipline shared by agents in the *same role*; this is
  one reader cutting *across* roles — which is also why it is the first shared file reaching both
  preloaded agents and invoking skills. Its §9 keeps only the **two exclusions**
  (`commit-code-reviewer`: correctness and contracts, so pedagogical findings sit outside its remit;
  `pipeline-retrospector`: reviews the run, ships no reader prose) and points at the coupling for the
  roster — the delivered nine-row injection table was a seventh copy of the wiring and already named
  the retired agent.
- **Registered as a coupling ("the reader profile"), spanning nine files**, plus two `PIPELINE.md`
  rows (file index + troubleshooting). **Cost is a projection, not a measurement:** ~3.4k tokens
  preloaded into four agents, order $3 against a measured $445 feature — the next
  [[pipeline-metrics]] row is what settles it.

---

# 2026-08-10 — the radical prune (operator-directed)

**The brief:** *"We have accumulated too much bloat and overspecification … prune it of all that is
not absolutely necessary … if we'll have to put something back then we'll know that we did not
undercut too badly. Overspecification makes models stupid in a sense that they just obey them and do
not even try to assess whether in a given situation it is reasonable."*

**Measured before:** 3,334 lines / 33,381 words across 13 governing files + 4 hooks. 53 embedded
incident narratives (20 in `feature-plan` alone); 36 restatements of *the plan holds no code /
mechanics / tolerances*; the identical project-agnostic preamble in 5 files; a `Preferences &
tradeoffs` section in 6; 13 inline decision records.

**The cut line adopted, and now the standing rule in `pipeline-maintenance` → *Editing discipline*:
keep information, cut instruction.** Information is what an agent cannot derive from its own
context — harness mechanics whose failure is silent, cross-session state, arbitrary coordination
conventions, facts about this reader, measured findings. Instruction a frontier model already brings
is pure cost: it consumes attention and teaches the agent to demonstrate compliance rather than
assess the case. *Rejected alt:* cutting by token budget per file — it optimises the wrong quantity,
since a short file of over-narrow prescriptions is worse than a long file of un-derivable facts.

**Second new rule: at most one incident narrative per file, and only where the rule inverts an
instinct** the model would otherwise follow (the surviving example: *more sampling makes a biased
gate worse*). A war story makes a rule feel specific and authoritative, which is precisely what stops
an agent asking whether it applies here — the operator's diagnosis, generalized. The history lives
here and in git.

**Operator decisions taken at the question round** (all four as recommended): cut war stories hard;
slim `PIPELINE.md` to one screen (the 4-step table, the end-to-end diagram, the troubleshooting
table — §3–§7 were mirrors); compress `reader-profile` in place with §2–§4 marked math-project-scoped;
and **delete the expected-effort apparatus entirely** across all five sites (plan §0's
wall-clock/compute estimate, the Phase 4 budget table, the implementer's *Respect the commit's effort
budget*, Phase 5's stall heuristic, the `PIPELINE.md` row) — five sites for a number that never bound
anything, on a pipeline where the operator is now present at every dispatch.

**Structural decisions and what was rejected.**

- **`hooks/pre-commit` was kept** after being costed for deletion. Removing the shim looked free (it
  enforces nothing), but `pipeline-marker.sh` never unsets `core.hooksPath`, so during a dispatch git
  would find no `pre-commit` in our directory and silently skip the repo's own. *Rejected alt:*
  unset `core.hooksPath` on disarm — it buys nothing the shim's chaining does not, and adds a failure
  mode when disarm does not fire.
- **`reviewer-core` was kept** at 41 lines with two consumers. The one-consumer test that retired
  `writer-core` does not fire here, and churning the preload wiring for ~30 net lines is not a win.
- **The project-`CLAUDE.md`-wins layering was cut with the boilerplate preamble and then restored**
  as a single clause in each of the seven run-time files. It is an arbitrary precedence convention —
  information, not instruction — and the F1 retrospective had named it as confirmed-working and at
  risk from exactly this edit round, having absorbed two standing overrides with zero friction. This
  is the session's own instance of *put it back and you learn you cut too deep*.

**Two decision records relocated here from `feature-plan`, where they governed nothing** (a planner
does not act differently for knowing what an earlier design rejected):

- *Why the planner writes no code bodies.* An earlier design had it complete them just-in-time in a
  second "Tier 2". A pre-written body turns the implementer into a transcriber that stops
  interrogating whether the code integrates; it drains context twice; and it grounds "final" code in
  infrastructure that does not exist at plan time. The safety net was never the pre-written code — it
  is the pinned test target and discrimination, plus the implementer's verification loop.
  *Rejected alt:* keep planner-written code for load-bearing commits only — "is this commit subtle
  enough?" is a fuzzy per-commit judgement that gets mis-called, and it keeps the whole just-in-time
  machinery alive for a minority of commits.
- *Why measurement splits by question, not by rung.* *Rejected (a):* the planner measures nothing and
  argues falsifiability in prose — the decomposition-changing measurements would then surface during
  the last commit's implementation, as a halt. *Rejected (b):* the planner may pin any number it
  measured, tolerances included, provided the reviewer re-measures — this is what produced frozen
  expressions in shipped tests, and made three passes measure the same quantities. The split keeps
  one pass per question: the planner certifies discrimination, the reviewer re-verifies it, the
  implementer derives the bound.

**Measured after:** ~1,900 lines / ~19,000 words — **43% cut by words**, with the rule count down
much further (the effort apparatus gone, 50 of 53 narratives gone, 6 `Preferences` sections gone, 5
preambles gone, both decision records relocated, the README writer's 8-section skeleton and
emphasis/rhythm rules gone). Per-dispatch system-prompt context: implementer ~4.7k words, plan-review
round ~3.2k, code review ~1.5k. `validate-config.sh` exits 0; the retired-vocabulary sweep is clean.

**Same session, two inboxes reconciled — 9 items, all shipped.** F1's five (suppressed values;
session ids written where they can be seen; the commit-message cap made arithmetically honest at ~20
lines after four consecutive commits overshot ~15; the Phases 1–4 boundary resolved toward *the
planning session also dispatches commit 01*; `Explore` delegation given its cold-start threshold) and
F2's four, which arrived mid-session and had been checked against the rewritten files: the
reserved-namespace rule (a *minted* plausible identifier slips underneath a rule about *suppressed*
values, and §6's certify-the-negative-control requirement manufactures the hazard on purpose); a
**conditional** disclosure objective in `commit-code-reviewer` plus a pre-stage scan in the
implementer, after three occurrences in two features; headless-satisfiable pass conditions; and the
halt contradiction — the implementer carried both *stop and report* and *never return in a waiting
state*, which a subagent with no operator cannot both obey, now re-specified as *make the minimal
change and mark it a contract change in the handoff*.

**What the next run tests.** Whether anything was cut too deep — the retrospector's inbox is the
instrument, and an item asking for a deleted rule back is the signal, not a failure. Two watch items
carried forward from F2: the ~20-line message cap (F2's bodies ran 18/20/25) and the Phases 1–4
boundary resolution, which F2's planner read the other way.

---

# 2026-08-10 — backlog review (same day, after the prune)

An Intake pass over the five remaining [[pipeline-improvement-inbox]] bullets — two `APPROVAL-GATED`,
three deferred, none reviewed since the corpus was cut 43% that morning. **Checking a backlog against
the files is what found the defect; checking it against the reasons on file would have found
nothing.**

- **The prune broke two cross-references and nothing reported it.** `commit-code-reviewer` and
  `feature-readme-writer` were both left pointing at `commit-plan-implementer` → *Generated
  artifacts* — a heading **no revision of any file has ever had**. Both correctly named *Make outputs
  self-explanatory* before `43a35575`; the prune merged that section into *Headless, and safe to
  publish* and rewrote both referrers to a third name. `validate-config.sh` exits 0 either way. Fixed
  by restoring `### Generated artifacts` as its own heading over the figure paragraph, which makes
  both referrers correct **as written** and restores one-section-one-object. *Rejected alt:*
  re-point the two referrers — two files edited instead of one, and three objects (headless,
  disclosure, figures) left under a heading naming one.
- **The generalizable half, now a clause in post-edit check 1: a renamed or merged heading is retired
  vocabulary.** The check already said to sweep for retired vocabulary and still missed this, because
  "vocabulary" reads as terminology and headings are cited *literally* across files. This is the
  cheap half of the gated regression-test item, bought at checklist altitude instead.
- **`Explore` on a cheaper model was already shipped** and the bullet had survived its own
  implementation — both planner skills dispatch `Agent(subagent_type: "Explore", model: "sonnet")`,
  landed with F1's cold-start threshold. *An inbox item is not self-retiring; a shipped item left in
  the queue is indistinguishable from an open one.*
- **Two items closed rather than deferred again.** The **planner context-offload subagent** is dead
  twice over (Phase 6's retrospective moved to `pipeline-retrospector` for independence;
  one-commit-per-session resets coordinator context each session). The **deterministic
  static-analysis pass** (`APPROVAL-GATED`, operator-approved closure) is resolved *against*
  `~/.claude` by its own 2026-08-05 reframe: if the loop is the skill rather than the tool, the loop
  is project-specific (JET.jl, Aqua.jl, a repo's own check target) and belongs in the project's
  `.claude/skills/`, which three existing seams already reach — the project-`CLAUDE.md`-wins clause,
  *"use the `run` skill where available"*, and *"drive the real flow, not just the tests"*. A clause
  in `~/.claude` would be instruction a frontier model derives. **The reason for closing rather than
  re-deferring:** an item that resurfaces each cycle to be re-deferred for the same reason is noise
  in a queue whose whole value is that an untouched item resurfaces.
- **The remaining deferral was re-justified from measurement, not from its own earlier wording.**
  Standalone API-doc artifacts: template §4's contract surface still serves the implementer, and
  context peaks are 198k–260k across four features (20–26% of the window, nothing compacted). Noted
  what would reopen it — a rising implementer peak, not a recollection.
- **Behavioural regression tests stay gated and unimplemented** (operator: "leave gated, untouched"),
  with the two same-day incidents recorded under the item as its strongest evidence to date. A POSIX-sh
  alternative was costed and declined: cross-reference resolution plus a capped list of literal clause
  anchors, no dependency and no API spend, but it proves a rule still *exists* and never that it still
  *bites* — which is the half only this item buys.

---

# 2026-08-11 — the field layer (operator-directed)

**The brief:** *"the ecosystem is not truly field independent — though the documents state it. It's
built for computational projects. We need a way to separate domain knowledge / preferences from the
core ecosystem."*

**The claim was literally false and measurably so.** Seven files opened with *"This file is
project-agnostic"* while the implementer sized gates "to about 3σ", forbade sharing a constant between
"exactness checks (order 1e-10) and statistical gates", and derived bounds "theory-first"; `feature-plan`
§6 *defined* method class as "an exactness check or a statistical gate"; `project-plan` illustrated the
altitude line with "a fitted log-log slope against the analytic rate"; and `reader-profile` — preloaded
into four agents on **every** project — carried a 50-line functional-analysis prerequisite ledger, a UQ
notation table and an open research fork.

**The deeper defect was ownership, not vocabulary.** The same knowledge was maintained in three places
with no owner: the core (as universal rules), `reader-profile` (as one programme's ledger), and each
project's `CLAUDE.md` — `bip-lab` independently re-stating *"experiments are seeded; claims gated on
random draws are gated over an ensemble; rates are reported as fitted slopes against an analytic
target"*. Three copies is the drifting-restatement defect at ecosystem scale.

## The three layers, and the test for which one a rule belongs to

**Core** states what holds in any field · a **domain profile** (`~/.claude/domains/<name>.md`) gives one
field its concrete form · the project's `CLAUDE.md` wins over both. The new `pipeline-maintenance`
editing rule is the generalizable half: *would this rule be wrong in another field?* → a profile;
*would it be wrong in another repo of the same field?* → that repo's `CLAUDE.md`; otherwise core.

**A profile may only give the field-specific form of a standard the core already states** — never a
rung, a workflow step, a handoff field, an agent, or an obligation of its own. Without that bound it
becomes a second ecosystem with no reviewer enforcing it. Cap ~80 lines.

- **`domains/computational-science.md` (72 lines)** — bounds (theory-first, 3σ, the tolerance-regime
  ban, `atol`/`rtol`/SE multiples), the two method classes, reproducibility (seeds; ensemble-gating;
  fitted slopes with their range), gate diagnosis, the figure checklist, Julia, predict-before-you-
  compute, a bound naming its derivation.
- **`domains/uq-operator-learning.md` (84 lines)** — `reader-profile` §2/§3/§4/§7 lifted whole: the
  prerequisite ledger, the notation table and its two collisions, the six known imprecisions, the fork.
- **`reader-profile` 188 → 107 lines**, now only what is true of this reader on *every* project. Two
  things deliberately stayed: **software engineering at professional level** (a reader fact, not a
  field fact) and the diagnostic rule (*supply the missing prerequisite; do not simplify*). Its
  precedence clause now names the four never-yielding rules **by name rather than by section number**,
  since the renumbering would otherwise have broken every citation silently — the 2026-08-10 lesson.

**Declaration: a `## Domain profiles` block in the project's `CLAUDE.md`**, seeded by `project-plan`
step 4 (which also surfaces the choice at the approval gate) and resolved by `feature-plan`'s bare
invocation, which **announces it in its first line** alongside the feature. `none` is written out
explicitly, for the reason `handoff-core` already relies on: an absent block and a genuine nothing are
otherwise identical on arrival.

**Wiring: one extended sentence in each of the seven run-time files** — the project-`CLAUDE.md`-wins
clause they already carried. No new preload. *Why plain files rather than a fourth core or a skill:*
`skills:` is static per agent, so a *conditional* preload does not exist; and four of the seven agents
carry explicit `tools:` lists **without `Skill`**, so `Read` is the only mechanism that reaches all of
them. A plain file also stays inert in unrelated sessions, which a model-invocable skill would not.
*Rejected alt (a):* profiles inside each project — the same math profile would then exist in ~10 repos
and drift, which is the defect being fixed. *Rejected alt (b):* a section of the project plan — the
implementer is barred from reading anything above its own commit plan, so the agent needing the method
rules most could not reach them.

**The failure mode this trades into, stated in the coupling:** a project whose declaration is missing
or misspelled loses its field's standards **silently**, and no script can catch it —
`validate-config.sh` never reads project files. The Phase 1 announcement is the only check, so an edit
that drops it re-opens the hole. The validator gained the one mechanical half it can do: a `WARN` if
`domains/` itself has been renamed or emptied.

## Neutralizations worth not re-litigating

The cut line was drawn against evidence, not taste. The retired `var-pi.github.io` (deleted by the
operator during this session; its rows in [[pipeline-metrics]] and its plan sets under `~/.claude/plans/`
survive) had already planned three non-numeric features on the *skeleton* — intent/target/method
class/discrimination, mutation testing as the negative control, the shared-invariance rule verbatim —
so the skeleton is field-independent and only its vocabulary was not.

**Kept in core, generalized:** *a bound is derived, never observed* and *bounds of different kinds never
share a constant* (the field-neutral residue of theory-first + tolerance regimes) · *a marginal gate is
a question about mechanism before configuration* · the negative control · the shared-invariance rule ·
*every generated artifact carries its own meaning* under the **preserved `### Generated artifacts`
heading**, which two agreements cite literally · `commit-code-reviewer`'s two objectives rewritten as
**Bounds and thresholds are sound** and **Reproducibility is pinned**.

**Moved down:** 3σ, `1e-10`, `atol`/`rtol`, seeds, seed-variation, the plot checklist, `bbox_inches`,
Julia, and **the ecosystem's one surviving incident narrative** (*more sampling makes a biased gate
worse*) — which now sits in the profile, where it bites, and out of the context of every project it
cannot apply to.

**Cold-read test found what the vocabulary sweep did not.** Reading the implementer as if the project
were a CLI tool caught three directives the grep passed over: *"non-square, asymmetric fixtures"*
(array-shaped; now *"asymmetric enough that a swapped axis, order or role cannot hide"*), *"run the
verifying experiment"* (now *the verifying run*), and a surviving `atol`/`rtol`/theory-first sentence
in the file's header rather than its testing section. **A cold read against a foreign field is the
check; a term sweep is not.**

## Measured

Core 13 files: **1817 → 1795 lines**, 19193 → 19167 words — *this relocates, it does not prune*, and
saying otherwise would misread the next row. What actually moved is **per-dispatch context**:

| Dispatch | Before | After, no domain | After, both profiles |
|---|---|---|---|
| implementer (+ `handoff-core` + `reader-profile`) | 496 lines | **412** (−17%) | 568 (+15%) |
| plan-review round (+ `reviewer-core` + `reader-profile`) | 329 lines | **250** (−24%) | 406 (+23%) |

So a field-neutral project pays ~20% less and a declared numeric project pays ~15–23% more, buying a
single-owner statement of its field in place of clauses scattered across five files. **At ~2% of a
dispatch's cost either way, this is not a cost change and must not be argued as one.**

`bip-lab` was migrated in the same session (declaration added; the three clauses now owned by
`computational-science.md` deleted from its conventions) — the only project with a live state block.
`validate-config.sh` exits 0; all three cross-file section citations resolve.

**What the next run tests:** whether the announcement actually makes a missing declaration visible, and
whether a profile stays inside its bound or starts accreting obligations. The inbox is the instrument.

---

# 2026-08-11 — assume competence (operator-directed, third leaning pass)

**The brief:** *"lean towards natural intelligence of modern agents… we don't have to engage in
extreme hand-holding… decrease the size of ecosystem documents by at least a few multiples."*
Delivered as ~20 example passages to generalize from, drawn from `domains/computational-science.md`,
`commit-plan-implementer` and `commit-code-reviewer`.

**The generalization.** Every example was a rule a competent practitioner follows unprompted (seed
the RNG, don't re-implement a library routine, build only what the increment needs, review
independently) or a *definition* of a term the model already owns (`method class`, exactness check vs
statistical gate). **Why the 2026-08-10 cut line let this survive:** *keep information, cut
instruction* removed whole sections but explicitly licensed keeping "the mistake-preventing tail that
makes a rule generalize" — which is what regrew the corpus as tails on rules needing none.

**New standing rule in `pipeline-maintenance` → *Editing discipline*, replacing that licence:**
**assume competence** (cut any rule a competent practitioner follows unprompted; what earns a place is
only harness mechanics that fail silently, coordination conventions, facts about this operator, and
measured findings contradicting a reasonable prior) plus **one rule, one sentence, no rationale** — a
*why* is earned only where the rule **inverts** what the model would otherwise do. That is the same
bar the one-incident-narrative rule already used, now generalized from narratives to rationale tails.

## The finding that matters most: the corpus has a floor, and it is ~1.6×

**Measured: 21,304 → 13,253 words (1.61×), 2,046 → 1,264 lines.** The brief asked for "a few
multiples" and it was not reachable. This is recorded so the next session does not re-attempt it
blindly.

Five successive strategies were tried and measured. *Dropping derivable rules* and *phrase-density
rewriting* each bought 10–15% and then stopped. Three **structural** consolidations — collapsing the
dependency graph to a table, collapsing the map to two columns, pushing duplicated notes to their
owning coupling — bought **48, 15 and 15 words**. That is the evidence: after three passes the
remaining text is not prose around rules, it *is* the rules.

**What the floor consists of, in the two files that resisted hardest** (`feature-plan` 3,090 → 1,963;
`pipeline-maintenance` 3,430 → 2,263): **artifact specification** — the §0–§8 commit-plan template,
the eight brief fields, the state-block schema, the three bundle field sets — and **coordination
convention**: which rung owns what, which path holds which artifact, which phase writes which record.
Neither is derivable, and cutting either does not make an agent leaner, it makes the pipeline
underspecified. `feature-plan` is the coordination spine and has the highest floor of any file.

**What would have to go to reach 3×, none of it taken:** the numbered plan template (leaving the
planner to invent a section set per feature), the state-block field list, the two reviewers' remaining
inverted duties, and `PIPELINE.md`. Each is a named class, and the operator can pick one.

## Operator decisions at the question round

- **Reference layer cut at the same multiple** — `uq-operator-learning`'s **known-imprecisions table
  was dropped** (six corrected errors; recoverable from git) and its ledger compressed to headline
  categories; the notation table survives at ten load-bearing rows, since it fixes which symbol means
  what and nothing else does. 899 → 567.
- **Hard on `pipeline-maintenance`, light on `PIPELINE.md` and `dotfiles-sync`** — the last two cost
  no per-dispatch context.
- **Of `feature-plan` §6/§7's four test-design rules, only the irreversible one survives.** Cut:
  shared-invariance-and-a-check-that-breaks-it, negative-control certification, and the
  systematic-bias-first diagnosis note. Kept: **never write a suppressed or minted real-world value**,
  because a leak in git history cannot be walked back. **The coupling moved with it** — the two
  matching `feature-plan-reviewer` objectives, `commit-code-reviewer`'s "confirm the negative control
  fails for the reason it claims", and the implementer's *Ship a negative control per feature* all
  went in the same pass. *Boundary held:* `project-plan` brief field 3 **Falsifier** and the
  *Falsifiability* reviewer objective stay — a fixed template field at project altitude is not test
  mechanics.

## The structural cut worth keeping

**Both plan reviewers read the agreement they review against, so a restated objective list is
duplication.** `feature-plan-reviewer` (1,116 → 554) and `project-plan-reviewer` (593 → 434) now say
*derive your objective list from the `feature-plan`/`project-plan` skill* and carry only what those
files cannot give them: the priority (set-coordination / altitude is first-class), the **inverted
duties** (fault a plan that *contains* bodies or a drafted message; fault a delta that *names* a
signature), the asymmetry (**marked on none is the finding to hunt**), the whole-set checks (each
plan's "stays unmodified" against every later delta; re-verify every discrimination claim), and
Legibility. `reviewer-core` step 1 — write a justified objective list each round — is the mechanism
that makes deriving safe. *Not applied to `commit-code-reviewer`:* it reads the diff and its bundle,
never the implementer's agreement, so its standing objectives must stay stated.

## Also cut, and verification

Whole sections deleted from `commit-plan-implementer`: *Scope* (build-only-what-is-needed,
never-re-implement), *Code style* (the LaTeX ban — now owned solely by `feature-readme-writer` for
GitHub rendering and by `uq-operator-learning` for commit messages), the TDD paragraph, "tests must
bite", the CI-headline rule. From `commit-code-reviewer`: the *you exist because `/code-review` is
user-triggered* framing (the one line that matters stays in the implementer, which is the agent that
might try to invoke it) and the *Preferences* section. From `computational-science`: theory-first, 3σ,
the tolerance-regime ban, `atol`/`rtol`, the two method-class definitions, seeding, ensemble-gating,
and fitted-slope reporting — the operator's own examples. 635 → 332.

**`validate-config.sh` exits 0; all four literal section citations resolve** (*Write the commit
message*, *Generated artifacts* ×2, *How the plan reads*); the §0–§8, Phase 1–6 and step 0–5 spines
are intact; the retired-vocabulary sweep is clean.

**The cold read against a foreign field earned its place again** — reading the field-neutral files as
if the project were a CLI tool caught four array-shaped directives the term sweep passed over:
*"orientation and transpose, sign and factor-of-2 conventions"*, *"between the noise and the
margin"*, *"a grid size"* (twice), and *"sample sizes"*. All generalized in place.

**This pass does not buy tokens and must not be argued as a cost change** — the implementer's
agreement is ~2% of its own dispatch cost, and cost scales as ~turns^1.56. It buys attention.

**What the next run tests:** whether anything was cut too deep. The retrospector's inbox is the
instrument, and an item asking for a deleted rule back is the signal rather than a failure — the four
test-design rules and the reviewers' derived objective lists are the two places to watch.

---

# 2026-08-11 — state it once (operator-directed, fourth leaning pass)

**The brief:** *"Last pass told me that nothing else can be compressed. There is plenty actually…
be an extremely radical minimalist,"* delivered as ~13 passages from the current files to generalize
from.

**The operator was right, and the reason is the durable output.** Every earlier pass asked *does this
rule belong?* (keep information, cut instruction; assume competence). **None asked how many times a
rule is said inside its own passage.** The "floor" the previous session recorded was the floor of the
strategies tried, not of the corpus — a mistake now corrected in
[[editing-subagent-guideline-files]], with the general form: *do not record a floor as a property of
the corpus.*

## The generalization: four forms of re-encoding

Every one of the 13 passages was a rule stated once correctly and then re-encoded around itself —
an **instance list** after the category the rule already names; a **paraphrase in the rationale
slot**, spending the slot a real *why* would earn; a **second site**, including one the reader
already holds from a preloaded core or the sentence directly above; or the **history behind a
number** (the README cap's eight-feature series; the disjoint-must-fix-lists anecdote). Now a
standing rule in `pipeline-maintenance` → *Editing discipline* — **state it once, at full strength,
and stop** — with the test *would deleting this change what an agent does?*, and the same clause
added to post-edit check 2, which is where it gets applied.

**One exception was registered rather than resolved,** at the operator's decision: the
**must-not-ship / reserved-namespace rule keeps all four sites** (`feature-plan` as owner, its
reviewer, the implementer's pre-stage scan, `commit-code-reviewer`), one sentence each, ~270 → ~110
words. Those four agents cannot read each other's agreements, git history cannot walk the defect
back, and across three incidents in two features **each was caught by a different site than
introduced it**. It is now a row in the dependency graph, labelled the deliberate exception, so a
later pass does not "finish the job" — the generalizable half being that a single-source-of-truth
violation kept on purpose must be recorded as one.

## Measured: 13,253 → 12,485 words (−5.8%), 1,380 → 1,240 lines

**The estimate was wrong by 3× and that is worth recording.** The plan projected ~10,600 (−20%) by
assuming ~20% of each file was prose around rules; it is ~6%. Where the words actually are:
`pipeline-maintenance` is 53% tables (the map's 14 rows, the graph's 19), `feature-plan` is the §0–§8
template plus six phases, `project-plan` the eight brief fields. Per-file yields ran −2% to −11%,
with the largest single win in `PIPELINE.md`'s troubleshooting table, whose *Owner* column had been
re-explaining the dependency graph it points at — the four-forms rule finding a site nobody had
flagged.

**A further multiple requires deleting capabilities, not better editing** — the named classes remain
what the last pass listed (the numbered plan template, the state-block field list, the reviewers'
inverted duties, `PIPELINE.md`), plus `PIPELINE.md`'s Mermaid diagram (~430 words) and
`reader-profile` §4's banned-vocabulary examples. None taken.

**Also decided:** `PIPELINE.md` compressed in place rather than deleted (operator) — it stays the
only whole-shape view, and its verified line was re-dated. Two field-neutrality fixes rode along,
caught by the cold read rather than by any word count: `project-plan`'s altitude example ("a measured
rate checked against the value theory predicts") is now field-neutral, and the retrospector's
inbox-path incident lost its narrative.

**Verified:** `validate-config.sh` exits 0; all four literal section citations resolve
(*Generated artifacts* ×2, *Write the commit message* ×2, *How the plan reads*); the §0–§8, Phase 1–6,
step 0–5 and brief-field-1–8 spines intact; three bundles unchanged; cold read against a CLI-tool
project clean.

**What the next run tests:** unchanged from the previous entry — the retrospector's inbox is the
instrument. Nothing in this pass deleted a rule, so a regression here would show up as ambiguity
rather than as a missing check.

---

# 2026-08-12 — mantra (operator-directed, fifth leaning pass)

**The brief:** *"Prefer the writing style that reads like mantra or haiku: extremely concept dense and
clear at the same time,"* delivered with five passages to generalize from.

**New standing rule in `pipeline-maintenance` → *Editing discipline*: *Mantra, not prose*** —
load-bearing term first, the relation on a dash, no connective scaffolding, and a stop clause:
*density a cold reader has to reconstruct is not density.* Three rules already decided whether a rule
belongs, how many times it is said, and how much rationale it carries; **none said how the surviving
sentence is written.**

## The five passages, and the defect each named

- **An objective derivable from the agreement a reviewer already reads is a second site.**
  `project-plan-reviewer`'s *Falsifiability* checked brief field 3, which it derives — cut, with its
  cold-reader bullet (verbatim in `project-plan`) and *Legibility*'s instance list. **Field 3 is not
  left unenforced:** the reviewer still derives field by field, which is the whole point of the
  2026-08-11 structural cut. Registered as an extension of the second-site form — *…or the agreement
  it reviews against.*
- **A rule followed by the cost of breaking it states the rule twice.** The retrospector's *Generalize,
  never transcribe* is now one line ending *filing nothing is a fine outcome*; its cost blockquote is
  one line keeping *every figure comes from the script* and the ~170×.
- **Name the class, never the surface.** `reader-profile` §1.3 (sourcing), §1.4 (the three-way
  epistemic sort), the diagnostic rule and — at the operator's decision — **all of §4, the no-verdict
  clause**, are gone: *"this kind of instruction makes an agent's life extremely difficult and results
  in little to no positive effect. Negative maybe even."* The generalizable half is a **scope, not a
  ban**: a list the agent must check *its own prose* against taxes every sentence it writes; **a list
  it searches outward for — a reviewer's defect classes — is not this**, and `commit-code-reviewer`
  keeps its standing objectives whole.
- **An absence needs no defense** — the fifth re-encoding form. `handoff-core`'s *token counts are
  deliberately not a field* is gone; the rule survives at its sender (`feature-plan` Phase 6) and its
  reader (the retrospector's objective 1).
- **One gate per decision** — new discipline rule. `dotfiles-sync` step 4 shows what is going out and
  **pushes**, no pause: invoking the skill is the approval. **Scoped to `~/.dotfiles`** — the git guard
  blocking a *dispatched implementer* is a different mechanism, untouched. Its model-name paragraph
  went the same way: **never write a rule about reading this file**, and never restate what the harness
  supplies (the `Co-Authored-By` trailer is in the harness instructions; the heredoc placeholder
  carries it).

## What moved with the reader profile

**`reader-profile` 85 → 44 lines** — intuition-first, terse, software-engineering-at-professional-level,
and the three-row *where to spend words* table. **The never-yielding list is now one rule, cited by
name:** `feature-readme-writer`'s mirror says *where to spend words*, not *four rules*, and the file's
section numbers are gone — a count and a number have nothing to break loudly.

**Nothing was orphaned by the sourcing cut,** checked rather than assumed: the *legitimacy certificate*
row still demands a citation, `computational-science` still demands a theorem name and number, and
`project-plan` → *How the plan reads* still demands an external claim be labelled.

**The cold read against a foreign field earned its place for the third pass running** — it caught
`reader-profile`'s *"the picture, then the theorem"*, field-shaped prose preloaded into four agents on
**every** project, which the field-layer split and two leaning passes had walked past.

## Measured: 12,466 → 11,745 words (−5.8%), 1,244 → 1,185 lines

**The projection missed by 3×, the same miss as the previous pass, and the cause is now known.**
Planned −15%. The named deletions delivered ~700 words; **the style pass over the rest delivered almost
nothing** — `commit-plan-implementer` rewritten whole for **−0.8%**, `feature-readme-writer` −0.5%,
`feature-plan` −1.6%, `PIPELINE.md` 0%. The sampling error is the durable lesson, now in
[[editing-subagent-guideline-files]]: **both sampled files were ones already chosen for their
deletions.** Sample a file you have *not* chosen.

Two independent methods now agree the prose floor is real, at ~1.06× per pass. `pipeline-maintenance`
**grew** by 144 words — it holds the rules — which is the shape to expect of any future pass.

**Verified:** `validate-config.sh` exits 0; all three cited headings resolve (*Generated artifacts*,
*Write the commit message*, *How the plan reads*); §0–§8, Phase 1–6, step 0–5 and brief-field-1–8
spines intact; three bundles unchanged; retired-vocabulary sweep clean.

**What the next run tests:** whether `reader-profile` still calibrates anything with §4 gone. It is
preloaded into four agents on every project, and the signal would be a shipped artifact grading its
own content — the retrospector's inbox is the instrument.

---

# 2026-08-12 — is the rule still live? (operator-directed, sixth leaning pass)

**The brief:** *"Reassess whether these are really needed. As always, generalise as well"* — five
passages, four from `commit-plan-implementer`, one from `feature-plan`.

**The generalization, and why no earlier pass could have found it.** Three of the five trace to one
era: the 2026-07-24 stall/re-run tune-up and the 2026-07-28 *never return in a waiting state* item,
written against Opus-4.8 behaviour and against a **symptom whose cause was fixed on 2026-08-05**
(`run_in_background: false`). That entry kept the recovery machinery, reasoning it "costs little";
two features then ran with all seven dispatches in the foreground. **New standing rule in
`pipeline-maintenance` → *Editing discipline*: *A rule outlives its failure — delete it once the
cause is fixed*, with *kept because it costs little* named as how a corpus regrows.** The four
existing rules ask whether a rule belongs (*assume competence*), how often it is said (*state it
once*), how it is written (*mantra*) and where gates go; **none asks whether its failure still
exists.**

## The five verdicts

- **Passage 1 (*one synchronous gated run*) cut, three dead halves.** *"Redirected to a log"* was the
  orphaned end of a broken gate (below); *"foreground"* restated the Bash default; and the re-run ban
  was a second site of ***Stop when the work converges*** in the same file. **It survives at exactly
  one site — `feature-plan` Phase 5 beat 2 — where it is a coordination decision (single verification
  owner, model (a), 2026-07-24) rather than a behavioural nudge.** The altitude story is the durable
  half: *don't redo your own work* is derivable, *don't re-run as a second ground truth* is a pipeline
  decision.
- **Passage 4 (*never return in a waiting state*) cut whole — three re-encoding forms in one
  passage.** `run_in_background: false` is in the **preloaded `handoff-core`**; *re-dispatch once*
  duplicated ***At most one re-dispatch*** 27 lines up; *proceed and record as not performed* is
  `handoff-core`'s *Receiver: name the gap, then proceed* plus *Hand back*'s deviation field; and the
  headline restated the sentence directly above it (*"You have no interactive operator"*).
- **Passage 2 kept at −55%** — *"diagnose which you have before touching a number"* was
  *mechanism before configuration* restated. Now `**Marginal gate — mechanism before configuration.**
  Never widen a bound to reach green.` The phrase is preserved **verbatim** because
  `domains/computational-science.md` cites it by name as *the field's form of* it.
- **Passage 3 kept**, both halves live: the `run` skill is one of the three seams the 2026-08-10
  static-analysis closure rests on, and *display-less, non-interactive, sandboxed* governs a **second
  act** no plan covers — hence a new graph row, **Headless constraint** (`feature-plan` §7 writes
  conditions it can satisfy; the implementer's own scripts and artifacts must also run without a
  display), so a collapsing pass does not take one for a duplicate of the other.
- **Passage 5 (must-not-ship) keeps all four sites** — operator decision, evidence unchanged. Trimmed
  6 words at the owner: the instance list *"present, its length, a parse succeeds"* after the category
  *a property*, which the rule already names, and which the other three sites already omitted.

## The break the coupling check found

**`feature-plan` Phase 5 gated on `` `ALL GATES: PASS` `` in the returned log; the implementer's half
was deleted on 2026-08-11 in `eaa8bf01`, the assume-competence pass.** The check survived its
producer for a full session, and `validate-config.sh` exits 0 either way. **Operator's call: drop the
marker from Phase 5** — gate on the handoff showing the commit landed and its pass conditions holding
— rather than restore the emitter, since a competent implementer's handback carries the same evidence
without a second convention to keep in sync. Post-edit check 1 generalized from *a heading you
renamed* to **a heading or literal token**: other files cite sections *and match strings* verbatim.
This is the same class as the 2026-08-10 *Generated artifacts* break, one layer down, and it is the
second time a leaning pass has cut one end of a cross-file literal.

## Measured: the corpus is net zero, and that is the point

**12,483 → 12,483 words** (1,286 → 1,282 lines). Run-time files **−82**; `pipeline-maintenance`
**+82**, which is the shape every pass now predicts of the file that holds the rules. What actually
moved is per-dispatch context on the most-preloaded agent: **`commit-plan-implementer` 871 → 799
words, −8.3%** — the largest single-file drop since the assume-competence pass, from deleting two
passages rather than rewriting any.

**The corpus-wide sweep found exactly one dead-machinery instance** (passage 4). Every other
recovery clause is live — the preload-failure fallbacks in both cores, `none`-vs-gap in the handoff
protocol, the README path fallback. **So this rule prevents regrowth far more than it buys
deletions**, and a future pass should expect ~one instance, not a class.

**Verified:** `validate-config.sh` exits 0; all four literal citations resolve (*Generated artifacts*
×2, *Write the commit message* ×2, *How the plan reads*, and `computational-science`'s *mechanism
before configuration*); §0–§8, Phase 1–6, step 0–5 and brief-field-1–8 spines intact; three bundles
unchanged; retired-vocabulary sweep clean; cold read against a CLI-tool project clean on both
rewritten bullets.

**What the next run tests:** whether anything in passage 4 is missed — a child dispatched
backgrounded now has only `handoff-core` behind it, and a stalled dispatch has only *Hand back*. The
retrospector's inbox is the instrument, and an item asking for it back is the signal.

---

# 2026-08-20 — the first run on the compacted ecosystem

**No inbox items and no operator brief.** The trigger was that all four leaning passes (08-10 prune →
08-12 *is the rule still live?*) closed with *"what the next run tests"*, and that run was **live**:
`bip-lab` F1, 3 of 6 commits landed, the first feature to execute on the compacted files. A session
with an empty inbox reads the run instead.

**Measured mid-run** (`pipeline-stats.py`, 3 sessions, 77.0M tokens, $94.43): **108 turns/commit**
against F2's 144, **1.0 reviews/commit**, peaks 151k–197k implementer / 266k main. Not attributable
to the compaction — an agreement is ~2% of its dispatch's cost and diff weight dominates — and the
row itself is the retrospector's at close. **This feature straddles two ecosystem versions**: commits
1–3 ran the 08-12 files, 4–6 run these.

**Confirmed working, and named so the next pass does not cut them:** the resumed review loop (2
rounds, 10 must-fixes integrated); `commit-code-reviewer` finding a real test hole in all three
commits; the `model: sonnet` discrimination alive — 5 Opus / 1 Sonnet on a six-plan set, with plan 05
*declining* the downgrade in writing, which is the marked-on-none objective doing its job; the
pre-stage must-not-ship scan; `validate-config.sh` and the Phase 1 announcement in all three sessions.

## Five defects, and what each fix rests on

- **§8 under-listed the wiring file in 3 of 3 commits** — the line registering a new test file or a
  new dependency, which no plan pinned. Cost was never a wrong commit: it was an implementer
  reporting a deviation, a reviewer confirming it, and the coordinator writing a **workaround
  paragraph into the project's own `CLAUDE.md`** — a pipeline rule living at project altitude. §8 now
  scopes itself to *the files carrying the delta*, with the wiring the implementer's and **not a
  deviation**; the implementer's *staged **exactly** as §8 names* lost the word that manufactured the
  conflict. One owner, since the implementer reads §8 directly. *Rejected alt:* state the exception
  at the implementer — it would leave §8 still claiming completeness, and the reviewer with two
  readings.
- **The foreground rule reached two of four dispatch sites.** `feature-plan-reviewer` was dispatched
  `run_in_background: true`. `handoff-core` owns the rule, a skill cannot preload it, and the
  registered workaround — *the planner needs its own copy* — had been satisfied **per phase**, at
  Phase 1 and Phase 5, leaving Phase 3 and Phase 6 (and `project-plan` steps 3 and 5) silent. Both
  skills now carry it **once in the preamble**, covering every dispatch; the two per-phase repeats are
  gone. *The generalizable half, now in the coupling row:* a copy stated per-phase covers the phases
  it is written in and no others.
- **Phase 4 did not finish, and the invocation branch pointed at the hazard.** The planning session
  persisted six reviewed plans and stopped — no state block opened, no commit 01 dispatched. The next
  session met *record-says-unstarted + plans-on-disk*, which step 3 routed to *"plan the next brief"*:
  one turn from silently replacing the reviewed set the landed commits would be built against. It was
  caught only because the agent checked file mtimes before trusting the block. Two fixes: **a plan set
  on disk now outranks the block's status**, and **Phase 4 states the boundary where the planner
  actually stops.**
- **Operator decision: the planning session no longer dispatches commit 01.** Two consecutive
  planners stopped at Phase 4 unprompted, the second with the rule stated explicitly one phase further
  on. Deleted rather than relocated — it buys one session's cold start (~$4–6 of coordinator), the
  planning session already carries the series' highest context peak (266k), and a rule three planners
  have now read the same way is describing the workflow rather than governing it. `PIPELINE.md` row 2
  moved with it. *Not a change to one-commit-per-session:* the operator invoked `/feature-plan` twice
  in one terminal session for commits 2 and 3 and the coordinator cost **$3.66 for two commits**
  against $6.92 for one in a fresh session — the 2026-08-05 rationale is about unattended chains, and
  re-invoking is not one.
- **A dangling `reader-profile §6` citation in live artifacts**, from the 08-12 pass that deleted that
  file's section numbers so citations could not break silently. Two agents flagged it in two commits;
  the unlanded commit-6 README plan carried it. **Third instance of a leaning pass cutting one end of
  a cross-file literal, and the first outside `~/.claude/{skills,agents,hooks,domains}`** — post-edit
  check 1's sweep could not have seen it. The check now names the two places citations escape to:
  `~/.claude/plans/` and the `CLAUDE.md` of any project with a live state block. The persisted plan
  was corrected; `bip-lab/CLAUDE.md:239` was **left alone and reported** — it sits below the
  human-owned line, and the rule it names is now that project's own.
- **The commit-message cap was not biting** — 6 of 6 commits over ~20 lines across two features and
  two models (F1: 21/25/29, rising), having already been raised 15→20 for the same reason.
  **Operator's call: ~30.** The cap is kept rather than dropped because a bound survives an eager
  agent where an encouragement does not; it is raised rather than enforced because the body's four
  required elements *are* the length, and the operator is the only reader.

**Measured: 11,745 → 11,889 words (+1.2%), 1,181 → 1,188 lines** — the first pass since 2026-08-10
to add rather than cut, because none of the five defects was over-specification. `feature-plan` +31,
`project-plan` +28, `PIPELINE.md` +20, the implementer **−1**, and `pipeline-maintenance` +66, which
is the shape every pass now predicts of the file holding the rules.

**Verified:** `validate-config.sh` exits 0; the four literal citations resolve; §0–§8, Phase 1–6,
step 0–5 and brief-field-1–8 spines intact; three bundles unchanged; cold read against a CLI-tool
project clean. **The cold read paid again at check 2**, catching two re-encodings this pass had just
introduced — the disk hazard restated one section below its owner, and Phase 5 beat 1's paraphrase of
the new preamble rule.

**What the next run tests:** whether §8's new scope ends the deviation reports at commit 4, which
hits the same case by construction, and whether a preamble-level dispatch rule reaches Phase 3.

---

# 2026-08-22 — the `bip-lab F1` inbox, reconciled

**No operator brief.** Intake was the retrospector's six-item block filed at F1's close; five
ordinary defects plus one flagged `n=1`. The pass **adds** — 11,889 → 12,106 words (+1.8%), 1,188 →
1,196 lines — because none of the six was over-specification, the same shape as 2026-08-20.

**Three of the six were fixed differently than proposed, and that is the durable half.** A
retrospector names the site where the defect appeared; the maintainer's job is the site where the
*rule* belongs.

## The six verdicts

- **An open decision needs a home in the record.** Precedence (`CLAUDE.md` over a domain profile)
  settles which rule to follow, never whether the higher layer is right; commit 3's `@info`
  diagnostics reached the operator only in the **next session**, carried by coordinator recall.
  Two sites: the implementer's *Hand back* gains **an open decision** as a field, and the state
  block's shape (`feature-plan` Phase 4) gains **any open decision a dispatch handed back** — its
  **fifth** load-bearing field. Nothing at Phase 5: the shape is nine lines up and a field name is
  the whole instruction. *Rejected:* an explicit `none`, which the block has no gap-checking reader
  to earn — the defect was an absent **field**, not an unwritten one; and a slot in the
  retrospective bundle, since a decision that reached the operator is already an intervention.
  **`project-plan` step 4's re-enumeration of the block's fields was deleted** rather than extended
  (*"commit count, plan-set path and session ids are its to add"* → *"every other field is
  `feature-plan`'s to add"*) — the copy would have gone stale the moment the list moved, which is
  the cross-file-literal class one step before it breaks.
- **A pass condition states a property, never an enumerated source.** Plan 06's condition
  whitelisted *where* four quoted constants had to come from, written before the evidence existed;
  two legitimate sources then read as a failure. One clause in `feature-plan` §7. The implementer's
  half cost **zero words**: *"contradict its own contract surface"* → *"contradict what the plan
  itself establishes"*, *"implement the contract"* → *"implement the intent"* — the same failure one
  rung out, covered by widening rather than by a second clause. No reviewer-side edit; it derives.
- **The README increment's verification is the dispatcher's.** Commit 6 ran **zero**
  `commit-code-reviewer` dispatches (docs-only, no diff), and both README defects were caught by an
  act no file required. One sentence in the implementer's *The README increment*. **§0's `model:
  sonnet` licence deliberately did not move** though the retrospector flagged the coupling — the
  [[pipeline-metrics]] row contradicts it: the Sonnet implementer on that very commit found the run's
  only marginal gate itself and corrected an Opus child on a factual point.
- **A dispatch is one-shot — and the proposed fix was two sites for one pair.** The retrospector
  asked for `commit-code-reviewer`'s *"one-shot per commit"* mirrored onto `feature-readme-writer`
  **and** the implementer's delegation clause. The mechanic is a harness fact that fails silently,
  and `handoff-core` already owns its sibling (`run_in_background: false`, same consequence: the
  result lands in front of whoever is listening) — so **one Sender bullet there**, reaching the
  implementer by preload and covering every future delegation. The planner skills need no copy:
  they resume a **returned** reviewer between rounds, the licensed case, which a bare "one-shot"
  line would muddy. Registered as **Dispatch shape (c)**.
- **Cap the defect, not the legitimate form** — new standing rule in `pipeline-maintenance` →
  *Editing discipline*, extending *a rule stated as a cap survives an eager agent*. The trigger:
  `feature-readme-writer`'s *"antithesis tic — at most one per document"* paired a **count** with a
  **semantic tell**, and the shipped README's ~10 negation contrasts **all pass the tell**, so
  nothing downstream can tell obedience from override. Resolution: the test governs and the cap
  moves onto the defect — **`Antithesis (X, not Y) — only where Y was genuinely on the table.`**
  Zero of the defective form, unlimited of the legitimate one, so cap-ness survives.
  **A sweep found the identical defect at a second site the retrospector did not name** —
  `project-plan` → *How the plan reads*, the `X, not Y` cadence capped at one per plan — fixed the
  same way; fixing only the reported site would have transcribed the example. Two other cap+tell
  pairs (one narrative per file; one runnable block) were checked and **left**: their legitimate
  population is ~zero, so cap and test agree.
- **`Co-Authored-By` presence in `hooks/commit-msg`** (operator: ship it). `6a01c55` is the only
  commit in the repository without its trailer, and the requirement lives in the **harness's own
  system prompt** — a live rule with no owner in this ecosystem, the cross-file-citation class one
  layer further out. Matches `^Co-Authored-By:`, the field name only, so a model-name change is
  harmless. **This does not reopen the hook's refusal to measure quality** — presence is not a
  proxy — and both the hook's header and the implementer's *Commit conventions* now say it measures
  **length and the attribution trailer**, that second clause being a relic the change would
  otherwise have left behind.

## What the change did not touch

Named so a later pass does not cut them: the **~30-line message cap**, now calibrated over two
features (19/23/27 under the old cap, 29/31/18 under this one, the single overrun being the largest
commit); **Phase 5's *resume that same session***, whose first live exercise recovered commit 6 at no
cost; **§0's `model: sonnet`**; the **2026-08-20 deletion** of "the planning session also dispatches
commit 01", which produced the series' lowest planning share (19%); and `run_in_background: false`
on all fourteen dispatches.

**Verified:** `validate-config.sh` exits 0; all four literal citations resolve (*Generated artifacts*
×2, *Write the commit message* ×2, *How the plan reads*, *mechanism before configuration*); §0–§8,
Phase 1–6, step 0–5 and brief-field-1–8 spines intact; three bundles unchanged; retired-vocabulary
sweep clean across `{skills,agents,hooks,domains}`, `~/.claude/plans/` and `bip-lab/CLAUDE.md`; the
hook exercised on all six branches (armed/inert × trailer-present/absent/short-subject). One
out-of-tree hit was **reported and left**: `plans/look-into-docs-plan-ideas-md-for-ethereal-brook.md`
records the 2026-08-07 project-plan session applying the old cap — history, not a live citation, and
its own reasoning already anticipated the new rule.

**What the next run tests:** whether the state block's fifth field is actually written when a
dispatch hands one back — the one field with no downstream reader forcing it — and whether the
`handoff-core` one-shot bullet reaches the implementer where two per-agent copies would have. The
inbox is the instrument.
