---
name: TDD workflow preference
description: User follows Red→Green→Refactor for each implementation step
type: feedback
---

Tests are #1 priority. User works in strict TDD order: write failing tests first, then implement, then refactor together.

**Why:** Keeps interface design honest; user acknowledges curiosity can pull them away from this — so I should nudge if tests are missing before moving on.

**How to apply:** When a new feature is requested, expect to write tests first. Do not jump to implementation before there are tests. If the user approves work before tests exist, gently flag it. The refactor pass is collaborative — don't skip it.

During the exploratory phase of an iteration, use `tests/explore/` as a scratch pad — files there satisfy TDD discipline without polluting the real suite. `tests/explore/` is for experimentation only; any test tied to a spec must live in the main `tests/` directory (numbered, e.g. `test-0014-arrays.cc`). At iteration close, each explore file is either promoted (moved into a numbered test file in `tests/`) or deleted. Set up the `tests/explore/` directory and an opt-in `pinp_explore_tests` CMake target at the start of each new iteration.

All C++ code must pass clang-tidy before commit. Run `scripts/lint.sh` to check. The pre-commit hook enforces this automatically once installed via `scripts/install-hooks.sh`. Config is in `.clang-tidy` at the repo root.
