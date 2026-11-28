---
name: pipeline-improvement-inbox
description: "Rolling queue of pipeline-improvement suggestions — filed by feature-close retrospectives and by the operator, consumed and reconciled by pipeline-maintenance; APPROVAL-GATED items need explicit operator sign-off before implementation"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b5754bbc-be30-4fea-9c42-56f330fe29c6
  modified: 2026-08-12T12:17:41.971Z
---

Rolling inbox of **pipeline-improvement suggestions**. The `pipeline-retrospector` subagent files
here at feature close (dispatched by `feature-plan` Phase 6); `pipeline-maintenance` reads this
first (its Intake step), acts on what it can, then **reconciles** — deletes an implemented item,
annotates a deferred one with the reason. An item left here resurfaces next cycle; that is
intentional. Part of the improvement-inbox loop recorded in [[pipeline-ecosystem]].

**How to file (retrospector):** add a bullet under a `## <date> — <feature-slug>` heading carrying
the **principle** (the rule that should exist, generalized — never the incident verbatim), the
**evidence** (one line), the **owning file**, and the **cost of not doing it**. Filing nothing is a
fine outcome. Link related design records with [[…]].

**How to file (operator):** the operator files here too, in the same shape. An operator-filed item
may carry the marker **`APPROVAL-GATED`**, which means: *research it, cost it, bring a concrete
proposal — but do not implement it until the operator says so in that session.* This is stronger
than the ordinary Intake license to "act on what you can", and it exists because an idea the
operator wants to think about is not the same as one they have decided on. Treat an
`APPROVAL-GATED` item as a standing agenda entry, not a backlog ticket: it stays in the file,
un-reconciled, until it is explicitly approved and shipped, or explicitly dropped.

**How to reconcile (maintainer):** on implementing a suggestion, delete its bullet (the change is
now recorded in [[pipeline-ecosystem]]); on deferring, append `— deferred: <reason>`.
Never reconcile an `APPROVAL-GATED` item on your own judgement — neither by shipping it nor by
deferring it away.

**Where this file lives, and why that matters.** The one path is
`~/.claude/projects/-Users-var-pi--claude/memory/pipeline-improvement-inbox.md`. A retrospector once
filed six well-argued items to the *project's* memory directory instead; `/pipeline-maintenance`
does not read there, and they sat unseen until someone went looking. **Never create a second inbox** —
if you cannot resolve the path from your bundle, use the absolute one above.

---

*(The `2026-07-26 — 06-fbm` retrospector block was fully reconciled on 2026-07-28 — all five items
shipped. The altitude one shipped in a **narrower** form than proposed: the planner may measure only
to certify that a gate *discriminates* and writes the **margin**, never a tolerance; every
`atol`/`rtol`/SE-multiple/sample size is the implementer's. See [[pipeline-ecosystem]].)*

*(The `2026-08-04 — 07-sde-bridge` block — six items, filed to the wrong directory — was merged here
and **fully reconciled on 2026-08-05**: all six shipped. Two were folded into larger changes rather
than shipped as written — the marginal-gate protocol became part of the Opus-5 implementer
re-baseline, and the late/misrouted-result item was split across the implementer's merge half and
`feature-plan` Phase 5's relay half. See [[pipeline-ecosystem]].)*

---

*(The `2026-08-10 — var-pi.github.io F1` block — five items — was **fully reconciled on 2026-08-10**
during the radical-prune maintenance session; all five shipped. The suppressed-value rule landed on
both ends (`feature-plan` §6 + the reviewer's objective list); the session-id field is now written at
Phase 4 and appended at every Phase 5 dispatch, and `handoff-core` no longer claims the list is
unrecoverable; the commit-message cap was made arithmetically honest by dropping the four-section
prescription and raising the cap to ~20 lines; the session boundary now says explicitly that the
planning session also dispatches commit 01; and `Explore` delegation carries its cold-start
threshold. See [[pipeline-ecosystem]]. **Two of those five were reversed on 2026-08-20** — the cap is
~30 and the planning session no longer dispatches commit 01; the entry below says why.)*

*(Also confirmed working on that run and deliberately preserved through the prune: the `model:
sonnet` discrimination, `run_in_background: false`, `commit-code-reviewer`'s licence to read
neighbouring code for a convention, `validate-config.sh` at Phase 1, and the project-`CLAUDE.md`-wins
layering — the last of which was cut with the boilerplate preamble and **restored as a one-line
clause in each of the seven run-time files** once the retrospector's warning was re-read.)*

---

*(The `2026-08-10 — var-pi.github.io F2` block — four items — was **fully reconciled on 2026-08-10**,
in the same radical-prune session, minutes after the retrospector filed it. All four shipped. The
reserved-namespace rule widened `feature-plan`'s *Never write a real-world value…* heading in place
(minted values, not only suppressed ones) with the matching reviewer objective; the project-declared
must-not-ship class became a **conditional** standing objective in `commit-code-reviewer` plus a
pre-stage scan in the implementer's *Headless, and safe to publish*; headless-satisfiable pass
conditions landed in `feature-plan` §7, the implementer's headless clause and a reviewer objective;
and the halt contradiction was re-specified — the implementer now makes the minimal change and marks
it a contract change in its handoff, since a subagent has no operator to halt to, with the planner-side
half (a "stays unmodified" condition must agree with the plan's own contract surface) and a reviewer
objective that checks it across the set. See [[pipeline-ecosystem]].)*

*(Confirmed working on that run and preserved: `run_in_background: false` on all seven dispatches,
`commit-code-reviewer`'s per-objective "say clean when it is clean", the resumed `feature-plan-reviewer`
catching five set-level defects, `model: sonnet` replicating F1's saving, and the
project-`CLAUDE.md`-wins layering. The ~20-line message cap is calibrated but unsettled — F2's bodies
ran 18/20/25 — and the Phases 1–4 boundary resolution is untested, since F2's planner read it the
other way. Both are watch items for the next run, not actions.)*

*(**Both watch items were exercised by `bip-lab` F1 and both moved, 2026-08-20.** The cap failed
again — 21/25/29, six commits over ~20 across two features — and is now ~30. The boundary was read
the same way a second time, on a bare invocation with no operator interruption, and the rule was
**deleted**: planning ends the session. Three further defects the same run exposed are recorded in
[[pipeline-ecosystem]], with what stayed working named beside them.)*

---

## 2026-07-25 — operator-filed candidates from the FOSS survey (**all `APPROVAL-GATED`**)

Five ideas surfaced by a survey of open-source agentic-development tooling, filed by the operator
to discuss later. **None may be implemented without explicit approval in the session that does it.**
Sourced from external tools, so each needs its own design pass before it fits the ecosystem's
altitude contract — adopting a foreign shape wholesale is how a pipeline acquires machinery that
serves someone else's workflow.

*(**2026-07-28:** the operator worked all five. Three shipped and are deleted — the
feature-altitude brownfield delta, the fixed handoff artifacts as the new `handoff-core`, and the
config schema check as `skills/pipeline-maintenance/validate-config.sh`; see
[[pipeline-ecosystem]]. The other two were **deferred by the operator**, not by a
maintainer's judgement, and kept their marker: they are still gated if reopened.)*

*(**2026-08-10:** the operator worked both again. The deterministic static-analysis pass was
**closed** — the 2026-08-05 reframe resolves it against `~/.claude` rather than for it; see
[[pipeline-ecosystem]]. The one below stays gated, unimplemented, with new evidence recorded under
it.)*

- **Behavioural regression tests for the agent definitions** (`APPROVAL-GATED`)
  **— deferred 2026-07-28 by the operator ("pass on this for now").** It is a project rather than
  an edit: a new dependency, real API spend per CI run, and LLM variance that tends to get
  assertions loosened until they assert nothing. Reopen scoped to three or four cap-shaped
  assertions, or not at all. *Principle:* the
  schema check now shipped catches a dead key; nothing catches a **live rule that stopped biting** — a
  core compacted until a discipline is merely implied, a cap softened into an encouragement. Pinning
  a handful of observable behaviours (the reviewer emits its justified objective list before any
  finding; the implementer never attempts a push; a docs-only commit is exempted) as assertions run
  in CI would fail the edit rather than the next feature run. *Evidence:* `promptfoo` — open source,
  has a Claude Agent SDK provider and can forward subagent transcripts to assert against what a
  subagent actually did. *Owning file:* a new test suite beside the ecosystem files; conceptually
  owned by `skills/pipeline-maintenance/SKILL.md`, since it is what makes the editing discipline
  enforceable rather than aspirational. *Cost of not doing it:* every rule in ~2,500 lines is
  enforced only by the next agent reading it carefully, and a dulled rule is invisible until a run
  goes wrong. Note the known trap first: a rule stated as a **cap** is assertable, one stated as an
  encouragement is not — so this would also be a forcing function on how rules are written.
  **Evidence added 2026-08-10 — status unchanged, operator chose "leave gated, untouched".** The
  failure mode this item names was realized twice in one day, by the radical prune itself: the
  project-`CLAUDE.md`-wins layering was cut and restored only because someone re-read the F1
  retrospective, and the prune rewrote two cross-references to
  `commit-plan-implementer` → *Generated artifacts*, **a heading no revision has ever had**, while
  `validate-config.sh` kept exiting 0. A cheap mechanical alternative was costed and declined
  (cross-reference resolution plus a capped list of literal clause anchors, in POSIX sh); the
  checklist-level half of it shipped instead, as a clause in post-edit check 1. What stays unbought
  is the half only this item buys: whether a rule that still *exists* still *bites*.
  **Evidence added 2026-08-11 — no decision taken, still gated.** The field-layer split
  ([[pipeline-ecosystem]]) enlarged exactly the surface this item covers: a project's field standards
  now arrive through a `## Domain profiles` declaration in its own `CLAUDE.md`, which **no script can
  check** — `validate-config.sh` never reads project files — so a missing or misspelled declaration
  silently drops a whole layer of rules, and only `feature-plan`'s Phase 1 announcement surfaces it.
  Two of this item's three suggested assertions would cover it directly (*the planner announces the
  resolved profiles before planning*; *a plan for a project declaring `computational-science` states a
  method class from it*). Also worth recording as method: the split's mis-cuts were caught by a **cold
  read against a foreign field**, not by the term sweep — which is the manual version of what this
  item would automate.
  **Evidence added 2026-08-11 (second session) — no decision taken, still gated.** The
  assume-competence pass ([[pipeline-ecosystem]]) is the largest single deletion of *live rules* the
  ecosystem has taken: four test-design rules retired from `feature-plan` §6/§7 with their three
  mirrors, both plan reviewers' objective lists replaced by *derive them from the agreement you
  review against*, and whole sections cut from the implementer and the code reviewer. Every one of
  those is a rule that used to bite and now depends on a frontier model doing the right thing
  unprompted — which is exactly the proposition this item exists to measure and nothing else can.
  The two watch items the next run should exercise are named in the design record. Cheap assertions
  that would cover this directly: *a plan for a project declaring `computational-science` states a
  method class from it*; *the reviewer emits its justified objective list before any finding* (now
  load-bearing, since the list is derived rather than transcribed).
  **Evidence added 2026-08-11 (fourth pass) — no decision taken, still gated.** The *state it once*
  pass deleted no rule, so it adds no new exposure — but it nearly did: the four-site must-not-ship
  rule was one operator decision away from being collapsed into three pointers, and **nothing
  mechanical could have flagged that** (all four sites would still have "existed"; only their bite
  would have gone). That collision is now a registered exception in the dependency graph, which is
  the checklist-altitude half again. The unbought half stays the same one.
  **Evidence added 2026-08-12 — no decision taken, still gated.** The *mantra* pass
  ([[pipeline-ecosystem]]) deleted `reader-profile`'s §1.3 (sourcing), §1.4 (epistemic sort) and all
  of §4 (the no-verdict clause), plus `project-plan-reviewer`'s *Falsifiability* objective — live
  rules on a file preloaded into four agents on **every** project. Nothing mechanical can tell whether
  a shipped artifact stops grading its own content, and the whole no-verdict apparatus was assertable
  in exactly this item's shape (*a README/commit message contains no evaluative adjective about its own
  result*). Also: the pass's own claim that the reviewers' derived objective lists still cover field 3
  is **unmeasured** — it is the same "does a rule still bite?" question, one rung up.
  **Evidence added 2026-08-12 (second session) — no decision taken, still gated. The most mechanical
  evidence so far, because it is this item's mirror image.** The *is the rule still live?* pass found
  `feature-plan` Phase 5 gating on `` `ALL GATES: PASS` `` in the implementer's returned log — a
  marker the implementer stopped being told to emit on 2026-08-11 in `eaa8bf01`. Not a rule that
  stopped biting but **a check with nothing satisfying it**, live for a full session, `validate-config.sh`
  exiting 0 throughout. Second cross-file literal a leaning pass has cut one end of (after the
  `Generated artifacts` heading), and the checklist half was again bought cheap — post-edit check 1
  now reads *a heading or literal token*. **What stays unbought is unchanged:** an assertion in this
  item's own shape (*the coordinator's gate is satisfiable by what the implementer actually returns*)
  is the only thing that would have failed the **edit** rather than the next run. The same pass also
  deleted a live rule outright — *never return in a waiting state*, whose only remaining cover is
  `handoff-core`.
  **Evidence added 2026-08-20 — no decision taken, still gated. First instance the checklist half
  could not have bought.** The 08-12 mantra pass deleted `reader-profile`'s section numbers *so that
  citations could not break silently*; two live artifacts still cite `reader-profile §6`, and both
  are **outside `~/.claude`** — a project's `CLAUDE.md` and a persisted plan for an unlanded commit.
  Two agents spent a paragraph each on it, in two commits. Third cross-file-literal break in three
  passes, and the first that no sweep of `{skills,agents,hooks,domains}` could reach; the checklist
  was widened again (post-edit check 1 now names `~/.claude/plans/` and live project `CLAUDE.md`s),
  which is the cheap half for the third time. **The unbought half is unchanged and now has a second
  shape:** an assertion that *every cross-file citation resolves against the file it names* is
  mechanical, but *the reviewer's dispatch runs in the foreground* — the defect this run actually
  hit, where a rule existed, was correct, and simply did not cover the site — is only assertable in
  this item's own shape.
  **Evidence added 2026-08-22 — no decision taken, still gated (operator: "leave gated, record
  evidence"). The first entry that moves a rule *into* this item's reach.** The `bip-lab F1`
  reconciliation found `feature-readme-writer`'s antithesis rule stated as a **count and a semantic
  tell at once** — ~10 constructions shipped, every one passing the tell, so obedience and override
  were indistinguishable downstream. The fix recasts the count onto the **defect** (zero where Y was
  never on the table), which is exactly this item's own note that *a rule stated as a cap is
  assertable, one stated as a tell is not* — so the pass acted as the forcing function on rule-writing
  that this item predicts it would be, without buying the assertions. A **second cap+tell pair was
  found by sweep** in `project-plan`, unreported by the retrospector: the class is corpus-wide, and a
  mechanical check for *a rule carrying both a number and a judgement* is cheap and would have found
  both. **The unbought half is unchanged**, and this run adds one more instance of its shape: the
  state block's new fifth field (an open decision handed back) is the **only** state-block field with
  no downstream reader forcing it to be written, so nothing but an assertion in this item's shape
  could tell whether it is being written at all.

---

## 2026-07-24 — deferred candidates (evaluated during the 05-bm-scaling-limit tune-up)

*(Reviewed 2026-08-10 against the files and [[pipeline-metrics]]. One was found already shipped and
one closed; both are deleted. The survivor's reason was re-derived from the measurements rather than
copied forward — a deferral re-justified from its own earlier wording is not a review.)*

- Standalone **API-doc artifacts** so an agent needn't scan whole implementation files — **deferred:**
  the plan's pinned **contract surface** (`feature-plan` template §4) already serves the implementer,
  and the metric that would justify it — a **rising** implementer peak — has moved the other way.
  Re-checked 2026-08-20 against `bip-lab` F1's three dispatches: **151k, 168k, 197k**, against
  198k–260k across the four earlier features. Build only if that trend reverses.

---

*(The `2026-08-21 — bip-lab F1` block — six items — was **fully reconciled on 2026-08-22**; all six
shipped. **Three landed at a different site than proposed**, which is the reusable half: the
one-shot-delegation rule went into `handoff-core` as a Sender bullet rather than being mirrored onto
two agents, since a running child's answer surfacing at the top-level session is a harness fact and
that core already owns its sibling; the pass-condition item cost the implementer **zero words**
(*"contradict its own contract surface"* widened to *"contradict what the plan itself establishes"*)
instead of a second clause; and the cap-versus-tell item was fixed at **two** sites, the reported
`feature-readme-writer` one and the identical `X, not Y` cadence rule in `project-plan` that a sweep
turned up. Two proposals were declined on evidence and recorded: §0's `model: sonnet` licence does
**not** move off the README commit ([[pipeline-metrics]] shows that Sonnet dispatch catching the run's
only marginal gate and correcting an Opus child), and the state block's new open-decision field takes
**no** explicit `none` — the block has no gap-checking reader to earn one. See
[[pipeline-ecosystem]].)*

*(Confirmed working that run and deliberately preserved: the `~30`-line commit-message cap, now
calibrated across two features; Phase 5's *resume that same session*, whose first live exercise
recovered commit 6 at no cost; §0's `model: sonnet` firing correctly on the README commit; the
2026-08-20 boundary deletion, which produced the series' lowest planning share (19%); and
`run_in_background: false` on all fourteen dispatches.)*
