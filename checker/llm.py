"""DeepSeek client (OpenAI-compatible) with an on-disk cache.

Config comes from /Users/yingxizhao/dev/cs2520/.env (keys are matched case-insensitively):
  DEEPSEEK_API_KEY, model, Base_URL
Every call is cached by sha256(model, messages, temperature) in data/llm_cache.jsonl,
so reruns are free and reproducible.
"""

import asyncio
import hashlib
import json
from pathlib import Path

from openai import AsyncOpenAI

ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
CACHE_PATH = Path(__file__).resolve().parents[1] / "data" / "llm_cache.jsonl"


def load_env(path=ENV_PATH):
    env = {}
    for line in path.read_text().splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip().lower()] = v.strip().strip("'\"")
    return env


class LLM:
    def __init__(self, concurrency=1):  # endpoint allows 1 concurrent request
        env = load_env()
        self.model = env["model"]
        self.client = AsyncOpenAI(api_key=env["deepseek_api_key"], base_url=env["base_url"])
        self.sem = asyncio.Semaphore(concurrency)
        self.cache = {}
        if CACHE_PATH.exists():
            for line in CACHE_PATH.open():
                e = json.loads(line)
                self.cache[e["key"]] = e
        self.usage = {"calls": 0, "cached": 0, "prompt_tokens": 0, "completion_tokens": 0}

    def _key(self, messages, temperature):
        blob = json.dumps({"model": self.model, "messages": messages, "t": temperature}, sort_keys=True)
        return hashlib.sha256(blob.encode()).hexdigest()

    async def chat_json(self, messages, temperature=0.0, retries=4):
        """Return parsed JSON object from the model (json_object response format)."""
        key = self._key(messages, temperature)
        if key in self.cache:
            self.usage["cached"] += 1
            return json.loads(self.cache[key]["content"])
        async with self.sem:
            for attempt in range(retries):
                try:
                    r = await self.client.chat.completions.create(
                        model=self.model, messages=messages, temperature=temperature,
                        response_format={"type": "json_object"},
                    )
                    content = r.choices[0].message.content
                    parsed = json.loads(content)
                    break
                except Exception as e:  # network / rate limit / bad JSON
                    if attempt == retries - 1:
                        raise
                    print(f"  llm retry {attempt + 1}: {type(e).__name__}: {str(e)[:120]}")
                    await asyncio.sleep(2 ** attempt)
        self.usage["calls"] += 1
        if r.usage:
            self.usage["prompt_tokens"] += r.usage.prompt_tokens
            self.usage["completion_tokens"] += r.usage.completion_tokens
        entry = {"key": key, "model": self.model, "messages": messages, "content": content}
        self.cache[key] = entry
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with CACHE_PATH.open("a") as f:
            f.write(json.dumps(entry) + "\n")
        return parsed


if __name__ == "__main__":  # smoke test
    async def _t():
        llm = LLM()
        out = await llm.chat_json([{"role": "user", "content": 'Reply with JSON {"ok": true, "model": "<your name>"}'}])
        print(llm.model, out, llm.usage)
    asyncio.run(_t())
