---
name: Project-related memory goes under the project repo's .claude/memory/
description: For work tied to mlsys-wiki (and similar project-scoped work), write memory into the project's own .claude/memory/, not the global ~/.claude/projects/.../memory/ path
type: feedback
---

Memory that is **project-related** (scoped to a specific repo's work — e.g., mlsys-wiki wiki-building, its topics, its source repos like vllm/sglang/dynamo/nixl/lmcache) must be written under the project's `.claude/memory/` directory (i.e., `.claude/memory/` relative to the wiki repo root), rather than the default auto-memory path at `~/.claude/projects/<flat-cwd>/memory/`.

**Why:** The mlsys-wiki repo is synced across multiple devices, so memory must travel with the repo itself — absolute paths like `/home/hkang/wl/mlsys-wiki/...` break on any other machine. Keeping project-scoped memory inside the repo makes it git-tracked, portable, and visible alongside the wiki content it informs. The default auto-memory path is keyed to the cwd where Claude was invoked (e.g., `~/.claude/projects/-home-hkang-wl-vllm/memory/` when cwd is `vllm/`), which is both machine-specific AND invisible the next time the user works from a different cwd for the same logical project. The user asked me to switch on 2026-04-20 after I had saved one memory to the default location.

**How to apply:**
- **Always use repo-relative paths inside memory files.** Reference files as `.claude/memory/foo.md`, `topics/pd-disaggregation/config.md`, `repos/vllm/vllm/distributed/...` — never `/home/hkang/wl/mlsys-wiki/...`. The repo checkout location differs per device.
- **The same rule extends to *any* repo-tracked file that will be synced across devices** — not just `.claude/memory/`, but also `wikis.json`, `_index.md` / `config.md` inside topic wikis, shell snippets inside `repos/_index.md` bump instructions, and raw notes under `topics/*/raw/`. Use tilde paths (`~/wl/mlsys-wiki/...`) when an absolute-looking form is needed for external resolvers like llm-wiki's `wikis.json`, and relative paths (`repos/<name>`, run "from the hub root") inside documentation snippets. User flagged this on 2026-04-21 after I added a `/home/hkang/wl/mlsys-wiki/topics/cute-kernels` entry to `wikis.json`.
- When writing a memory that is about **mlsys-wiki**, its topics (`pd-disaggregation`, future `speculative-decode` etc.), the wiki's conventions, or the submoduled source repos *as they are used for the wiki* → write to `.claude/memory/` (relative to wiki root) and update `.claude/memory/MEMORY.md` in the same directory.
- When writing a memory that is about **the user themselves** (role, preferences, broad working style) → the default auto-memory path is still appropriate since those memories are user-scoped and not repo-portable anyway.
- When in doubt, prefer the project path — co-locating with the project is the safer default.
- The project's `.claude/memory/MEMORY.md` is NOT auto-loaded at session start. At the beginning of any session touching mlsys-wiki work, read it explicitly via the Read tool. A pointer has been left in the global auto-memory MEMORY.md to remind future sessions, but that pointer only exists on the machine where it was written — so future sessions on other devices need to learn the convention by reading this file from the repo.
