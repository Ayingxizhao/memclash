You decide whether ONE rule from a coding agent's memory folder is about git.

Answer "git": true if the rule says anything about what the agent does with git or GitHub:
commits, pushes, pulls, fetches, merges, rebases, branches, checkouts, tags, stashes,
cherry-picks, resets, reverts, worktrees, submodules, pull requests, reviews of pull requests,
branch protection, what may or may not go into the repository or version control, or which
tool to use for any of these.

Answer "git": false if the rule is only about something else, such as how code is written,
which language, library or version to use, how to run or write tests, deployment that does not
involve git, which task to do next, or how to talk to the user.

If you are unsure, answer true.

Return JSON: {"git": true|false, "reason": "<one short sentence>"}
