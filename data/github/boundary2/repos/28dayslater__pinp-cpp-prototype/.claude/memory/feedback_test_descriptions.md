---
name: TEST_CASE description capitalisation
description: Rule for capitalising Catch2 TEST_CASE description strings in this project
type: feedback
---

Capitalise the first character of every TEST_CASE description string.

**Exception**: if the description starts with a language keyword (e.g. `if/else`, `::name`), leave it lowercase — capitalising a keyword would be misleading.

**Why:** user preference for consistent, sentence-style capitalisation in test output, without misrepresenting language syntax.

**How to apply:** when writing or editing TEST_CASE descriptions, uppercase the first letter unless it is a language keyword.
