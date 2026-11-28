---
name: feedback-no-scoring-changes-without-permission
description: "Never change an app's scoring/eval attributes (waivers, criteria) without explicit permission"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d3dce43e-e946-49b3-959b-57e3ba431cc0
---

Never change the scoring attributes for an application without explicit permission from Erwin.

This covers anything that alters how a run is judged: `APP_WEAVER_WAIVERS` and other eval-side
config in `apps/<app>/config.sh`, `EVALUATION.md` criteria, and the eval logic in `src/evaluation.ts`
/ `src/weaver.ts`. Suggest-and-ask; do not edit these on my own initiative even when a failure looks
like a tooling/library limitation rather than a skill defect.

**Why:** waiving or loosening a criterion silently hides a real signal about skill/library quality and
overfits the harness to today's apps. Deciding what is a legitimate library limitation vs a skill gap
is Erwin's call, not mine. Related: [[project-goal-portable-skills]], and the waiver mechanism itself
[[project-configurable-semconv-expectations]].

**How to apply:** when a bucket fails on something the agent can't fix (e.g. beaverhabits' SQLAlchemy
0.49b2 emitting old `db.*` semconv, or an ASGI/library passthrough attribute), report it and propose a
waiver — then wait for explicit approval before touching `config.sh` / criteria. This mirrors the
[[feedback-no-preamble-edits]] posture (suggest-and-ask, never bake in).
