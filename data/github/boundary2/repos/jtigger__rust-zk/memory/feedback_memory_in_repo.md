---
name: feedback-memory-in-repo
description: For this project, memory files live inside the repo (./memory/), not at the user-root auto-memory path
metadata:
  type: feedback
---

The canonical memory directory for this project is `$HOME/workspace/jtigger/rust-zk/memory/`. The auto-memory path `$HOME/.claude/projects/-Users-johnnycyberseed-workspace-jtigger-rust-zk/memory` is a symlink pointing at it.

**Why:** User wants memory artifacts to live with the project (likely for git-tracking / portability), not buried in `~/.claude/`.

**How to apply:** Write new memory files into the repo path directly. The symlink keeps the auto-memory loader working, so no behavior change is needed — just be aware that if the symlink ever breaks, recreate it rather than re-creating a separate directory at the user-root path.
