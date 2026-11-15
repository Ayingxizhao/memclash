"""Record shape v2: fixed verb + object COPIED from the rule text (no invented action names).

One DeepSeek call per rule (prompts/translate_v2.md). The validator is deterministic and,
unlike v1, looks at the rule text: the object must literally appear in the rule or its quote.

Usage:
  uv run python checker/translate_v2.py --run dev_v2 --rules data/dev/rules.json --base data/github/repos
Output: data/runs/<run>/records.json, summary.json
"""

import argparse
import asyncio
import json
import re
from collections import Counter
from pathlib import Path

from llm import LLM
from translate import load_rules

ROOT = Path(__file__).resolve().parents[1]
PROMPT = (ROOT / "prompts" / "translate_v2.md").read_text()
MAX_RETRIES = 2
VERBS = ("run", "edit", "create", "delete", "commit", "read", "use", "set")
KINDS = ("command", "path", "tool", "format", "source", "setting", "code_symbol")
MODALITIES = ("O", "F", "P")
CONDITIONS = ("user_confirmed", "user_requested")


def norm(s):
    """Comparison form of a copied span: lower case, no backticks/quotes, single spaces."""
    return re.sub(r"\s+", " ", re.sub(r"[`'\"*]", "", s.lower())).strip()


def validate(rec, rule, file_text):
    if not isinstance(rec, dict):
        return ["the reply must be one JSON object"]
    if rec.get("fits") is False:
        ok = isinstance(rec.get("unfit_reason"), str) and rec["unfit_reason"].strip()
        return [] if ok else ["fits=false needs a one-sentence unfit_reason"]
    errors = []
    near = norm(rule["quote"] + " " + rule["rule"])
    far = near + " " + norm(file_text)
    if rec.get("modality") not in MODALITIES:
        errors.append(f"modality must be one of {list(MODALITIES)}")
    if rec.get("verb") not in VERBS:
        errors.append(f"verb must be one of {list(VERBS)}; if none describes the rule, set fits=false")
    obj = rec.get("object")
    if not isinstance(obj, dict) or not isinstance(obj.get("text"), str) or not obj["text"].strip():
        errors.append("object must be {'kind': ..., 'text': '<copied name>'}")
    else:
        if obj.get("kind") not in KINDS:
            errors.append(f"object.kind must be one of {list(KINDS)}")
        if norm(obj["text"]) not in near:
            errors.append(f"object.text '{obj['text']}' does not appear in the rule or its quote. Copy the "
                          f"name exactly as written there, or set fits=false if the rule names no such thing.")
        if len(obj["text"].split()) > 6:
            errors.append("object.text is too long: copy only the name itself (at most 6 words)")
    if not isinstance(rec.get("only"), bool):
        errors.append("only must be true or false")
    if (rec.get("verb") == "set") != (rec.get("value") is not None):
        errors.append("value must be given for verb 'set' and be null for every other verb")
    where = rec.get("where")
    if not isinstance(where, list) or not all(isinstance(w, str) for w in where):
        errors.append("where must be a list of copied spans")
    else:
        errors += [f"where '{w}' does not appear in the rule, its quote, or the file: copy it exactly"
                   for w in where if norm(w) not in far]
    for key in ("when", "unless"):
        v = rec.get(key)
        if not isinstance(v, list) or any(c not in CONDITIONS for c in v):
            errors.append(f"{key} must be a list with only {list(CONDITIONS)}")
    actor = rec.get("actor")
    if not isinstance(actor, str) or (actor != "main_agent" and norm(actor) not in far):
        errors.append("actor must be 'main_agent' or a subagent name copied from the text")
    return errors


async def translate_rule(llm, rule, file_text):
    messages = [
        {"role": "system", "content": PROMPT},
        {"role": "user", "content": f"FILE `{rule['file']}`:\n<<<\n{file_text}\n>>>\n\n"
                                    f"RULE to translate:\n- quote: {rule['quote']}\n- rule: {rule['rule']}"},
    ]
    errors, rec = [], None
    for attempt in range(MAX_RETRIES + 1):
        rec = await llm.chat_json(messages)
        errors = validate(rec, rule, file_text)
        if not errors:
            status = "unfit" if rec.get("fits") is False else "valid"
            return {"status": status, "attempts": attempt + 1, "record": rec, "errors": []}
        messages += [{"role": "assistant", "content": json.dumps(rec)},
                     {"role": "user", "content": "The record is invalid:\n- " + "\n- ".join(errors)
                                                 + "\nReturn the corrected full JSON record."}]
    return {"status": "invalid", "attempts": MAX_RETRIES + 1, "record": rec, "errors": errors}


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--rules", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()
    out_dir = ROOT / "data" / "runs" / args.run
    out_dir.mkdir(parents=True, exist_ok=True)
    llm, results = LLM(), []
    items = list(load_rules(ROOT / args.rules, ROOT / args.base))[: args.limit]
    for i, (folder, rule, text) in enumerate(items, 1):
        res = await translate_rule(llm, rule, text)
        results.append({"folder": folder, **rule, **res})
        r = res["record"] if isinstance(res["record"], dict) else {}
        shown = (f"{r.get('modality')} {r.get('verb')} {json.dumps(r.get('object'))}" if res["status"] == "valid"
                 else str(r.get("unfit_reason"))[:60])
        print(f"[{i}/{len(items)}] {res['status']:7} x{res['attempts']} {rule['id']:>4} {rule['rule'][:60]:60} -> {shown}", flush=True)
        (out_dir / "records.json").write_text(json.dumps(results, indent=1, ensure_ascii=False))
    status = Counter(r["status"] for r in results)
    summary = {"run": args.run, "shape": "v2", "model": llm.model, "rules": len(results),
               "valid": status["valid"], "unfit": status["unfit"], "invalid": status["invalid"],
               "coverage": round(status["valid"] / len(results), 3), "usage": llm.usage}
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    asyncio.run(main())
