---
name: prefers-in-repo-deploy-config
description: User prefers infra/deploy config committed in the repo over interactive/local CLI setup
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b24cf6ca-e170-4441-9ed6-4783473e3826
  modified: 2026-08-03T22:01:38.264Z
---

The user prefers **infrastructure and deploy configuration to live in the repo** (e.g. a GitHub Actions workflow) rather than being set up via interactive/local CLI commands. When offered a local `wrangler login` path they rejected it: *"no, I prefer this from the github action. I want my deploy config in the repo code as much as possible."*

**Why:** reproducibility and no dependence on machine-local state; also their Windows machine hits recurring `EBUSY` errors running `npx wrangler` locally.

**How to apply:** when proposing deploy/CI/infra changes, default to committed config (workflows, config files) over "run this command on your machine."
