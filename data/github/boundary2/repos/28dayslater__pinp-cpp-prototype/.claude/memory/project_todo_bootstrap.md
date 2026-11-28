---
name: LLVM bootstrap automation TODO
description: Automate LLVM submodule setup for when pinp goes public
type: project
---

Manual LLVM submodule bootstrap needs automation before pinp can go public.

**Why:** Current setup requires several manual git commands (submodule add, fetch tag, checkout) that are not contributor-friendly and have no CI story.

**How to apply:** When user returns to this, implement a `scripts/bootstrap.sh` that handles the full submodule setup, and a GitHub Actions workflow that caches `third_party/llvm-install/` to avoid full rebuilds on CI.
