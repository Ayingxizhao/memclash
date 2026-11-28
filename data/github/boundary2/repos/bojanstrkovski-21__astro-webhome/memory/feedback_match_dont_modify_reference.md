---
name: feedback-match-dont-modify-reference
description: "When asked to make element A match element B's size/style, only change A — never touch B, even to make the match easier"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 37b80f78-a56f-4059-a23f-26598f5c9ccf
  modified: 2026-09-18T11:58:31.544Z
---

When the user asks to make one or more elements match an existing reference element (e.g. "make the dropdown and button the same height as the search field"), only adjust the elements being conformed — do not add/change sizing on the reference element itself, even if that would make hitting an exact pixel match more convenient.

**Why**: In astro-webhome, asked to make the search-engine dropdown and Search button match the search input's height, the fix included adding an explicit `height: 34px` to `.search-input` too (an arbitrary guess, not even the input's real natural height). The user immediately caught it: "you increased search field height why i told you to make search button and dropdown same height as the search field" — the reference element was never supposed to move.

**How to apply**: For "make X match Y" requests, treat Y as read-only. If an exact match requires knowing Y's rendered size, measure it (e.g. via a headless browser `getBoundingClientRect()`) rather than eyeballing a round number, then apply that exact value only to X.
