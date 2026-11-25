---
name: dev-progress
description: "Current state of the codebase — what's done, what's in progress, what's next. Update every session."
metadata:
  type: project
---

Last updated: [date]

## Team
<!-- List team members and their service ownership -->
- **[Name/Alias]**: [service-a], [service-b]
- **[Name/Alias]**: [service-c], [service-d]

## Overall Status
[One-line summary of where the project is — e.g., "Scaffold phase complete, moving into implementation"]

## Services

<!-- Repeat this block for each service/module -->

### [service-name] (:[port]) — [status]
- Domain: [list domain classes implemented]
- Application: [use cases, commands, DTOs]
- Infrastructure: [controllers, JPA entities, repos, consumers]
- **Status:** [what's working / what's a stub / what's missing]

---

<!-- Example filled-in entry:
### user-service (:8081) — Scaffold done
- Domain: `UserProfile`, VOs (`UserId`, `ContactInfo`, `Role`)
- Application: `RegisterUserUseCase`, `GetUserProfileUseCase`
- Infrastructure: JPA entity + mapper + repo, `UserController`, `SecurityConfig`
- **Status:** Skeleton in place. Business logic not yet implemented.
-->

## Next Up
1. [Most important next task]
2. [Second priority]
3. [Third priority]

## Deadline
[Phase/milestone name]: **[date]** (~[N] weeks remaining)
