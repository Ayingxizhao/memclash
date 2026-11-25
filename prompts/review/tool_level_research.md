You are a research consultant for a class project. Work read-only in the repo (do not edit or
create files; your final message is saved as your report). You may search the web. Do not open
`data/gold/` or any file named `labels_*`. Do not call any paid LLM API.

## The project

An LLM translates each rule from a coding agent's memory folder, alone, into a fixed format
(git and file actions, conditions, path patterns; see `docs/review/vocab_draft.md`,
`prompts/rules/translate.md`, `pipeline/rules/template.py`). Z3 then checks every pair of
translated rules for a clash. The LLM fills a fixed template (a tool call); our code checks the
answer's layout and vocabulary and retries once on errors.

## The problem

The layout is now reliable, but in a pilot the translation was wrong in ways no layout check
catches:
1. Part of a rule dropped: "Before any commit, verify no secrets are staged" became only
   "check for secrets before committing"; the "no secrets in the commit" part was lost.
2. A concrete item called vague: "Keep the repo clean: no stale branches, no credentials,
   tested code" became "nothing left to translate".
3. Over-cautious: "Do not add secrets to version control" was marked unclear because of the
   word "add", although "to version control" settles it.
4. Small differences between rewordings of the same rule (one includes "files shown", the
   other does not).

The obvious fix, adding more instructions to the prompt for each error we see, is what we want
to AVOID: it tunes the prompt to the errors we happened to find. We want fixes at the level of
the tool / pipeline that are general and defensible in a research report.

## Questions

1. How do others make natural language -> formal language translation reliable, without
   hand-patching the prompt? Look at NL-to-logic and NL-to-spec work (e.g. nl2spec, NL2LTL,
   Lang2LTL, Logic-LM, LINC, SatLM, SymbolicAI), NL-to-SQL (e.g. self-consistency, execution or
   round-trip checks), policy / access-control translation from text, and structured-output
   tools (constrained decoding, grammars). For each technique: what it does, evidence it
   works, cost. Give only references you actually found; mark any you saw only an abstract of.
2. Which of these fit our pipeline and our four failure types? For each candidate say exactly
   what would change in the pipeline (not in the prompt wording), which failures it addresses,
   how much it costs per rule, and how we would measure that it helped. Candidates to consider
   (add others): splitting translation into smaller fixed questions (e.g. first list the
   requirements of the rule, then translate each), checking that every requirement of the
   English appears in the translation (coverage check), back-translation (formal -> English ->
   compare), voting across several samples, a second model as a checker, asking the model to
   pick from enumerated candidate translations, solver feedback loops.
3. Recommend the 2-3 best options for a class project presenting on Dec 1 (today is Nov 22),
   with the measurement that would show each works. Say what each would NOT fix.

Output: Markdown, under about 1500 words, sections 1-3, then a 5-bullet summary. Cite URLs.
Plain language a person with no context can follow. Say plainly when unsure.
