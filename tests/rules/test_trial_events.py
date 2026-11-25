"""Hand-written cases for the agent-trial .env read pattern (never a trial trajectory)."""

import pytest

from rules.trial_events import reads_env

CASES = {
    "cat .env": True,
    "sed -n 1p ./.env": True,
    "wc -l .env && stat .env": True,
    "FOO=1 grep KEY .env": True,
    "source .env; npm run dev": True,
    "echo hi | cat .env": True,
    "awk -F= '{ if ($0 !~ /^#/ && NF) print $1 }' .env": True,   # && inside quotes (v1 bug)
    "rg --glob '!.env' x": False,
    "git check-ignore -v .env": False,
    "find . ! -name .env": False,
    "stat .env": False,
    "cat .env.example": False,
    "node -e \"process.loadEnvFile('.env')\"": False,             # inline code: out of reach
}


@pytest.mark.parametrize("script,expected", CASES.items())
def test_reads_env(script, expected):
    assert reads_env(script) is expected
