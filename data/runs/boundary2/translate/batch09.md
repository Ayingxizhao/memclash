```json
{
  "rules": [
    {
      "folder": "noorinalabs__noorinalabs-data-acquisition",
      "id": "R123",
      "translation": {
        "status": "not_in_scope",
        "clauses": null,
        "left_out": "The checkpoint is not identified by a path, so its on-disk state cannot be named without inventing one."
      },
      "new_names": []
    },
    {
      "folder": "noorinalabs__noorinalabs-data-acquisition",
      "id": "R124",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": [
                "create",
                "edit"
              ]
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The condition that the run stopped at its --stop-after limit and the fact that the file action writes the final output cannot be checked."
      },
      "new_names": []
    },
    {
      "folder": "noorinalabs__noorinalabs-data-acquisition",
      "id": "R126",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:pip install"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "Being inside a loader container attached to noorinalabs_backend at runtime cannot be checked. The requirement that dependencies be baked into the image at build time cannot be expressed."
      },
      "new_names": [
        "other:pip install"
      ]
    },
    {
      "folder": "noorinalabs__noorinalabs-data-acquisition",
      "id": "R128",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:staging loader container"
            }
          }
        ],
        "left_out": "Attachment to the noorinalabs_backend Docker network cannot be expressed."
      },
      "new_names": [
        "other:staging loader container"
      ]
    },
    {
      "folder": "noorinalabs__noorinalabs-data-acquisition",
      "id": "R130",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "commit",
              "has_secret": true
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "noorinalabs__noorinalabs-data-acquisition",
      "id": "R133",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": [
                "create",
                "edit"
              ],
              "path": "/tmp/"
            },
            "when_unmodeled": true
          },
          {
            "type": "never",
            "where": {
              "cmd": [
                "create",
                "edit"
              ],
              "path": "/home/deploy/"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The condition that the file is being written on the staging host cannot be checked."
      },
      "new_names": []
    },
    {
      "folder": "noorinalabs__noorinalabs-data-acquisition",
      "id": "R134",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:apply loads to production"
            },
            "needs": {
              "user_confirmed": true
            }
          }
        ],
        "left_out": "The vocabulary records confirmation but cannot distinguish the owner from another user."
      },
      "new_names": [
        "other:apply loads to production"
      ]
    },
    {
      "folder": "noorinalabs__noorinalabs-data-acquisition",
      "id": "R139",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:delete existing nodes"
            },
            "when_unmodeled": true
          },
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:load data",
              "after": "run",
              "after_task": "other:delete existing nodes"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The condition that a node-keying change prevents MERGE, and the purpose of avoiding stale duplicates, cannot be checked."
      },
      "new_names": [
        "other:delete existing nodes",
        "other:load data"
      ]
    },
    {
      "folder": "noorinalabs__noorinalabs-data-acquisition",
      "id": "R145",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:cut over to production"
            },
            "needs": {
              "after": "run",
              "after_task": "other:cross corpus deduplication audit on shia content"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:cut over to production",
        "other:cross corpus deduplication audit on shia content"
      ]
    },
    {
      "folder": "noorinalabs__noorinalabs-data-acquisition",
      "id": "R31",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "edit"
            },
            "when_unmodeled": true
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:git stash"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The A/B-testing context, the base ref, and the requirement that the edit swap file content cannot be checked. git show is given only as an example."
      },
      "new_names": [
        "other:git stash"
      ]
    },
    {
      "folder": "noorinalabs__noorinalabs-data-acquisition",
      "id": "R38",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:structural ontology emit script"
            },
            "when_unmodeled": true
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:uv python structural ontology emit"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The condition that the structural ontology index is being regenerated locally cannot be checked."
      },
      "new_names": [
        "other:structural ontology emit script",
        "other:uv python structural ontology emit"
      ]
    },
    {
      "folder": "noorinalabs__noorinalabs-data-acquisition",
      "id": "R45",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:local docker neo4j instance"
            },
            "when_unmodeled": true
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:staging neo4j box"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The purpose of seeing real data cannot be checked."
      },
      "new_names": [
        "other:local docker neo4j instance",
        "other:staging neo4j box"
      ]
    },
    {
      "folder": "noorinalabs__noorinalabs-data-acquisition",
      "id": "R46",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:docker info"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The condition that container work suddenly failed and the possible WSL-integration cause cannot be checked."
      },
      "new_names": [
        "other:docker info"
      ]
    },
    {
      "folder": "noorinalabs__noorinalabs-data-acquisition",
      "id": "R47",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:enable docker in wsl2"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The wave-time condition and the instruction to treat this as an environment or owner action outside scope cannot be expressed."
      },
      "new_names": [
        "other:enable docker in wsl2"
      ]
    },
    {
      "folder": "noorinalabs__noorinalabs-data-acquisition",
      "id": "R74",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:edge connectivity query"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The purpose of checking whether Chain nodes are populated cannot be checked."
      },
      "new_names": [
        "other:edge connectivity query"
      ]
    },
    {
      "folder": "noorinalabs__noorinalabs-data-acquisition",
      "id": "R75",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:check chain length or narrator ids size"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:check chain length or narrator ids size"
      ]
    },
    {
      "folder": "noorinalabs__noorinalabs-data-acquisition",
      "id": "R76",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:resolve from disambiguate"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The crashed-run recovery context, skipping NER, and verbatim reuse of narrator_mentions_resolved.parquet cannot be checked."
      },
      "new_names": [
        "other:resolve from disambiguate"
      ]
    },
    {
      "folder": "noorinalabs__noorinalabs-data-acquisition",
      "id": "R77",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:bare resolve"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The crashed-disambiguate recovery context and the stated effects on mention IDs and the checkpoint cannot be checked."
      },
      "new_names": [
        "other:bare resolve"
      ]
    },
    {
      "folder": "noorinalabs__noorinalabs-data-acquisition",
      "id": "R84",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:can merge check"
            },
            "when_unmodeled": true
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:lexical heuristic"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The purpose of determining whether two names merge cannot be checked."
      },
      "new_names": [
        "other:can merge check",
        "other:lexical heuristic"
      ]
    },
    {
      "folder": "ridopark__oh-my-opentrade",
      "id": "R10",
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
              "user_confirmed": true
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The condition that the code implements an ENGINE_CHANGE or strategy rewrite, and the separate requirement to present the design, cannot be checked."
      },
      "new_names": []
    },
    {
      "folder": "ridopark__oh-my-opentrade",
      "id": "R11",
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
              "after_task": "other:enter plan mode or present a structured plan",
              "user_confirmed": true
            },
            "when_unmodeled": true
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:go architect"
            },
            "needs": {
              "after": "run",
              "after_task": "other:enter plan mode or present a structured plan",
              "user_confirmed": true
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "Whether a change is significant and belongs to one of the listed categories cannot be checked."
      },
      "new_names": [
        "other:enter plan mode or present a structured plan",
        "other:go architect"
      ]
    },
    {
      "folder": "ridopark__oh-my-opentrade",
      "id": "R22",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:use filer ciks in production"
            },
            "needs": {
              "after": "run",
              "after_task": "other:verify filer ciks against live edgar"
            }
          }
        ],
        "left_out": "The vocabulary cannot associate the verification with the exact CIK values in sec/filer_config.go."
      },
      "new_names": [
        "other:use filer ciks in production",
        "other:verify filer ciks against live edgar"
      ]
    },
    {
      "folder": "ridopark__oh-my-opentrade",
      "id": "R23",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:backfill 13f with from quarter and user agent"
            }
          }
        ],
        "left_out": "The vocabulary cannot inspect the --from-quarter value or verify that --user-agent contains a company name and contact email."
      },
      "new_names": [
        "other:backfill 13f with from quarter and user agent"
      ]
    },
    {
      "folder": "ridopark__oh-my-opentrade",
      "id": "R25",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "read",
              "path": ".env"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The stuck-login-screen condition and checking specifically that TWS_USERID and TWS_PASSWORD are set cannot be expressed."
      },
      "new_names": []
    },
    {
      "folder": "ridopark__oh-my-opentrade",
      "id": "R27",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:log in with staging100"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The condition involving the multi-account selector, blocked auto-login, IB Gateway staging, and the paper-specific nature of the login cannot be checked."
      },
      "new_names": [
        "other:log in with staging100"
      ]
    },
    {
      "folder": "ridopark__oh-my-opentrade",
      "id": "R4",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:rebuild omo core"
            },
            "needs": {
              "after": "edit",
              "after_path": "*.go"
            }
          }
        ],
        "left_out": "The vocabulary cannot establish that the edited Go source belongs to omo-core."
      },
      "new_names": [
        "other:rebuild omo core"
      ]
    },
    {
      "folder": "ridopark__oh-my-opentrade",
      "id": "R8",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:omo data"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The condition that omo-data is being run locally as a tmux process cannot be checked."
      },
      "new_names": [
        "other:omo data"
      ]
    },
    {
      "folder": "ridopark__oh-my-opentrade",
      "id": "R9",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:docker compose omo data run once"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The condition that omo-data is being triggered manually cannot be checked."
      },
      "new_names": [
        "other:docker compose omo data run once"
      ]
    },
    {
      "folder": "vipulbms__crypto-trader-agent",
      "id": "R11",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The unknown condition identifies Bash execution of a download, model pull, or other human-executable task. Delegating the task to the user cannot be expressed."
      },
      "new_names": []
    },
    {
      "folder": "vipulbms__crypto-trader-agent",
      "id": "R14",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": [
                "create",
                "edit",
                "move",
                "delete"
              ]
            },
            "needs": {
              "after": "run",
              "after_task": "other:gh issue list crypto trader agent"
            }
          }
        ],
        "left_out": "The vocabulary cannot verify that the issue-list result was checked for an issue corresponding to the particular change."
      },
      "new_names": [
        "other:gh issue list crypto trader agent"
      ]
    },
    {
      "folder": "vipulbms__crypto-trader-agent",
      "id": "R20",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:create github issue"
            },
            "needs": {
              "after": "run",
              "after_task": "other:investigate and confirm root cause"
            }
          },
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
              "after_task": "other:investigate and confirm root cause"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "For file actions, whether the action is making a fix cannot be checked."
      },
      "new_names": [
        "other:create github issue",
        "other:investigate and confirm root cause"
      ]
    },
    {
      "folder": "vipulbms__crypto-trader-agent",
      "id": "R21",
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
              "after_task": "test",
              "after_ok": true,
              "tests_passed": true
            }
          }
        ],
        "left_out": "The earlier-step vocabulary cannot record that the prior test run used the full suite."
      },
      "new_names": []
    },
    {
      "folder": "vipulbms__crypto-trader-agent",
      "id": "R45",
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
              "path": "tests/"
            },
            "when_unmodeled": true
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "move"
            },
            "needs": {
              "dest_path": "tests/"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "Whether the affected file contains a test cannot be checked. The reasons concerning future discovery, reruns, and extension are not expressible."
      },
      "new_names": []
    },
    {
      "folder": "vipulbms__crypto-trader-agent",
      "id": "R46",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:python3 c inline test"
            },
            "when_unmodeled": true
          },
          {
            "type": "must_do",
            "where": {
              "cmd": [
                "create",
                "edit"
              ],
              "path": "tests/test_*.py"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The conditions that the inline script contains test logic and validates a real feature cannot be checked."
      },
      "new_names": [
        "other:python3 c inline test"
      ]
    },
    {
      "folder": "vipulbms__crypto-trader-agent",
      "id": "R5",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "commit",
              "user_asked": false
            },
            "needs": {
              "after": "run",
              "after_task": "other:prepare commit message for review"
            }
          }
        ],
        "left_out": "The user_asked field cannot distinguish a direct \"commit\" request or /commit invocation from other ways the user might request a commit."
      },
      "new_names": [
        "other:prepare commit message for review"
      ]
    },
    {
      "folder": "vipulbms__crypto-trader-agent",
      "id": "R50",
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
              "after": "read"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "Whether the action is a code or configuration change, which file constitutes \"this project context,\" and whether reading it produced full-system understanding cannot be checked."
      },
      "new_names": []
    },
    {
      "folder": "vipulbms__crypto-trader-agent",
      "id": "R65",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "stage",
              "path": ".env"
            },
            "when_unmodeled": true
          },
          {
            "type": "never",
            "where": {
              "cmd": "stage"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The first unknown condition limits the .env prohibition to staging by /commit. The second identifies staging by /commit of a data or log file; those categories are not concrete paths in the rule."
      },
      "new_names": []
    },
    {
      "folder": "vipulbms__crypto-trader-agent",
      "id": "R7",
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
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "vipulbms__crypto-trader-agent",
      "id": "R9",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "read",
              "path": "agent.log"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The condition that the user opened agent.log and the diagnostic purpose cannot be checked."
      },
      "new_names": []
    },
    {
      "folder": "wbniv__llvm-mos-65816",
      "id": "R38",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "any_branch_delete"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "Whether the target is one of the user's fork branches cannot be checked."
      },
      "new_names": []
    },
    {
      "folder": "wbniv__llvm-mos-65816",
      "id": "R39",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "any_branch_delete"
            },
            "needs": {
              "user_asked": true
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "Whether the target is a fork branch and whether the request applies to that specific case cannot be checked."
      },
      "new_names": []
    },
    {
      "folder": "wbniv__llvm-mos-65816",
      "id": "R42",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "delete",
              "path": [
                "build/",
                "vendor/"
              ]
            },
            "when_unmodeled": true
          },
          {
            "type": "never",
            "where": {
              "cmd": "any_branch_delete"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The retained-branch or worktree context and whether the directories are duplicate copies cannot be checked. Keeping the tracked diff cannot be expressed without its paths."
      },
      "new_names": []
    },
    {
      "folder": "wbniv__llvm-mos-65816",
      "id": "R63",
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
              "after": "read",
              "after_path": "docs/snes-demo-cookbook.md"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "Whether the file action implements a new SNES ROM in the compiler stress-test battery cannot be checked."
      },
      "new_names": []
    },
    {
      "folder": "wbniv__llvm-mos-65816",
      "id": "R66",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:dev run toolchain"
            }
          }
        ],
        "left_out": "The vocabulary cannot verify that the toolchain is rebuilt specifically from the committed patches."
      },
      "new_names": [
        "other:dev run toolchain"
      ]
    },
    {
      "folder": "wbniv__llvm-mos-65816",
      "id": "R71",
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
              ]
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The unknown condition identifies a compiler-changing file action while de-XFAILing a stale XFAIL; neither property can be checked directly."
      },
      "new_names": []
    },
    {
      "folder": "wbniv__llvm-mos-65816",
      "id": "R77",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:regen patch verification"
            }
          }
        ],
        "left_out": "The vocabulary cannot inspect whether the command actually verifies the worktree against the committed patches."
      },
      "new_names": [
        "other:regen patch verification"
      ]
    },
    {
      "folder": "wbniv__llvm-mos-65816",
      "id": "R80",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "delete"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The teardown context and whether the deletion target is a core script used to determine results cannot be checked."
      },
      "new_names": []
    },
    {
      "folder": "wbniv__llvm-mos-65816",
      "id": "R82",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "worktree_remove"
            },
            "needs": {
              "after": "merge"
            }
          }
        ],
        "left_out": "The vocabulary cannot verify that the earlier merge was upstream or that it contained the particular worktree's work."
      },
      "new_names": []
    },
    {
      "folder": "wbniv__llvm-mos-65816",
      "id": "R84",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "delete",
              "path": [
                "build/",
                "vendor/"
              ]
            },
            "when_unmodeled": true
          },
          {
            "type": "never",
            "where": {
              "cmd": "worktree_remove"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "Whether the worktree is being kept and whether build/ and vendor/ are duplicate copies cannot be checked."
      },
      "new_names": []
    },
    {
      "folder": "wbniv__llvm-mos-65816",
      "id": "R85",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "may_do",
            "where": {
              "cmd": "delete",
              "path": "build/",
              "in_worktree": true
            }
          }
        ],
        "left_out": "The assertion that the directory contains only compiled output cannot be checked."
      },
      "new_names": []
    }
  ]
}
```