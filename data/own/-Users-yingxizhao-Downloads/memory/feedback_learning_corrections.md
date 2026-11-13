---
name: learning-corrections
description: Add corrected framing section when user explains concepts in their own words
metadata:
  type: feedback
---

When the user explains a technical concept in their own words (e.g., "So subnet is like...") or asks "Am I understanding this right...", respond with ONLY the "Your Framing Corrected:" section below.

**Why:** Helps the user solidify understanding by seeing exact corrections to their mental model, without a full explanation diluting the focus on the correction itself.

**How to apply:** Trigger automatically whenever the user phrases a concept back in their own words or explicitly checks their understanding. Skip straight to the format below; only add a full explanation (structured per [[feedback_response_format]]) if the user explicitly requests it.

Problem:
> "user's problem"

What you said:
> "user's exact words in quotes"

Corrected:
> "improved version with key adjustments explained and **key adjustments highlighted in bold**"
