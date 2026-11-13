---
name: Coder must follow references exactly, not copy nearby code
description: Three recurring coder mistakes — arrow vs function declaration, wrong param source, manual workspace filter — all caused by copying nearby code instead of reading codebase-onboard references
type: feedback
agent: coder
---

## Wrong vs Good

### 1. Arrow function instead of async function

**Wrong:**
```ts
export const getInitDropdownDataAction = async (workspaceFilter) => {
```

**Good:**
```ts
export async function getInitDropdownDataAction(workspaceFilter) {
```

Reference explicitly says "Regular `async function` (not arrow)". Read the Function Signature section before writing.

### 2. Wrong param type — looked at other module's code instead of reference

**Wrong:** Copied purchase-request's real code which takes `cookie` param
**Good:** Reference says `workspaceFilter: WorkspaceFilterDTOType` — use that

### 3. Manual workspace filter instead of buildWorkspaceFilter

**Wrong:**
```ts
if (workspaceFilter.companyId) workspace.push(eq(table.companyId, workspaceFilter.companyId));
if (workspaceFilter.companyBranchId) workspace.push(eq(table.companyBranchId, workspaceFilter.companyBranchId));
// ...4 more lines
```

**Good:**
```ts
const baseWhereFilter = buildWorkspaceFilter(table, workspaceFilter);
```

## Root Cause

Copied from nearby code in the same file / other modules instead of reading the codebase-onboard reference. CLAUDE.md rule #1: "Never copy nearby modules as reference — rule files + codebase-onboard win."

## How to Apply

Before writing any architectural layer code (action, repository, service, form), run codebase-onboard skill and read the matching reference. Follow its function signature, param types, and patterns exactly.
