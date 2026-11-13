---
name: rebuild-workflow
description: How the user wants the ContentGuard rebuild run — I make design decisions myself; show a prototype at every stage for feedback
metadata:
  node_type: memory
  type: feedback
  originSessionId: 01ef75b6-e33b-4b2e-8c2a-b22225f3cc22
  modified: 2026-10-18T03:39:24.963Z
---

For the ContentGuard rebuild (see [[contentguard-rebuild]]):
- Make design decisions myself (pick the best-practice option, state what I chose and why in one line). Don't stop to ask A/B/C.
- At every stage, show a runnable/visible prototype; the user reviews it and points out what they don't like.
- 2026-10-17 update: user said "keep going dont stop until everything is finished or i said so" — run all remaining steps back-to-back, showing prototypes as I go; only stop for things only they can do (secrets, Cloudflare login, deploy approval).

**Why:** user (2026-10-17) said "For these types of design decisions I'll just let you choose on your own. At every stage show me some sort of prototype."
**How to apply:** prefer stages that end in something visible (UI over raw JSON when possible).
