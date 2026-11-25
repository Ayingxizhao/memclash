---
name: TODO — get_attention_context(layer_name) lookup mechanism
description: Pending study of how vLLM's attention code looks up kv_cache + attn_metadata keyed by layer_name through the forward_context
type: project
---

# TODO: `get_attention_context(layer_name)` — layer_name → (kv_cache, attn_metadata) 反查机制

**Logged:** 2026-04-21 (deferred during `maybe_transfer_kv_layer` decorator walkthrough)

**What:** Study how `get_attention_context(layer_name)` works — specifically how the attention-layer code (inside `unified_attention_with_output`) uses `layer_name` as a key to retrieve:
- `attn_metadata` (the per-step scheduler-computed attention metadata — causal mask, block table slice, etc.)
- `kv_cache` (the actual torch.Tensor backing this layer's paged KV)
- the `self` reference for the Attention module

**Why:** This is the other half of the "layer-by-layer sync" protocol. The `maybe_transfer_kv_layer` decorator walkthrough covered the *injection points* (where `wait_for_layer_load` / `save_kv_layer` get wired into attention forward), but the lookup mechanism that turns a string `layer_name` back into tensor handles is its dependency — and it's non-trivial: it involves a forward-context-scoped registry that must be populated before forward starts and cleared after. Understanding this is required before we can meaningfully read `NixlConnector.save_kv_layer` / the MLA variant.

**How to apply:**
- Grounding file: `repos/vllm/vllm/model_executor/layers/attention/attention.py` — grep for `get_attention_context` and its setter `set_attention_context` / populator.
- Related: `repos/vllm/vllm/forward_context.py` — the per-step context manager that wraps execute_model.
- Scope: (a) who populates the layer-name → (attn_metadata, Attention module, kv_cache, layer_slot_mapping) mapping, (b) when/where it's populated in the forward lifecycle, (c) why `layer_name` (string) is used as the key instead of a direct tensor reference.

**Don't forget:** This was option **(b)** in the follow-up menu after the `maybe_transfer_kv_layer` walkthrough on 2026-04-21. Also still on the menu from that message: (a) `use_direct_call` vs `torch.ops.vllm` dispatch choice, (c) reading a concrete connector's `save_kv_layer` / `wait_for_layer_load` implementation.
