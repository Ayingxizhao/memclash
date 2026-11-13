# Task: label relations between pairs of agent-memory rules

<!-- ===== FILLED IN FOR THIS RUN ===== -->
ANNOTATOR: agent_b
RULES_FILE: /Users/yingxizhao/dev/cs2520/projects/data/gold/rules.json
OUTPUT: /Users/yingxizhao/dev/cs2520/projects/data/gold/labels_agent_b.json
PART_B (exploratory catalog): off
Label all 10 folders in RULES_FILE. Each folder entry gives `repo` and `dir`; its files live under
/Users/yingxizhao/dev/cs2520/projects/data/github/repos/<owner>__<name>/<dir>
(some are inside hidden `.claude/` directories, so use exact paths or `ls -a`).
Ignore each repo's root `CLAUDE.md` and `repo.json`: only the memory folder is in scope.
Also do not read data/gold/rules_agent_*.json, data/gold/rules2_agent_*.json, design/, or checker/.
<!-- ================================== -->

## Context
Coding agents keep "memory": markdown files of rules plus a `MEMORY.md` index. Nothing
checks a new rule against existing ones. You are one of several independent annotators
building ground truth: for every pair of rules within a folder, decide which relation
holds. Your labels are compared with other annotators' labels pair by pair.

## Independence
- Do not read other annotators' outputs (any `labels_*` file other than your own),
  `data/runs/`, `data/llm_cache.jsonl`, or `data/open_coding/`.
- Do not use an LLM API or script to judge pairs. Scripts are allowed only for mechanical
  help (e.g. listing pairs).
- Do not modify any file except OUTPUT.

## Procedure
1. Use the rule list in RULES_FILE exactly. Do not add, split, merge, or renumber rules. If
   you think the list is wrong, note it under `segmentation_notes`; still label the list.
2. Read every memory file in the folder in full for context (dates, sections, "Why").
3. Consider EVERY unordered pair of rules within a folder, including same-file pairs,
   index/file pairs, and pairs with a `CLAUDE.md` if RULES_FILE includes one (it is loaded in
   the same session). Never pair rules from different folders. Record only pairs whose label is not `none`; an unrecorded pair means
   `none`.

## Labels: apply in this order, take the first that fits
1. **duplicate**: both rules require the same behavior; scope is the same, or one rule's
   scope is contained in the other's with the same behavior (subsumption). Includes index
   or user-profile restatements. Set `subsumed` to the narrower rule's id if scopes differ.
2. **contradiction** (strict): there is a realistic situation in which both rules apply
   and the agent cannot comply with both. Counts: obligation vs prohibition of the same
   action; an EXPLICIT permission vs a prohibition. Does not count: an implied permission;
   rules that can both be satisfied by doing more (e.g. confirm AND proceed).
3. **override**: both rules are still meant to hold, but one (more specific, or newer)
   changes the behavior the other requires for part of its scope, without an explicit
   exception linking them.
4. **stale**: one rule is outdated relative to other memory content: it reflects an earlier
   state or decision that has been replaced (e.g. an index entry or status line that no
   longer matches the file; an old convention after a documented change). Set `outdated`
   to the outdated rule's id.
5. **tension**: both can be followed, but they pull in different directions, or it is
   unclear whether one rule's trigger covers the other's action (scope ambiguity).
6. **none**: unrelated, compatible, merely same topic, or one states an explicit exception
   to the other.

**Test for override vs stale:** "If the user cleaned up memory, would they delete or rewrite
one of the two rules?" Yes -> `stale`. No (both are valid; one is a special case) -> `override`.

## Structural defects (not pairs)
Record separately: links to missing memory files, files not listed in the index, index
entries pointing to missing files, and step sequences that cannot execute as written
(e.g. deleting a branch while it is checked out).

## Output (write OUTPUT)
```json
{"annotator": "<name>", "rules_file": "<RULES_FILE>",
 "folders": [{"repo": "owner/name",
   "relations": [{"a": "R1", "b": "R4", "label": "contradiction",
     "subsumed": null, "outdated": null,
     "situation": "concrete situation where both apply (contradiction/override/tension)",
     "explanation": "1-3 sentences", "confidence": "high|medium|low"}],
   "structural": [{"type": "dangling_link|unindexed_file|missing_indexed_file|unexecutable_sequence",
     "rules": ["R9"], "files": ["..."], "explanation": "..."}],
   "segmentation_notes": ["..."]}]}
```
If a folder has no relations, give an empty list. Do not invent relations to fill space.

## PART_B = on only (exploratory)
Also write `<OUTPUT without .json>.md`: group the issues into types using your own names
(definition, count, 1-2 verbatim examples); list the scope dimensions the rules condition on
(tool, file, task, output medium, time, agent role, ...) with rough counts; list rules that
would be hard to encode as typed logic, with a short reason each.
