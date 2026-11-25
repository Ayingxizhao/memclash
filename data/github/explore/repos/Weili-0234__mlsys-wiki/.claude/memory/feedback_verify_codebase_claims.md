---
name: Verify codebase architectural claims before stating them
description: User expects claims about vLLM (and other codebases) internals to be grounded in current code, not recollection
type: feedback
---

Any statement about the **current structure** of a codebase — "X is folded into Y", "module A was replaced by B", "abstraction Z still exists" — must be verified against the actual files (Grep / Read / ls) before being stated, not offered from training-era memory.

**Why:** On 2026-04-20 the user caught me claiming "vLLM v1 folded LookupBuffer + Pipe into Connector" while walking through `repos/vllm/docs/features/disagg_prefill.md`. When they asked me to double-check, the truth was that in `repos/vllm` @ v0.19.1, LookupBuffer and Pipe **do not exist at all** — the directories are gone, grep returns zero hits, and `kv_connector/base.py` is now a 7-line alias re-exporting `KVConnectorBase_V1`. The v1 abstraction model is fundamentally different (scheduler/worker split + layer-wise `save_kv_layer` / `wait_for_layer_load`), not a repackaging of v0. The user is a careful reader who notices imprecision; a confidently-stated wrong architectural claim costs more trust than saying "let me check."

**How to apply:**
- When explaining a file/doc that may be mixing v0 and v1 (or old and new) concepts, explicitly identify which parts describe which, and verify by opening the referenced code.
- For vLLM PD work specifically: `repos/vllm/vllm/distributed/kv_transfer/kv_connector/v1/base.py` is the current truth; `base.py` one level up is a 7-line alias. The old `kv_lookup_buffer/` and `kv_pipe/` concepts are gone, not relocated.
- When uncertain, prefer "let me check" + one Grep / Read over confident paraphrase. The user welcomes the extra round trip.
