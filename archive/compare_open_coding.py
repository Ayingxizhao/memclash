"""Align agent_a vs agent_b open-coding relations by quote overlap.

Rule segmentation differs between annotators, so relations are matched at the
span level: A-relation (a1,a2) matches B-relation (b1,b2) if each side's quote
overlaps (token-containment >= 0.5) with a side of the other, in either order.
Output: data/open_coding/comparison.md
"""

import json
import re
from pathlib import Path

D = Path(__file__).resolve().parents[1] / "data" / "open_coding"


def toks(s):
    s = re.sub(r"[*`\\]", "", s.lower())
    return set(re.findall(r"[a-z0-9_<>]+", s))


def overlap(q1, q2):
    t1, t2 = toks(q1), toks(q2)
    return len(t1 & t2) / min(len(t1), len(t2)) if t1 and t2 else 0.0


def load(name):
    d = json.loads((D / f"{name}.json").read_text())
    out = {}
    for f in d["folders"]:
        rules = {r["id"]: r for r in f["rules"]}
        rels = []
        for x in f["relations"]:
            ra, rb = rules.get(x["a"]), rules.get(x.get("b"))
            rels.append({**x, "qa": ra["quote"] if ra else "", "qb": rb["quote"] if rb else "",
                         "fa": ra["file"] if ra else "", "fb": rb["file"] if rb else ""})
        out[f["repo"]] = {"rules": rules, "rels": rels}
    return out


def side_match(q, r):
    return max(overlap(q, r["qa"]), overlap(q, r["qb"]) if r["qb"] else 0)


def rel_match(x, y, th=0.5):
    if not x["qb"] or not y["qb"]:  # single-sided relations (e.g. dangling ref): match on one side
        return max(overlap(x["qa"], y["qa"]), overlap(x["qa"], y["qb"] or ""),
                   overlap(x["qb"] or "", y["qa"])) >= th
    straight = overlap(x["qa"], y["qa"]) >= th and overlap(x["qb"], y["qb"]) >= th
    crossed = overlap(x["qa"], y["qb"]) >= th and overlap(x["qb"], y["qa"]) >= th
    return straight or crossed


def main():
    A, B = load("agent_a"), load("agent_b")
    lines = ["# Open coding comparison: agent_a vs agent_b", "",
             "Matching is by quote overlap, not IDs (segmentation differs). One relation may match",
             "several on the other side (e.g. B splits one index line into several pairs).", ""]
    tot = {"both": 0, "a_only": 0, "b_only": 0, "label_agree": 0}
    for repo in A:
        a, b = A[repo]["rels"], B.get(repo, {"rels": []})["rels"]
        lines += [f"## {repo}", ""]
        b_hit = set()
        rows = []
        for x in a:
            ms = [j for j, y in enumerate(b) if rel_match(x, y)]
            b_hit.update(ms)
            if ms:
                tot["both"] += 1
                labs = sorted({b[j]["label"] for j in ms})
                agree = x["label"] in labs
                tot["label_agree"] += agree
                rows.append(f"- **BOTH** A:{x['a']}-{x['b']} `{x['label']}` | B:{', '.join(b[j]['a'] + '-' + str(b[j]['b']) for j in ms)} `{'/'.join(labs)}`"
                            f"{'' if agree else '  ← label differs'}")
            else:
                tot["a_only"] += 1
                rows.append(f"- **A only** {x['a']}-{x['b']} `{x['label']}` ({x['confidence']}): {x['explanation'][:160]}")
        for j, y in enumerate(b):
            if j not in b_hit:
                tot["b_only"] += 1
                rows.append(f"- **B only** {y['a']}-{y['b']} `{y['label']}` ({y['confidence']}): {y['explanation'][:160]}")
        lines += rows + [""]
    lines.insert(5, f"**Totals:** A relations matched by B: {tot['both']}; A only: {tot['a_only']}; "
                    f"B relations unmatched: {tot['b_only']}; label agreement on matched A relations: "
                    f"{tot['label_agree']}/{tot['both']}.\n")
    (D / "comparison.md").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
