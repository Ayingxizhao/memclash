```json
{
  "rules": [
    {
      "folder": "dbwg2009__Noted",
      "id": "R7",
      "translation": {
        "status": "not_in_scope",
        "clauses": null,
        "left_out": "The vocabulary cannot simultaneously identify Development as the pull request source branch and main as its target branch."
      },
      "new_names": []
    },
    {
      "folder": "dbwg2009__Noted",
      "id": "R76",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:bump major version"
            },
            "needs": {
              "user_asked": true
            }
          },
          {
            "type": "must_do",
            "where": {
              "cmd": "commit",
              "after": "run",
              "after_task": "other:bump major version"
            }
          }
        ],
        "left_out": "The vocabulary cannot require that the commit use the breaking-change conventional-commit form."
      },
      "new_names": [
        "other:bump major version"
      ]
    },
    {
      "folder": "dbwg2009__Noted",
      "id": "R77",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:bump major version",
              "user_asked": false
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:bump major version"
      ]
    },
    {
      "folder": "dbwg2009__Noted",
      "id": "R8",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "branch_create",
              "branch": "infra/**"
            }
          },
          {
            "type": "never",
            "where": {
              "cmd": "branch_create",
              "branch": "docs/**"
            }
          },
          {
            "type": "never",
            "where": {
              "cmd": "branch_create",
              "branch": "chore/**"
            }
          }
        ],
        "left_out": "The rule does not state patterns for phase-work and bug-fix branches, so the broader restriction against every other branch type cannot be encoded."
      },
      "new_names": []
    },
    {
      "folder": "evanderkoogh__instrumentation-skill-test-harness",
      "id": "R102",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "create",
              "path": "apps/*/files/"
            },
            "when_unmodeled": "the upstream repository lacks files required by the harness"
          }
        ],
        "left_out": "Whether the upstream repository lacks harness-required files cannot be checked."
      },
      "new_names": []
    },
    {
      "folder": "evanderkoogh__instrumentation-skill-test-harness",
      "id": "R133",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:broadleaf demosite"
            },
            "when_unmodeled": "the invocation uses java -jar"
          }
        ],
        "left_out": "The java -jar invocation method cannot be checked."
      },
      "new_names": [
        "other:broadleaf demosite"
      ]
    },
    {
      "folder": "evanderkoogh__instrumentation-skill-test-harness",
      "id": "R134",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:broadleaf demosite"
            },
            "when_unmodeled": "the invocation uses mvn spring-boot:run"
          }
        ],
        "left_out": "The mvn spring-boot:run invocation method cannot be checked."
      },
      "new_names": [
        "other:broadleaf demosite"
      ]
    },
    {
      "folder": "evanderkoogh__instrumentation-skill-test-harness",
      "id": "R142",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:rebuild language images"
            },
            "needs": {
              "after": "run",
              "after_task": "other:rebuild base image"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:rebuild language images",
        "other:rebuild base image"
      ]
    },
    {
      "folder": "evanderkoogh__instrumentation-skill-test-harness",
      "id": "R146",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:rebuild images",
              "after": "edit",
              "after_path": "container.ts"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:rebuild images"
      ]
    },
    {
      "folder": "evanderkoogh__instrumentation-skill-test-harness",
      "id": "R161",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "commit",
              "branch": "main"
            },
            "when_unmodeled": "the action is in the agent-skill repository"
          }
        ],
        "left_out": "The agent-skill repository context and the requirement to use the current long-running feature branch cannot be checked."
      },
      "new_names": []
    },
    {
      "folder": "evanderkoogh__instrumentation-skill-test-harness",
      "id": "R162",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "checkout",
              "branch": "main"
            },
            "when_unmodeled": "the action is in the agent-skill repository"
          },
          {
            "type": "never",
            "where": {
              "cmd": "push",
              "branch": "main"
            },
            "when_unmodeled": "the action is in the agent-skill repository"
          }
        ],
        "left_out": "The agent-skill repository context cannot be checked."
      },
      "new_names": []
    },
    {
      "folder": "evanderkoogh__instrumentation-skill-test-harness",
      "id": "R163",
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
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "push"
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
      "folder": "evanderkoogh__instrumentation-skill-test-harness",
      "id": "R164",
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
              "after_task": "other:git branch"
            },
            "when_unmodeled": "the action is in the agent-skill repository"
          }
        ],
        "left_out": "The repository context and whether git branch confirmed that the current branch is the feature branch cannot be checked."
      },
      "new_names": [
        "other:git branch"
      ]
    },
    {
      "folder": "evanderkoogh__instrumentation-skill-test-harness",
      "id": "R18",
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
            "when_unmodeled": "the edit is a warranted preamble change"
          }
        ],
        "left_out": "Whether an edit is a warranted preamble change and the requirement to suggest it before asking permission cannot be checked."
      },
      "new_names": []
    },
    {
      "folder": "evanderkoogh__instrumentation-skill-test-harness",
      "id": "R2",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "test"
            },
            "needs": {
              "suite": "all"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "evanderkoogh__instrumentation-skill-test-harness",
      "id": "R25",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "may_do",
            "where": {
              "cmd": "edit",
              "path": [
                "config.sh",
                "evaluation.ts",
                "EVALUATION.md"
              ],
              "user_confirmed": false
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "evanderkoogh__instrumentation-skill-test-harness",
      "id": "R80",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:run application"
            },
            "when_unmodeled": "otel-verification is being performed"
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:generate traffic"
            },
            "when_unmodeled": "otel-verification is being performed"
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:stand up collector"
            },
            "when_unmodeled": "otel-verification is being performed"
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:stand up weaver"
            },
            "when_unmodeled": "otel-verification is being performed"
          }
        ],
        "left_out": "Whether otel-verification is being performed cannot be checked."
      },
      "new_names": [
        "other:run application",
        "other:generate traffic",
        "other:stand up collector",
        "other:stand up weaver"
      ]
    },
    {
      "folder": "ferazfhansurie__ai-memory-faeez",
      "id": "R132",
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
      "folder": "ferazfhansurie__ai-memory-faeez",
      "id": "R83",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "may_do",
            "where": {
              "cmd": "run",
              "task": "other:trigger autopost endpoint",
              "has_secret": true
            }
          }
        ],
        "left_out": "The vocabulary cannot identify CRON_SECRET specifically or identify the external source."
      },
      "new_names": [
        "other:trigger autopost endpoint"
      ]
    },
    {
      "folder": "ilyasergey__vermilion",
      "id": "R1",
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
              "path": "case-studies/aeneas/"
            }
          }
        ],
        "left_out": "User ownership cannot be represented."
      },
      "new_names": []
    },
    {
      "folder": "ilyasergey__vermilion",
      "id": "R14",
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
              "path": "case-studies/aeneas/"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "ilyasergey__vermilion",
      "id": "R2",
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
                "delete",
                "stage",
                "commit"
              ],
              "path": "case-studies/aeneas/"
            }
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "format",
              "path": "case-studies/aeneas/"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "ilyasergey__vermilion",
      "id": "R26",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "create",
              "path": "docs/features.md",
              "after": "delete",
              "after_path": "docs/features.md"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "ilyasergey__vermilion",
      "id": "R27",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "create",
              "path": "docs/wrinkles.md",
              "after": "delete",
              "after_path": "docs/wrinkles.md"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "ilyasergey__vermilion",
      "id": "R31",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_hold",
            "where": {
              "path": "docs/"
            },
            "when_unmodeled": "the repository item is a report"
          }
        ],
        "left_out": "Whether a repository item is a report cannot be checked."
      },
      "new_names": []
    },
    {
      "folder": "ilyasergey__vermilion",
      "id": "R4",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "may_do",
            "where": {
              "cmd": [
                "create",
                "edit",
                "move",
                "delete",
                "stage",
                "commit"
              ],
              "path": "case-studies/aeneas/",
              "user_asked": true
            },
            "when_unmodeled": "a later instruction explicitly names work inside the folder for this task"
          }
        ],
        "left_out": "The vocabulary cannot check that the permission came from a later instruction naming work inside the folder for the particular task."
      },
      "new_names": []
    },
    {
      "folder": "ilyasergey__vermilion",
      "id": "R76",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "create"
            },
            "needs": {
              "path": "docs/reports/"
            },
            "when_unmodeled": "the new file is a report, ledger, or measurement summary"
          }
        ],
        "left_out": "Whether a new file is a report, ledger, or measurement summary cannot be checked."
      },
      "new_names": []
    },
    {
      "folder": "ilyasergey__vermilion",
      "id": "R77",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "create",
              "path": "reports/",
              "kind": "dir",
              "after": "delete",
              "after_path": "reports/"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "infonl__podiumd-minikube",
      "id": "R155",
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
              "after_task": "other:run python checks",
              "after_ok": true
            }
          }
        ],
        "left_out": "The vocabulary cannot inspect whether the successful check included jscpd and vulture."
      },
      "new_names": [
        "other:run python checks"
      ]
    },
    {
      "folder": "infonl__podiumd-minikube",
      "id": "R21",
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
              "after_task": "other:ledger check"
            },
            "when_unmodeled": "the deploy is on minikube or kees00"
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:reset environment"
            },
            "needs": {
              "after": "run",
              "after_task": "other:ledger check"
            },
            "when_unmodeled": "the reset is on minikube or kees00"
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:chart test"
            },
            "needs": {
              "after": "run",
              "after_task": "other:ledger check"
            },
            "when_unmodeled": "the chart test is on minikube or kees00"
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "test"
            },
            "needs": {
              "after": "run",
              "after_task": "other:ledger check"
            },
            "when_unmodeled": "the test is beyond smoke or a single rerun and is on minikube or kees00"
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:disruptive step"
            },
            "needs": {
              "after": "run",
              "after_task": "other:ledger check"
            },
            "when_unmodeled": "the disruptive step is on minikube or kees00"
          }
        ],
        "left_out": "The target environment, the distinction between broader tests and smoke or single reruns, and which ledger-check command corresponds to an environment cannot be checked."
      },
      "new_names": [
        "other:ledger check",
        "other:reset environment",
        "other:chart test",
        "other:disruptive step"
      ]
    },
    {
      "folder": "infonl__podiumd-minikube",
      "id": "R33",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:release podiumd minikube cluster lock"
            }
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:bypass podiumd minikube cluster lock"
            }
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:release kees00 podiumd tests lock"
            }
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:bypass kees00 podiumd tests lock"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:release podiumd minikube cluster lock",
        "other:bypass podiumd minikube cluster lock",
        "other:release kees00 podiumd tests lock",
        "other:bypass kees00 podiumd tests lock"
      ]
    },
    {
      "folder": "infonl__podiumd-minikube",
      "id": "R65",
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
              "after_task": "other:run python checks"
            }
          }
        ],
        "left_out": "The vocabulary cannot require that the check be immediately before the commit or after the last edit."
      },
      "new_names": [
        "other:run python checks"
      ]
    },
    {
      "folder": "infonl__podiumd-minikube",
      "id": "R71",
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
              "after_task": "other:git diff cached"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:git diff cached"
      ]
    },
    {
      "folder": "jemcik__the-radio-bench",
      "id": "R1",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "read",
              "path": "memory/"
            },
            "when_unmodeled": "project memory is being read while working on this project"
          }
        ],
        "left_out": "The external ~/.claude/projects/<project>/memory/ location and the project-working context cannot be represented as repository paths."
      },
      "new_names": []
    },
    {
      "folder": "jemcik__the-radio-bench",
      "id": "R155",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "pr_merge"
            }
          }
        ],
        "left_out": "The statement that the user performs every merge is explanatory and cannot be represented."
      },
      "new_names": []
    },
    {
      "folder": "jemcik__the-radio-bench",
      "id": "R156",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "pr_merge"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "jemcik__the-radio-bench",
      "id": "R159",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "branch_delete",
              "after": [
                "merge",
                "push"
              ]
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "jemcik__the-radio-bench",
      "id": "R2",
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
              "path": "memory/"
            },
            "when_unmodeled": "the write adds a new project-memory entry"
          }
        ],
        "left_out": "Whether a write adds a memory entry cannot be checked, and the external ~/.claude/projects/<project>/memory/ location cannot be represented as a repository path."
      },
      "new_names": []
    },
    {
      "folder": "jemcik__the-radio-bench",
      "id": "R23",
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
              "after_task": "other:beginner review rerun"
            },
            "when_unmodeled": "the commit belongs to the fix pass"
          }
        ],
        "left_out": "Declaring the fix pass done is not an available action, and whether a commit belongs to that fix pass cannot be checked."
      },
      "new_names": [
        "other:beginner review rerun"
      ]
    },
    {
      "folder": "jemcik__the-radio-bench",
      "id": "R291",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:preview start"
            },
            "when_unmodeled": "the action is in the Radiopedia repository"
          },
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:connect to user running dev server"
            },
            "when_unmodeled": "preview access is needed in the Radiopedia repository"
          }
        ],
        "left_out": "The repository context and the requirement to use the specifically named mcp__Claude_in_Chrome__* tools cannot be checked."
      },
      "new_names": [
        "other:preview start",
        "other:connect to user running dev server"
      ]
    },
    {
      "folder": "jemcik__the-radio-bench",
      "id": "R328",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "edit",
              "path": "glossary.ts"
            },
            "needs": {
              "after": "run",
              "after_task": "other:check glossary coverage"
            },
            "when_unmodeled": "the edit adds a glossary key"
          }
        ],
        "left_out": "Whether the edit adds a glossary key cannot be checked."
      },
      "new_names": [
        "other:check glossary coverage"
      ]
    },
    {
      "folder": "jemcik__the-radio-bench",
      "id": "R338",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:extract glossary"
            },
            "when_unmodeled": "a glossary entry is being translated"
          },
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:translate glossary entry",
              "after": "run",
              "after_task": "other:extract glossary"
            },
            "when_unmodeled": "a glossary entry is being translated"
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:translate glossary entry"
            },
            "needs": {
              "after": "run",
              "after_task": "other:extract glossary"
            }
          }
        ],
        "left_out": "The glossary term argument and whether the work is translating a glossary entry cannot be checked."
      },
      "new_names": [
        "other:extract glossary",
        "other:translate glossary entry"
      ]
    },
    {
      "folder": "jemcik__the-radio-bench",
      "id": "R416",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:apply translations"
            },
            "needs": {
              "user_confirmed": true
            }
          }
        ],
        "left_out": "The vocabulary cannot distinguish a general go-ahead from approval containing specific overrides."
      },
      "new_names": [
        "other:apply translations"
      ]
    },
    {
      "folder": "jemcik__the-radio-bench",
      "id": "R9",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "create"
            },
            "needs": {
              "after": "run",
              "after_task": "other:check existing memory coverage"
            },
            "when_unmodeled": "the created file is a new memory file"
          }
        ],
        "left_out": "Whether the created file is a memory file and whether an existing file covers the same ground cannot be checked."
      },
      "new_names": [
        "other:check existing memory coverage"
      ]
    },
    {
      "folder": "kingh0730__interregnum",
      "id": "R13",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "test"
            },
            "needs": {
              "user_confirmed": true
            },
            "when_unmodeled": "the test is new and paid"
          }
        ],
        "left_out": "Whether the test is new and paid, and who or what constitutes applicable authorization, cannot be checked."
      },
      "new_names": []
    },
    {
      "folder": "kingh0730__interregnum",
      "id": "R136",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:run image batch"
            },
            "needs": {
              "after": "run",
              "after_task": "other:a b test image prompts"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:run image batch",
        "other:a b test image prompts"
      ]
    },
    {
      "folder": "kingh0730__interregnum",
      "id": "R137",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:run image batch"
            },
            "needs": {
              "after": "run",
              "after_task": "other:a b test image models"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:run image batch",
        "other:a b test image models"
      ]
    },
    {
      "folder": "kingh0730__interregnum",
      "id": "R148",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:concept work"
            },
            "needs": {
              "after": "read",
              "after_path": "bible/taste.md"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:concept work"
      ]
    },
    {
      "folder": "kingh0730__interregnum",
      "id": "R29",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:seedance step"
            },
            "needs": {
              "user_confirmed": true
            },
            "when_unmodeled": "the Seedance step is being started on an episode"
          }
        ],
        "left_out": "The vocabulary cannot check that the confirmation came specifically from King or identify the episode context."
      },
      "new_names": [
        "other:seedance step"
      ]
    },
    {
      "folder": "kingh0730__interregnum",
      "id": "R30",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:seedance step"
            },
            "needs": {
              "after": "run",
              "after_task": "other:estimate seedance cost"
            },
            "when_unmodeled": "the Seedance step is being started on an episode"
          }
        ],
        "left_out": "The vocabulary cannot identify the episode context or verify the contents of the cost estimate."
      },
      "new_names": [
        "other:seedance step",
        "other:estimate seedance cost"
      ]
    }
  ]
}
```