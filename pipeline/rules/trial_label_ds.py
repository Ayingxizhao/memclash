"""Agent trial: DeepSeek labels (replaces Codex after the spend cap; changes.log).
  PYTHONPATH=pipeline uv run python -m rules.trial_label_ds A D
"""
import asyncio
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
L = ROOT / "data" / "runs" / "agent_trial" / "label"
TPL = (ROOT / "prompts" / "review" / "trial_label.md").read_text()


async def main(keys):
    os.environ["LLM_PROVIDER"] = "2"
    sys.path.insert(0, str(ROOT / "pipeline"))
    from llm import LLM
    llm = LLM()
    for k in keys:
        text = (L / f"input_{k}.json").read_text()
        p = TPL.replace("Input file: {input}", "Input (JSON):\n" + text)
        out = await llm.chat_json([{"role": "user", "content": p}])
        json.dump(out, open(L / f"deepseek_{k}.json", "w"), indent=1)
        print(k, len(out.get("labels", [])), llm.usage, flush=True)


asyncio.run(main(sys.argv[1:]))
