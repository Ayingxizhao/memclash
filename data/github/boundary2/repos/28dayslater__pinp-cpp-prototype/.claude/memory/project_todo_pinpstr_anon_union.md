---
name: PinpStr anonymous union fix
description: Name the union in PinpStr to eliminate -Wgnu-anonymous-struct extension warning from clangd
type: project
---

`lib/immutable-string.hh` `PinpStr` has an anonymous union containing two named struct members (`heap`, `inl`). clangd flags this as a GNU extension (`-Wgnu-anonymous-struct`).

Fix: give the union a member name (e.g. `u`) and update all access sites in `lib/immutable-string.cc` and `lib/immutable-string.hh` to use `str_.u.heap.ptr` / `str_.u.inl.tag_len` etc.

**Why:** Not a correctness issue; g++ accepts it silently. Deferred until the first real string feature work to avoid churn.

**How to apply:** Do this fix at the start of the next strings iteration, before adding new string features.
