---
name: AOT compiler roadmap
description: Future plan to add ahead-of-time compilation alongside JIT
type: project
---

pinp will eventually support compiling source to a native executable (AOT), separate from the JIT path.

**Why:** JIT will remain for REPL and script execution only. AOT compilation is a distinct target.

**How to apply:** Built-in constant injection (and likely other JIT-specific setup) must not live in `jit.cc` long-term — it needs to move into `CodegenContext` so both the JIT and AOT paths can share it without duplication. Keep this in mind when designing codegen APIs: anything that both paths need belongs on `CodegenContext`, not on `PinpJIT`.
