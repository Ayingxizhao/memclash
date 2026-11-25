---
name: TODO — NIXL KV connector in Dynamo case study
description: Pending deep-dive into how NIXL connector is used specifically inside NVIDIA Dynamo's PD orchestration (not the generic vLLM NIXL connector path, but the Dynamo-integrated variant)
type: project
---

# TODO: NIXL KV Connector in Dynamo — Case Study

**Logged:** 2026-04-21 (deferred during pd-disaggregation walkthrough)

**What:** After the generic PD walkthrough (figures 1–4 from `repos/vllm/docs/features/disagg_prefill.md`) completes, come back and do a focused case study specifically on how NVIDIA Dynamo wraps / uses the NIXL KV connector.

**Why:** Dynamo is the most production-grade PD orchestrator currently paired with vLLM, and the "NIXL as seen from Dynamo" story involves pieces that aren't in the vLLM repo itself — Dynamo's own routing / autoscaling / planner layers sit above the `kv_transfer_params` protocol and make non-trivial choices (cache-aware routing, SLA-driven scaling, P/D instance pool management). The generic vLLM-side NIXL code tells you *how* the transfer happens but not *why this particular prefill engine* was picked for *this particular request*.

**How to apply:**
- Trigger this after the user finishes the current `workflow.png` / figure 4 walkthrough and any other directly-continuing questions on the vLLM PD internals.
- Grounding material: `repos/dynamo/` submodule in mlsys-wiki (check if already present; if not, add it), plus Dynamo's public docs on P/D.
- Scope: cover (a) Dynamo's router's KV-cache-awareness heuristics, (b) how it decides which prefill instance gets a request, (c) how `kv_transfer_params` flows through Dynamo's proxy/planner layers differently from the toy `toy_proxy_server.py`, (d) Dynamo's handling of engine autoscaling vs. ongoing NIXL transfers.
- Output: a new raw note under `topics/pd-disaggregation/raw/notes/` with tag `dynamo` and cross-references to the 2026-04-21 control/data-plane note.

**Don't forget:** This is a separate thread from "deep-dive the generic vLLM NIXL connector in `vllm/distributed/kv_transfer/kv_connector/v1/nixl/connector.py`". That one is lower-level (wire protocol, agent handshake, block copy mechanics); this Dynamo case study is higher-level (orchestration, routing policy, production topology). Do both eventually; this TODO tracks the Dynamo-specific half.
