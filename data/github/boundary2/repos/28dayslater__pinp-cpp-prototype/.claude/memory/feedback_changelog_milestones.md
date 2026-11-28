---
name: CHANGELOG version entries link to GitHub milestone when one exists
description: Version bumps tied to a GitHub milestone should include the milestone URL in the CHANGELOG entry
type: feedback
---

When a version bump corresponds to a GitHub milestone, include the milestone URL in the CHANGELOG entry header or description.

**Why:** Upcoming versions covering the sema checks milestone (and future milestones) should be traceable back to the GitHub milestone for context.

**How to apply:** When writing a new CHANGELOG entry, check whether a milestone was created for that body of work. If so, link it — e.g. `## v0.x.y — [description](https://github.com/28dayslater/pinp/milestone/N)`.
