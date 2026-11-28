---
name: Plan & Task management
description: File structure, naming rules, format conventions and execution flow for project planning and task management
type: project
---

## Directory structure

```
.claude/
  plans/
    PLAN.md                        # Plan index (entry point for all plans)
    00-init.md                     # Specific plan file
    01-xxx.md                      # Subsequent plans, incrementing sequence number
  tasks/
    00-init-phase-0-preparation.md # Task file
    00-init-phase-1-xxx.md
```

## Naming rules

- **Plan files**: `{sequence}-{name}.md`, e.g. `00-init.md`, `01-vite-migration.md`
- **Task files**: `{planName}-phase-{number}-{name}.md`, e.g. `00-init-phase-0-preparation.md`
- **Plan index**: `PLAN.md`, records an index table of all plans

## File format

### Plan file frontmatter
```yaml
---
title: "Plan title"
description: "One-line description"
---
```

### Task file frontmatter
```yaml
---
title: "Px: Task title"
description: "One-line description"
phase: 0
plan: ".claude/plans/00-init.md"   # Associated plan file
status: pending                    # pending | in_progress | completed
depends_on: []                     # List of task file names this depends on
blocks: []                         # Which tasks depend on this one
risk: low                          # low | medium | high (optional)
---
```

## Plan file content structure

1. frontmatter (title, description)
2. Context (background and current state)
3. Task index table (phase, task file link, description, risk)
4. Dependency graph (ASCII diagram + critical path notes)

Specific phase task lists, acceptance criteria and other details go in the corresponding task files; the plan file only serves as an index.

## Task file content structure

1. frontmatter (including dependency relationships)
2. Task checklist (checkbox list)
3. Acceptance criteria

## Execution flow

1. **Plan first**: After exploring the codebase, update the detailed design (changed files, key decisions, implementation details) into the current task document under `.claude/tasks/`
2. **Execute next**: Implement according to the design in the task document
3. **Write summary**: After task completion, append a `## Summary` section at the end of the task document, recording actually modified files, newly created files, deleted files, and key design decisions

**Why:** Task documents serve as both planning and execution records, maintaining a single source of truth
**How to apply:** Update the design into the task document at the start of each task; append a summary to the same document when complete.

**How to apply:** All plans/tasks use the project-local `.claude/` directory, not the global Claude path. When creating a new plan, also update the `PLAN.md` index and memory.
