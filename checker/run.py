"""One command: translate the rules (Stage A), then check all pairs with Z3 (Stage B).

Usage:
  uv run python checker/run.py --run dev_v1 --rules data/dev/rules.json --base data/github/repos
Output in data/runs/<run>/: records.json, vocab_additions.json, summary.json, flags.json,
pairs_summary.json
"""

import asyncio
import json
import sys

import check_pairs
import translate

if __name__ == "__main__":
    asyncio.run(translate.main())                       # parses --run / --rules / --base / --limit
    run_name = sys.argv[sys.argv.index("--run") + 1]
    flags, summary = check_pairs.run(run_name)
    print(json.dumps({k: v for k, v in summary.items() if k != "folders"}, indent=1))
