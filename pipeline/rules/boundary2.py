"""Boundary test, round 2 (docs/review/boundary2_prereg.md): headless-Claude LLM client and steps.

  PYTHONPATH=pipeline uv run python -m rules.boundary2 extract      # Haiku extraction of new repos
"""

import asyncio
import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / "data" / "runs" / "boundary2"
REPOS = ROOT / "data" / "github" / "boundary2" / "repos"
HAIKU = "claude-haiku-5-5"
EMPTY = Path(tempfile.mkdtemp(prefix="b2_"))  # cwd with no CLAUDE.md, so no project instructions load


class ClaudeLLM:
    """Same interface as pipeline/llm.LLM (chat_json, usage), backed by headless Claude Code with no
    tools, no MCP and no user settings."""

    def __init__(self, model=HAIKU, parallel=4):
        self.model, self.sem = model, asyncio.Semaphore(parallel)
        self.usage = {"calls": 0, "input_tokens": 0, "output_tokens": 0, "failed": 0}

    async def chat_json(self, msgs):
        system = "\n".join(m["content"] for m in msgs if m["role"] == "system")
        turns = [m for m in msgs if m["role"] != "system"]
        prompt = turns[0]["content"] if len(turns) == 1 else "\n\n".join(
            f"[{m['role'].upper()}]\n{m['content']}" for m in turns)
        prompt += "\n\nReply with the JSON object only."
        cmd = ["claude", "-p", "--model", self.model, "--tools", "", "--strict-mcp-config",
               "--setting-sources", "project", "--no-session-persistence", "--output-format", "json"]
        if system:
            cmd += ["--system-prompt", system]
        async with self.sem:
            for _ in range(2):
                p = await asyncio.create_subprocess_exec(*cmd, cwd=EMPTY, stdin=asyncio.subprocess.PIPE,
                                                         stdout=asyncio.subprocess.PIPE,
                                                         stderr=asyncio.subprocess.PIPE)
                out, _ = await p.communicate(prompt.encode())
                try:
                    r = json.loads(out)
                    self.usage["calls"] += 1
                    for k in ("input_tokens", "output_tokens"):
                        self.usage[k] += r.get("usage", {}).get(k, 0)
                    m = re.search(r"\{.*\}", r["result"], re.S)
                    return json.loads(m.group(0))
                except Exception:
                    continue
        self.usage["failed"] += 1
        return {}


async def extract():
    sys.path.insert(0, str(ROOT / "prep"))
    sys.path.insert(0, str(ROOT / "pipeline"))
    import extract as ex  # round-1 extractor, unchanged; only the client differs
    out = D / "rules"
    out.mkdir(parents=True, exist_ok=True)
    llm = ClaudeLLM()
    repos = sorted(p.name.replace("__", "/", 1) for p in REPOS.iterdir() if (p / "repo.json").exists())
    for repo in repos:
        if (out / f"{repo.replace('/', '__')}.json").exists():
            continue  # resume
        await ex.extract_repo(llm, repo, out, REPOS)
    print("usage:", llm.usage)
    json.dump(llm.usage, open(D / "extract_usage.json", "w"))


def blind():
    """All extracted rules, by folder, in round 1's blind format (file + rule text only)."""
    out = {}
    for p in sorted((D / "rules").glob("*.json")):
        rec = json.load(open(p))
        out[p.stem] = {r["id"]: {"file": r["file"], "rule": r["rule"]} for r in rec["rules"]}
    json.dump(out, open(D / "full_blind.json", "w"), indent=1, ensure_ascii=False)
    print(len(out), "folders", sum(map(len, out.values())), "rules")


def select(batch=20):
    """Codex eligibility screen, round 1's prompt with only the file path and rule count changed.
    Folders are split into batches (one Codex call each) so each answer stays a manageable size."""
    tpl = (ROOT / "prompts/review/enforce_select_full.md").read_text()
    allr = json.load(open(D / "full_blind.json"))
    folders = sorted(allr)
    sel = D / "select"
    sel.mkdir(exist_ok=True)
    for i in range(0, len(folders), batch):
        part = {f: allr[f] for f in folders[i:i + batch]}
        n = sum(map(len, part.values()))
        name = f"batch{i // batch + 1:02d}"
        if (sel / f"{name}.md").exists():
            continue
        json.dump(part, open(sel / f"{name}_blind.json", "w"), indent=1, ensure_ascii=False)
        prompt = (tpl.replace("data/runs/natural/full_blind.json", f"data/runs/boundary2/select/{name}_blind.json")
                     .replace("1,287", f"{n:,}"))
        codex(name, prompt, "select")
        print(name, n, "rules done")


def select_missing(chunk=700):
    """Mechanical retry (changes.log): re-screen only rules a batch answer left out, in smaller chunks."""
    tpl = (ROOT / "prompts/review/enforce_select_full.md").read_text()
    allr = json.load(open(D / "full_blind.json"))
    miss = [tuple(x) for x in json.load(open(D / "eligible.json"))["missing"]]
    for i in range(0, len(miss), chunk):
        part, name = {}, f"retry{i // chunk + 1:02d}"
        for f, r in miss[i:i + chunk]:
            part.setdefault(f, {})[r] = allr[f][r]
        n = sum(map(len, part.values()))
        json.dump(part, open(D / "select" / f"{name}_blind.json", "w"), indent=1, ensure_ascii=False)
        codex(name, tpl.replace("data/runs/natural/full_blind.json", f"data/runs/boundary2/select/{name}_blind.json")
                       .replace("1,287", f"{n:,}"), "select")
        print(name, n, "rules done")


def select_result():
    """Parse every batch answer; check each rule was judged exactly once."""
    allr = json.load(open(D / "full_blind.json"))
    got = {}
    for p in sorted((D / "select").glob("*.md")):
        m = re.search(r"```json\s*(\{.*\})\s*```", p.read_text(), re.S)
        for r in json.loads(m.group(1))["rules"]:
            got[(r["folder"], r["id"])] = r
    want = {(f, i) for f, rs in allr.items() for i in rs}
    print("judged", len(got), "of", len(want), "missing", len(want - set(got)), "extra", len(set(got) - want))
    el = [k for k, r in got.items() if r["eligible"] and k in want]
    json.dump({"n_rules": len(want), "eligible": [{"folder": f, "id": i, **allr[f][i]} for f, i in sorted(el)],
               "missing": sorted(want - set(got))}, open(D / "eligible.json", "w"), indent=1)
    print("eligible", len(el))


def codex(name, prompt, sub):
    """One read-only Codex call; final message saved to data/runs/boundary2/<sub>/<name>.md."""
    import subprocess
    d = D / sub
    d.mkdir(parents=True, exist_ok=True)
    if (d / f"{name}.md").exists():
        return
    with open(d / f"{name}.log", "w") as log:
        subprocess.run(["codex", "exec", "-s", "read-only", "-o", str(d / f"{name}.md"), prompt],
                       cwd=ROOT, stdin=subprocess.DEVNULL, stdout=log, stderr=log)


def answers(sub, key="rules"):
    out = []
    for p in sorted((D / sub).glob("*.md")):
        m = re.search(r"```json\s*(\{.*\})\s*```", p.read_text(), re.S)
        out += json.loads(m.group(1))[key]
    return out


def translate(batch=50):
    """Codex translates the eligible rules, round 1's prompt with only paths and counts changed."""
    tpl = (ROOT / "prompts/review/boundary_translate.md").read_text()
    from concurrent.futures import ThreadPoolExecutor
    el = json.load(open(D / "eligible.json"))["eligible"]
    pool = ThreadPoolExecutor(4)
    for i in range(0, len(el), batch):
        part, name = el[i:i + batch], f"batch{i // batch + 1:02d}"
        (D / "translate").mkdir(exist_ok=True)
        json.dump({"rules": [{"folder": r["folder"], "id": r["id"], "rule": r["rule"]} for r in part]},
                  open(D / "translate" / f"{name}_english.json", "w"), indent=1)
        pool.submit(codex, name, tpl.replace("data/runs/natural/boundary_rules_english.json",
                                f"data/runs/boundary2/translate/{name}_english.json")
                       .replace("(86 real\nrules)", f"({len(part)} real\nrules)")
                       .replace("all 86 rules", f"all {len(part)} rules"), "translate")
    pool.shutdown(wait=True)
    print("translate done")


def compiles(tr):
    from rules.model import Event, action_clauses, constraints, prepared
    try:
        constraints(Event("t"), prepared(action_clauses(tr["clauses"]), "c"))
        return True
    except Exception:
        return False


def filt():
    """Round 1's fixed filter: status ok; only never / only_if; no when_unmodeled; compiles."""
    el = {(r["folder"], r["id"]): r for r in json.load(open(D / "eligible.json"))["eligible"]}
    tr = {(t["folder"], t["id"]): t for t in answers("translate")}
    keep = []
    for k, t in sorted(tr.items()):
        x = t["translation"]
        if (k in el and x.get("status") == "ok" and x.get("clauses")
                and all(c["type"] in ("never", "only_if") and not c.get("when_unmodeled") for c in x["clauses"])
                and compiles(x)):
            keep.append({**t, "rule": el[k]["rule"]})
    print("translated", len(tr), "of", len(el), "-> filtered", len(keep))
    json.dump({"rules": keep}, open(D / "review_input.json", "w"), indent=1)


def review():
    """Exactness review by a fresh Codex (round 1's prompt, paths and counts changed); the Claude
    review runs as a separate helper on the same file."""
    tpl = (ROOT / "prompts/review/boundary_review.md").read_text()
    n = len(json.load(open(D / "review_input.json"))["rules"])
    codex("codex", tpl.replace("data/runs/natural/boundary_review_input.json", "data/runs/boundary2/review_input.json")
                      .replace("(47 rules", f"({n} rules").replace("for all 47", f"for all {n}"), "review")


# ---------------------------------------------------------------- per stage: blind files, labels, arms, score
def prep(st):
    """Shuffle actions (seed 2520), neutral ids, key file, and the kept rules by folder (English)."""
    import random
    acts = json.load(open(D / f"actions_{st}.json"))["actions"]
    random.Random(2520).shuffle(acts)
    blind, key = [], {}
    for n, a in enumerate(acts, 1):
        i = f"{st.upper()}-{n:03d}"
        blind.append({"id": i, "folder": a["folder"], "description": a["description"], "event": a["event"]})
        key[i] = {k: a[k] for k in ("aid", "rule_id", "category", "intended")}
    rules = {}
    for r in json.load(open(D / f"kept_english_{st}.json"))["rules"]:
        rules.setdefault(r["folder"], {})[r["id"]] = {"rule": r["rule"]}
    json.dump({"actions": blind}, open(D / f"actions_blind_{st}.json", "w"), indent=1)
    json.dump(key, open(D / f"actions_key_{st}.json", "w"), indent=1)
    json.dump(rules, open(D / f"rules_blind_{st}.json", "w"), indent=1)
    print(st, len(blind), "actions", len(rules), "folders")


def label_codex(st):
    n = len(json.load(open(D / f"actions_blind_{st}.json"))["actions"])
    tpl = (ROOT / "prompts/review/boundary_label.md").read_text()
    codex(f"codex_{st}", tpl.replace("data/runs/natural/boundary_actions_blind.json", f"data/runs/boundary2/actions_blind_{st}.json")
                            .replace("data/runs/natural/boundary_rules_blind.json", f"data/runs/boundary2/rules_blind_{st}.json")
                            .replace("(150 proposed", f"({n} proposed").replace("all 150 actions", f"all {n} actions"), "labels")


def gold(st):
    """Agreement of the Claude and Codex labels (same rule set, neither unsure) = gold; rest ambiguous."""
    cl = {x["id"]: x for x in json.load(open(D / "labels" / f"claude_{st}.json"))["labels"]}
    m = re.search(r"```json\s*(\{.*\})\s*```", (D / "labels" / f"codex_{st}.md").read_text(), re.S)
    cx = {x["id"]: x for x in json.loads(m.group(1))["labels"]}
    labels, amb = [], []
    for i in sorted(cl):
        a, b = cl[i], cx.get(i, {})
        if set(a.get("breaks", [])) == set(b.get("breaks", [None])) and not a.get("unsure") and not b.get("unsure"):
            labels.append({"id": i, "breaks": sorted(a["breaks"])})
        else:
            amb.append({"id": i, "claude": a.get("breaks"), "codex": b.get("breaks")})
    json.dump({"how": "Fresh Claude helper and fresh Codex labelled independently; identical rule sets (and no "
               "unsure) = gold; rest ambiguous (prereg).", "labels": labels, "ambiguous": amb},
              open(D / f"labels_final_{st}.json", "w"), indent=1)
    print(st, "gold", len(labels), "ambiguous", len(amb))


def judge_prompts(st):
    R = json.load(open(D / f"rules_blind_{st}.json"))
    A = json.load(open(D / f"actions_blind_{st}.json"))["actions"]
    tpl = (ROOT / "prompts/review/enforce_judge.md").read_text()
    out = {}
    for f in sorted({a["folder"] for a in A}):
        rules = "\n".join(f"{i}: {r['rule']}" for i, r in R[f].items())
        acts = "\n".join(json.dumps({"id": a["id"], **a["event"]}) for a in A if a["folder"] == f)
        out[f] = tpl.format(rules=rules, actions=acts)
    return out


def arms(st):
    """Z3, Codex x3 and Haiku x1 on the same rules and events (prereg 'Arms')."""
    import time
    from concurrent.futures import ThreadPoolExecutor
    from rules.enforce import judge
    J = D / f"judge_{st}"
    J.mkdir(exist_ok=True)
    tr = {(r["folder"], r["id"]): r["translation"] for r in json.load(open(D / f"kept_{st}.json"))["rules"]}
    A = json.load(open(D / f"actions_blind_{st}.json"))["actions"]
    t0, res = time.perf_counter(), []
    for a in A:
        r = judge(a["event"], {i: t for (f, i), t in tr.items() if f == a["folder"]})
        res.append({"action": a["id"], "allowed": r["allowed"], "rule_ids": r["rule_ids"], "errors": r["errors"]})
    json.dump({"arm": "Z3", "seconds": time.perf_counter() - t0, "results": res}, open(J / "Z3.json", "w"), indent=1)
    print("Z3 done", sum(not r["allowed"] for r in res), "blocked", sum(bool(r["errors"]) for r in res), "errors")
    P = judge_prompts(st)
    jobs = [(f"run{k}", f, p) for k in (1, 2, 3) for f, p in P.items()]
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda j: codex(j[1], j[2], f"judge_{st}/codex/{j[0]}"), jobs))
    print("codex done")

    async def haiku():
        llm, out, t = ClaudeLLM(parallel=4), [], time.perf_counter()
        rs = await asyncio.gather(*(llm.chat_json([{"role": "user", "content": p}]) for p in P.values()))
        for r in rs:
            out += r.get("actions", [])
        json.dump({"arm": "haiku", "seconds": time.perf_counter() - t, "usage": llm.usage, "results": out},
                  open(J / "haiku.json", "w"), indent=1)
        print("haiku done", llm.usage)
    asyncio.run(haiku())


def score(st):
    """Round 1's scorer (rules.boundary_score), pointed at this stage's files; ambiguous scored both ways too."""
    import rules.boundary_score as bs
    J = D / f"judge_{st}"
    key = json.load(open(D / f"actions_key_{st}.json"))
    L = json.load(open(D / f"labels_final_{st}.json"))
    res = {"Z3": json.load(open(J / "Z3.json"))["results"], "haiku": json.load(open(J / "haiku.json"))["results"]}
    for k in (1, 2, 3):
        fs = sorted((J / "codex" / f"run{k}").glob("*.md"))
        res[f"codex{k}"] = [x for f in fs for x in bs.parse(f)]
    out = {}
    for mode in ("primary", "amb_as_violation", "amb_as_allowed"):
        g = {x["id"]: set(x["breaks"]) for x in L["labels"]}
        if mode != "primary":
            for x in L["ambiguous"]:
                g[x["id"]] = set((x["claude"] or []) + (x["codex"] or [])) or {"?"} if mode == "amb_as_violation" else set()
        ids = sorted(g)
        A = {}
        for arm, rr in res.items():
            m = {r["action"]: (not r.get("allowed", True), set(r.get("rule_ids") or [])) for r in rr}
            A[arm] = {i: m.get(i, (False, set())) for i in ids}
        t = {}
        for arm, got in A.items():
            p, r, f = bs.prf(got, g, ids)
            t[arm] = {"P": round(p, 3), "R": round(r, 3), "F1": round(f, 3),
                      "exact_set": round(sum((got[i][1] if got[i][0] else set()) == g[i] for i in ids) / len(ids), 3),
                      "acc_by_category": {c: round(sum(got[i][0] == bool(g[i]) for i in ids if key[i]["category"] == c)
                                                   / max(1, sum(key[i]["category"] == c for i in ids)), 3)
                                          for c in sorted({v["category"] for v in key.values()})}}
        llm = [a for a in A if a != "Z3"]
        best = max(llm, key=lambda a: t[a]["F1"])
        import random
        rules = sorted({key[i]["aid"].rsplit("-", 1)[0] for i in ids})
        by = {r: [i for i in ids if key[i]["aid"].rsplit("-", 1)[0] == r] for r in rules}
        rng, diffs = random.Random(2520), []
        for _ in range(2000):
            s = [i for r in (rng.choice(rules) for _ in rules) for i in by[r]]
            diffs.append(bs.prf(A["Z3"], g, s)[2] - bs.prf(A[best], g, s)[2])
        diffs.sort()
        t["_bootstrap"] = {"vs": best, "diff_F1": round(t["Z3"]["F1"] - t[best]["F1"], 3),
                           "ci95": [round(diffs[49], 3), round(diffs[1949], 3)]}
        out[mode] = {"n": len(ids), "table": t}
    json.dump(out, open(J / "scores.json", "w"), indent=1)
    for a, v in out["primary"]["table"].items():
        print(a, {k: v[k] for k in v if k != "acc_by_category"})


if __name__ == "__main__":
    f = {"extract": lambda: asyncio.run(extract()), "blind": blind, "select": select,
     "select_result": select_result, "select_missing": select_missing, "translate": translate, "filter": filt, "review": review}.get(sys.argv[1]) or (lambda: {
        "prep": prep, "label_codex": label_codex, "gold": gold, "arms": arms, "score": score}[sys.argv[1]](sys.argv[2]))
    f()
