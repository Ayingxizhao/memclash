# Memory index

One line per memory. Recall loads this to decide what to read.

- [Prefers root-cause fixes](prefers-root-cause-fixes.md) — offered a workaround or a durable fix, they pick durable: "I want the durable fix please"
- [Prefers in-repo deploy config](prefers-in-repo-deploy-config.md) — wants infra/deploy config committed, not set up via local CLI
- [Reviews implementations in a browser](reviews-implementations-in-browser.md) — after /implement runs, start each worktree's dev server and print the links before merging
- [Dictates prompts by voice](dictates-prompts-by-voice.md) — read past filler words; a negation that contradicts the same turn is probably a transcription slip
- [Stacking implementation branches](stacking-implementation-branches.md) — a plan blocked on an unmerged sibling can stack on its branch instead of waiting; check what's actually pushed
- [Silent semantic merge conflicts](silent-semantic-merge-conflicts.md) — clean merges are routinely wrong; diff resolved files against the branch tip, never trust missing markers
- ["I upgraded the plan"](upgraded-the-plan-means-usage-plan.md) — means the Claude Code usage plan after a session limit, not plan.md; just resume the interrupted work
- [Self-verify CI work](self-verify-ci-work.md) — trigger the live run and read its logs before reporting workflow changes done; don't re-ask confirmed setup steps
