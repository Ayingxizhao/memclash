Round 3. You are co-authoring a fixed vocabulary with Claude. Work read-only (do not edit or
create files; your final message is saved). Do not open `data/gold/` or any file named
`labels_*`. Do not call any paid LLM API.

The user asked for two changes, which Claude made in `docs/review/vocab_draft.md` (section 5
and item 7 of section 8):
- Translation rows describe meanings, not exact phrases.
- Model only what can be justified. Rows that were silent judgment calls ("write", "delete"
  vs move, "change", "can/may") moved to a fixed list of words with more than one meaning (5b).
  The translator writes the word id; the checker tries every reading and reports clash /
  depends on reading / compatible.

Read the current draft in full. Reply in Markdown, under about 600 words:
1. Is every row left in 5a justified by the words' plain meaning or by git's own definition?
   Name any row that is still a judgment call and should move to 5b.
2. Are the readings in 5b complete and correct? Is any other common word in the survey
   folders (`data/runs/survey/`, `data/github/explore/`) a 5b candidate? Quote it and its folder.
3. Any problem with how the checker handles 5b words (e.g. two such words in one pair, or a
   5b word inside a must_do vs a never)? Give exact text changes.
4. If no changes are needed, write `SIGN OFF`. Do not repeat the draft back.
