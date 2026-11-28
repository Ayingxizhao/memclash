---
name: Maplibre-gl v5 migration notes
description: API changes and caveats when upgrading from maplibre-gl v4 to v5
type: feedback
---

## WebGL context options moved to canvasContextAttributes

In v5, `antialias`, `preserveDrawingBuffer`, and `failIfMajorPerformanceCaveat` are no longer top-level MapOptions fields; they must be placed inside the `canvasContextAttributes` object. The `INIT_OPTION_KEYS` array needs to be updated accordingly.

**Why:** v5 refactored WebGL initialization config to support choosing WebGL version (`contextType`); all canvas-related options are consolidated into `canvasContextAttributes`.

**How to apply:** Remove these three keys from the Map component's `INIT_OPTION_KEYS` and add `canvasContextAttributes`. Users pass it via attrs like `:canvasContextAttributes="{ antialias: true }"`.

## getProjection/setProjection are standard APIs in v5

In v4, `getProjection()` and `setProjection()` were optional methods (requiring `?.` and `@ts-ignore`); in v5 they are standard Map instance methods.

**Why:** v5 introduced globe projection and projection type expression support; projection became a first-class citizen.

**How to apply:** Remove optional chaining (`map.getProjection?.()`) and `@ts-ignore` comments for `map.setProjection?.()` in the bridge class.

## Marker is inside canvasContainer in both v4 and v5

In v5, `marker.addTo(map)` adds the marker element to `map.getCanvasContainer()` (same as v4). This means DOM click events on the marker bubble up to the canvas container, triggering the map's 'click' event.

**Why:** maplibre-gl always places markers inside the canvas container for correct positioning and event handling.

**How to apply:** Consider the interaction between marker click and map click when designing. Popup's `closeOnClick: true` can be affected by the map click event triggered by marker clicks.
