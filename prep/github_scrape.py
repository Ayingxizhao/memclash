"""Scrape public agent-memory folders from GitHub.

Phase 1 (search): GitHub code search for memory files, sharded by file size to
get past the 1000-results-per-query cap. Results cached in search_hits.jsonl.

Phase 2 (fetch): group hits into memory folders (dir whose last component is
"memory"), list each folder, download its .md files, and keep folders that pass
the quality filter. Data is stored per repo: data/github/repos/<owner>__<repo>/.

Quality filter (v1):
  - folder path ends in "memory" (.claude/memory, .claude/projects/*/memory, memory/)
  - >= MIN_RULE_FILES files with frontmatter type: feedback | user
  - repo is not a fork
  - >= 80% of memory files detected as English (prep/lang.py)
Template/boilerplate and duplicate detection are done later, in post-processing.

Usage:
  uv run python prep/github_scrape.py search [--max-pages N]
  uv run python prep/github_scrape.py fetch  [--max-repos 30] [--seed 2520]
Auth: uses the token from `gh auth token`.
"""

import argparse
import hashlib
import json
import random
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

from lang import MIN_EN_FRAC, english_fraction

ROOT = Path(__file__).resolve().parent.parent / "data" / "github"
HITS = ROOT / "search_hits.jsonl"
CANDIDATES = ROOT / "candidates.jsonl"
REPOS = ROOT / "repos"

QUERIES = [
    '"type: feedback" path:.claude/memory',
    '"type: feedback" path:.claude/projects',
    '"type: feedback" path:memory',
    '"type: user" path:memory',
]
# Initial size shards (bytes); shards with >1000 hits are bisected.
SIZE_SHARDS = [(0, 600), (601, 1000), (1001, 1500), (1501, 2500), (2501, 5000), (5001, 400000)]
MIN_RULE_FILES = 3
MAX_RULE_FILES = 40  # skip huge folders (pair count grows quadratically)
RULE_TYPES = {"feedback", "user"}
SEARCH_SLEEP = 6.5  # code search: 10 requests/min

TOKEN = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()


# ---------------------------------------------------------------- HTTP helpers
def _request(url, accept="application/vnd.github+json", auth=True, retries=5):
    url = urllib.parse.quote(url, safe=":/?&=%+@,~")  # non-ASCII file names
    headers = {"Accept": accept, "User-Agent": "memory-consistency-research"}
    if auth:
        headers["Authorization"] = f"Bearer {TOKEN}"
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return 404, b""
            if e.code in (403, 429):  # rate limited: wait for reset
                reset = e.headers.get("x-ratelimit-reset")
                retry_after = e.headers.get("retry-after")
                wait = int(retry_after) if retry_after else max(int(reset) - int(time.time()), 5) if reset else 60
                print(f"  rate limited ({e.code}); sleeping {wait + 2}s", file=sys.stderr)
                time.sleep(wait + 2)
                continue
            print(f"  HTTP {e.code} on {url}", file=sys.stderr)
            time.sleep(2 ** attempt)
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"  network error {e} on {url}", file=sys.stderr)
            time.sleep(2 ** attempt)
    return None, b""


def api(endpoint, **params):
    url = f"https://api.github.com/{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    status, body = _request(url)
    return status, (json.loads(body) if status == 200 else None)


# ---------------------------------------------------------------- phase 1: search
def search_shard(query, lo, hi, max_pages, out):
    q = f"{query} size:{lo}..{hi}"
    status, data = api("search/code", q=q, per_page=100, page=1)
    time.sleep(SEARCH_SLEEP)
    if data is None:
        print(f"  search failed: {q}", file=sys.stderr)
        return 0
    total = data["total_count"]
    if total > 1000 and hi - lo > 1:  # too many: bisect
        mid = (lo + hi) // 2
        return search_shard(query, lo, mid, max_pages, out) + search_shard(query, mid + 1, hi, max_pages, out)
    print(f"  {q}: total={total}")
    n_pages = min((min(total, 1000) + 99) // 100, max_pages)
    items = data["items"]
    for page in range(2, n_pages + 1):
        _, d = api("search/code", q=q, per_page=100, page=page)
        time.sleep(SEARCH_SLEEP)
        if d:
            items += d["items"]
    for it in items:
        out.write(json.dumps({"repo": it["repository"]["full_name"], "path": it["path"],
                              "sha": it["sha"], "query": query}) + "\n")
    return len(items)


def cmd_search(args):
    ROOT.mkdir(parents=True, exist_ok=True)
    with HITS.open("w") as out:
        for query in QUERIES:
            print(f"query: {query}")
            n = sum(search_shard(query, lo, hi, args.max_pages, out) for lo, hi in SIZE_SHARDS)
            print(f"  -> {n} hits")


# ---------------------------------------------------------------- phase 2: fetch
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---", re.S)
TYPE_LINE = re.compile(r"^\s*type:\s*['\"]?(\w+)", re.M)


def memory_type(text):
    text = text.lstrip("\ufeff").replace("\r\n", "\n")
    m = FRONTMATTER.match(text)
    if not m:
        return None
    t = TYPE_LINE.search(m.group(1))
    return t.group(1).lower() if t else None


def candidate_folders():
    """Group search hits into (repo, memory_dir) folders."""
    folders = defaultdict(set)
    for line in HITS.open():
        h = json.loads(line)
        d = h["path"].rsplit("/", 1)[0] if "/" in h["path"] else ""
        if d.split("/")[-1].lower() == "memory":
            folders[(h["repo"], d)].add(h["path"])
    return folders


def fetch_raw(url):
    status, body = _request(url, accept="*/*", auth=False)
    return body.decode("utf-8", errors="replace") if status == 200 else None


def save(repo_dir, rel_path, text):
    p = repo_dir / rel_path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def process_folder(repo, d):
    """List folder, download .md files, return stats + file texts."""
    status, listing = api(f"repos/{repo}/contents/{urllib.parse.quote(d)}")
    if not isinstance(listing, list):
        return None, {}
    files = {}
    for e in listing:
        if e["type"] == "file" and e["name"].lower().endswith(".md") and e.get("download_url"):
            text = fetch_raw(e["download_url"])
            if text is not None:
                files[e["path"]] = text
    types = {p: memory_type(t) for p, t in files.items()}
    stats = {
        "repo": repo, "dir": d,
        "n_md": len(files),
        "n_rule_files": sum(t in RULE_TYPES for t in types.values()),
        "type_counts": {k: sum(v == k for v in types.values()) for k in set(types.values()) if k},
        "has_index": any(p.endswith("/MEMORY.md") for p in files),
    }
    return stats, files


def repo_metadata(repo):
    _, m = api(f"repos/{repo}")
    if not m:
        return None
    return {"repo": repo, "fork": m["fork"], "archived": m["archived"], "stars": m["stargazers_count"],
            "description": m["description"], "default_branch": m["default_branch"],
            "license": (m.get("license") or {}).get("spdx_id"), "pushed_at": m["pushed_at"],
            "created_at": m["created_at"]}


def last_commit_date(repo, d):
    _, c = api(f"repos/{repo}/commits", path=d, per_page=1)
    return c[0]["commit"]["committer"]["date"] if c else None


def cmd_fetch(args):
    """Random order (fixed seed), one folder per owner, stop after --max-repos kept."""
    by_repo = defaultdict(list)
    for repo, d in candidate_folders():
        by_repo[repo].append(d)
    rng = random.Random(args.seed)
    repos = sorted(by_repo)
    rng.shuffle(repos)
    done, kept_repos, kept_owners = set(), set(), set()
    if CANDIDATES.exists():
        for c in map(json.loads, CANDIDATES.open()):
            if c.get("skip_reason") not in ("over_max_md", "over_max_kb"):
                done.add((c["repo"], c["dir"]))  # size skips depend on the run's cap: re-check
            if c.get("kept"):
                kept_repos.add(c["repo"])
                kept_owners.add(c["repo"].split("/")[0])
    out_cands, repos_dir = CANDIDATES, REPOS
    if args.out_dir:
        # separate exploration set: folders already in the dataset (and their owners) are
        # skipped, and nothing is written to the dataset's own files
        out = Path(args.out_dir)
        out_cands, repos_dir = out / "candidates.jsonl", out / "repos"
        out.mkdir(parents=True, exist_ok=True)
        if out_cands.exists():
            for c in map(json.loads, out_cands.open()):
                done.add((c["repo"], c["dir"]))
                if c.get("kept"):
                    kept_owners.add(c["repo"].split("/")[0])
        excluded = set(kept_repos)
        kept_repos = {c["repo"] for c in map(json.loads, out_cands.open()) if c.get("kept")} \
            if out_cands.exists() else set()
        kept_owners |= {r.split("/")[0] for r in excluded}
    if args.exclude:  # owners listed after "# owners" in the file are never fetched
        lines = Path(args.exclude).read_text().split("\n")
        kept_owners |= {x for x in lines[lines.index("# owners") + 1:] if x}
    print(f"{len(repos)} candidate repos, {len(kept_repos)} already kept, target {args.max_repos}")
    with out_cands.open("a") as cand_out:
        for repo in repos:
            if len(kept_repos) >= args.max_repos:
                break
            if repo in kept_repos or repo.split("/")[0] in kept_owners:
                continue  # one folder per owner (same user's folders are not independent)
            dirs = sorted(by_repo[repo])
            rng.shuffle(dirs)
            meta = None
            for d in dirs:
                if (repo, d) in done:
                    continue
                stats, files = process_folder(repo, d)
                if stats is None:
                    cand_out.write(json.dumps({"repo": repo, "dir": d, "error": "listing_failed"}) + "\n")
                    continue
                keep, reason = MIN_RULE_FILES <= stats["n_rule_files"] <= MAX_RULE_FILES, "rule_count"
                if keep and args.max_md and stats["n_md"] > args.max_md:
                    keep, reason = False, "over_max_md"  # only used for the small dev set
                if keep and args.max_kb:
                    stats["kb"] = round(sum(len(t.encode()) for p, t in files.items() if p.endswith(".md")) / 1024, 1)
                    if stats["kb"] > args.max_kb:
                        keep, reason = False, "over_max_kb"  # gold cap: folders must be hand-labelable
                if keep:
                    meta = meta or repo_metadata(repo)
                    keep, reason = meta is not None and not meta["fork"], "fork_or_no_meta"
                if keep:
                    stats["en_frac"] = round(english_fraction(files), 2)
                    keep, reason = stats["en_frac"] >= MIN_EN_FRAC, "non_english"
                stats["kept"] = keep
                if not keep:
                    stats["skip_reason"] = reason
                cand_out.write(json.dumps(stats) + "\n")
                cand_out.flush()
                print(f"[{len(kept_repos) + keep}/{args.max_repos}] {'KEEP' if keep else 'skip'} "
                      f"{repo}/{d} md={stats['n_md']} rules={stats['n_rule_files']}")
                if keep:
                    save_repo(repo, d, meta, stats, files, repos_dir)
                    kept_repos.add(repo)
                    kept_owners.add(repo.split("/")[0])
                    break  # one folder per repo


def save_repo(repo, d, meta, stats, files, repos_dir=REPOS):
    repo_dir = repos_dir / repo.replace("/", "__")
    for path, text in files.items():
        save(repo_dir, path, text)
    claude = fetch_raw(f"https://raw.githubusercontent.com/{repo}/{meta['default_branch']}/CLAUDE.md")
    if claude is not None:
        save(repo_dir, "CLAUDE.md", claude)
    info = {**meta, "root_claude_md": claude is not None, "folder": {
        **{k: stats[k] for k in ("dir", "n_md", "n_rule_files", "type_counts", "has_index")},
        "last_commit": last_commit_date(repo, d),
        "files": {p: hashlib.sha256(t.encode()).hexdigest() for p, t in files.items()},
    }}
    (repo_dir / "repo.json").write_text(json.dumps(info, indent=2))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("--max-pages", type=int, default=10, help="pages (of 100) per shard")
    f = sub.add_parser("fetch")
    f.add_argument("--max-repos", type=int, default=30)
    f.add_argument("--seed", type=int, default=2520)
    f.add_argument("--max-md", type=int, default=None, help="skip folders with more .md files (dev set)")
    f.add_argument("--max-kb", type=float, default=None, help="skip folders whose .md files exceed this size (gold cap)")
    f.add_argument("--out-dir", default=None,
                   help="write a separate exploration set here (skips folders and owners already in the dataset)")
    f.add_argument("--exclude", default=None, help="file listing owners to skip (after a '# owners' line)")
    args = ap.parse_args()
    {"search": cmd_search, "fetch": cmd_fetch}[args.cmd](args)


if __name__ == "__main__":
    main()
