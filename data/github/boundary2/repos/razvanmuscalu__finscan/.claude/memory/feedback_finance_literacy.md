---
name: User is finance-novice — explain investment concepts plainly
description: User builds a personal trading project but is NOT familiar with investment/finance jargon. Treat every domain term as new and explain.
type: feedback
originSessionId: 17d7a45f-5f54-48bb-baf2-3ad8dec041ec
---
User is learning investment/finance concepts as they go while building this project. Most terms (GICS sectors, screening, top-down vs bottom-up, regime, sector posture, multiplier bounds, friction hurdle, conviction-weighted scoring, etc.) are being seen for the first time.

**Why:** User stated explicitly: "this is going miles above my financial knowledge right now... be more and more careful and aware that i am NOT familiar with these things. i'm seeing most of them for the first time and i'm learning as i go." They're a senior software engineer, not a finance professional.

**How to apply:**
- Default to plain-language explanations of any finance/investment term before using it. Don't assume the user knows what "regime", "tilt", "posture", "drawdown", "alpha", "beta", "P/E", "consensus", etc. mean in trading context.
- When proposing investment logic, separate **what the code does** (user understands) from **what the finance concept is** (user is learning). Lead with the concept in everyday words, then the implementation.
- For trade-off questions (e.g. "conservative vs aggressive multiplier bounds"), don't just present the numbers — explain *what each choice does to the trader's behavior in plain terms* (e.g. "0.78–1.22 means macro can push a ticker's score up/down by 22% — strong sector tailwind can promote a mediocre ticker over a great one in a bad sector"). Give a recommendation with reasoning, not just options.
- Avoid jargon stacking. "Top-down sector posture override" → "if the whole sector is in trouble, don't buy a stock from it unless you have a specific reason."
- When user says "i don't understand" to a question — that's the signal to explain the concept itself, not just rephrase the question.
- Pair every finance term with a 1-line gloss the first time it appears in a session.
