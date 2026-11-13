---
name: learning-corrections
description: Add corrected framing section when user explains concepts in their own words
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ff611b65-533f-4d36-b125-db48dbca3669
  modified: 2026-08-11T14:11:22.948Z
---

When the user explains a technical concept in their own words (e.g., "So subnet is like...") or asks "Am I understanding this right...", provide:
1. Normal explanation first
2. Then add a "Your Framing Corrected:" section at the bottom

**Why:** Helps the user solidify understanding by seeing exact corrections to their mental model.

**How to apply:** Automatic when the user phrases a concept back in their own words or asks "Am I understanding this right...".

**Format:**

Problem:

| "describe user's problem"

What you said:

| "user's exact words in quotes"

Corrected Version:

| "improved version with key adjustments explained and **key adjustments highlighted**"
