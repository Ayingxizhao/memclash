---
name: prefer-official-generators
description: Scaffold via official generators (create-next-app); don't hand-roll — only update/add project changes on top
metadata:
  type: feedback
---

User wants scaffolding done through official generators (e.g. `create-next-app`), not hand-written. Do everything through the generator, keep its files, then only UPDATE or ADD what's project-specific on top — don't substitute hand-rolled versions of files the generator provides (configs, layout, page, globals.css, etc.).

**Why:** the generated structure is familiar to other Next devs and keeps proper framework features/support intact; hand-rolled diverges and risks missing framework support. The user pushed back twice on hand-rolled scaffolding.

**How to apply:** run the generator with the right flags, keep its output, layer project code/config on top. Reverted my custom `page.tsx` back to the generated one; removed a smoke test that forced a custom page. Also recorded as decisions in DECISIONS.md. Relates to [[work-as-coworker-copilot]].
