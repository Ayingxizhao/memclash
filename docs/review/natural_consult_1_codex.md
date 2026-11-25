The result is clear and still worth presenting: the bottleneck is semantic translation, not logical inference. Z3 reasons correctly about what it receives, but independently translated rules omit permissions, scope, and cross-rule links. Giving an LLM the rules jointly avoids that information loss. At natural prevalence, your current formal pipeline is worse than direct folder-level review.

There is still an honest hybrid story, but not “Z3 improves accuracy.” Its plausible roles are:

- Scaling: folder-level LLM review may deteriorate as rule count and context grow. Retrieval plus pairwise judgment may then be necessary.
- Stability: Z3 is deterministic after translation, although end-to-end stability remains limited by translation variation.
- Conditional guarantees: Z3 can exhaustively prove no contradiction in the formalized model—not “no clash in the original text.” That qualification is essential.
- Auditability: solver witnesses expose exactly which formal assumptions caused a flag. This helps debugging, but does not ensure a more faithful explanation.
- Compositional conflicts: a shared formal theory could infer that “map and player data” includes `server-world.dat`. The present independent-pair translation cannot. This is promising but requires ontology/linking work.
- Complementary errors: a hybrid is justified only if Z3 finds real clashes missed by direct judgment, or reliably verifies/rejects LLM flags. The present evidence does not show either.

With the remaining budget, the strongest test is scale. Stability needs repeated paid runs; exhaustive natural-language guarantees are impossible; multi-rule formalization needs substantial implementation; planted adversarial examples would support only a synthetic diagnostic claim. Free Codex/Claude can provide independent screens and adjudication, though Claude’s prior exposure should be disclosed.

I would slightly expand the proposed test. DeepSeek should receive all three full folders containing known clear clashes, including `sparkling__ruflo-patch`; otherwise its scale recall is measured on only two of three known cases. At the estimated rate this should cost about $0.06. Freeze the prompt and inputs first. Record:

- known clashes recovered out of three;
- additional flags per folder and per thousand possible pairs;
- clear, ambiguous, and false additional flags after independent adjudication;
- context size and rule count;
- whether failures are missed retrieval, misunderstood semantics, or output truncation.

Do not treat “no extra flags” as proof of no other clashes; it is only observed selectivity.

If the scale test also favors the LLM, the Dec 1 story should be a useful negative result:

> On real repository instructions, formal solving was not the hard part. Translating rules independently into logic discarded precisely the scope, permission, and relational information needed to detect conflicts. Joint-context LLM screening found all three clear natural clashes with no false alarms in 951 evaluated pairs, while saved-translation Z3 missed two and produced one unstable false alarm. Formal methods remain valuable for conditional verification and audit trails, but only after reliable semantic normalization. For this task, direct LLM screening is the stronger baseline, and hybrid complexity must earn its place through scale or complementary-error evidence.

That is more credible than forcing a hybrid win, and it yields a concrete design lesson.

**CHANGE — exact next step:** freeze one full-folder prompt; run fresh blind Codex screens on all five complete folders; run one thinking-enabled DeepSeek call on each complete known-clash folder—QuagKhai, RDForward, and ruflo-patch—then have fresh Codex and disclosed non-blind Claude independently adjudicate every additional flag as clear, ambiguous, or false, reporting known-clash recall and extra flags per thousand pairs.