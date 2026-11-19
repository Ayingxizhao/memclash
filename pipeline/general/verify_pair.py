"""Stage 3, verifier: formalize BOTH rules of a flagged pair in one LLM call, then let Z3 decide.

The LLM is not told the pair was flagged and is not asked for a verdict. It returns shared
names (situations, actions), world facts, and for each rule a `when` and a `demand` formula
(prompts/general/verify_pair.md). Z3 then decides:
  conflict    there is a possible situation in which both rules apply and no behavior meets
              both demands (the situation is returned as a witness)
  compatible  both rules can apply together, and in every such situation both demands can be met
  no_overlap  no possible situation makes both rules apply
  unfit       the LLM said a rule has no checkable behavior
  invalid     the answer does not parse (undeclared name, bad syntax), or one rule cannot be
              met on its own
`same_demand` is true when the two demands are equivalent given the facts.

Second pass. A `compatible` verdict has two possible reasons, recorded as `link`:
  implies      following one rule already satisfies the other (a real "no conflict")
  independent  the two required actions were named separately and nothing says how they relate
For a flagged pair with link `independent`, one more LLM call (prompts/general/verify_link.md) states
how each action of rule A relates to each action of rule B (exclusive / one means the other /
unrelated). The answers are added as facts and Z3 decides again. `first_verdict` keeps the
verdict before the second pass.
Formulas accept `->`; a demand may also name situations (a conditional demand).

Usage:
  uv run python pipeline/general/verify_pair.py --run dev --rules data/dev/rules.json \
      --pairs data/runs/dev/judge.json [--labels data/open_coding/agent_a.json]
Pairs taken: those labelled contradiction/override in --pairs, plus (for analysis) every
labelled pair of --labels.
Output: data/runs/<run>/verify.json
"""

import argparse
import asyncio
import json
import re
from collections import Counter
from itertools import product
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # shared LLM client: pipeline/llm.py

from z3 import And, Bool, BoolVal, Implies, Not, Or, Solver, Xor, sat

from llm import LLM

ROOT = Path(__file__).resolve().parents[2]
PROMPT = (ROOT / "prompts" / "general" / "verify_pair.md").read_text()
LINK_PROMPT = (ROOT / "prompts" / "general" / "verify_link.md").read_text()
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


def decide(f, extra_facts=()):
    """f: the LLM's formalization; extra_facts: formulas added by the second pass.
    Return (verdict, detail)."""
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
        facts = [to_z3(x, both) for x in [*(f.get("facts") or []), *extra_facts]]
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
    if not overlap:
        return "no_overlap", detail
    # why compatible: does following one rule already satisfy the other?
    a_gives_b, b_gives_a = not is_sat(*facts, da, Not(db)), not is_sat(*facts, db, Not(da))
    return "compatible", {**detail, "link": "implies" if a_gives_b or b_gives_a else "independent"}


def names_in(formula, names):
    return [n for n in dict.fromkeys(TOKEN.findall(str(formula))) if n in names]


async def second_pass(llm, f, ra, rb):
    """Ask how the actions of the two rules relate; return (extra facts, the model's answer)."""
    acts = f.get("actions") or {}
    in_a, in_b = names_in(f["rule_a"]["demand"], acts), names_in(f["rule_b"]["demand"], acts)
    pairs = [(a, b) for a in in_a for b in in_b if a != b]
    if not pairs:
        return [], []
    text = (show("A", ra) + "\n\n" + show("B", rb) + "\n\nACTIONS\n"
            + "\n".join(f"- {n}: {acts[n]}" for n in dict.fromkeys(in_a + in_b))
            + f"\n\nRule A requires: {f['rule_a']['demand']}\nRule B requires: {f['rule_b']['demand']}"
            + "\n\nPAIRS\n" + "\n".join(f"- a: {a}   b: {b}" for a, b in pairs))
    ans = await llm.chat_json([{"role": "system", "content": LINK_PROMPT}, {"role": "user", "content": text}])
    answers = [x for x in (ans.get("pairs") or []) if isinstance(x, dict) and (x.get("a"), x.get("b")) in pairs]
    form = {"exclusive": "not ({a} and {b})", "a_means_b": "{a} -> {b}", "b_means_a": "{b} -> {a}"}
    return [form[x["relation"]].format(**x) for x in answers if x.get("relation") in form], answers


def show(tag, r):
    return f"RULE {tag} (file `{r['file']}`)\n- quote: {r['quote']}\n- rule: {r['rule']}"


async def run(llm, rules_path, out_dir, pairs_path, labels_path=None):
    out_dir.mkdir(parents=True, exist_ok=True)
    folders = {(f.get("repo") or f["folder"]): {r["id"]: r for r in f["rules"]}
               for f in json.loads((ROOT / rules_path).read_text())["folders"]}
    todo = {}                                        # (folder, a, b) -> {"judge": label, "gold": label}
    for r in json.loads((ROOT / pairs_path).read_text()):
        if r["label"] in CONFLICT:
            todo.setdefault((r["folder"], *sorted((r["a"], r["b"]))), {})["judge"] = r["label"]
    if labels_path:
        for f in json.loads((ROOT / labels_path).read_text())["folders"]:
            name = f.get("repo") or f["folder"]
            for r in f.get("relations", []):
                if r.get("a") and r.get("b"):
                    todo.setdefault((name, *sorted((r["a"], r["b"]))), {})["gold"] = r["label"]

    results = []
    for (folder, a, b), src in todo.items():
        ra, rb = folders[folder][a], folders[folder][b]
        f = await llm.chat_json([{"role": "system", "content": PROMPT},
                                 {"role": "user", "content": show("A", ra) + "\n\n" + show("B", rb)}])
        verdict, detail = decide(f) if isinstance(f, dict) else ("invalid", {"error": "not an object"})
        if verdict == "compatible" and detail["link"] == "independent" and "judge" in src:
            extra, answers = await second_pass(llm, f, ra, rb)
            detail.update(first_verdict=verdict, link_answers=answers, link_facts=extra)
            if extra:
                again, more = decide(f, extra)
                if again != "invalid":           # an added fact that breaks a rule on its own is ignored
                    verdict = again
                    detail.update({k: v for k, v in more.items() if k in ("witness", "link", "same_demand")})
        results.append({"folder": folder, "a": a, "b": b, **src, "verdict": verdict, **detail,
                        "formal": f, "rule_a": ra["rule"], "rule_b": rb["rule"]})
        print(f"verify {verdict:10} {'(2nd pass)' if 'first_verdict' in detail else '':10} judge={src.get('judge', '-'):13} gold={src.get('gold', '-'):13} {folder[-14:]} {a}-{b}", flush=True)
        (out_dir / "verify.json").write_text(json.dumps(results, indent=1, ensure_ascii=False))
    (out_dir / "verify.json").write_text(json.dumps(results, indent=1, ensure_ascii=False))
    print("verify:", dict(Counter(r["verdict"] for r in results)), flush=True)
    return results


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--rules", required=True)
    ap.add_argument("--pairs", required=True, help="judge.json; its contradiction/override pairs are checked")
    ap.add_argument("--labels", help="also check every labelled pair of this open-coding file")
    args = ap.parse_args()
    asyncio.run(run(LLM(), args.rules, ROOT / "data" / "runs" / args.run, args.pairs, args.labels))
