"""Run agent-trial sessions with Codex (docs/review/agent_trial_prereg.md).

  PYTHONPATH=pipeline uv run python -m rules.trial_run <run_id> <task> <cond>   # one run
  PYTHONPATH=pipeline uv run python -m rules.trial_run plan [--pilot]           # print the run list
Sandboxes live in the scratch directory given by TRIAL_SCRATCH; results are copied to
data/runs/agent_trial/runs/<run_id>/.
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from rules.trial_sandbox import build
from rules.trial_tasks import TASKS, prompt

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "runs" / "agent_trial" / "runs"
MODEL = "gpt-5.6-sol"
EFFORT = "medium"


def run(run_id, task, cond):
    scratch = Path(os.environ["TRIAL_SCRATCH"]) / hashlib.sha1(run_id.encode()).hexdigest()[:10]
    ws, aux = build(scratch, task, cond)
    p = prompt(task, cond)
    initial = sorted(str(f.relative_to(ws)) for f in ws.rglob("*") if f.is_file() and f.name != ".git")
    out = OUT / run_id
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    cmd = ["codex", "exec", "--json", "-s", "workspace-write", "--skip-git-repo-check",
           "-m", MODEL, "-c", f"model_reasoning_effort={EFFORT}", "--add-dir", str(aux), "--add-dir", str(scratch / "origin.git"), "-C", str(ws), p]
    t0 = time.time()
    with open(out / "codex.jsonl", "w") as f, open(out / "codex.err", "w") as e:
        rc = subprocess.run(cmd, stdout=f, stderr=e, stdin=subprocess.DEVNULL, timeout=1800).returncode
    secs = time.time() - t0
    shutil.copy(aux / "hooklog.jsonl", out / "acts.jsonl")
    g = lambda *a: subprocess.run(["git", *a], cwd=ws, capture_output=True, text=True).stdout
    (out / "git.txt").write_text("## status\n" + g("status", "--short", "--branch") + "\n## branches\n" +
                                 g("branch", "-a") + "\n## log\n" + g("log", "--all", "--oneline", "--graph") +
                                 "\n## diff vs first commit\n" + g("diff", "--stat", g("rev-list", "--max-parents=0", "HEAD").strip()))
    json.dump({"run_id": run_id, "task": task, "cond": cond, "prompt": p, "model": MODEL, "effort": EFFORT,
               "codex_rc": rc, "initial_files": initial, "seconds": round(secs, 1), "ws": str(ws)}, open(out / "meta.json", "w"), indent=1)
    print(run_id, task, cond, rc, round(secs), flush=True)


def plan():
    """70 scored runs (prereg): NI, MS, ML x 2 repeats, MG x 1; repeat 1 of all first."""
    out = []
    for r in (1, 2):
        for task in TASKS:
            for cond in ("NI", "MS", "ML", "MG"):
                if cond == "MG" and r == 2:
                    continue
                out.append((f"{task}-{cond}-{r}", task, cond))
    return out


if __name__ == "__main__":
    if sys.argv[1] == "plan":
        for r in plan():
            print(*r)
    else:
        run(*sys.argv[1:4])
