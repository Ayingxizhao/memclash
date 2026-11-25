"""Agent trial: blinded labelling input, one file per folder (prompts/review/trial_label.md).

Sessions get neutral ids (S001...); the key (session -> run id) is written separately. Command
output is cut to 400 characters. The gate's counterfactual verdicts are never included.
  PYTHONPATH=pipeline uv run python -m rules.trial_label_input
"""

import json
import random
from pathlib import Path

from rules.trial_events import RUNS, steps
from rules.trial_gate import english
from rules.trial_tasks import FAMILIES, FOLDERS, TASKS

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "runs" / "agent_trial" / "label"
REPOS = ROOT / "data" / "github" / "explore" / "repos"


def main():
    OUT.mkdir(exist_ok=True)
    runs = sorted(p for p in RUNS.iterdir() if (p / "meta.json").exists() and not p.name.startswith("pilot"))
    rng = random.Random(2520)
    rng.shuffle(runs)
    key, n = {}, 0
    for k, folder in FOLDERS.items():
        en = english(folder)
        policies = {f: [en[r] for r in rs if r in en] for f, rs in FAMILIES.items()}
        policies = {f: v for f, v in policies.items() if v}
        src = REPOS / folder
        memory = (src / "CLAUDE.md").read_text() + "\n\n" + (src / ".claude" / "memory" / "MEMORY.md").read_text()
        sessions = []
        for r in runs:
            meta, st = steps(r)
            if TASKS[meta["task"]]["folder"] != k:
                continue
            n += 1
            sid = f"S{n:03d}"
            key[sid] = r.name
            for s in st:
                if s["kind"] == "cmd":
                    s["output"] = s["output"][:400]
            sessions.append({"session": sid, "task_text": meta["prompt"], "steps": st})
        doc = {"folder": folder, "policies": policies, "memory_text": memory, "sessions": sessions}
        json.dump(doc, open(OUT / f"input_{k}.json", "w"), indent=1)
        print(k, len(sessions), "sessions", len(json.dumps(doc)) // 1000, "k chars")
    json.dump(key, open(OUT / "key.json", "w"), indent=1)


if __name__ == "__main__":
    main()
