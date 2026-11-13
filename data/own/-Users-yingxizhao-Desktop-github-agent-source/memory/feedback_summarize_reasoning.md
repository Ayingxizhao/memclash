---
name: feedback-summarize-reasoning
description: "User wants a short plain-language summary after multi-step reasoning or tool-call chains, not just a trail of edits/commands to reconstruct from."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bd3b8e3c-75ce-4acd-9bad-c8cf6ec088ac
  modified: 2026-08-07T15:27:26.385Z
---

When reporting a bug found mid-task, compress it into ONE line following this exact causal chain, not a narrated play-by-play and not just a bare conclusion:

**Template:** "Found a bug: while doing X, found Y → that's a bug because it causes Z → fix is A."

**Why:** User explicitly gave this template after two failed attempts. First attempt (live "let me check X... note Y... let me check Z again" narration) was too much noise. Second attempt (bare "Found a bug: X copied into Y, but Y never created. Fixed by adding Z.") dropped the causal reasoning entirely — user said that's not what they meant either. They want the *chain* (what I was doing -> what I found -> why it's a bug -> what fixes it) preserved, just compressed to one line instead of spread across a paragraph of narration.

**How to apply:** Investigate silently as normal. When surfacing a bug/finding, write it as a single compressed sentence with explicit -> steps: context/action -> discovery -> why it's a problem -> the fix. Do not expand this into multiple sentences or paragraphs, and do not strip it down to just "found X, fixed by Y" — both are wrong per direct correction. This stacks with the user's existing global CLAUDE.md instruction to stay concise and summarize each edit's core logic/expected behavior.
