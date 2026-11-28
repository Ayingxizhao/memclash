---
name: String struct layout design
description: Planned pinp string layout — 16-byte SSO with mutability flag, for JIT+AOT compatibility
type: project
---

Pinp strings must use a custom struct (not std::string) because AOT cannot depend on the C++ runtime ABI. The layout must be defined as an LLVM struct type usable in both JIT and AOT codegen.

**Layout (16 bytes):**

```cpp
union {
    struct {          // heap
        char    *ptr;
        uint32_t len;
        uint32_t cap;
    };
    struct {          // inline (immutable only)
        char    buf[15];
        uint8_t tag_len; // bit 7: is_heap | bit 6: is_mutable | bits 3-0: inline length
    };
};
```

**Rules:**
- `is_heap=0, is_mutable=0` — inline, immutable (SSO, up to 15 chars)
- `is_heap=1, is_mutable=0` — heap, immutable
- `is_heap=1, is_mutable=1` — heap, mutable
- `is_heap=0, is_mutable=1` — illegal, never constructed

**Key decisions:**
- Strings are immutable by default; mutable strings always heap-allocated (no mutable inline)
- Heap length capped at uint32_t (4GB) — leaves 32 bits free vs a 64-bit length field
- SSO max 15 chars; inline length needs only 4 bits (0–15), leaving bit 5 spare in tag_len
- Layout must be committed to before codegen is written — changing it later touches all string codegen

**Why:** AOT compatibility. std::string is fine for JIT but its layout is a C++ runtime ABI contract that generated AOT code cannot rely on.
