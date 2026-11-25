# Memory

- [Background work must be tracked](background-work-must-be-tracked.md): never launch long work with `&` inside a Bash call; use run_in_background and confirm the process before you say it runs
- [Bare URLs in chat](bare-urls-in-chat.md): PR references go out as bare URLs on their own line, never markdown links or a bare number
- [Keep tool output small](keep-tool-output-small.md): filter every Bash and MCP result at the source with head, tail, grep, jq or fields
- [Lean test check ins](lean-test-checkins.md): prune tests before every PR, keep contracts, regressions and boundary cases, aim for PRs of about 2k lines
- [Scout counts need an independent recount](scout-counts-need-independent-recount.md): specify the discriminator, not the string, and recount any load bearing number by a different method
- [Surgical git and worktrees](surgical-git-and-worktrees.md): one worktree per task, cd into it in every command, no broad destructive git, follow ups as new commits
