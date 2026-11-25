# Memory format

This directory holds six example memories and the index that lists them. `install.sh` seeds
`~/.claude/memory` from here when that store is empty. After that the store is yours.

## One fact per file

Each memory is one Markdown file that holds one fact, one rule, or one lesson. When a file
starts to carry two rules, split it. Small files are easier to find, to correct, and to
delete when a rule stops being true.

## Frontmatter

Every file opens with this block:

```
---
name: keep-tool-output-small
description: "One line that says when the memory applies and what it says"
metadata:
  node_type: memory
  type: feedback
---
```

- `name` matches the file name without `.md`.
- `description` is the hook. A reader must be able to decide from this line alone whether
  the body is relevant.
- `metadata.node_type` is always `memory`.
- `metadata.type` is one of four values:
  - `user`: a fact about the user, such as their role, their setup, or how they like to work.
  - `feedback`: a correction or a preference the user stated, and the rule that follows.
  - `project`: a fact about one piece of work, such as its scope, its state, or a decision.
  - `reference`: a pointer to where something lives, such as a doc, a dashboard, or a tool.

## Body

The body states the fact first, then the evidence that taught it, written as a generic
example. A `feedback` or `project` memory ends with two labelled lines:

- `**Why:**` the reason the rule exists. A rule without a reason gets argued away.
- `**How to apply:**` the concrete action, written so an agent can follow it without
  judgment calls.

Every "How to apply" line is binding. Treat it as an instruction from the user, not as a
suggestion. When two memories conflict, the more specific one wins; when that does not settle
it, ask the user.

## Links

Link one memory to another with `[[file-name]]`, the file name without `.md`. Link a jig
skill by its command name, for example the `jig:multitask` skill.

## MEMORY.md, the index

`MEMORY.md` lists every memory file, one line per file, in the form
`- [Title](file.md): hook`. It is loaded every session, so keep each line short and keep the
whole index small. Add a line when you add a file, and remove the line when you delete one.
A file that is not in the index is easy to forget.

The memory loader in `hooks/load-memory.py` injects the bodies of the other files into
context at session start, in shards that each stay under the 10,000 character cap.
