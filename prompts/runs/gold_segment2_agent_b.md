# Task: segment agent-memory files into a fixed rule list

<!-- ===== FILLED IN FOR THIS RUN ===== -->
ANNOTATOR: agent_b
MODE: segment
RULES_FILE: (not used in segment mode)
OUTPUT: data/gold/rules2_agent_b.json
FOLDERS (paths relative to /Users/yingxizhao/dev/cs2520/projects; some are inside hidden
`.claude/` directories, so use exact paths or `ls -a`). In OUTPUT, write `dir` exactly as the
path after the repo folder (e.g. `.claude/memory`), not the full path:
| repo | memory folder | .md files |
|---|---|---|
| SealProjectDAO/seal-dao-public | data/github/repos/SealProjectDAO__seal-dao-public/.claude/projects/-Users-bechaderenaud-work-seal-seal-dao-master/memory | 9 |
| KuangHu/DL_RNA_guide_editor_positive_generator | data/github/repos/KuangHu__DL_RNA_guide_editor_positive_generator/.claude/memory | 5 |

Independence: do not read any other file under data/gold/, data/open_coding/, data/runs/,
or data/llm_cache.jsonl. Do not use an LLM API or script to segment; scripts only for
mechanical help (listing files, checking quotes). Do not modify any file except OUTPUT.
<!-- ================================== -->

## Context
This is a research project on coding-agent memory: a folder of markdown files (one rule per
file, usually written by the agent after a user correction, plus a `MEMORY.md` index).
This step produces ONE fixed list of rules per folder. Later, several annotators label pairs
of these rules, so the list must be complete, atomic, and verbatim. Do not judge conflicts
here.

## Rules for segmentation
- Read EVERY `.md` file in each folder in full, including `MEMORY.md`. Check the file count
  matches the table. Ignore the repo's root `CLAUDE.md` and `repo.json`.
- A RULE prescribes, prohibits, or permits an agent behavior (do X / never X / prefer X /
  X is allowed), possibly under a condition (when / if / for / until ...).
  Include: "How to apply" instructions, imperative headings, agreed conventions, explicit
  permissions, operative user preferences ("wants X" that tells the agent what to do).
  Exclude: facts about the project/user/code, rationale ("Why: ..."), history, past
  mistakes, frontmatter fields other than `description`.
- **Frontmatter `description` can carry rules.** If it states an instruction, extract it as
  its own rule (same file), even if it summarizes the body: descriptions sometimes add or
  change details (e.g. "~3 sentences per idea" appears only in a description).
- If a `CLAUDE.md` file is listed in FOLDERS, segment it too (file = `CLAUDE.md`); it is
  loaded in the same session as the memory folder.
- **Index lines are rules too.** Each `MEMORY.md` entry that states an instruction is
  extracted as its own rule (file = `MEMORY.md`), even if it only restates a file.
- **Atomic = one action + its condition.** Split conjunctions of actions:
  "delete the branch locally and on the remote" -> 2 rules. Do not split a single action
  with several examples ("articles, books, RFCs") or a condition from its action.
- **A procedure is one rule.** Numbered steps, a command/code block, or a how-to table that
  together describe one procedure = ONE rule ("follow procedure X", quote = its heading or
  first line). Split out a step only if it carries its own condition or prohibition (e.g.
  "**Never use plain `gh`.**"). A table that assigns different behavior per row (e.g. which
  tool for which operation) is one rule per row.
- **Explicit exceptions stay with their rule**: "X, except Y" is one rule (the exception is
  part of its condition). An exception stated in a separate sentence is a separate rule.
- `quote`: the shortest contiguous span that states the rule, copied EXACTLY (same words and
  punctuation; line breaks may be written as spaces). No joining of separate spans.
- `rule`: self-contained imperative restatement including condition and scope (resolve
  "this", "it", and which project/course/tool it applies to).
- `modality`: `obligation` (must/always/do), `prohibition` (never/don't), `permission`
  (may/is allowed/is sufficient), `preference` (prefer/values/wants).
- IDs: R1, R2, ... per folder, in file order (files sorted by name).

## MODE = segment
Write OUTPUT:
```json
{"annotator": "<name>", "mode": "segment",
 "folders": [{"repo": "owner/name", "dir": "...",
   "rules": [{"id": "R1", "file": "...", "quote": "...", "rule": "...",
              "modality": "obligation"}]}]}
```

## MODE = review
Read RULES_FILE and the same folders. Check every rule against the guidelines above and
check for missing rules. Do not rewrite the list; write only proposed changes to OUTPUT:
```json
{"annotator": "<name>", "mode": "review", "reviewed": "<RULES_FILE>",
 "changes": [{"repo": "owner/name", "action": "add|remove|split|merge|edit",
   "ids": ["R3"], "proposal": {"file": "...", "quote": "...", "rule": "...", "modality": "..."},
   "reason": "..."}]}
```
If no change is needed for a folder, write nothing for it. Disagreements are settled by the
project lead before labeling starts.
