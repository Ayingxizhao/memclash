---
name: ViewState controlled mode reactivity
description: Map component watch must explicitly access viewState nested properties, and must not use flush:'sync'
type: feedback
---

Two pitfalls when the Map component's watch tracks changes inside `viewState`:

1. **`{...props}` shallow spread doesn't track nested changes**: When a `reactive()` object is passed as a prop, the watch getter must explicitly access inner fields (e.g. `vs?.longitude`), otherwise Vue won't track nested property changes.
2. **`flush: 'sync'` causes infinite loops**: setProps → resize → emit onMove → viewState change → watch → setProps synchronous death loop. Remove `flush: 'sync'` and use the default `pre`.
3. **`viewState.width/height` being 0 triggers loops**: `_updateSize` checks size mismatch and calls `resize()`; width=0 never matches actual dimensions. Add a `width > 0 && height > 0` guard.

**Why:** react-map-gl uses React setState which naturally avoids these issues; Vue's reactive proxy + watch mechanism requires explicit handling.

**How to apply:** Whenever the Map component watches prop changes to sync to the bridge, destructure every field of viewState in the getter, and don't use `flush: 'sync'`.
