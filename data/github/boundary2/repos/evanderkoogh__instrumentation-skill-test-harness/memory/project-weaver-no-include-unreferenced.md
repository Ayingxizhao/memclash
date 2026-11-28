---
name: project-weaver-no-include-unreferenced
description: "The harness NOW runs weaver live-check WITH --include-unreferenced, as a temporary workaround for the released-weaver crediting gap. Will be removed once weaver credits imported/referenced standard attrs. (Reversed the earlier no-flag design.)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 30cd11f6-a60f-4ba7-b066-d6bd1a501eb5
---

**Reversed 2026-07-02.** The harness's `weaver registry live-check` invocation
(`docker/lifecycle.sh`) now **passes `--include-unreferenced`**. Erwin decided this because on any
currently-released weaver it is **not possible** to make live-check credit the standard semconv
attributes an app emits without the flag — so without it `weaver_live_check_*` is unpassable by any
registry the agent could author (see [[reference-weaver-livecheck-crediting-unreleased]]).

**This is explicitly a temporary workaround.** Remove `--include-unreferenced` once weaver ships a
build where a proper `imports:` block (or plain references) credits standard/imported attributes at
live-check without the flag (weaver `main` PRs #1267/#1442). At that point, restore the stricter
no-flag posture and fix the skill's registry recipe to reference/import every emitted standard attr.

**What the flag changes for scoring:** with `--include-unreferenced` ON, weaver credits attributes
present in the resolved registry's dependencies even when the registry doesn't explicitly reference
them — so standard attrs (`http.request.method`, `url.path`, `server.address`, `db.*`) no longer show
up as `missing_attribute` violations just because the registry didn't enumerate them. The registry
still must declare its `dependencies:` correctly (see [[reference-weaver-registry-import-syntax]]).

**Same flag, opposite direction for the verification skill (2026-07-02).** The `otel-verification`
skill now runs `weaver registry live-check` **offline** (fed a JSON sample file built from Honeycomb
columns — tagged `{"attribute":{"name":...,"value":...}}` samples, `--input-source file --input-format
json --no-stream`) to compare emitted attrs vs the app's registry. There it **must NOT** pass
`--include-unreferenced`: the flag folds the whole upstream semconv into the registry universe
(broadleaf: 14 authored attrs → 741), which flattens `registry_coverage` to ~0 and buries the
"defined but never emitted" signal (`seen_registry_attributes` count-0) under attrs the app never
touches. Without the flag, `seen_registry_attributes` = just the authored registry (count-0 is
meaningful) and standard attrs the app emits surface under `seen_non_registry_attributes`, where the
agent credits real conventions via `search_semconv` and flags only the genuinely-unknown remainder.
So: harness scoring wants the flag ON (crediting); verification wants it OFF (coverage/staleness).

Related: [[project-configurable-semconv-expectations]], [[project-two-box-skill-model]].
