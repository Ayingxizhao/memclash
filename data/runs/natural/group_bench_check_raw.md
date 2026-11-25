```json
[
  {"group":"G1","label":"compatible","why":"The changelog can live under docs/ because the release-metadata rule explicitly exempts human-readable changelogs."},
  {"group":"G2","label":"clash","why":"A completed hotfix must deploy, but deployment requires a prior tag while that tag requires a prior successful deployment; each pair alone remains workable."},
  {"group":"G3","label":"compatible","why":"Relevant targeted tests may be run and passed before pushing, without running the full regression suite."},
  {"group":"G4","label":"clash","why":"A documentation fix must be committed, but its commit can be neither documentation-only nor mixed with another file type; each pair permits a commit."},
  {"group":"G5","label":"clash","why":"Without a user build request, deletion remains explicitly permitted yet requires a successful build that is forbidden; every pair preserves a usable deletion path."},
  {"group":"G6","label":"clash","why":"An approved audit PR must be merged, but squash merging cannot preserve every commit; each pair allows a suitable merge or permits deferral."},
  {"group":"G7","label":"clash","why":"Committing requires prior lint, lint requires prior tests, and testing requires the change already be committed; every pair admits an ordering."},
  {"group":"G8","label":"ambiguous","why":"It clashes only if a maintenance-only release branch is also a task branch and 'tagged' means release-tagged; otherwise a non-release tag or disjoint branch categories resolves it."},
  {"group":"G9","label":"clash","why":"A completed task must be pushed, but pushing requires the full suite while running that suite requires an absent explicit user request; every pair is workable."},
  {"group":"G10","label":"compatible","why":"Generated-file cleanup activates the stated build exception, allowing the required successful build immediately before deletion."},
  {"group":"G11","label":"clash","why":"An approved non-fast-forwardable PR must be merged, while merge commits, squashing, and rebasing are all forbidden; each pair leaves a merge strategy available."},
  {"group":"G12","label":"compatible","why":"The rules allow the straightforward order unit tests, lint, then commit."},
  {"group":"G13","label":"clash","why":"A release changelog is required and, as release metadata, must be outside docs/, while every new Markdown document must be inside docs/; each pair allows a location."},
  {"group":"G14","label":"compatible","why":"After hotfix CI passes on main, the commit can be tagged, deployed, and then handed back."},
  {"group":"G15","label":"clash","why":"An untagged merged maintenance-only task branch must be deleted only after tagging, but creating that tag is forbidden; every pair remains satisfiable."},
  {"group":"G16","label":"compatible","why":"A documentation-only task may use a documentation-only commit, while mixed tasks can keep documentation separate unless both change types are jointly required."}
]
```