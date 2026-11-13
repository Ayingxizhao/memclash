---
name: precise-column-labels
description: Table column labels must say exactly what the number is; define every self-made abbreviation in every table
metadata:
  type: feedback
---

Label every table column with what the number actually is (e.g. "跑题图的平均 diversity reward", not "跑题", which reads as a share of off-topic images). Do not use self-made abbreviations (top1, nz, corr) as column names; if one is unavoidable, define it right above every table that uses it, not only the first time.

**Why:** the user (2026-10-24) could not read the periodic diversity tables: "跑题 / 切题" looked like proportions that should sum to 1, and nz / corr were used without explanation in later tables.

**How to apply:** before sending any table, read each column header as a stranger would and check it names the quantity and its unit / aggregation. Related: [[describe-runs-not-ids]].
