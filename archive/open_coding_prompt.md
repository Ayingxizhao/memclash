# Open-coding task: conflicts in coding-agent memory

You are an independent annotator in a research project. Coding agents (e.g. Claude Code)
keep "memory": a folder of small markdown files, each usually holding one rule the agent
wrote after a user correction. Nothing checks a new rule against existing ones, so memory
may accumulate contradictions, duplicates, and outdated rules. Your job is to read a few
real memory folders from public GitHub repos and record, carefully and by hand, what
relations between rules actually occur. The results will be used to design a formal
schema, so precise evidence matters more than volume.

## Independence rules (important)
- Another annotator does the same task. Do NOT read `data/open_coding/` (except your own
  output files), `data/runs/`, or `data/llm_cache.jsonl`.
- Do not use any LLM API or script to judge rules. Read the files yourself.
- Do not modify any file except your two output files. No network access needed.

## Input
Project root: `/Users/yingxizhao/dev/cs2520/projects`. The 5 memory folders (paths
relative to the root; several are inside hidden `.claude/` directories, so use exact
paths or `ls -a`):

| repo | memory folder | .md files |
|---|---|---|
| Consteon/web-spreadsheet-example | `data/github/repos/Consteon__web-spreadsheet-example/.claude/memory` | 6 |
| M-Hernandez/setflow | `data/github/repos/M-Hernandez__setflow/.claude/projects/-Users-miguelhernandez-Desktop-projects-setflow/memory` | 7 |
| MCMike0399/from-tcp-to-http | `data/github/repos/MCMike0399__from-tcp-to-http/memory` | 3 |
| shabelson-picker/applied_math | `data/github/repos/shabelson-picker__applied_math/memory` | 9 |
| thesteve0/local-llm-benchmark | `data/github/repos/thesteve0__local-llm-benchmark/.claude/memory` | 6 |

Read EVERY `.md` file in each folder in full, including `MEMORY.md` (the index), and
check the file count matches the table. Ignore the repo's root `CLAUDE.md` and
`repo.json` for this task.

## Step 1: list the rules (per folder)
A RULE is an instruction that prescribes, prohibits, or permits an agent behavior (do X /
never X / prefer X / X is allowed), possibly under a condition. NOT rules: facts about the
project/user/code, rationale ("Why: ..."), history, frontmatter fields. A "How to apply"
line that instructs the agent IS a rule. Split compound instructions into atomic rules
(one action each). For each rule record:
- `id` (R1, R2, ... per folder), `file`, `quote` (verbatim, shortest span that states it),
  `rule` (self-contained imperative restatement including its condition/scope).

## Step 2: check every pair of rules within the folder
Consider ALL pairs, including pairs inside the same file and pairs between `MEMORY.md`
and the files it indexes. Record every pair that has one of these relations:
- `contradiction`: there is a realistic situation where BOTH rules apply and the agent
  cannot follow both. State that situation concretely.
- `duplicate`: both rules require the same behavior in the same scope (redundant).
- `override`: one rule changes the behavior required by the other for part of its scope
  (e.g. a more specific or newer rule), without an explicit exception linking them.
- `other`: a problem that fits none of the above (e.g. index entry disagrees with the
  file, a rule refers to something that no longer applies, one rule is too vague to
  tell). Describe it.
Not a relation: rules whose scopes do not overlap; rules where one states an explicit
exception to the other ("except when ..."); rules that are merely on the same topic.
For each recorded pair give: rule ids, label, `situation` (for contradiction/override),
`explanation` (1-3 sentences), `confidence` (high / medium / low).
If a folder has no relations, say so explicitly. Do not invent relations to fill space.

## Step 3: catalog (across all folders)
- Group the issues you found into types, using your own names (open coding: do not force
  them into the labels above if a better category emerges). For each type: definition,
  count, 1-2 verbatim examples.
- Scope dimensions: what do the rules condition on? (e.g. tool, language, file path, git
  operation, task type, communication/output style, time). Count roughly.
- Hard-to-formalize rules: list rules that would be hard to encode as typed logic
  (vague: "be careful"; numeric/approximate: "~3 sentences"; temporal: "until X ships";
  preference strength: "prefer" vs "must"), with a short reason each.

## Output (write exactly these two files)
1. `data/open_coding/<ANNOTATOR>.json`:
```json
{"annotator": "<ANNOTATOR>",
 "folders": [{"repo": "owner/name", "dir": "...",
   "rules": [{"id": "R1", "file": "...", "quote": "...", "rule": "..."}],
   "relations": [{"a": "R1", "b": "R4", "label": "contradiction",
     "situation": "...", "explanation": "...", "confidence": "high"}]}]}
```
2. `data/open_coding/<ANNOTATOR>.md`: human-readable report with, per folder, the
   relations (quoting both rules), then the Step 3 catalog. Keep it concise.

Replace `<ANNOTATOR>` with: agent_b
