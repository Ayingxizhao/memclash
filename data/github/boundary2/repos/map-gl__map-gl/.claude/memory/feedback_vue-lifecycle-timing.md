---
name: Vue 3 lifecycle timing for overlay components
description: Child onMounted fires before parent, async onMounted leaves context unavailable, use watch instead of onMounted to access context
type: feedback
---

## Vue 3 child onMounted fires before parent

In Vue 3, children's `onMounted` fires **before** the parent's `onMounted`. If the parent's `onMounted` is `async` (contains `await`), context is set in a microtask, and children's `onMounted` gets the initial empty value.

**Why:** Vue 3 lifecycle order is: children setup → children render → children mounted → parent mounted. The `await` in an async `onMounted` defers subsequent code to a microtask, while children's `onMounted` has already completed in the synchronous phase.

**How to apply:** All overlay components depending on Map context (Marker/Popup/Source/Layer/Control) should not use `onMounted` to directly read context; instead use the `useMapContext` composable (internally uses `watch` + `immediate: true`) to wait for context availability before initializing. File: `packages/vue-maplibre/src/components/use-map-context.ts`.

## Popup addTo must be deferred to setTimeout(0)

In maplibre-gl v5, the map's click event is dispatched with a delay (handleEvent → click → fire chain). If popup does `addTo(map)` in a Vue microtask and registers a `closeOnClick` handler, the pending map click arrives shortly after and immediately closes the just-opened popup.

**Why:** v5's click dispatch executes with delay in the `handleEvent` callback; after popup's `addTo` registers a click listener, the pending click arrives right after.

**How to apply:** In the Popup component, `popup.setDOMContent(container)` executes synchronously, but `popup.addTo(map.getMap())` is wrapped in `setTimeout(0)` to ensure the pending click is processed first before registering the close handler.

## Popup closeOnClick vs v-if control race condition

When Popup uses `v-if="selectedCity"` + `@onClose="selectedCity = null"` + `closeOnClick: true`, clicking another marker triggers two synchronous events: `selectCity(newCity)` and map click → popup close → `onClose` → `selectedCity = null`. The final `null` overwrites the new selection, requiring two clicks.

**Why:** `selectCity` and `onClose` execute in the same synchronous block; Vue batches reactive updates, and the final value depends on the last write.

**How to apply:** The recommended pattern is `closeOnClick: false` + marker toggle behavior (clicking the same marker closes), avoiding the `onClose` vs `selectCity` race.
