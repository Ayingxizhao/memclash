"""Score how likely a memory folder was written by an agent (Claude Code auto-memory).

Not proof of authorship: humans can copy the template and edit agent output.
Signals (per folder):
  path_signal   dir is .claude/projects/<encoded-local-path>/memory (created by Claude Code itself)
  frac_typed    share of memory files with frontmatter type: feedback|user|project|reference
  frac_why_how  share of memory files with **Why:** and **How to apply:** lines
  index_links   MEMORY.md exists and is mostly "- [Title](file.md)" link lines
Tiers:
  high    path_signal and frac_typed >= 0.5
  medium  frac_typed >= 0.5 (format only)
  low     otherwise

Usage: python scraper/provenance.py   (scores all data/github/repos/*)
Writes a "provenance" block into each repo.json; prints a summary.
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from github_scrape import REPOS, memory_type  # noqa: E402

PATH_SIGNAL = re.compile(r"(^|/)\.claude/projects/[^/]+/memory$")
MEMORY_TYPES = {"feedback", "user", "project", "reference"}
WHY = re.compile(r"\*\*why:?\*\*", re.I)
HOW = re.compile(r"\*\*how to apply:?\*\*", re.I)
LINK_LINE = re.compile(r"^\s*[-*]\s*\[[^\]]+\]\([^)]+\.md\)")


def score_folder(mem_dir: Path, rel_dir: str):
    files = {p.name: p.read_text(errors="replace") for p in mem_dir.glob("*.md")}
    index = files.pop("MEMORY.md", None)
    n = len(files) or 1
    frac_typed = sum(memory_type(t) in MEMORY_TYPES for t in files.values()) / n
    frac_why_how = sum(bool(WHY.search(t) and HOW.search(t)) for t in files.values()) / n
    index_links = False
    if index:
        lines = [l for l in index.splitlines() if l.strip() and not l.lstrip().startswith("#")]
        index_links = bool(lines) and sum(bool(LINK_LINE.match(l)) for l in lines) / len(lines) >= 0.5
    path_signal = bool(PATH_SIGNAL.search(rel_dir))
    tier = "high" if path_signal and frac_typed >= 0.5 else "medium" if frac_typed >= 0.5 else "low"
    return {"tier": tier, "path_signal": path_signal, "frac_typed": round(frac_typed, 2),
            "frac_why_how": round(frac_why_how, 2), "index_links": index_links}


def main():
    tiers = Counter()
    for info_path in sorted(REPOS.glob("*/repo.json")):
        info = json.loads(info_path.read_text())
        d = info["folder"]["dir"]
        prov = score_folder(info_path.parent / d, d)
        info["provenance"] = prov
        info_path.write_text(json.dumps(info, indent=2))
        tiers[prov["tier"]] += 1
        print(f"{prov['tier']:6} why/how={prov['frac_why_how']:.2f} typed={prov['frac_typed']:.2f} "
              f"index={int(prov['index_links'])} {info['repo']}/{d}")
    print(dict(tiers))


if __name__ == "__main__":
    main()
