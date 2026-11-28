---
name: Vue component implementation patterns
description: Pitfalls and recommended patterns for Vue 3 component implementation (common to Map/Marker/Popup etc.)
type: feedback
---

- **Use `h()` not JSX**: tsup/esbuild does not support JSX syntax in .ts files. Vue component render functions should uniformly use the `h()` function
  - **Why:** JSX requires extra configuration (babel-plugin-jsx / vite-plugin-vue-jsx), and tsup does not natively support Vue JSX transform
  - **How to apply:** All Vue component render sections use `h('div', {attr: val}, children)` form

- **Use static arrays to build callbacks, don't access emit internals**: `emit.$.args` does not exist in Vue 3 defineComponent setup. Maintain a `CALLBACK_EVENTS: (keyof MapCallbacks)[]` static array and iterate over it to build callbacks
  - **Why:** Vue 3's emit function has no `$.args` property; this is a React pattern. TypeScript DTS builds will error on it
  - **How to apply:** In emit-bridging components like map.ts, always use predefined static arrays to build callbacks

- **emits are not props, cannot be read from `props.onError`**: After `onError` is declared in emits, it is not part of props. Use `emit('onError', ...)` directly for error handling
  - **Why:** Vue 3 distinguishes props and emits; emits do not appear in the props object. `props.onError` will throw TS2551
  - **How to apply:** When needing to emit events, use `emit('eventName', payload)`, don't try to read from props

- **Optional string props need `??` fallback when passed to functions**: `props.id` type is `string | undefined`, passing to `(id: string) => void` requires `props.id ?? 'default'`
  - **Why:** TypeScript strict mode doesn't allow assigning `undefined` to `string` parameter
  - **How to apply:** All optional string props should have `?? defaultValue` when passed as arguments

- **MapInitOptions props passthrough via attrs**: Core props are explicitly declared in defineComponent; MapOptions init fields are dynamically collected from `attrs`, avoiding manually listing 50+ fields
  - **Why:** MapOptions has many fields and the two libraries differ slightly; explicit listing has high maintenance cost and is prone to type mismatches
  - **How to apply:** Maintain an `INIT_OPTION_KEYS` constant array, extracting corresponding values from attrs to pass to the bridge class

- **Layered build error diagnosis**: ESM/CJS build errors (syntax issues) and DTS build errors (type issues) are separate. Fix syntax to get ESM/CJS passing first, then fix types for DTS
  - **Why:** tsup builds in three steps (ESM → CJS → DTS); ESM/CJS use esbuild (no type checking), DTS uses tsc (strict type checking)
  - **How to apply:** When encountering build failures, look at ESM/CJS errors first to fix syntax, then DTS errors to fix types
