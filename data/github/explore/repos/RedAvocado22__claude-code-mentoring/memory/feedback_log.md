---
name: feedback-log
description: "Loose feedback and confirmed patterns that don't fit decisions.md or recurring_mistakes.md — tool usage, pacing, scope calls, confirmed approaches"
metadata:
  type: feedback
---

<!--
This file is for the quieter half of feedback: not mistakes (those go in
recurring_mistakes.md), and not formal technical decisions (those go in
decisions.md) — just moments where you corrected Claude's approach, or
confirmed an unusual approach was right. Corrections are easy to notice.
Confirmations are quieter — watch for them too, or Claude will avoid past
mistakes but drift away from approaches you already validated.

Format per entry:
## <short title>

<what happened, one or two sentences>

**Why:** <the reasoning behind the correction/confirmation>

**How to apply:** <when this should change Claude's behavior going forward>
-->

## Example: Confirmed an unusual scope call

User pushed back on Claude adding defensive hardening nobody asked for, then
confirmed the smaller scope was correct once Claude explained the trade-off.

**Why:** Not every "best practice" is worth the extra surface area for this
project's actual constraints (deadline, audience, blast radius).

**How to apply:** Before adding scope beyond what was asked, weigh whether
it's cheap (few lines, no new complexity) or expensive (new files, new
dependency, architecture change). Cheap — just add it. Expensive — ask first,
don't assume "best practice" means "necessary here".

<!-- Add your own entries below this line -->
