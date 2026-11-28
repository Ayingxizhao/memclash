---
name: C++ column width preference
description: User prefers 100-column line limit for C/C++ code
type: feedback
---

Use 100-column line limit for all C/C++ code, not 80.

**Why:** User uses a 21:9 ultrawide monitor; longer lines are comfortable and preferred.

**How to apply:** The project `.clang-format` is set to `ColumnLimit: 100`. Always run `clang-format -i` after editing C/C++ files; the project config will enforce 100 columns automatically.
