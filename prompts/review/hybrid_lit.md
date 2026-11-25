You are an independent research reviewer for a class project. Work read-only (do not edit or
create files; your final message is saved). You may search the web; read papers, not just
abstracts, where you can. Do not open `data/gold/`, files named `labels_*`, or any `frozen_*`
label file. Do not call any paid LLM API.

## Context

Read `docs/review/method_audit.md`, `docs/review/method_audit_codex.md`,
`docs/review/method_audit_followup_codex.md`, `docs/adr/0003-clash-definition.md`.

Our method: an LLM translates each memory-folder rule alone into a narrow formal vocabulary,
Z3 checks each pair for a clash. On a precommitted 20-pair test (7 planted clashes, 3 real, 10
hard compatible pairs; one run), a direct LLM judge (both rules + clash definition) found 10/10
with 0 false alarms; our method found 7/10 (any of 3 runs) with 1 false alarm. The author asks:
is there an honest, presentable story, and how can the method be improved?

## Questions

1. **Literature: when do LLM + solver hybrids beat the LLM alone, and when not?** Cover
   logic/reasoning (e.g. Logic-LM, SatLM, LINC, and later work), NL -> temporal logic / policy /
   access-control translation, requirements and norm conflict detection, and LLM-instruction or
   system-prompt conflict work. For each: what baseline, what metric, did the hybrid win, on
   what kind of data, and why. Note especially reported wins on precision/false alarms,
   faithfulness/explanation, stability across runs, harder compositional cases, or scale.
   Cite only work you actually found; mark abstract-only.
2. **Improvements supported by the literature** that fit our setting and could be tried
   without new paid translation of whole folders (e.g. solver as verifier of LLM flags, LLM
   verifying the solver's witness, self-refinement on solver errors, ensembles, abstaining).
   Rank by expected value for us.
3. **Interpretation.** Given our numbers, list claims we CAN honestly make and claims we
   CANNOT. Be strict.
4. **Fair next test, near-zero cost.** We will reuse saved translations (Z3 is free), use you
   (Codex) as the LLM-alone judge and labeller, and spend at most ~$0.03 on one run of the
   DeepSeek direct judge on ~30 pairs. Propose the pair set (how to pick from real folders +
   hard cases so the test is not saturated), the arms to compare (LLM alone, Z3 alone, hybrid
   variants), the measures, and what result would support which claim. Fix it before data.

Output: Markdown, under about 1500 words, sections 1-4, then a 5-bullet summary. Plain
language. Say plainly when unsure.
