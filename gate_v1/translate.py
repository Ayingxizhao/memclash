"""Stage A: translate each rule into a schema record (LLM) and validate it (code).

One DeepSeek call per rule, with the rule's source file as context and the current
vocabulary. An invalid record is sent back with the validator's errors (at most MAX_RETRIES
times); a rule that still fails, or that the model says does not fit, is marked unchecked.
Accepted new terms are added to the vocabulary, so later rules see and reuse them.

Usage:
  uv run python gate_v1/translate.py --run own_v1 --rules data/own/rules.json --base data/own
Output: data/runs/<run>/records.json, vocab_additions.json, summary.json
"""

import argparse
import asyncio
import json
from collections import Counter
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pipeline"))  # shared LLM client
from llm import LLM

from validate import Vocab

ROOT = Path(__file__).resolve().parents[1]
PROMPT = (ROOT / "prompts" / "gate_v1" / "translate.md").read_text()
MAX_RETRIES = 2


def load_rules(rules_path, base):
    """Yield (folder, rule, file_text). Supports data/own/rules.json and data/gold/rules.json."""
    data = json.loads(Path(rules_path).read_text())
    for r in data.get("global", []):
        yield "global", r, (base / r["file"]).read_text()
    for f in data["folders"]:
        if "repo" in f:   # GitHub layout
            name, d = f["repo"], base / f["repo"].replace("/", "__") / f["dir"]
        else:             # own-memory layout
            name, d = f["folder"], base / f["dir"]
        for r in f["rules"]:
            yield name, r, (d / r["file"]).read_text()


async def translate_rule(llm, vocab, folder, rule, file_text):
    messages = [
        {"role": "system", "content": PROMPT.replace("{VOCAB}", vocab.render())},
        {"role": "user", "content": f"FILE `{rule['file']}`:\n<<<\n{file_text}\n>>>\n\n"
                                    f"RULE to translate:\n- quote: {rule['quote']}\n- rule: {rule['rule']}"},
    ]
    confirmed, errors, rec = set(), [], None
    for attempt in range(MAX_RETRIES + 1):
        rec = await llm.chat_json(messages)
        errors, new = vocab.validate(rec, confirmed)
        if not errors:
            for t in new:
                vocab.add(t, source=f"{folder}:{rule['id']}")
            status = "unfit" if rec.get("fits") is False else "valid"
            return {"status": status, "attempts": attempt + 1, "record": rec, "errors": []}
        nt = rec.get("new_terms") if isinstance(rec, dict) and isinstance(rec.get("new_terms"), list) else []
        confirmed |= {t["name"] for t in nt if isinstance(t, dict) and isinstance(t.get("name"), str)}
        messages += [{"role": "assistant", "content": json.dumps(rec)},
                     {"role": "user", "content": "The record is invalid:\n- " + "\n- ".join(errors)
                                                 + "\nReturn the corrected full JSON record."}]
    return {"status": "invalid", "attempts": MAX_RETRIES + 1, "record": rec, "errors": errors}


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--rules", required=True)
    ap.add_argument("--base", required=True, help="directory the rule files live under")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    out_dir = ROOT / "data" / "runs" / args.run
    out_dir.mkdir(parents=True, exist_ok=True)
    llm, vocab, results = LLM(), Vocab(), []
    items = list(load_rules(ROOT / args.rules, ROOT / args.base))[: args.limit]
    for i, (folder, rule, text) in enumerate(items, 1):
        res = await translate_rule(llm, vocab, folder, rule, text)
        results.append({"folder": folder, **rule, **res})
        print(f"[{i}/{len(items)}] {res['status']:7} x{res['attempts']} {folder[-24:]}:{rule['id']}  {rule['rule'][:70]}")
        (out_dir / "records.json").write_text(json.dumps(results, indent=1, ensure_ascii=False))

    status = Counter(r["status"] for r in results)
    summary = {
        "run": args.run, "model": llm.model, "rules": len(results),
        "valid": status["valid"], "unfit": status["unfit"], "invalid": status["invalid"],
        "coverage": round(status["valid"] / len(results), 3),
        "first_try_valid": sum(r["status"] == "valid" and r["attempts"] == 1 for r in results),
        "new_terms": len(vocab.additions),
        "new_actions": sum(t["kind"] == "action" for t in vocab.additions),
        "usage": llm.usage,
    }
    (out_dir / "vocab_additions.json").write_text(json.dumps(vocab.additions, indent=1, ensure_ascii=False))
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    asyncio.run(main())
