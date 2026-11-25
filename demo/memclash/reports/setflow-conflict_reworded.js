window.MEMCLASH_REPORT = {
 "tool": "memclash",
 "format": 1,
 "created": "2026-11-22",
 "folder": "M-Hernandez/setflow#conflict_reworded",
 "model": "deepseek-v4-flash",
 "run": 1,
 "source": "data/runs/rules/pilot/translations_run1.json",
 "summary": {
  "rules": 21,
  "checked": 14,
  "not_in_scope": 7,
  "unclear": 0,
  "bad_output": 0,
  "with_unknown_condition": 1,
  "clash": 5,
  "exception": 1,
  "state_conflict": 0
 },
 "rules": [
  {
   "id": "R1",
   "file": "feedback_cleanup_branches.md",
   "rule": "After every merge to main, delete the feature branch locally and on the remote.",
   "status": "ok",
   "word": "",
   "reason": "after every merge to main, delete the feature branch locally and on the remote",
   "left_out": "\"the feature branch\" names no specific branch, so no branch name is given for the deletion",
   "retried": false,
   "off_template": false,
   "clauses": [
    {
     "type": "must_do",
     "where": {
      "cmd": [
       "branch_delete"
      ],
      "after": [
       "merge"
      ],
      "after_branch": "main"
     },
     "text": "Must delete a branch locally after a merge into main"
    },
    {
     "type": "must_do",
     "where": {
      "cmd": [
       "push_delete"
      ],
      "after": [
       "merge"
      ],
      "after_branch": "main"
     },
     "text": "Must delete a branch on the remote after a merge into main"
    }
   ],
   "unmodeled": []
  },
  {
   "id": "R2",
   "file": "feedback_cleanup_branches.md",
   "rule": "After gh pr merge, run git branch -d and git push origin --delete for the branch, then switch to main and pull.",
   "status": "ok",
   "word": "",
   "reason": "after a PR merge, delete the branch locally and remotely, then switch to main and pull",
   "left_out": "",
   "retried": false,
   "off_template": false,
   "clauses": [
    {
     "type": "must_do",
     "where": {
      "cmd": [
       "branch_delete"
      ],
      "after": [
       "pr_merge"
      ]
     },
     "text": "Must delete a branch locally after a PR merge"
    },
    {
     "type": "must_do",
     "where": {
      "cmd": [
       "push_delete"
      ],
      "after": [
       "pr_merge"
      ]
     },
     "text": "Must delete a branch on the remote after a PR merge"
    },
    {
     "type": "must_do",
     "where": {
      "cmd": [
       "checkout"
      ],
      "after": [
       "branch_delete",
       "push_delete"
      ],
      "branch": "main"
     },
     "text": "Must switch branch on branch main, after a local branch delete or a remote branch delete"
    },
    {
     "type": "must_do",
     "where": {
      "cmd": [
       "pull"
      ],
      "after": [
       "checkout"
      ],
      "branch": "main"
     },
     "text": "Must pull on branch main, after switching branch"
    }
   ],
   "unmodeled": []
  },
  {
   "id": "R3",
   "file": "feedback_confirm_before_push.md",
   "rule": "Before git push, git merge, or creating a PR, confirm with the user which files will be pushed or merged.",
   "status": "ok",
   "word": "",
   "reason": "confirm with the user before push, merge, or PR creation",
   "left_out": "",
   "retried": false,
   "off_template": true,
   "clauses": [
    {
     "type": "only_if",
     "where": {
      "cmd": [
       "push",
       "merge",
       "pr_create"
      ]
     },
     "needs": {
      "user_confirmed": true,
      "files_shown": true
     },
     "text": "Push (any kind) or merge (any kind) or open a pull request, only if with the user's approval, the files were shown to the user"
    }
   ],
   "unmodeled": []
  },
  {
   "id": "R4",
   "file": "feedback_confirm_before_push.md",
   "rule": "Do not assume approval for pushes/merges; show the file list and get explicit approval.",
   "status": "ok",
   "word": "",
   "reason": "pushes and merges need the file list shown and explicit approval",
   "left_out": "\"Do not assume approval\" — no separate requirement beyond the explicit-approval need",
   "retried": false,
   "off_template": true,
   "clauses": [
    {
     "type": "only_if",
     "where": {
      "cmd": [
       "push",
       "merge"
      ]
     },
     "needs": {
      "files_shown": true,
      "user_confirmed": true
     },
     "text": "Push (any kind) or merge (any kind), only if the files were shown to the user, with the user's approval"
    }
   ],
   "unmodeled": []
  },
  {
   "id": "R5",
   "file": "feedback_confirm_before_push.md",
   "rule": "Before any git push or gh pr create, show the changed files and ask for confirmation.",
   "status": "ok",
   "word": "",
   "reason": "before push or PR creation, show changed files and get confirmation",
   "left_out": "",
   "retried": false,
   "off_template": true,
   "clauses": [
    {
     "type": "only_if",
     "where": {
      "cmd": [
       "push",
       "pr_create"
      ]
     },
     "needs": {
      "files_shown": true,
      "user_confirmed": true
     },
     "text": "Push (any kind) or open a pull request, only if the files were shown to the user, with the user's approval"
    }
   ],
   "unmodeled": []
  },
  {
   "id": "R6",
   "file": "feedback_no_credentials_in_repo.md",
   "rule": "Never commit credentials to the repo.",
   "status": "ok",
   "word": "",
   "reason": "never do X (commit files holding credentials)",
   "left_out": "",
   "retried": false,
   "off_template": true,
   "clauses": [
    {
     "type": "never",
     "where": {
      "cmd": [
       "commit"
      ],
      "has_secret": true
     },
     "text": "Never commit a file holding secrets"
    }
   ],
   "unmodeled": []
  },
  {
   "id": "R7",
   "file": "feedback_no_credentials_in_repo.md",
   "rule": "Keep credentials in gitignored .env files; commit only .env.example with placeholder values.",
   "status": "ok",
   "word": "",
   "reason": "credentials stay out of the repo; only the example file is committed",
   "left_out": "\"with placeholder values\" (file content requirement)",
   "retried": false,
   "off_template": false,
   "clauses": [
    {
     "type": "never_hold",
     "where": {
      "in_repo": [
       ".env"
      ]
     },
     "text": "Must not be in the repo: .env"
    },
    {
     "type": "must_hold",
     "where": {
      "in_repo": [
       ".env.example"
      ]
     },
     "text": "Must be in the repo: .env.example"
    }
   ],
   "unmodeled": []
  },
  {
   "id": "R8",
   "file": "feedback_no_credentials_in_repo.md",
   "rule": "Before any commit, verify no .env files, API keys, or secrets are staged.",
   "status": "ok",
   "word": "",
   "reason": "before committing, verify no secrets are staged",
   "left_out": "\".env files, API keys, or secrets\" as the thing checked (named group, no path given)",
   "retried": false,
   "off_template": false,
   "clauses": [
    {
     "type": "only_if",
     "where": {
      "cmd": [
       "commit"
      ]
     },
     "needs": {
      "secrets_checked": true
     },
     "text": "Commit, only if secrets were checked first"
    }
   ],
   "unmodeled": []
  },
  {
   "id": "R9",
   "file": "feedback_no_credentials_in_repo.md",
   "rule": "Load any credentials used by code from environment variables.",
   "status": "not_in_scope",
   "word": "",
   "reason": "how code reads credentials, not about git, files or running a task",
   "left_out": "",
   "retried": false,
   "off_template": false,
   "clauses": [],
   "unmodeled": []
  },
  {
   "id": "R10",
   "file": "feedback_no_credentials_in_repo.md",
   "rule": "Immediately flag hardcoded values that look like real credentials.",
   "status": "not_in_scope",
   "word": "",
   "reason": "code-review practice about spotting credentials, not a git, file or task action",
   "left_out": "",
   "retried": false,
   "off_template": false,
   "clauses": [],
   "unmodeled": []
  },
  {
   "id": "R11",
   "file": "project_phase0_progress.md",
   "rule": "Work on issue #17 next: run the ingestion pipeline end-to-end on 6 seed DJs before Phase 2.",
   "status": "ok",
   "word": "",
   "reason": "run a named task before a later phase",
   "left_out": "\"Work on issue #17 next\" (ordering of work items) and \"end-to-end on 6 seed DJs\" (details of the task)",
   "retried": false,
   "off_template": false,
   "clauses": [
    {
     "type": "must_do",
     "where": {
      "cmd": [
       "run"
      ],
      "task": "other:ingestion pipeline"
     },
     "when_unmodeled": "before Phase 2",
     "text": "Must run task “ingestion pipeline” (only when: before Phase 2, which the format cannot check)"
    }
   ],
   "unmodeled": [
    "before Phase 2"
   ]
  },
  {
   "id": "R12",
   "file": "reference_local_setup.md",
   "rule": "Do not use the system Python 3.9.6 (/usr/bin/python3) for this project.",
   "status": "not_in_scope",
   "word": "",
   "reason": "which tool/interpreter to use, not git, files or running a task",
   "left_out": "",
   "retried": false,
   "off_template": false,
   "clauses": [],
   "unmodeled": []
  },
  {
   "id": "R13",
   "file": "user_profile.md",
   "rule": "(Preference) Always confirm files with the user before push/merge.",
   "status": "ok",
   "word": "",
   "reason": "confirm with the user before push or merge",
   "left_out": "",
   "retried": false,
   "off_template": true,
   "clauses": [
    {
     "type": "only_if",
     "where": {
      "cmd": [
       "push",
       "merge"
      ]
     },
     "needs": {
      "user_confirmed": true
     },
     "text": "Push (any kind) or merge (any kind), only if with the user's approval"
    }
   ],
   "unmodeled": []
  },
  {
   "id": "R14",
   "file": "user_profile.md",
   "rule": "(Preference) Keep the repo clean: no stale branches, no credentials, tested code.",
   "status": "not_in_scope",
   "word": "",
   "reason": "nothing left",
   "left_out": "",
   "retried": false,
   "off_template": false,
   "clauses": [],
   "unmodeled": []
  },
  {
   "id": "R15",
   "file": "user_profile.md",
   "rule": "(Preference) Work incrementally with feature branches, PRs, merge, and cleanup.",
   "status": "ok",
   "word": "",
   "reason": "Stated as a preference, so the git actions are permitted rather than required; vague parts dropped.",
   "left_out": "\"work incrementally\" and \"cleanup\" are too vague to describe.",
   "retried": false,
   "off_template": false,
   "clauses": [
    {
     "type": "may_do",
     "where": {
      "cmd": [
       "branch_create"
      ]
     },
     "text": "May create a branch"
    },
    {
     "type": "may_do",
     "where": {
      "cmd": [
       "pr_create"
      ]
     },
     "text": "May open a pull request"
    },
    {
     "type": "may_do",
     "where": {
      "cmd": [
       "merge"
      ]
     },
     "text": "May merge (any kind)"
    }
   ],
   "unmodeled": []
  },
  {
   "id": "R16",
   "file": "MEMORY.md",
   "rule": "(Index) Next work items are issues #4 and #5.",
   "status": "not_in_scope",
   "word": "",
   "reason": "project planning note about which issues come next, not about git, files or running a task",
   "left_out": "",
   "retried": false,
   "off_template": false,
   "clauses": [],
   "unmodeled": []
  },
  {
   "id": "X2",
   "file": "feedback_preserve_work.md",
   "rule": "Once a pull request is merged into the primary branch, retain the source branch in both local and remote repositories.",
   "status": "ok",
   "word": "",
   "reason": "after a PR merge, the source branch must not be deleted locally or on the remote",
   "left_out": "the primary branch and the source branch are not named, so no branch value is given",
   "retried": false,
   "off_template": false,
   "clauses": [
    {
     "type": "never",
     "where": {
      "cmd": [
       "branch_delete"
      ],
      "after": [
       "pr_merge"
      ]
     },
     "text": "Never delete a branch locally after a PR merge"
    },
    {
     "type": "never",
     "where": {
      "cmd": [
       "push_delete"
      ],
      "after": [
       "pr_merge"
      ]
     },
     "text": "Never delete a branch on the remote after a PR merge"
    }
   ],
   "unmodeled": []
  },
  {
   "id": "X5",
   "file": "interpreter_selection.md",
   "rule": "Select the default OS binary located at /usr/bin/python3 as the runtime for all development tasks.",
   "status": "not_in_scope",
   "word": "",
   "reason": "which tool/runtime to use, not git, files or running a task",
   "left_out": "",
   "retried": false,
   "off_template": false,
   "clauses": [],
   "unmodeled": []
  },
  {
   "id": "X8",
   "file": "feedback_auto_merge_small_prs.md",
   "rule": "When a pull request modifies less than three files, bypass the approval step and merge immediately.",
   "status": "ok",
   "word": "",
   "reason": "PRs touching fewer than three files merge without the approval step",
   "left_out": "\"merge immediately\" — no timing field to record",
   "retried": true,
   "off_template": true,
   "clauses": [
    {
     "type": "only_if",
     "where": {
      "cmd": [
       "pr_merge"
      ],
      "max_files": 2
     },
     "needs": {
      "user_confirmed": false
     },
     "text": "Merge a pull request with at most 2 files, only if without the user's approval"
    }
   ],
   "unmodeled": []
  },
  {
   "id": "X14",
   "file": "feedback_dev_secrets_storage.md",
   "rule": "It is permissible to store sensitive authentication tokens and secret strings within the version-controlled codebase.",
   "status": "ok",
   "word": "",
   "reason": "it is permitted to store secrets in the repo",
   "left_out": "\"version-controlled codebase\" gives no specific paths; the kinds of secrets (\"sensitive authentication tokens and secret strings\") are covered by has_secret",
   "retried": false,
   "off_template": false,
   "clauses": [
    {
     "type": "may_do",
     "where": {
      "cmd": [
       "commit"
      ],
      "has_secret": true
     },
     "text": "May commit a file holding secrets"
    }
   ],
   "unmodeled": []
  },
  {
   "id": "X17",
   "file": "feedback_hardcoded_secrets.md",
   "rule": "Embed API keys and passwords as literal strings within the application logic instead of relying on external variable injection.",
   "status": "not_in_scope",
   "word": "",
   "reason": "how code handles credentials, not a git, file or task rule",
   "left_out": "",
   "retried": false,
   "off_template": false,
   "clauses": [],
   "unmodeled": []
  }
 ],
 "findings": [
  {
   "id": "F1",
   "type": "clash",
   "a": "R1",
   "b": "X2",
   "needs": {
    "rule": "R1",
    "clause": 0,
    "text": "Must delete a branch locally after a merge into main"
   },
   "blocked_by": [
    {
     "rule": "X2",
     "clause": 0,
     "text": "Never delete a branch locally after a PR merge"
    }
   ],
   "situation": [
    "earlier: a PR merge",
    "on branch main"
   ]
  },
  {
   "id": "F2",
   "type": "clash",
   "a": "R2",
   "b": "X2",
   "needs": {
    "rule": "R2",
    "clause": 0,
    "text": "Must delete a branch locally after a PR merge"
   },
   "blocked_by": [
    {
     "rule": "X2",
     "clause": 0,
     "text": "Never delete a branch locally after a PR merge"
    }
   ],
   "situation": [
    "earlier: a PR merge"
   ]
  },
  {
   "id": "F3",
   "type": "clash",
   "a": "R3",
   "b": "X8",
   "needs": {
    "rule": "X8",
    "clause": 0,
    "text": "Merge a pull request with at most 2 files, only if without the user's approval"
   },
   "blocked_by": [
    {
     "rule": "R3",
     "clause": 0,
     "text": "Push (any kind) or merge (any kind) or open a pull request, only if with the user's approval, the files were shown to the user"
    }
   ],
   "situation": [
    "whenever the agent would merge a pull request with at most 2 files"
   ]
  },
  {
   "id": "F4",
   "type": "clash",
   "a": "R4",
   "b": "X8",
   "needs": {
    "rule": "X8",
    "clause": 0,
    "text": "Merge a pull request with at most 2 files, only if without the user's approval"
   },
   "blocked_by": [
    {
     "rule": "R4",
     "clause": 0,
     "text": "Push (any kind) or merge (any kind), only if the files were shown to the user, with the user's approval"
    }
   ],
   "situation": [
    "whenever the agent would merge a pull request with at most 2 files"
   ]
  },
  {
   "id": "F5",
   "type": "exception",
   "a": "R6",
   "b": "X14",
   "needs": {
    "rule": "X14",
    "clause": 0,
    "text": "May commit a file holding secrets"
   },
   "blocked_by": [
    {
     "rule": "R6",
     "clause": 0,
     "text": "Never commit a file holding secrets"
    }
   ],
   "situation": [
    "whenever the agent would commit a file holding secrets"
   ]
  },
  {
   "id": "F6",
   "type": "clash",
   "a": "R13",
   "b": "X8",
   "needs": {
    "rule": "X8",
    "clause": 0,
    "text": "Merge a pull request with at most 2 files, only if without the user's approval"
   },
   "blocked_by": [
    {
     "rule": "R13",
     "clause": 0,
     "text": "Push (any kind) or merge (any kind), only if with the user's approval"
    }
   ],
   "situation": [
    "whenever the agent would merge a pull request with at most 2 files"
   ]
  }
 ]
};
