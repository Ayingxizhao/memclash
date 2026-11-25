"""File-name and branch patterns (ADR 0008, section 4)."""

import pytest

from rules.patterns import glob_re, matches, path_re, target_re

PATH_CASES = [
    ("docs/*", "docs/a.md", True),
    ("docs/*", "docs/a/b.md", False),     # `*` stays inside one folder level
    ("docs/*", "docs", False),
    ("docs/**", "docs/a/b.md", True),
    ("vendor/", "vendor", True),           # the folder itself
    ("vendor/", "vendor/x/y.c", True),     # and everything in it
    ("vendor/", "vendorx", False),
    ("vendor/", "lib/vendor/x", False),    # has a "/": relative to the repo root
    ("server-world.dat", "server-world.dat", True),
    ("server-world.dat", "world/server-world.dat", True),  # bare name: any depth
    ("server-world.dat", "xserver-world.dat", False),
    ("*.md", "README.md", True),
    ("*.md", "docs/guide.md", True),
    ("a/**/b", "a/b", True),
    ("a/**/b", "a/x/y/b", True),
    ("game/objects/*/", "game/objects/01-ship", True),
    ("game/objects/*/", "game/objects/01-ship/main.c", True),
    ("./src/x.py", "src/x.py", True),
    ("src/?.py", "src/a.py", True),
    ("src/?.py", "src/ab.py", False),
]

TARGET_CASES = [
    ((["vendor/"], ["vendor/cmake/"]), "vendor/a.c", True),
    ((["vendor/"], ["vendor/cmake/"]), "vendor/cmake/x.txt", False),
    ((["vendor/"], ["vendor/cmake/"]), "vendor/cmake", False),
]

BRANCH_CASES = [
    ("feat/*", "feat/login", True),
    ("feat/*", "feat/a/b", False),
    ("main", "main", True),
    ("main", "x/main", False),             # no any-depth rule for branch names
    ("release-*", "release-1.2", True),
]


@pytest.mark.parametrize("pattern,text,want", PATH_CASES)
def test_path(pattern, text, want):
    assert matches(path_re(pattern), text) == want


@pytest.mark.parametrize("target,text,want", TARGET_CASES)
def test_target(target, text, want):
    assert matches(target_re(*target), text) == want


@pytest.mark.parametrize("pattern,text,want", BRANCH_CASES)
def test_branch(pattern, text, want):
    assert matches(glob_re(pattern), text) == want
