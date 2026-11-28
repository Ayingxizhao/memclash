---
name: walkthrough-explanations-in-doc
description: "User prefers walkthrough/teaching explanations written INTO thesis_code_walkthrough_QA.md in LaTeX, not the terminal"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f613f78b-84ad-430d-b890-1e6c3d164eb1
  modified: 2026-08-01T17:18:59.822Z
---

When explaining code/concepts from `thesis_code_walkthrough_QA.md` (the topic-by-topic
learning doc), WRITE the explanation directly into that doc using LaTeX math ($…$ inline,
$$…$$ display) — do NOT deliver it only as a terminal reply.

**Why:** the user reads the doc rendered; LaTeX is far easier for them to read than plain-text
math, and they want the explanation persisted alongside the topic. This is the CLAUDE.md
"walkthrough doc = LaTeX" convention applied to teaching answers, not just short notes.

**How to apply:** for "explain topic X" / "walk through this code" requests tied to the
walkthrough, Edit the doc (add a subsection under the relevant Topic) as the primary
deliverable; keep the terminal reply short (a pointer + offer next step). Line-by-line code
walkthroughs go in the doc too. See [[exp-folder-walkthrough]].

**Write it seamlessly.** Integrate answers/corrections into the existing prose as if always
written that way. Never restate the question in the doc, never add meta-notes about the edit
("Notation warning", "As requested", "renamed X to Y"), never leave changelog markers — the
doc must read as a finished text, not a Q&A transcript with the assistant. Also integrate
rather than accrete: merge into the existing explanation instead of appending a second,
overlapping one. **Check the doc before writing** — if the answer is already there, say so in
chat and leave the doc unchanged, or sharpen the existing passage; add a new paragraph only
when the information is genuinely new. Only annotate if explicitly asked.
