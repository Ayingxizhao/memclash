"""Confirm step: formalize BOTH rules of a candidate pair in one LLM call, then let Z3 decide.

The LLM is not told the pair was flagged and is not asked for a verdict. It returns shared
names (situations, actions), world facts, and for each rule a `when` and a `demand` formula
(prompts/formalize_pair.md). Z3 then decides:
  conflict    there is a possible situation in which both rules apply and no behavior meets
              both demands (the situation is returned as a witness)
  compatible  both rules can apply together, and in every such situation both demands can be met
  no_overlap  no possible situation makes both rules apply
  unfit       the LLM said a rule has no checkable behavior
  invalid     the answer does not parse (undeclared name, bad syntax, a `when` using actions)
Formulas accept `->`; a demand may also name situations (a conditional demand).
`same_demand` is true when the two demands are equivalent given the facts.

Usage:
  uv run python checker/confirm_pair.py --run dev_confirm --rules data/dev/rules.json \
      --pairs data/runs/dev_judge/judge.json [--labels data/open_coding/agent_a.json]
Pairs taken: those labelled contradiction/override in --pairs, plus those in --labels.
Output: data/runs/<run>/confirm.json
"""

import argparse
import asyncio
import json
import re
from collections import Counter
from itertools import product
from pathlib import Path

from z3 import And, Bool, BoolVal, Implies, Not, Or, Solver, Xor, sat

from llm import LLM

ROOT = Path(__file__).resolve().parents[1]
PROMPT = (ROOT / "prompts" / "formalize_pair.md").read_text()
CONFLICT = ("contradiction", "override")
MAX_SITUATIONS = 10


TOKEN = re.compile(r"\s*(->|==|!=|\(|\)|[A-Za-z_][A-Za-z0-9_]*)")


def to_z3(text, names):
    """Parse a formula into Z3. Raises ValueError.
    Operators, loosest first: `->` (right-assoc), `or`, `and`, `not`, `==` / `!=`."""
    text, toks, pos = str(text).strip(), [], 0
    while pos < len(text):
        m = TOKEN.match(text, pos)
        if not m:
            raise ValueError(f"bad formula `{text}`")
        toks.append(m.group(1))
        pos = m.end()
    toks.append(None)
    i = 0

    def take(tok=None):
        nonlocal i
        if tok is not None and toks[i] != tok:
            raise ValueError(f"bad formula `{text}`: expected `{tok}`")
        i += 1
        return toks[i - 1]

    def implies():
        left = disj()
        if toks[i] == "->":
            take()
            return Implies(left, implies())
        return left

    def disj():
        parts = [conj()]
        while toks[i] == "or":
            take()
            parts.append(conj())
        return Or(parts) if len(parts) > 1 else parts[0]

    def conj():
        parts = [neg()]
        while toks[i] == "and":
            take()
            parts.append(neg())
        return And(parts) if len(parts) > 1 else parts[0]

    def neg():
        if toks[i] == "not":
            take()
            return Not(neg())
        left = atom()
        if toks[i] in ("==", "!="):
            op = take()
            right = atom()
            return left == right if op == "==" else Xor(left, right)
        return left

    def atom():
        tok = take()
        if tok == "(":
            inner = implies()
            take(")")
            return inner
        if tok in ("True", "False"):
            return BoolVal(tok == "True")
        if tok is None or tok in ("and", "or", "not", ")", "->", "==", "!="):
            raise ValueError(f"bad formula `{text}`")
        if tok not in names:
            raise ValueError(f"undeclared name `{tok}`")
        return names[tok]

    out = implies()
    if toks[i] is not None:
        raise ValueError(f"bad formula `{text}`: unexpected `{toks[i]}`")
    return out


def is_sat(*fs):
    s = Solver()
    s.add(*fs)
    return s.check() == sat


def decide(f):
    """f: the LLM's formalization. Return (verdict, detail)."""
    try:
        if not (f["rule_a"].get("fits", True) and f["rule_b"].get("fits", True)):
            return "unfit", {}
        sit = {n: Bool(f"sit_{n}") for n in f.get("situations") or {}}
        act = {n: Bool(f"act_{n}") for n in f.get("actions") or {}}
        if set(sit) & set(act):
            raise ValueError("a name is both a situation and an action")
        if len(sit) > MAX_SITUATIONS:
            raise ValueError("too many situations")
        both = {**sit, **act}
        facts = [to_z3(x, both) for x in f.get("facts") or []]
        wa, wb = to_z3(f["rule_a"]["when"], sit), to_z3(f["rule_b"]["when"], sit)
        # a demand may be conditional on the situation ("mutate only if user_confirmed")
        da, db = to_z3(f["rule_a"]["demand"], both), to_z3(f["rule_b"]["demand"], both)
    except (ValueError, KeyError, TypeError, AttributeError) as e:
        return "invalid", {"error": str(e)}

    detail = {"same_demand": not is_sat(*facts, Xor(da, db))}
    overlap = False
    for values in product([False, True], repeat=len(sit)):      # every situation, exhaustively
        fixed = [v == BoolVal(x) for v, x in zip(sit.values(), values)]
        if not is_sat(*facts, *fixed):                           # impossible situation
            continue
        for w, d, tag in ((wa, da, "a"), (wb, db, "b")):         # sanity: a rule alone must be satisfiable
            if is_sat(*facts, *fixed, w) and not is_sat(*facts, *fixed, d):
                return "invalid", {"error": f"rule_{tag} cannot be met on its own"}
        if not is_sat(*facts, *fixed, wa, wb):                   # a rule does not apply
            continue
        overlap = True
        if not is_sat(*facts, *fixed, da, db):                   # no behavior meets both demands
            return "conflict", {**detail, "witness": dict(zip(sit, values))}
    return ("compatible" if overlap else "no_overlap"), detail


def show(tag, r):
    return f"RULE {tag} (file `{r['file']}`)\n- quote: {r['quote']}\n- rule: {r['rule']}"


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--rules", required=True)
    ap.add_argument("--pairs", required=True, help="judge.json; its contradiction/override pairs are checked")
    ap.add_argument("--labels", help="also check every labelled pair of this open-coding file")
    args = ap.parse_args()
    out_dir = ROOT / "data" / "runs" / args.run
    out_dir.mkdir(parents=True, exist_ok=True)

    folders = {(f.get("repo") or f["folder"]): {r["id"]: r for r in f["rules"]}
               for f in json.loads((ROOT / args.rules).read_text())["folders"]}
    todo = {}                                        # (folder, a, b) -> {"judge": label, "gold": label}
    for r in json.loads((ROOT / args.pairs).read_text()):
        if r["label"] in CONFLICT:
            todo.setdefault((r["folder"], *sorted((r["a"], r["b"]))), {})["judge"] = r["label"]
    if args.labels:
        for f in json.loads((ROOT / args.labels).read_text())["folders"]:
            name = f.get("repo") or f["folder"]
            for r in f.get("relations", []):
                if r.get("a") and r.get("b"):
                    todo.setdefault((name, *sorted((r["a"], r["b"]))), {})["gold"] = r["label"]

    llm, results = LLM(), []
    for (folder, a, b), src in todo.items():
        ra, rb = folders[folder][a], folders[folder][b]
        f = await llm.chat_json([{"role": "system", "content": PROMPT},
                                 {"role": "user", "content": show("A", ra) + "\n\n" + show("B", rb)}])
        verdict, detail = decide(f) if isinstance(f, dict) else ("invalid", {"error": "not an object"})
        results.append({"folder": folder, "a": a, "b": b, **src, "verdict": verdict, **detail,
                        "formal": f, "rule_a": ra["rule"], "rule_b": rb["rule"]})
        print(f"{verdict:10} judge={src.get('judge', '-'):13} gold={src.get('gold', '-'):13} {folder[-14:]} {a}-{b}", flush=True)
        (out_dir / "confirm.json").write_text(json.dumps(results, indent=1, ensure_ascii=False))
    print(dict(Counter(r["verdict"] for r in results)), llm.usage)


if __name__ == "__main__":
    asyncio.run(main())
