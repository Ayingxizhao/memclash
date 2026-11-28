---
name: Tooling decisions
description: Build toolchain and development environment decision records
type: project
---

- **ESLint deferred**: Phase 0 only configures Prettier; ESLint is left for later phases as needed, to avoid spending time on lint rules early on
- **tsup external**: mapbox-gl, maplibre-gl, and vue are all marked as external and not bundled into output
- **Playground aliases must use absolute paths**: In vite.config.ts, aliases must use `resolve(__dirname, '..')` to build absolute paths, and point to `src/index.ts` files rather than directories. Relative paths cause `Failed to resolve import` errors

**Why:** Relative paths like `../packages/vue-maplibre/src` cannot be correctly resolved during Vite's import analysis phase; pointing to a directory causes EISDIR errors
**How to apply:** When modifying vite.config.ts aliases, always use `resolve(__dirname, '..')` to build paths, pointing to specific entry files (e.g. `src/index.ts`)
