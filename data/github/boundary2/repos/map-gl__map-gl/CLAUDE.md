# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
pnpm build              # Build all packages (tsup)
pnpm dev                # Start playground (dev mode, aliases point to source)
pnpm preview            # Start playground using built dist artifacts (run build first)
pnpm test               # Run unit tests
pnpm test:watch         # Run tests in watch mode
pnpm test:e2e           # Run E2E tests (sequential, 60s timeout)
pnpm typecheck          # TypeScript check all packages
```

Run a single test file: `pnpm vitest run packages/vue-maplibre/src/components/map.test.ts`

## Architecture

This is a pnpm monorepo that provides Vue 3 components for MapLibre GL JS and Mapbox GL JS, modeled after [react-map-gl](https://github.com/visgl/react-map-gl).

### Package Layout

```
packages/shared/        → @map-gl/shared          # Types and utilities (map-library-agnostic)
packages/vue-maplibre/  → @map-gl/vue-maplibre     # MapLibre GL JS bridge + components
packages/vue-mapbox/    → @map-gl/vue-mapbox       # Mapbox GL JS bridge + components
packages/vue-map-gl/    → vue-map-gl               # Umbrella package re-exporting both
```

Users import from `vue-map-gl/maplibre` or `vue-map-gl/mapbox`. The scoped packages (`@map-gl/*`) can also be imported directly.

### Bridge Pattern

Each map library has its own bridge class (`packages/vue-maplibre/src/maplibre/maplibre.ts`, `packages/vue-mapbox/src/mapbox/mapbox.ts`) that wraps the native map instance. The two bridges are **independent** — they share types/utilities from `@map-gl/shared` but have separate implementations because the underlying camera control APIs differ fundamentally:

- **MapLibre**: uses native `transformCameraUpdate` callback
- **Mapbox**: uses ProxyTransform (JS Proxy wrapping transform)

Never try to abstract bridge logic into `@map-gl/shared`.

### Component Architecture

Components live in `src/components/` within each bridge package:

- **Map** — root component, creates the bridge instance, provides context to children via `MapProvider`/`useMap()`
- **Overlays** (Marker, Popup, Source, Layer) — access map context via `useMapContext()` composable (not `onMounted` directly, due to Vue child-before-parent mount order)
- **Controls** — use `useControl()` composable for adding native maplibre/mapbox controls

Components use `h()` for render functions (no JSX — tsup doesn't support Vue JSX transform).

### Key Conventions

- `INIT_OPTION_KEYS` array in bridge classes: defines which props pass through to the native map constructor
- `CALLBACK_EVENTS` static array: used to build event callbacks from emits
- Overlay components use `watch` + `immediate: true` (not `onMounted`) to wait for map context availability
- Map watch getters must explicitly destructure viewState fields for Vue reactivity tracking; never use `flush: 'sync'`
- `tsup.config.ts` externalizes `maplibre-gl`/`mapbox-gl`, `vue`, and `@map-gl/shared`

### Playground Modes

- **dev** (`pnpm dev`): vite aliases resolve `@map-gl/*` and `vue-map-gl/*` to TypeScript source files (HMR friendly)
- **preview** (`pnpm preview`): no aliases, resolves via pnpm workspace links to built dist files

### Tests

- Unit tests: Vitest with happy-dom, colocated as `*.test.ts` alongside source files
- E2E tests: `e2e/` directory, uses puppeteer-core against playground pages
