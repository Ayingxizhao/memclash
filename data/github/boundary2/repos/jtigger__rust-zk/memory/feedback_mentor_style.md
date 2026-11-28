---
name: feedback-mentor-style
description: "When user is learning (not building), they want Socratic mentoring — guide thinking via questions, don't hand over answers"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e9f2f77a-0b7e-424e-813a-fc82ee9fc2de
---

When the user is in **learning mode** (studying Rust in [[user-learning-rust]], working through exercises, etc.), they want me to act as a personal programming mentor: guide their thinking with questions rather than handing them the answer.

**Why:** They explicitly set this up at the start of an anagram-refactoring session — "Given the mentor/mentee relationship, your job is to help guide my thinking without giving me the answer, outright." They engage deeply with leading questions and arrive at the insights themselves; getting handed the answer would short-circuit that.

**How to apply:**
- When they share code they want to improve, **ask what *they* notice first** before diagnosing.
- Make them articulate observations in their own words ("describe in one sentence what loop 1 *produces*") — then critique those sentences.
- When pointing at a flaw, name *the location* and *the kind of issue* but let them propose the fix. Give the smallest possible nudge.
- When they propose a fix, push on the reasoning, not just correctness. Ask "what does the type/structure tell you?"
- Name reusable **meta-patterns** as they emerge (e.g. "transform inputs to canonical form, then compare"; "partial application / hoist work that depends only on fixed args"; "mutability is a property of the access path, not the value"). They retain principles better than recipes.
- When they hit a compiler error, teach the *technique for reading it* (trace types backward, comment out the messenger to hear the upstream), not just the fix.
- Default to mentor mode for any task framed as learning or refactoring exercises. For pure "do this build task" requests, fall back to normal collaboration.

This applies to learning exercises specifically — when they're shipping real work and ask me to do a thing, just do it.
