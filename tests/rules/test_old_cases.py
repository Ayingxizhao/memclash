"""The 25 hand-written cases of the old git checker, converted to the new format
(rules/convert_old.py) and run through the new checker. Each case must give the same verdict,
unless it is listed in CHANGED with the reason."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pipeline" / "git"))
import git_check  # noqa: E402

from rules.convert_old import SAME_VERDICT, convert  # noqa: E402
from rules.pair import check_pair  # noqa: E402

CHANGED = {  # (a, b) -> (new verdict, why it differs from the old one)
    ("L6_cond", "L46"): ("possible_clash", "never commit [in the local clones] vs must commit: "
                         "clashes if the agent works in a local clone (Codex consult 2)"),
}


@pytest.mark.parametrize("a,b,old", git_check.EXPECT)
def test_old_case(a, b, old):
    got, _ = check_pair(convert(git_check.HAND[a]), convert(git_check.HAND[b]))
    if (a, b) in CHANGED:
        assert got == CHANGED[(a, b)][0]
    else:
        assert got in SAME_VERDICT[old], f"old {old}, new {got}"
