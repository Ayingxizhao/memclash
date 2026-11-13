---
name: feedback-response-format
description: "Response format — conclusion first, then bold topic sentence + bullets; ~3 sentences per idea, no rhetorical language"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 316bf5f2-8a3e-4878-9287-0a4acf0d7990
  modified: 2026-11-26T00:00:00.000Z
---

Lead with the conclusion, then structure detail as bold topic sentences with bullet points underneath, not prose paragraphs.

**Why:** Helps user to

**How to apply:**
- The first line of the response is the conclusion of the whole response — the answer, finding, or recommendation.
- Every bold topic sentence is likewise a conclusion, not a label for what follows.
- Supporting detail goes as short bullets immediately below the bold sentence — never as an inline paragraph continuing after it.
- One idea per subsection.
- Keep bullets short — one fact per bullet, not compound sentences.
- A one-line **Recommendation:** (bold label, plain text after) can close out a subsection when a decision is being proposed.

**Format example**:

**Recommendation:** Use `virtual_mode=True` with `root_dir` pointed at `skills/` only.

**Reason:**: FilesystemBackend's default mode doesn't sandbox the agent.
- `root_dir` only affects relative paths, not absolute ones
- An agent could still read `/app/.env` directly

**`virtual_mode=True` fixes this.**
- Blocks path traversal (`..`, `~`) and absolute-path escapes
- Verifies resolved paths stay inside `root_dir`

This format applies broadly across all directories/projects, not just one repo.
