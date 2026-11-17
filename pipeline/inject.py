"""Injection test, step 1: write rules that conflict with real host rules.

For each (host rule, pattern), a model that is NOT the judge writes three new rules
(prompts/inject_rule.md): a conflict in direct wording, the same conflict reworded, and a
paraphrase of the host (control: must not be reported as a conflict). The output is reviewed
by hand before it is used; set "keep": false on an item to drop it.

Usage:
  uv run python pipeline/inject.py --rules data/dev/rules.json --folder setflow \
      --hosts R1:opposite,R12:value --out data/inject/dev_pilot.json
Output: a JSON list, one item per injected rule:
  {folder, host, pattern, kind, id, file, rule, situation, keep}
"""

import argparse
import asyncio
import json
from pathlib import Path

from llm import LLM

ROOT = Path(__file__).resolve().parents[1]
PROMPT = (ROOT / "prompts" / "inject_rule.md").read_text()
WRITER = "qwen3.6-35b"
PATTERNS = ("opposite", "value", "narrower", "number", "permission")
KINDS = ("conflict_direct", "conflict_reworded", "paraphrase")


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rules", required=True)
    ap.add_argument("--folder", required=True, help="substring of the folder / repo name")
    ap.add_argument("--hosts", required=True, help="comma list of <rule id>:<pattern>")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    folder = next(f for f in json.loads((ROOT / args.rules).read_text())["folders"]
                  if args.folder in (f.get("repo") or f["folder"]))
    name, rules = folder.get("repo") or folder["folder"], {r["id"]: r for r in folder["rules"]}
    listing = "\n".join(f"{r['id']} (file `{r['file']}`): {r['rule']}" for r in folder["rules"])
    out_path = ROOT / args.out
    items = json.loads(out_path.read_text()) if out_path.exists() else []
    items = [it for it in items if it["folder"] != name]          # regenerate this folder only
    llm, n = LLM(model=WRITER), 0
    for spec in args.hosts.split(","):
        host, pattern = spec.split(":")
        assert host in rules and pattern in PATTERNS, spec
        ans = await llm.chat_json([
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": f"FOLDER RULES\n{listing}\n\nHOST RULE: {host}: {rules[host]['rule']}\nPATTERN: {pattern}"}])
        if not ans.get("fits", True):
            print(f"{host} [{pattern}] does not fit: {ans.get('reason')}")
            continue
        print(f"\n{host} [{pattern}]  {rules[host]['rule']}\n  situation: {ans.get('situation')}")
        for kind in KINDS:
            n += 1
            items.append({"folder": name, "host": host, "pattern": pattern, "kind": kind, "id": f"X{n}",
                          "file": ans[kind]["file"], "rule": ans[kind]["rule"],
                          "situation": ans.get("situation"), "keep": True})
            print(f"  X{n} {kind:17} {ans[kind]['rule']}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(items, indent=1, ensure_ascii=False))
    print(f"\n{n} injected rules for {name} -> {args.out}", llm.usage)


if __name__ == "__main__":
    asyncio.run(main())
