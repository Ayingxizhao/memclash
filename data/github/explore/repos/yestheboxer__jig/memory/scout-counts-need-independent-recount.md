---
name: scout-counts-need-independent-recount
description: "A subagent's counts are only as precise as the discriminator in its prompt; recount by a different method before any number becomes a load bearing claim"
metadata:
  node_type: memory
  type: feedback
---

A delegated scan reports what its prompt told it to match, which is rarely what you meant. In one mapping of a shared data hook in a front end app, a scout was asked which files reference each returned member. It reported `error` in 47 consumers and `isLoading` in 37. Parsing the actual `const { ... } = useHook(` destructure blocks gave 1 and 2. The scout had grepped each name anywhere in each file, so every local state variable, `catch (error)` and unrelated prop counted.

Those numbers had already gone into a design doc whose central claim was that the hook's shared state is effectively private. The wrong counts inverted it. An earlier hand grep had also been wrong in the other direction (zero), so both cheap methods failed and only parsing settled it.

**Why:** a number in a design doc gets treated as established fact by every later reader, including the implementer who never re derives it. A grep for a common identifier like `error` or `data` has a false positive rate near 100 percent in a typical codebase.

**How to apply:** put the discriminator in the dispatch prompt, not the string to match ("count only names bound inside a `const { ... } = useHook(` destructure" rather than "grep for each member name"). Then recount anything load bearing by a DIFFERENT method before writing it down, and prefer a real parse (a `python3` heredoc over the file) to a grep for structural questions. Also check the non conforming cases the parse misses: whole object bindings like `const api = useHook()` and injected object parameters hide real usage from any destructure based count. State the corrected number and the method in the doc so the next reader knows which to trust. Related: the `jig:principle-verify-delegated-work` skill for the same distrust applied to any delegate's report, and the `jig:multitask` skill for the model routing this refines.

**Two different methods can share one blind spot.** A scout reported a large handler module as untested. A recount by dotted import path agreed. Both were wrong: the tests imported it as `from pkg.handlers import query_handler as handler_module`, which neither a dotted path regex nor the scout's method matched. A third pass that also matched `from <pkg> import <name>` in single line and parenthesised forms found over a hundred test functions against it. "Two methods agree" is not verification when both encode the same assumption about how code is imported. For import based counts, match all four forms: dotted `from a.b.c import`, `import a.b.c`, `patch("a.b.c`, and `from a.b import c`.
