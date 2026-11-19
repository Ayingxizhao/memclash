You help build a test set for a tool that finds conflicting rules in a coding agent's memory
folder. You are given the folder's rules, one HOST rule from it, and a conflict PATTERN.
Write three new rules that a user could plausibly have saved to the same memory folder on a
different day:

1. `conflict_direct`: a rule that conflicts with the HOST rule following the PATTERN, using
   the same key terms as the host (same command, file, tool or setting names).
2. `conflict_reworded`: the same conflict, but phrased so that it shares as few words with
   the host as possible (describe the command, file or setting differently). It must still
   be about exactly the same behavior.
3. `paraphrase`: a rule that demands the SAME behavior as the host in different words. It
   must not add or remove any requirement.

A conflict means: there is a realistic situation in which both rules apply and the agent
cannot comply with both.

Patterns:
- `opposite`: the host requires an action and the new rule forbids it, or the reverse.
- `value`: both rules fix the same choice (tool, format, source, setting) to different values.
- `narrower`: the new rule covers a specific case inside the host's scope and demands the
  opposite there, without mentioning the host or calling itself an exception.
- `number`: both rules fix the same quantity to different numbers.
- `permission`: the host forbids an action and the new rule explicitly allows it ("may ..."),
  or the reverse.

Requirements:
- Each rule is one sentence, imperative, in the style of the folder's rules.
- Do not mention the host rule, and do not use words like "instead", "exception", "unlike",
  "override" that point at another rule.
- The conflicting rules must conflict with the HOST rule. Avoid creating a conflict with any
  other rule of the folder if you can.
- Each rule gets a plausible new memory file name (e.g. `feedback_<topic>.md`).
- If the pattern cannot be applied to the host rule, return {"fits": false, "reason": "..."}.

Return JSON:
{"fits": true,
 "conflict_direct": {"file": "<name>.md", "rule": "<sentence>"},
 "conflict_reworded": {"file": "<name>.md", "rule": "<sentence>"},
 "paraphrase": {"file": "<name>.md", "rule": "<sentence>"},
 "situation": "<one sentence: a situation in which the host and the conflicting rule both apply>"}
