---
name: Bridge architecture: Mapbox vs Maplibre
description: Mapbox and Maplibre bridge layers are fundamentally different and must not be forced into a shared abstraction
type: feedback
---

Mapbox (mapbox-gl) and Maplibre (maplibre-gl) have completely different camera control APIs, so bridge layers must be implemented independently:

- **Mapbox**: Uses ProxyTransform (JS Proxy wrapping transform), requires hacking `_render`/`_renderTaskQueue.run`/`jumpTo`, high complexity
- **Maplibre**: Uses native `transformCameraUpdate` callback, returns a changes object → `map.jumpTo(changes)`, simple and direct
- **Shared package**: Only put truly shared code — `deep-equal.ts`, `style-utils.ts`, basic type definitions
- **Style differences**: Mapbox has `fog`/`light`/`terrain`; Maplibre has `sky`/`light`/`terrain`/`projection` (including globe)
- **ViewState**: Mapbox includes `elevation` field, Maplibre does not
- **Environment variables**: React uses `REACT_APP_MAPBOX_ACCESS_TOKEN`, Vue uses `VITE_MAPBOX_ACCESS_TOKEN`

**Why:** The internal APIs of the two libraries are too different; forcing a shared bridge class adds unnecessary complexity and maintenance burden
**How to apply:** Maintain fully independent bridge implementations for Mapbox and Maplibre, only putting pure utility functions and intersection types in the shared package
