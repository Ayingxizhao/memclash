---
name: keep-tool-output-small
description: "Filter every tool result at the source; unfiltered Bash and MCP output is the largest avoidable context cost"
metadata:
  node_type: memory
  type: feedback
---

In one session the context window hit 80 percent and the user asked to tighten output discipline. Bash results alone were about 15 percent of the window, and nearly all of it was avoidable.

**Filter at the source, never after.** A result that reaches the transcript is already paid for. There is no recovering it.

**The rules that produce most of the saving:**

- **Never `cat` a file.** Use `Read` with `offset` and `limit`, or `sed -n 'A,Bp'`.
- **Pipe every command through `head`, `tail` or `grep`.** Especially `git diff`, `git log`, test runs and CI logs.
- **Test runs:** `... -q 2>&1 | grep -E "^FAILED|passed|failed" | tail -3`. The pass count and any FAILED lines are the whole signal.
- **Delegated agent reports:** cap the output in the invocation itself, for example `| tail -40`, and `Read` only the tail of the output file afterwards. Never read a whole report.
- **CI logs:** grep for the failure signature rather than downloading the log. `gh api .../jobs/<id> --jq '.steps[] | select(.conclusion=="failure")'` names the failing step in one line.
- **MCP reads:** always pass `--jq` or a `fields` parameter when the tool has one. An issue list that asks only for id, title and status costs a fraction of the default, and a single issue fetch returns the entire description, so only fetch it when the body is genuinely needed.
- **`git diff`:** `--stat` first, then a targeted `grep -E "^[-+]"` on the one file that matters.
- **Health and status endpoints:** pipe through `python3 -c` or `jq` to print the one field, not the whole document.

**The reasoning trap this fixes.** Fetching everything feels safer, as though more context means fewer mistakes. It does not. It buys nothing and it brings compaction forward, which loses far more than the filter would have. When a filtered result turns out to be insufficient, run a second narrow command; two small reads beat one large one.

**Why:** every byte of tool output stays in the window until compaction, and compaction loses detail the session still needed.

**How to apply:** filter every command and MCP read at the source with the rules above, and widen only with a second narrow read. Related: the `jig:principle-guard-the-context-window` skill, and the `jig:principle-verify-refactors-against-base-commit` skill for what actually needs verifying, which is a small number of specific claims rather than whole outputs.
