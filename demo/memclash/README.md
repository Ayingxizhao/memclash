# memclash report viewer

Static pages that open a memclash report (`report.json`). No server and no build step: open
`index.html` in a browser.

- `index.html` overview, `findings.html` list, `finding.html?id=F1` detail, `rules.html`,
  `rule.html?id=R1`, `ambiguous.html`, `skipped.html` (what the scan could not decide)
- `assets/` shared style and script; `reports/` sample reports (`*.json` plus a `*.js` copy so
  they load from disk)
- Write a report: `uv run python pipeline/rules/cli.py report --translations <translations.json>
  --folder <name> --out demo/memclash/reports/<name>.json`, then add it to `reports/index.js`
