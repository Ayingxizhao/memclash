---
name: feedback-show-dont-describe
description: "Explain concepts with concrete examples, input/output, and ASCII visualizations rather than prose paragraphs"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1100512a-46cc-490a-bd7f-05edcb0a21c3
  modified: 2026-09-11T14:47:29.479Z
---

When explaining a technical concept, show it with concrete examples, input/output, and simple ASCII diagrams instead of describing it in prose. The user asked for this directly: "use some examples, like input/output and also visualization, instead of being word-heavy."

**Why:** prose descriptions of mechanisms are hard to hold onto. A side-by-side trace of what actually happens (events flowing, a crash, what the sink ends up holding) lands where a paragraph doesn't. The user confirmed the visual version worked after the prose version hadn't.

**How to apply:** prefer a small before/after or side-by-side block over a paragraph. Show the failure case concretely — actual event names, actual resulting state. Two-column comparisons work well for contrasting two modes. Keep diagrams small and unlabeled by arrows-with-captions; the trace itself carries the point.

Related: [[feedback-explain-mechanism-first]], [[feedback-answer-payload-length]], [[feedback-use-my-wording]]
