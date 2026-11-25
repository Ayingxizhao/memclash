## Two-step mode

This rule has already been split into requirements (listed after the rule, each with an id
and `keep`). This replaces the splitting in section 2: do not split again, translate the
requirements as given. Where this section and sections 1-2 differ, this section applies.

- Translate every requirement with `keep: translate`. Put its id in `req` on each clause that
  translates it. If the fixed vocabulary has no words for it, leave it out as
  `outside_vocabulary`.
- Every other requirement goes in `left_out`, with its id and one reason: `vague` or
  `outside_vocabulary` as given in `keep`, or `unclear_word` (then also give the `word`; see
  section 5). A requirement is either translated or left out, never both.
- `status` is `ok` if at least one clause is written.
- A requirement may have `applies_when` (the words that limit it). Express it with fields
  where you can and set `scope_encoded: true` on those clauses; otherwise set
  `scope_encoded: false`, and the limit is kept as a condition the format cannot check.
