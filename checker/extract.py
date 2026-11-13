"""Stage 1: extract atomic agent rules from each memory file.

For every .md file in a repo's memory folder (MEMORY.md index excluded), DeepSeek
returns rules as {quote, rule}. Each quote must be a verbatim span of the file
(after light normalization); otherwise we retry once with feedback, then drop it.

Usage:
  uv run python checker/extract.py --run pilot --repos owner/repo [owner/repo ...]
  uv run python checker/extract.py --run full --split prevalence
Output: data/runs/<run>/rules/<owner__repo>.json
"""

import argparse
import asyncio
import json
import re
from pathlib import Path

from llm import LLM

ROOT = Path(__file__).resolve().parents[1] / "data"
REPOS = ROOT / "github" / "repos"

SYSTEM = """You extract behavioral rules for an AI coding agent from one of its memory files.

A RULE is an instruction that prescribes, prohibits, or permits a behavior of the agent \
(do X, never do X, prefer X, X is allowed), possibly under a condition (when/if/for ...).
NOT rules: facts about the project, user, or codebase with no instruction; rationale \
("Why: ..."); history of how the rule came about; file metadata (name/description/type).
But a "How to apply" line that instructs the agent IS a rule.

Instructions:
- Split compound instructions into atomic rules: one action per rule.
- "quote": copy the shortest contiguous span of the file that states the rule, EXACTLY \
as written (same words, same punctuation). Do not paraphrase or join separate spans.
- "rule": a self-contained imperative restatement that a reader can understand without \
the file (include the condition/scope, resolve "this"/"it").
- If the file contains no rules, return an empty list.

Return JSON: {"rules": [{"quote": "...", "rule": "..."}]}"""


def normalize(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[*`]", "", s)  # markdown emphasis / code ticks
    return re.sub(r"\s+", " ", s).strip()


def quote_ok(quote: str, text_norm: str) -> bool:
    q = normalize(quote)
    return bool(q) and q in text_norm


async def extract_file(llm: LLM, fname: str, text: str):
    msgs = [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"File: {fname}\n\n{text}"}]
    out = await llm.chat_json(msgs)
    rules = out.get("rules", [])
    text_norm = normalize(text)
    bad = [r for r in rules if not quote_ok(r.get("quote", ""), text_norm)]
    if bad:  # one retry with feedback
        msgs += [{"role": "assistant", "content": json.dumps(out)},
                 {"role": "user", "content": "These quotes are not verbatim spans of the file. Return the full "
                  "corrected list, copying each quote exactly from the file:\n"
                  + "\n".join(f"- {r.get('quote')}" for r in bad)}]
        out = await llm.chat_json(msgs)
        rules = out.get("rules", [])
    good = [r for r in rules if quote_ok(r.get("quote", ""), text_norm) and r.get("rule")]
    dropped = [r for r in rules if r not in good]
    return good, dropped


async def extract_repo(llm: LLM, repo: str, out_dir: Path):
    repo_dir = REPOS / repo.replace("/", "__")
    info = json.loads((repo_dir / "repo.json").read_text())
    mem = repo_dir / info["folder"]["dir"]
    files = sorted(p for p in mem.glob("*.md") if p.name != "MEMORY.md")
    results = await asyncio.gather(*(extract_file(llm, p.name, p.read_text(errors="replace")) for p in files))
    rules, dropped = [], []
    for p, (good, bad) in zip(files, results):
        for r in good:
            rules.append({"id": f"R{len(rules) + 1}", "file": p.name, "quote": r["quote"], "rule": r["rule"]})
        dropped += [{"file": p.name, **r} for r in bad]
    rec = {"repo": repo, "dir": info["folder"]["dir"], "n_files": len(files),
           "n_rules": len(rules), "n_dropped": len(dropped), "rules": rules, "dropped": dropped}
    (out_dir / f"{repo.replace('/', '__')}.json").write_text(json.dumps(rec, indent=2, ensure_ascii=False))
    print(f"{repo}: files={len(files)} rules={len(rules)} dropped={len(dropped)}")
    return rec


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--repos", nargs="+")
    g.add_argument("--split", choices=["prevalence", "gold"])
    args = ap.parse_args()
    repos = args.repos or json.loads((ROOT / "github" / "split.json").read_text())[args.split]
    out_dir = ROOT / "runs" / args.run / "rules"
    out_dir.mkdir(parents=True, exist_ok=True)
    llm = LLM()
    for repo in repos:
        await extract_repo(llm, repo, out_dir)
    print("usage:", llm.usage)


if __name__ == "__main__":
    asyncio.run(main())
