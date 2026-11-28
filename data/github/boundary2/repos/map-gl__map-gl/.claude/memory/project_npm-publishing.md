---
name: npm publishing workflow
description: How to build, version, and publish packages to npm
type: project
---

## Publish order (by dependency)
1. `@map-gl/shared` (no deps)
2. `@map-gl/vue-maplibre` + `@map-gl/vue-mapbox` (depend on shared)
3. `vue-map-gl` (depends on all three)

## How to publish
Use `scripts/publish.sh` — builds all, publishes in order, skips already-published versions.
```bash
./scripts/publish.sh              # build + publish all
./scripts/publish.sh --skip-build # publish only
./scripts/publish.sh --dry-run    # preview commands
```

## Key details
- pnpm publish: `workspace:*` auto-resolved to real versions (don't use `npm publish` directly)
- Scoped packages (`@map-gl/*`) need `--access public`
- Default registry: `https://registry.npmjs.org`
- `--no-git-checks` required (pnpm rejects unclean working trees)
- npm warns about `--git-checks` being unknown CLI config — harmless, ignore it

## To update a single package
1. Bump `version` in its `package.json`
2. `pnpm --filter <name> build`
3. `cd packages/<dir> && pnpm publish --access public --no-git-checks --registry=https://registry.npmjs.org`

## Current published versions (as of 2026-04-12)
- `@map-gl/shared@0.0.1`
- `@map-gl/vue-maplibre@0.0.1`
- `@map-gl/vue-mapbox@0.0.1`
- `vue-map-gl@0.0.2`
