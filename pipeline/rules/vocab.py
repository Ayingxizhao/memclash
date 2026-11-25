"""The fixed word list (vocabulary v2, docs/adr/0008, sections 2-3). Everything a translation
may name is listed here; any other name is an error."""

GIT_CMDS = ["commit", "stage", "push_branch", "push_delete", "force_push", "local_merge",
            "pr_create", "pr_merge", "branch_create", "branch_delete", "checkout", "pull",
            "rebase", "reset_hard", "cherry_pick", "fetch", "worktree_add", "worktree_remove"]
FILE_CMDS = ["read", "create", "edit", "move", "delete"]
CMDS = GIT_CMDS + FILE_CMDS + ["run"]

# Fixed meanings: every kind of push is a push, every kind of merge is a merge. No file groups.
GROUPS = {"push": ["push_branch", "push_delete", "force_push"],
          "merge": ["local_merge", "pr_merge"],
          "any_branch_delete": ["branch_delete", "push_delete"]}

TASKS = ["test", "build", "lint", "format", "deploy", "migrate", "publish", "restart"]
OTHER_TASK = "other:"  # any other task: "other:<exact words>", matched only if identical

# Yes/no fields. The agent decides these as part of the action (it can ask for approval).
ACTION_BOOLS = ["has_secret", "user_confirmed", "files_shown", "secrets_checked",
                "admin_bypass", "in_worktree"]
# Yes/no fields the situation fixes; the agent cannot change them.
WORLD_BOOLS = ["user_asked", "tests_passed"]
BOOLS = ACTION_BOOLS + WORLD_BOOLS

PATH_FIELDS = ["path", "dest_path"]          # targets (patterns.path_re)
BRANCH_FIELDS = ["branch"]                   # globs (patterns.glob_re)
# Details of the earlier step that `after` names (vocabulary v2.1): each refers to the same
# earlier step, one earlier step per action kind.
AFTER_FIELDS = ["after_branch", "after_task", "after_path", "after_ok"]
FILE_ACTIONS = ["read", "create", "edit", "move", "delete", "stage", "commit"]
FIELDS = (["cmd", "path_except", "kind", "task", "suite", "after", "running",
           "min_files", "max_files"] + PATH_FIELDS + BRANCH_FIELDS + AFTER_FIELDS + BOOLS)

# Which fields describe the situation a pair is tested in: see pair.situations.

CLAUSE_TYPES = ["never", "only_if", "must_do", "may_do", "must_hold", "never_hold"]
STATE_TYPES = ["must_hold", "never_hold"]


def expand(names):
    """Action names and groups -> sorted list of actions."""
    out = []
    for n in names if isinstance(names, list) else [names]:
        if n in GROUPS:
            out += GROUPS[n]
        elif n in CMDS:
            out.append(n)
        else:
            raise ValueError(f"unknown action {n!r}")
    return sorted(set(out))


def norm_name(name):
    """Process and task names match only if identical after trivial clean-up:
    case, extra spaces and a leading "the" ("The game server" = "game server")."""
    s = " ".join(str(name).lower().split())
    return s[4:] if s.startswith("the ") else s


def task_name(task):
    t = str(task).strip()
    if t in TASKS:
        return t
    if t.startswith(OTHER_TASK) and len(t) > len(OTHER_TASK):
        return OTHER_TASK + norm_name(t[len(OTHER_TASK):])
    raise ValueError(f"unknown task {task!r}")
