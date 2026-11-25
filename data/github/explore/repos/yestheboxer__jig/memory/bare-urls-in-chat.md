---
name: bare-urls-in-chat
description: "PR references in chat replies must be BARE URLs on their own line, never markdown link syntax, because only bare URLs are command clickable in the terminal"
metadata:
  node_type: memory
  type: feedback
---

In replies to the user, print pull request references as **bare URLs**, never as markdown links. `https://github.com/example/repo/pull/1234` is command clickable in a terminal. `[#NNNN](https://...)` is NOT, and neither is a bare `#NNNN`.

This is easy to get wrong twice in a row. A first pass uses plain `#NNNN` text. A second pass "fixes" it with markdown links, which still do not work, and a memory gets written asserting markdown links are the answer. The user then has to say it a third time.

**Why:** terminals autodetect raw `https://` strings and make them clickable. They do not parse markdown link syntax, so the URL is hidden inside the markup and there is nothing to click. Many chat tools and their integrations mangle `[label](url)` the same way. Treat "bare URL, never markdown link syntax" as the house rule for every surface, not a quirk of one tool.

**How to apply:** when listing several PRs, give each its own line with the URL on that line, since a table cell full of long URLs is unreadable. Put the short description first and the bare URL after it, or on the next line. Include the URL on every occurrence that matters, not just the first, and never substitute a bare `#NNNN` for it. PR numbers collide across repos, so the full URL is also what tells the reader which repo it is in.
