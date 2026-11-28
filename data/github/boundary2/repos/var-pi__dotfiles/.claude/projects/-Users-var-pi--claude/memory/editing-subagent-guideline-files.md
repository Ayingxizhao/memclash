---
name: editing-subagent-guideline-files
description: "How to compact/edit agent & subagent guideline files (system prompts, skills) so subagents act precisely"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 685a0512-e644-4ce1-b0c2-2b309b52e7f9
  modified: 2026-08-12T12:17:20.176Z
---

When refactoring agent/subagent guideline files (system prompts, skill agreements) for
compactness, the goal is *precise subagent behavior*, not just fewer tokens.

**Why:** A subagent attends to its prompt rather than studying it. The enemy of precise action
is dilution and ambiguity — a load-bearing rule buried in motivational prose, or the same rule
restated 3–4× with drifting wording (the agent then can't tell if those are one rule or several).

**How to apply — "assume competence" (2026-08-11, supersedes the operative-why test).** Write for an
agent that already knows its craft.
- **Cut any rule a competent practitioner follows unprompted** — scope discipline, reuse, seeding,
  tolerance hygiene, independence. What earns a place is only what the agent cannot derive from its
  own context: harness mechanics that fail silently, coordination conventions (paths, field names,
  who owns which altitude), facts about this reader, measured findings contradicting a fair prior.
- **One rule, one sentence, no rationale.** A *why* is earned only where the rule **inverts** what
  the model would otherwise do. The earlier version of this memory kept "the tail that makes the rule
  generalize" — that licence is what regrew the corpus twice.
- Cut purely motivational framing ("the logic of the flow", "the payoff of the split").
- Each concern gets ONE owning file/section; others reference it by name (single source of truth).
- **Do not calibrate by model tier.** The implementer's agreement survived two tier flips unchanged.
  (Calibrating by the *file's job* — checklist vs judgment instrument — is also now subsumed by
  "assume competence", which is a floor, not a tier.)

**A rule outlives its failure (2026-08-12, sixth pass).** The three rules above ask whether a rule
belongs, how often it is said, and how much rationale it carries; this asks whether **the failure it
was written against still exists.** *Kept because it costs little* is how a corpus regrows — a
workaround for a cause since fixed still reads as current and still budgets attention for what can no
longer happen. Two riders, both measured: **the class is rare** (a corpus-wide sweep found exactly
one instance, every other recovery clause being live), so it prevents regrowth rather than buying
deletions; and **it is invisible from inside a file** — the tell is a dated design record, not the
prose.

**Mantra, not prose (2026-08-12, fifth pass).** The three rules above decide *whether* a rule belongs,
*how often* it is said, and *how much rationale* it carries. This decides how the surviving sentence
is written: **load-bearing term first, the relation on a dash, no connective scaffolding.** Compress
until only the concept is left, then stop — **density a cold reader has to reconstruct is not
density.** Also: **never write a rule about how to read the file itself**, and never restate what the
harness already supplies.

**State it once, at full strength, and stop (2026-08-11, fourth pass; fifth form added 2026-08-12).**
*Assume competence* decides whether a rule belongs; this decides how many times it is said. A stated
rule gets **re-encoded** five ways, each costing the attention the statement needs:
- an **instance list** after the category the rule already names ("any expression, fixture, grid or
  loop"; "not a quickstart, a usage tour, an install walkthrough"). **Scope matters:** a list the agent
  must check *its own prose* against taxes every sentence it writes, which is worse than wasteful; a
  list it searches *outward* for — a reviewer's defect classes — is not this and stays;
- a **paraphrase in the rationale slot**, spending the slot a real *why* would earn ("a systematic
  error and an unlucky run look identical" restating *mechanism before configuration*), of which the
  common form is **a clause restating the cost of breaking the rule**;
- a **second site** — including one the reader already holds from a preloaded core, the sentence
  directly above, or **the agreement it reviews against**;
- the **history behind a number** — a cap carries its bound, not its provenance;
- the **defense of an absence** — what a file does not say needs no note explaining why.

The test for any sentence beside a rule: **would deleting it change what an agent does?** *Exception,
registered in the dependency graph:* where two ends must both act and cannot read each other's file,
state it at each end in one sentence.

**Where the floor is — and how to estimate it (measured over four passes).** What resists is
**artifact specification** (templates, field lists, schemas) and **coordination convention**; cutting
either underspecifies the pipeline rather than leaning it out. Two calibration facts, both learned
the expensive way:
- **A floor measured after a pass is the floor of the strategies tried, not of the corpus.** Pass 3
  recorded "the remaining text *is* the rules" at 13,253 words; pass 4 then found a whole class it had
  never looked for. Do not record a floor as a property of the corpus.
- **Estimate the yield from a sample, never from a feeling — and never from a file you chose for its
  deletions.** Pass 4 projected −20% by assuming ~20% of each file was prose-around-rules; it is ~6%,
  and the pass returned **−5.8%**. Pass 5 sampled properly and still projected −15% for **−5.8%**,
  because both sampled files were ones it had already decided to cut from; rewriting a file with
  nothing to delete returned **−0.8%**. Sample a file you have *not* chosen.
- Diminishing returns are real: 1.61×, then 1.06×, then 1.06×. Two independent methods now agree the
  prose floor is reached. A further multiple requires **deleting capabilities** — a named class the
  operator picks — not better editing. Expect the file holding the editing rules to **grow** in any
  such pass.

**Generalize the feedback; never transcribe it (2026-07-25).** Feedback arrives as *examples*
("this sentence is bloat", "I liked this part"); the rule you write must be the *principle extracted
from the example*. A transcribed example gets applied to every case that superficially resembles it.
*Canonical failure:* "I liked the war story" became *include a war story* in `commit-doc-writer`, so
every doc grew one and the device became boilerplate. Corollary: state a rule as a **cap** ("at most
one", "under ~150 lines") — an eager agent honours a bound and inflates an encouragement. Full
statement lives in `skills/pipeline-maintenance/SKILL.md`.

**Cap the defect, not the legitimate form (2026-08-22).** The corollary above has a failure mode of
its own: a **count** paired with a **semantic test** disagrees with it in every borderline case, and
the agent applies whichever it weighted last, so nothing downstream tells obedience from override.
*Measured:* a README under *"the antithesis tic — at most one per document. The tell: was Y ever
actually on the table?"* shipped ~10 negation contrasts, **every one passing the tell**. Fix: recast
so the countable thing is the **defect** — zero of the form the tell rejects, unlimited of the form it
allows. Cap-ness survives; the disagreement does not. The same rewrite makes an unassertable rule
assertable, which is the forcing function the gated behavioural-regression item predicts.

Also: this user cares that the **objective-synthesis step is not skipped** — restate + extend
the user's stated objectives before exploring/editing. See [[pipeline-ecosystem]].
