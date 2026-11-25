# Memory Index — mlsys-wiki project

Memory scoped to the mlsys-wiki knowledge base and its submoduled source repos. Version-controlled with the wiki repo and synced across devices — **all paths in these memory files are relative to the wiki repo root**, never absolute.

This index is NOT auto-loaded — read it explicitly at the start of any session touching mlsys-wiki work.

- [Memory location rule](feedback_memory_location.md) — project-scoped memory lives here with repo-relative paths, not in the global auto-memory path
- [Verify codebase architectural claims](feedback_verify_codebase_claims.md) — grep/read before claiming "X was folded into Y"; caught on a vLLM v1 connector claim on 2026-04-20
- [Pin figure permalinks to commit SHA](feedback_pin_figure_permalinks.md) — when referencing images from submoduled repos in wiki notes, include a GitHub permalink pinned to the exact submodule commit (not a branch name, not just a local path)
- [TODO: NIXL in Dynamo case study](project_todo_nixl_in_dynamo_case_study.md) — pending deep-dive on how Dynamo wraps/uses NIXL (orchestration layer, not wire layer); triggered after current PD walkthrough finishes
- [TODO: get_attention_context(layer_name) lookup](project_todo_attention_context_lookup.md) — pending study of how layer_name string is reverse-mapped to kv_cache tensor + attn_metadata via forward_context registry; companion to the `maybe_transfer_kv_layer` decorator walkthrough
