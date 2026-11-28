---
name: Inline method rule
description: Short simple methods may be inline; anything with loops or >4 lines goes in .cc
type: feedback
---

Methods of up to 4 lines with no loops may be defined inline in the struct/class definition.
Everything more complex goes out-of-line in the `.cc` file.

**Why:** User prefers inline defs and would use them universally in a C++ modules world, but LLVM's build system isn't modules-ready yet, so header/TU separation is the practical constraint. Rule exists to be consistent with current C++ norms, not because inline is disliked.

**How to apply:** Before writing a method body in a header, check: does it have a loop? Is it more than 4 lines? If yes to either, put it in the `.cc`.
