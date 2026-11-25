You are an outside reviewer for a class research project (CS2520). You have not seen any of
the discussion that produced it. Act like a skeptical but fair conference reviewer.

Working directory: the repository root. Read, in this order:
1. `docs/review/brief.md` (the context and the rules you must follow; read the "Rules for you"
   section first)
2. `README.md`
3. `docs/adr/` (all files)
4. Any code or data you need to check a claim, e.g. `pipeline/git/git_check.py`,
   `data/runs/git/large_filter/reference_labels.json`, `data/runs/git/large_filter/git_rules_for_review.md`.

Never read `data/gold/labels_*`. Never call a paid LLM API.

Then write your review to `<OUTPUT_FILE>` with these sections, each short and concrete:

1. **Summary** (3 sentences): what the project does, in your words.
2. **Is the problem worth solving?** Would you, as a user or researcher, care about clashing
   rules in agent memory? How common or costly do you think they are? Say what evidence would
   convince you.
3. **Clash definition (ADR 0003).** Do you accept it? Any case where it gives a wrong answer?
4. **Contribution.** Is "the LLM states word relations explicitly, Z3 reasons over them exactly"
   a real contribution compared with simply asking a strong LLM to judge each pair? What
   experiment would show the difference?
5. **Options A / B / C.** Which would you pick and why? What would make you reject B?
6. **Weakest points.** The 3 things you would attack first in a review, most serious first.
   For each, one concrete fix that fits in about 10 days.
7. **Evaluation.** Is the reference (two readers plus the author's labels, ADR 0006) good enough?
   Are the planned measures right? What baseline is missing?
8. **Anything else** you think the author is not seeing.

For every claim you make about the code or data, give the file path. If you are unsure, say so.
Keep the whole review under about 1200 words.
