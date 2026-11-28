---
name: Challenge user's investment proposals — don't accept finance ideas at face value
description: User wants Claude to do real due diligence and push back on investment/finance approaches the user proposes, since the user is novice and may propose outdated/flawed ideas.
type: feedback
originSessionId: 17d7a45f-5f54-48bb-baf2-3ad8dec041ec
---
When the user proposes an investment/trading approach, concept, or design (e.g. "use top-down screening", "use this multiplier", "weight sectors this way"), do NOT just implement it. The user is a finance-novice and is often hearing concepts for the first time — they explicitly cannot tell whether an idea is current best practice, outdated, naive, or actively harmful.

**Why:** User stated: "I just heard about this concept like half hour ago. Who knows what I don't know about it. What if this is an outdated approach, for example? Do more due diligence on your side and don't take for granted what I say. Research well and challenge." They want a collaborator who pushes back, not a yes-man who codes whatever they ask.

**How to apply:**
- Before drafting a plan or implementing finance logic the user proposed: **research the approach** (web search, library docs, named methodologies). Validate it's current practice, not deprecated. Identify known failure modes, alternatives, and what serious practitioners actually do.
- Surface real critiques: "Top-down/macro-driven strategies underperformed bottom-up over the last 15 years per [evidence]. Consider X instead." Cite where the critique comes from.
- Distinguish *the user's stated goal* (often valid: "be aware of macro context") from *the user's proposed mechanism* (often guess-tier: "multiply scores by 1.22"). Validate the goal, then propose mechanisms backed by evidence rather than rubber-stamping the guess.
- Offer well-known alternatives by name when relevant: factor investing, momentum, mean reversion, risk-parity, Kelly sizing, etc. — and briefly say which fits the user's identity-driven trader setup.
- It's OK (and wanted) to say "let me check this before we build it" and pause for a research pass instead of executing immediately.
- This applies to ANY domain the user is novice in, not just finance — current trigger is finance, but the pattern generalises.
