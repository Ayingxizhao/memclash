---
name: Don't use single-letter parameter names in comments
description: Code comments must not rely on single-letter parameter names (M, F, B, V, etc.) to be intelligible; spell out the noun instead.
type: feedback
---

Code comments and documentation must read on their own, without the reader
needing to glance at the function signature for context. Single-letter parameter
names like `M` for module, `F` for function, `B` for basic block, `V` for value
are an LLVM-house idiom — they're fine *as parameter names* (LLVM source uses
them everywhere), but they leak into comments where they become opaque.

**Bad:**

    // Runs the optimisation pipeline over every defined function in M.

**Good:**

    // Runs the optimisation pipeline over every function in the given module
    // that has a body.

**Why:** Comments are read by people who may not have the surrounding signature
open — code review tools, grep output, AI assistants summarising the file, future
contributors skimming. The cost of spelling out "the module" instead of "M" is
two words; the cost of being clear once you've already lost the reader is
restarting the explanation.

**How to apply:**

- In comments, refer to entities by their type-noun (the module, the function,
  the basic block, the value) rather than by the parameter letter.
- If a comment really needs to name a specific parameter, write it out:
  "every function in `module` that has a body" reads fine and disambiguates
  if there's more than one candidate noun in scope.
- This applies regardless of whether the surrounding code is LLVM-flavoured or
  pinp-internal. The LLVM-style single-letter parameter *names* themselves
  remain acceptable; the constraint is only on comment text.
