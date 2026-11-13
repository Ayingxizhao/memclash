---
name: feedback-response-format
description: "Response format — sections with bold topic sentences, one idea per subsection, essential content only"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d859bb2f-a973-429d-940f-4eafba6febde
  modified: 2026-08-03T21:52:00.552Z
---

Structure longer responses as sections with bold topic sentences, not prose paragraphs or bullet dumps.

**Why:** The user reads faster when the first bold sentence of a subsection carries the full claim, and body text elaborates rather than restates.

**How to apply:**
- `#` for section title (big).
- A bold declarative sentence serves as the subsection title and topic sentence, with body text continuing inline right after it (not on a new line).
- One idea per subsection. Group related ideas under a single `#` section rather than spreading them across many.
- Include essential content only — no filler, no restating what the topic sentence already said.
- Use active voice, omit needless words, put emphatic words at the end of a sentence, use concrete language over abstract.
- Don't preemptively add extra detail — the user will ask a follow-up if they want more.

Example:

## Subagent Tool Access

DeepAgents provides no API to restrict built-in harness tools. The `tools` key adds MCP tools only — system prompt is the only lever for built-ins.

Our allowlist controls the right layer. It scopes MCP tools to read-only; built-in harness tools are a separate concern.

This format applies broadly across all directories/projects, not just one repo — see [[user_global_preferences]] if present.
