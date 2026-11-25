---
name: Always pin figure/image references to GitHub commit-permalinks
description: When a wiki note references an image/figure from a submoduled repo, include a GitHub permalink pinned to the exact commit hash of the submodule, not just the local repo-relative path
type: feedback
---

# Pin figure references to commit-permalinks on GitHub

**Rule:** When a raw note (or any wiki article) references an image, diagram, or figure that lives inside a submoduled repo (`repos/vllm/`, `repos/sglang/`, etc.), include a GitHub permalink pinned to the **exact commit SHA** of that submodule, not just the local `repos/.../path/to/fig.png` path.

**Format:** `https://github.com/<org>/<repo>/blob/<full-commit-sha>/<path-inside-repo>`

- Use the full 40-char SHA (or at least 7-char short hash), not a branch name like `main`. Branches move; commits don't.
- Grab the SHA with `git submodule status repos/<name>` from the wiki root — it prints ` <sha> repos/<name> (<tag>)`.
- For inline image embedding (rare in raw notes, common in compiled articles), also document the `raw.githubusercontent.com/<org>/<repo>/<sha>/<path>` form.

**Why:** Memory incident 2026-04-21 — the four-figures walkthrough note initially referenced figures only by local path `repos/vllm/docs/assets/features/disagg_prefill/workflow.png`. User pushed back: a local path is only meaningful to someone with this exact wiki checkout at this exact submodule version. A pinned GitHub permalink is:

- **Portable**: works for anyone reading the note, including across devices where the wiki is synced but submodules may not be initialized.
- **Stable against upstream churn**: vLLM's `main` branch rewrites docs all the time; pinning to the commit SHA this wiki currently tracks (e.g., `b1388b1` = v0.19.1) guarantees the note's text and the figure always line up.
- **Searchable**: readers can jump to the GitHub UI and navigate surrounding docs, blame history, etc.

**How to apply:**
- In every wiki note that references a figure/image from a submoduled repo, add either a table column "Permalink" in the figure index, or a `[→ view figure @ <tag>](permalink)` line at the top of each figure's section.
- Keep the local `repos/.../path` path too — it's still useful for readers with the wiki checked out who want to view offline.
- If updating an existing note to add permalinks, **also** update any prior notes in the same topic that reference the same figures, for consistency.
- When the submodule is bumped to a newer version, re-check any notes whose permalinks reference the old SHA — decide per note whether to repoint (if the figure content didn't change semantically) or leave pinned to the old SHA (if the note's analysis is tied to that version's specifics).
