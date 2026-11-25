"""DeepSeek client (OpenAI-compatible) with an on-disk cache.

Config comes from /Users/yingxizhao/dev/cs2520/.env (keys are matched case-insensitively):
  DEEPSEEK_API_KEY, model, Base_URL
Every call is cached by sha256(model, messages, temperature) in data/llm_cache.jsonl,
so reruns are free and reproducible.
LLM_PROVIDER=2 selects the second endpoint (DEEPSEEK_API_KEY2, Base_URL2); default is 1.
Each request times out after 120 s and is retried.
"""

import asyncio
import hashlib
import json
import os
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


class OutputCutOff(Exception):
    """The model stopped at its output limit; retrying would pay for the same reply again."""


class LLM:
    def __init__(self, concurrency=1, model=None):  # endpoint allows 1 concurrent request
        env = load_env()
        self.model = model or env["model"]             # model: override, e.g. the injection writer
        p = os.environ.get("LLM_PROVIDER", "1")       # "2": the second endpoint in .env
        sfx = "" if p == "1" else p
        self.client = AsyncOpenAI(api_key=env[f"deepseek_api_key{sfx}"],
                                  base_url=env[f"base_url{sfx}"], timeout=120, max_retries=0)
        # strict tool calls are a beta feature of the official API: same key, /beta base URL
        self.beta_url = env[f"base_url{sfx}"].rstrip("/").removesuffix("/v1") + "/beta"
        self.beta_client = None
        self.api_key = env[f"deepseek_api_key{sfx}"]
        self.sem = asyncio.Semaphore(int(os.environ.get("LLM_CONCURRENCY", concurrency)))
        self.cache = {}
        if CACHE_PATH.exists():
            for line in CACHE_PATH.open():
                e = json.loads(line)
                self.cache[e["key"]] = e
        self.usage = {"calls": 0, "cached": 0, "prompt_tokens": 0, "completion_tokens": 0}
        # LLM_THINKING=off switches DeepSeek's thinking mode off (default: the model's own, on)
        self.thinking_off = os.environ.get("LLM_THINKING", "").lower() == "off"

    def _count_failed(self, r):
        """Tokens of a reply that was billed but not usable (cut off or bad JSON)."""
        if getattr(r, "usage", None):
            self.usage["failed_calls"] = self.usage.get("failed_calls", 0) + 1
            self.usage["failed_completion_tokens"] = (self.usage.get("failed_completion_tokens", 0)
                                                      + r.usage.completion_tokens)

    def _key(self, messages, temperature, run=0, tool=None):
        d = {"model": self.model, "messages": messages, "t": temperature}
        if run:  # repeated runs of the same request are cached separately (old keys unchanged)
            d["run"] = run
        if tool:
            d["tool"] = tool
        if getattr(self, "thinking_off", False):
            d["thinking"] = "off"
        blob = json.dumps(d, sort_keys=True)
        return hashlib.sha256(blob.encode()).hexdigest()

    async def chat_json(self, messages, temperature=0.0, retries=4, run=0, tool=None):
        """Return parsed JSON object from the model (json_object response format).
        temperature None: the model's default sampling. run: a label for repeated runs of the
        same request, so each run is a separate call and a separate cache entry.
        tool: a strict function tool; the model must call it, and its arguments are returned
        (the server enforces the tool's schema; beta endpoint)."""
        key = self._key(messages, temperature, run, tool)
        if key in self.cache:
            self.usage["cached"] += 1
            return json.loads(self.cache[key]["content"])
        async with self.sem:
            for attempt in range(retries):
                try:
                    extra = {} if temperature is None else {"temperature": temperature}
                    if self.thinking_off:
                        extra["extra_body"] = {"thinking": {"type": "disabled"}}
                    if tool:
                        if self.beta_client is None:
                            self.beta_client = AsyncOpenAI(api_key=self.api_key, base_url=self.beta_url,
                                                           timeout=120, max_retries=0)
                        name = tool["function"]["name"]
                        # thinking mode accepts only tool_choice "auto"; a reply without the
                        # tool call is treated like bad JSON and asked again
                        # without thinking, the tool call can be forced
                        choice = ({"type": "function", "function": {"name": name}}
                                  if self.thinking_off else "auto")
                        r = await self.beta_client.chat.completions.create(
                            model=self.model, messages=messages, **extra, tools=[tool],
                            tool_choice=choice,
                        )
                        calls = [c for c in (r.choices[0].message.tool_calls or [])
                                 if c.function.name == name]
                        if not calls:
                            raise ValueError("the model did not call the tool")
                        content = calls[0].function.arguments
                    else:
                        r = await self.client.chat.completions.create(
                            model=self.model, messages=messages, **extra,
                            response_format={"type": "json_object"},
                        )
                        content = r.choices[0].message.content
                        if r.choices[0].finish_reason == "length":
                            # the reply was cut off (output limit): a retry would pay for the
                            # same long reply again, so stop here
                            self._count_failed(r)
                            raise OutputCutOff("reply cut off at the output limit")
                    try:
                        parsed = json.loads(content)
                    except json.JSONDecodeError:
                        self._count_failed(r)  # billed even though unusable
                        raise
                    break
                except OutputCutOff:
                    raise
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
        if tool:
            entry["tool"] = tool["function"]["name"]
        if run:
            entry["run"] = run
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
