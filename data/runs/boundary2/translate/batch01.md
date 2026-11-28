```json
{
  "rules": [
    {
      "folder": "28dayslater__pinp-cpp-prototype",
      "id": "R40",
      "translation": {
        "status": "not_in_scope",
        "clauses": null,
        "left_out": "The vocabulary cannot express the requirement that words in a newly created filename be separated with hyphens."
      },
      "new_names": []
    },
    {
      "folder": "28dayslater__pinp-cpp-prototype",
      "id": "R48",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "commit"
            },
            "needs": {
              "user_asked": true
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The condition that a task has been completed cannot be identified with the fixed fields."
      },
      "new_names": []
    },
    {
      "folder": "28dayslater__pinp-cpp-prototype",
      "id": "R5",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "commit",
              "branch": "main"
            }
          }
        ],
        "left_out": "The vocabulary cannot express that every change must have its own dedicated branch."
      },
      "new_names": []
    },
    {
      "folder": "28dayslater__pinp-cpp-prototype",
      "id": "R59",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "push_branch"
            },
            "needs": {
              "user_asked": true
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "28dayslater__pinp-cpp-prototype",
      "id": "R60",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "may_do",
            "where": {
              "cmd": "commit",
              "user_confirmed": false
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "28dayslater__pinp-cpp-prototype",
      "id": "R61",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "push_branch"
            },
            "needs": {
              "user_asked": true
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "28dayslater__pinp-cpp-prototype",
      "id": "R7",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": [
                "stage",
                "commit"
              ],
              "branch": "main"
            }
          }
        ],
        "left_out": "The explicit act of checking or confirming the current branch cannot be represented."
      },
      "new_names": []
    },
    {
      "folder": "28dayslater__pinp-cpp-prototype",
      "id": "R79",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "commit"
            },
            "needs": {
              "after": "run",
              "after_task": "lint",
              "after_ok": true
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The condition that the commit contains C++ code and the requirement that clang-tidy cover all such code cannot be checked."
      },
      "new_names": []
    },
    {
      "folder": "28dayslater__pinp-cpp-prototype",
      "id": "R8",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "commit",
              "branch": "main"
            },
            "needs": {
              "after": "branch_create"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "28dayslater__pinp-cpp-prototype",
      "id": "R87",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "edit",
              "path": "llvm-project/",
              "in_worktree": true
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The qualifier that the source is being edited per-branch cannot be checked."
      },
      "new_names": []
    },
    {
      "folder": "28dayslater__pinp-cpp-prototype",
      "id": "R9",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "merge",
              "branch": "main"
            },
            "needs": {
              "user_asked": true
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "AbuShaqra__TC_PLC_Toolkit",
      "id": "R121",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:audit"
            },
            "needs": {
              "after": "fetch"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The vocabulary cannot check that this is a repeated audit on a shallow clone or that fetch used --unshallow with the specified source and branch."
      },
      "new_names": [
        "other:audit"
      ]
    },
    {
      "folder": "AbuShaqra__TC_PLC_Toolkit",
      "id": "R129",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:download and launch vs code for a probe"
            },
            "needs": {
              "user_confirmed": true
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:download and launch vs code for a probe"
      ]
    },
    {
      "folder": "AbuShaqra__TC_PLC_Toolkit",
      "id": "R154",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "push_branch"
            },
            "needs": {
              "after": "run",
              "after_task": "other:scan committed bytes for c0 control characters",
              "after_ok": true
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The condition that the pushed change affects .github/workflows/*.yml cannot be attached to a push, and the vocabulary cannot express the exact byte range, exclusions, or the requirement to scan bytes rather than merely parse YAML."
      },
      "new_names": [
        "other:scan committed bytes for c0 control characters"
      ]
    },
    {
      "folder": "AbuShaqra__TC_PLC_Toolkit",
      "id": "R41",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "pr_create"
            },
            "needs": {
              "after": "run",
              "after_task": "other:confirm base branch exists with git ls-remote",
              "after_ok": true
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:confirm base branch exists with git ls-remote"
      ]
    },
    {
      "folder": "AbuShaqra__TC_PLC_Toolkit",
      "id": "R49",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": [
                "commit",
                "push"
              ]
            },
            "needs": {
              "after": "run",
              "after_ok": true
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The vocabulary cannot identify an unspecified gate, distinguish explicitly checking its exit code from observing success, or require both operations to occur in the same command chain."
      },
      "new_names": []
    },
    {
      "folder": "AbuShaqra__TC_PLC_Toolkit",
      "id": "R73",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "push_branch"
            },
            "needs": {
              "after": "run",
              "after_task": "other:mailmap pass"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The vocabulary cannot identify the final push or require the mailmap pass to be the immediately preceding step and not to have run earlier."
      },
      "new_names": [
        "other:mailmap pass"
      ]
    },
    {
      "folder": "AbuShaqra__TC_PLC_Toolkit",
      "id": "R82",
      "translation": {
        "status": "not_in_scope",
        "clauses": null,
        "left_out": "The vocabulary cannot express that a scan is restricted to one project or relate that scope to which other projects' .TcVIS, .TcTLO, and .TcTTO files may be rewritten."
      },
      "new_names": []
    },
    {
      "folder": "AbuShaqra__TC_PLC_Toolkit",
      "id": "R91",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "checkout",
              "running": [
                "other:delegated agent"
              ]
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The vocabulary cannot check that the branch switch and delegated agent are using the same checkout."
      },
      "new_names": [
        "other:delegated agent"
      ]
    },
    {
      "folder": "AbuShaqra__TC_PLC_Toolkit",
      "id": "R93",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "edit",
              "running": [
                "other:delegated agent"
              ]
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "Whether a file is likely to be rewritten, whether both actors use the same checkout, and the non-exhaustive nature of the HANDOFF.md, ROADMAP.md, and docs examples cannot be expressed."
      },
      "new_names": [
        "other:delegated agent"
      ]
    },
    {
      "folder": "AbuShaqra__TC_PLC_Toolkit",
      "id": "R95",
      "translation": {
        "status": "not_in_scope",
        "clauses": null,
        "left_out": "The vocabulary cannot record which files a delegated agent was instructed not to touch and therefore cannot express the allowed set for the caller's edits."
      },
      "new_names": []
    },
    {
      "folder": "AbuShaqra__TC_PLC_Toolkit",
      "id": "R97",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "fetch",
              "running": [
                "other:delegated agent"
              ]
            },
            "when_unmodeled": true
          },
          {
            "type": "never",
            "where": {
              "cmd": "checkout",
              "running": [
                "other:delegated agent"
              ]
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The vocabulary cannot identify a post-merge sync or the point immediately after delegation; the running process represents the period until the agent reports done."
      },
      "new_names": [
        "other:delegated agent"
      ]
    },
    {
      "folder": "Akagilnc__ak-ai-postflow",
      "id": "R15",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "local_merge"
            }
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "pr_merge"
            },
            "needs": {
              "after": "pr_create"
            }
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "pr_merge"
            },
            "needs": {
              "after": "run",
              "after_task": "other:codex automated review"
            }
          }
        ],
        "left_out": "The vocabulary does not distinguish GitHub from another PR host."
      },
      "new_names": [
        "other:codex automated review"
      ]
    },
    {
      "folder": "Akagilnc__ak-ai-postflow",
      "id": "R5",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "pr_create"
            },
            "needs": {
              "after": "run",
              "after_task": "test",
              "after_ok": true
            }
          }
        ],
        "left_out": "The vocabulary cannot verify that the tests are end-to-end or cover every major path rather than only one path."
      },
      "new_names": []
    },
    {
      "folder": "Akagilnc__ak-ai-postflow",
      "id": "R6",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "pr_create"
            },
            "needs": {
              "after": "run",
              "after_task": "other:list and verify trigger paths",
              "after_ok": true
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:list and verify trigger paths"
      ]
    },
    {
      "folder": "Alsesd__EasyMourningReport",
      "id": "R29",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": [
                "create",
                "edit",
                "move",
                "delete"
              ],
              "path": [
                "data/",
                "backups/",
                "reports.db",
                "secret.key",
                ".env"
              ]
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "Alsesd__EasyMourningReport",
      "id": "R35",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "test",
              "suite": "all"
            },
            "when_unmodeled": true
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "lint",
              "suite": "all"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The vocabulary cannot distinguish Go's literal ./... argument from other ways of selecting an entire test or lint suite."
      },
      "new_names": []
    },
    {
      "folder": "Alsesd__EasyMourningReport",
      "id": "R38",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "commit"
            },
            "needs": {
              "after": "run",
              "after_task": "other:verify skill"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The condition that the commit is for a finished feature cannot be checked."
      },
      "new_names": [
        "other:verify skill"
      ]
    },
    {
      "folder": "Augmented-Design-Capability-Studio__mopt-bot",
      "id": "R199",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "edit"
            },
            "needs": {
              "user_confirmed": true
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The vocabulary cannot identify a problem package's solver, evaluator, or instance data without named paths, and user confirmation does not identify the confirmer specifically as a maintainer."
      },
      "new_names": []
    },
    {
      "folder": "BeastHome__dice-roller",
      "id": "R1",
      "translation": {
        "status": "not_in_scope",
        "clauses": null,
        "left_out": "Paths in this vocabulary are repository-relative; it cannot require Edit/Write tool use with absolute paths under a different main-project root while the caller works in a named worktree path."
      },
      "new_names": []
    },
    {
      "folder": "BeastHome__dice-roller",
      "id": "R2",
      "translation": {
        "status": "not_in_scope",
        "clauses": null,
        "left_out": "The vocabulary cannot express which filesystem root a build or git command is run against, as distinct from the worktree in which the caller is working."
      },
      "new_names": []
    },
    {
      "folder": "BeastHome__dice-roller",
      "id": "R23",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "may_do",
            "where": {
              "cmd": "create"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The whole-file Write method cannot be represented; it is retained as the unmodeled condition on the permission."
      },
      "new_names": []
    },
    {
      "folder": "BeastHome__dice-roller",
      "id": "R3",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "checkout",
              "in_worktree": true
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The purpose of switching branches in order to commit in that worktree cannot be checked."
      },
      "new_names": []
    },
    {
      "folder": "BeastHome__dice-roller",
      "id": "R31",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "edit"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "No pre-commit-hook path is named, and the vocabulary cannot check that the purpose of an edit is to fix drift."
      },
      "new_names": []
    },
    {
      "folder": "BeastHome__dice-roller",
      "id": "R38",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "edit",
              "path": "dev-tools/dev-manifest.json"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The vocabulary cannot identify which edits are portable pre-commit-hook fixes."
      },
      "new_names": []
    },
    {
      "folder": "BeastHome__dice-roller",
      "id": "R39",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "edit"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The external ~/dev/templates/ location cannot be represented by the repository-relative path vocabulary, and the purpose of fixing the pre-commit hook cannot be checked."
      },
      "new_names": []
    },
    {
      "folder": "BeastHome__dice-roller",
      "id": "R43",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "create"
            },
            "needs": {
              "path": ".claude/memory/"
            },
            "when_unmodeled": true
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "move"
            },
            "needs": {
              "dest_path": ".claude/memory/"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "Whether a file is a memory file is unmodeled. The external ~/.claude/projects/<project>/memory/ location cannot be represented directly."
      },
      "new_names": []
    },
    {
      "folder": "BeastHome__dice-roller",
      "id": "R44",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "create"
            },
            "needs": {
              "path": ".claude/memory/"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "Whether the new file is a memory file is unmodeled. The external legacy user-directory location cannot be represented directly."
      },
      "new_names": []
    },
    {
      "folder": "Bretthb__jarble",
      "id": "R108",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "edit",
              "path": [
                "Jarble-mvp/components/canvas/",
                "useCanvasChat.ts",
                "AssistantUIChat.tsx",
                "SimpleCanvasGrid.tsx",
                "lib/assistantRuntime.ts"
              ]
            },
            "when_unmodeled": true
          },
          {
            "type": "never",
            "where": {
              "cmd": "edit",
              "path": "jarble-ui-server.js"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The vocabulary cannot distinguish extending legacy code from other edits or restrict the jarble-ui-server.js clause specifically to the render_ui and define_component tools."
      },
      "new_names": []
    },
    {
      "folder": "Bretthb__jarble",
      "id": "R110",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:canvas-component-builder agent"
            }
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:new-component skill"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:canvas-component-builder agent",
        "other:new-component skill"
      ]
    },
    {
      "folder": "Bretthb__jarble",
      "id": "R124",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "restart"
            },
            "needs": {
              "after": "delete"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The vocabulary cannot check that a modpack update is in progress or identify the itzg install marker because its path is not named."
      },
      "new_names": []
    },
    {
      "folder": "Bretthb__jarble",
      "id": "R129",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": [
                "create",
                "edit"
              ]
            },
            "needs": {
              "after": "run",
              "after_task": "other:profile group a state and show a need",
              "after_ok": true
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The vocabulary cannot identify edits that implement phase 3 or specifically introduce useReducer."
      },
      "new_names": [
        "other:profile group a state and show a need"
      ]
    },
    {
      "folder": "Bretthb__jarble",
      "id": "R134",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "deploy"
            },
            "needs": {
              "after": "run",
              "after_task": "other:fix critical audit issues c1-c4",
              "after_ok": true
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The vocabulary cannot check that the deployment target is production or connect the issue identifiers to AUDIT-REPORT.md."
      },
      "new_names": [
        "other:fix critical audit issues c1-c4"
      ]
    },
    {
      "folder": "Bretthb__jarble",
      "id": "R135",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "publish"
            },
            "needs": {
              "after": "run",
              "after_task": "other:fix high-priority audit issues h1-h11",
              "after_ok": true
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The vocabulary cannot check that the publication is a public beta or connect the issue identifiers to AUDIT-REPORT.md."
      },
      "new_names": [
        "other:fix high-priority audit issues h1-h11"
      ]
    },
    {
      "folder": "Bretthb__jarble",
      "id": "R144",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "local_merge",
              "branch": "main"
            },
            "needs": {
              "user_confirmed": true
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The vocabulary cannot check that the merge is a fast-forward or that its source is merge-branch."
      },
      "new_names": []
    },
    {
      "folder": "Bretthb__jarble",
      "id": "R158",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "force_push"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "Bretthb__jarble",
      "id": "R159",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "edit",
              "branch": "main"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "Bretthb__jarble",
      "id": "R161",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:db drop statements"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:db drop statements"
      ]
    },
    {
      "folder": "Bretthb__jarble",
      "id": "R162",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:force-delete deployments"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:force-delete deployments"
      ]
    },
    {
      "folder": "Bretthb__jarble",
      "id": "R176",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "test"
            },
            "when_unmodeled": true
          },
          {
            "type": "must_do",
            "where": {
              "cmd": "local_merge",
              "branch": "main",
              "after": "run",
              "after_task": "test"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The vocabulary cannot identify the next session, express that testing is action-oriented or the first focus, require immediate ordering, or identify the source branch."
      },
      "new_names": []
    }
  ]
}
```