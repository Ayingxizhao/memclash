# Communication notes

## 2026-11-21: review summary was too confusing

What happened: after the two outside reviews came in, the assistant summarised them in long,
nested bullets full of code names (`must_do`, `only_if`, glob sampling, file and line numbers).
The author could not follow it and had to ask: "Please summarize the problem that they found in
plain language using a short bullet list. It's so confusing to read this amount of text."

Why it matters: the author decides the direction from these summaries. If the summary cannot be
read, the decision is made blind.

Rule from now on:
- Give the short plain-language list first: one line per problem, everyday words, no code names.
- Details (files, line numbers, mechanisms) only when asked, or after the short list.
- One idea per bullet; at most about 6 bullets.

## 2026-11-21: still too much project jargon

What happened: a list of the checker's remaining problems still used project words ("the
model", "only_if", "unknown condition", "Z3"). The author: "it should be intuitive enough such
that a person never had any context about this project should be able to understand it."

Rule from now on:
- Write for a reader who has never seen this project.
- Say what the program does in everyday terms ("it only remembers the last thing you did"),
  not how it is built.
- Use a tiny everyday example instead of a project term. If a term is unavoidable, explain it
  in the same sentence.
