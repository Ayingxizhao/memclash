```json
{
  "rules": [
    {
      "folder": "Bretthb__jarble",
      "id": "R201",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "migrate"
            },
            "needs": {
              "after": "run",
              "after_task": "migrate",
              "after_ok": true
            },
            "when_unmodeled": "the migration is being run on the main database"
          }
        ],
        "left_out": "The vocabulary cannot identify a Neon branch forked from production or verify that the earlier migration used that database."
      },
      "new_names": []
    },
    {
      "folder": "Bretthb__jarble",
      "id": "R90",
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
              "user_asked": true
            },
            "when_unmodeled": "the source branch is develop"
          }
        ],
        "left_out": "The merge vocabulary has one branch field and cannot directly record both develop as the source and main as the target."
      },
      "new_names": []
    },
    {
      "folder": "Bretthb__jarble",
      "id": "R92",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "merge"
            },
            "needs": {
              "user_confirmed": true
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "Bretthb__jarble",
      "id": "R93",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "push"
            },
            "needs": {
              "branch": "develop"
            },
            "when_unmodeled": "the user's instruction was deploy or push"
          }
        ],
        "left_out": "The vocabulary cannot inspect the words used in the user's instruction."
      },
      "new_names": []
    },
    {
      "folder": "Bretthb__jarble",
      "id": "R94",
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
        "left_out": "The vocabulary records that the user asked but cannot require the exact phrases \"merge to main\" or \"deploy to production.\""
      },
      "new_names": []
    },
    {
      "folder": "Bretthb__jarble",
      "id": "R98",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:switch theme"
            },
            "needs": {
              "user_asked": true
            }
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:switch theme"
            },
            "when_unmodeled": "the switch was inferred from contextual keywords rather than an explicit slash command"
          }
        ],
        "left_out": "The vocabulary cannot distinguish /theme or /skin from other explicit requests."
      },
      "new_names": [
        "other:switch theme"
      ]
    },
    {
      "folder": "Bretthb__jarble",
      "id": "R99",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:set theme"
            },
            "needs": {
              "user_asked": true
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:set theme"
      ]
    },
    {
      "folder": "CaioLC__nvim-onepager",
      "id": "R1",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:remove software"
            },
            "needs": {
              "after": "run",
              "after_task": "other:check dependencies"
            },
            "when_unmodeled": "the software is an old Python interpreter or base Anaconda or Miniconda installation judged stale"
          }
        ],
        "left_out": "The vocabulary cannot represent declaring the software safe to remove or correlate the dependency check with the particular installation."
      },
      "new_names": [
        "other:remove software",
        "other:check dependencies"
      ]
    },
    {
      "folder": "CaioLC__nvim-onepager",
      "id": "R11",
      "translation": {
        "status": "not_in_scope",
        "clauses": null,
        "left_out": "Keeping an installed cloud-sync application during software cleanup is not a git, repository-file, or supported run-task relation."
      },
      "new_names": []
    },
    {
      "folder": "CaioLC__nvim-onepager",
      "id": "R14",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "delete"
            },
            "when_unmodeled": "OneDrive is being dropped and the deletion target is one of its files"
          }
        ],
        "left_out": "No path for the OneDrive files is named, and unlinking a sync account is not a vocabulary action."
      },
      "new_names": []
    },
    {
      "folder": "CaioLC__nvim-onepager",
      "id": "R19",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:debloat script"
            },
            "needs": {
              "after": "run",
              "after_task": "other:debloat script"
            },
            "when_unmodeled": "this is the real execution rather than the initial dry run"
          }
        ],
        "left_out": "The vocabulary cannot distinguish dry-run mode from real execution or record that the user curated the script between runs."
      },
      "new_names": [
        "other:debloat script"
      ]
    },
    {
      "folder": "CaioLC__nvim-onepager",
      "id": "R2",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:remove python installation"
            },
            "needs": {
              "after": "run",
              "after_task": "other:check console scripts"
            }
          }
        ],
        "left_out": "The vocabulary cannot correlate the check with each particular interpreter or distribution or identify its Scripts directory."
      },
      "new_names": [
        "other:remove python installation",
        "other:check console scripts"
      ]
    },
    {
      "folder": "CaioLC__nvim-onepager",
      "id": "R23",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "delete",
              "path": "%TEMP%\\claude/"
            },
            "when_unmodeled": "the deletion is part of clearing %TEMP%"
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "CaioLC__nvim-onepager",
      "id": "R3",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:remove python installation"
            },
            "needs": {
              "after": "run",
              "after_task": "other:search profiles for python path"
            }
          }
        ],
        "left_out": "The rule does not name the profile and init file paths, and the vocabulary cannot correlate the search with each particular interpreter or distribution."
      },
      "new_names": [
        "other:remove python installation",
        "other:search profiles for python path"
      ]
    },
    {
      "folder": "CaioLC__nvim-onepager",
      "id": "R6",
      "translation": {
        "status": "not_in_scope",
        "clauses": null,
        "left_out": "Labeling an installation safe to remove is not an action in the fixed vocabulary."
      },
      "new_names": []
    },
    {
      "folder": "CaioLC__nvim-onepager",
      "id": "R9",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:modify remote access stack"
            },
            "when_unmodeled": "the user's Windows desktop is being debloated"
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:remove remote access stack"
            },
            "when_unmodeled": "the user's Windows desktop is being debloated"
          }
        ],
        "left_out": "The vocabulary cannot enumerate the affected installed products as action targets."
      },
      "new_names": [
        "other:modify remote access stack",
        "other:remove remote access stack"
      ]
    },
    {
      "folder": "CodingButter__cardboard",
      "id": "R114",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": [
                "worktree_add",
                "worktree_remove"
              ]
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "CodingButter__cardboard",
      "id": "R121",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "worktree_remove"
            },
            "needs": {
              "user_confirmed": true
            },
            "when_unmodeled": "the removal uses --force to clean up a leftover worktree"
          }
        ],
        "left_out": "The vocabulary has no --force field and cannot distinguish direct user execution from an agent action beyond confirmation."
      },
      "new_names": []
    },
    {
      "folder": "CodingButter__cardboard",
      "id": "R165",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never_hold",
            "where": {
              "path": "*.png",
              "kind": "file"
            },
            "when_unmodeled": "the file is a Playwright screenshot and is located in the repository root"
          }
        ],
        "left_out": "The path language treats a bare filename pattern as matching at any depth, so repository-root placement is retained as an unmodeled condition."
      },
      "new_names": []
    },
    {
      "folder": "CodingButter__cardboard",
      "id": "R185",
      "translation": {
        "status": "not_in_scope",
        "clauses": null,
        "left_out": "The vocabulary cannot represent the presence of an architectural cross-window sync layer as a prerequisite for building Wave 3 stores."
      },
      "new_names": []
    },
    {
      "folder": "CodingButter__cardboard",
      "id": "R268",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "cherry_pick"
            },
            "needs": {
              "after": "run",
              "after_task": "other:check recent git log",
              "after_branch": "main"
            }
          }
        ],
        "left_out": "The vocabulary cannot verify that exactly five one-line log entries were inspected or that the check successfully confirmed the contents."
      },
      "new_names": [
        "other:check recent git log"
      ]
    },
    {
      "folder": "CodingButter__cardboard",
      "id": "R333",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:generate pack",
              "running": [
                "other:playwright"
              ]
            }
          },
          {
            "type": "must_do",
            "where": {
              "cmd": "read",
              "path": "Cardboard.apg",
              "running": [
                "other:playwright"
              ]
            }
          }
        ],
        "left_out": "The vocabulary represents use of the existing fixture as reading it, but cannot otherwise model a program selecting that fixture."
      },
      "new_names": [
        "other:generate pack",
        "other:playwright"
      ]
    },
    {
      "folder": "CrystalPlatforms__exsize",
      "id": "R11",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:start exsize phase"
            },
            "needs": {
              "after": "run",
              "after_task": "other:check issue blockers"
            }
          }
        ],
        "left_out": "The vocabulary cannot correlate the blocker check with the particular phase."
      },
      "new_names": [
        "other:start exsize phase",
        "other:check issue blockers"
      ]
    },
    {
      "folder": "CrystalPlatforms__exsize",
      "id": "R12",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:start issue work"
            },
            "needs": {
              "after": "run",
              "after_task": "other:check issue dependencies"
            },
            "when_unmodeled": "the work is being started in response to a /tdd N command"
          }
        ],
        "left_out": "The vocabulary cannot correlate issue N across the command, progress-table check, and work start, or verify that all dependencies were met."
      },
      "new_names": [
        "other:start issue work",
        "other:check issue dependencies"
      ]
    },
    {
      "folder": "Desgue__landscaper",
      "id": "R4",
      "translation": {
        "status": "not_in_scope",
        "clauses": null,
        "left_out": "The fixed vocabulary has no fact representing every reviewer's verdict, so it cannot express the prerequisite for proceeding."
      },
      "new_names": []
    },
    {
      "folder": "FearCleevan__final-project-acme",
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
              ],
              "has_secret": true
            },
            "when_unmodeled": "the target is a memory file or plan document"
          }
        ],
        "left_out": "The rule names document categories rather than concrete paths or filename patterns."
      },
      "new_names": []
    },
    {
      "folder": "FearCleevan__final-project-acme",
      "id": "R129",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:fix shopify private access token 401"
            }
          }
        ],
        "left_out": "The explanatory claim that the error resolves when the store goes live is not a normative action constraint."
      },
      "new_names": [
        "other:fix shopify private access token 401"
      ]
    },
    {
      "folder": "FearCleevan__final-project-acme",
      "id": "R13",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:fix exchange rate cors error"
            },
            "needs": {
              "user_asked": true
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:fix exchange rate cors error"
      ]
    },
    {
      "folder": "FearCleevan__final-project-acme",
      "id": "R22",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "create"
            },
            "needs": {
              "after": "read",
              "after_path": "MEMORY.md"
            },
            "when_unmodeled": "the file being created is a daily log"
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "FearCleevan__final-project-acme",
      "id": "R26",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "create"
            },
            "needs": {
              "after": "read"
            },
            "when_unmodeled": "the file being created is a daily log"
          }
        ],
        "left_out": "The rule does not give the June 18 log's filename, so the vocabulary cannot identify which prior read must be the format reference."
      },
      "new_names": []
    },
    {
      "folder": "FearCleevan__final-project-acme",
      "id": "R27",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "create",
              "path": "Client Requirements Checklist/DAILY_LOG_????-??-??.md"
            }
          }
        ],
        "left_out": "The path pattern enforces the stated date-shaped filename but cannot verify that its date equals today's date."
      },
      "new_names": []
    },
    {
      "folder": "FearCleevan__final-project-acme",
      "id": "R40",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": [
                "push",
                "commit",
                "stage"
              ]
            }
          }
        ],
        "left_out": "The phrase \"any destructive git command\" does not identify a fixed set of additional vocabulary actions, so only push, commit, and git add/stage are translated."
      },
      "new_names": []
    },
    {
      "folder": "FearCleevan__final-project-acme",
      "id": "R41",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": [
                "commit",
                "stage",
                "push_branch",
                "push_delete",
                "force_push",
                "local_merge",
                "pr_create",
                "pr_merge",
                "branch_create",
                "branch_delete",
                "checkout",
                "pull",
                "rebase",
                "reset_hard",
                "cherry_pick",
                "fetch",
                "worktree_add",
                "worktree_remove"
              ],
              "after": "edit"
            },
            "when_unmodeled": "the earlier file edit was a code change"
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "FearCleevan__final-project-acme",
      "id": "R43",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": [
                "stage",
                "commit",
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
      "folder": "FearCleevan__final-project-acme",
      "id": "R46",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": [
                "create",
                "edit"
              ],
              "path": "*.md",
              "has_secret": true
            }
          },
          {
            "type": "never",
            "where": {
              "cmd": [
                "create",
                "edit"
              ],
              "has_secret": true
            },
            "when_unmodeled": "the target is a plan document, specification document, code file, or non-Markdown documentation file"
          }
        ],
        "left_out": "The vocabulary has no fixed path sets for plan, specification, code, and documentation files."
      },
      "new_names": []
    },
    {
      "folder": "FearCleevan__final-project-acme",
      "id": "R48",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": [
                "create",
                "edit"
              ],
              "has_secret": true
            },
            "needs": {
              "path": ".env.local"
            },
            "when_unmodeled": "the secret is being stored in a repository file rather than in Vercel environment variables"
          },
          {
            "type": "never",
            "where": {
              "cmd": "commit",
              "has_secret": true
            }
          }
        ],
        "left_out": "Vercel environment variables are outside the file vocabulary."
      },
      "new_names": []
    },
    {
      "folder": "FearCleevan__final-project-acme",
      "id": "R73",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:build brisk crm import or send tooling"
            },
            "needs": {
              "user_confirmed": true
            },
            "when_unmodeled": "the 51k Brisk CRM lead list has resurfaced"
          }
        ],
        "left_out": "The confirmation field cannot specifically verify that the list's provenance was re-confirmed."
      },
      "new_names": [
        "other:build brisk crm import or send tooling"
      ]
    },
    {
      "folder": "FearCleevan__final-project-acme",
      "id": "R83",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:start next build phase"
            },
            "needs": {
              "user_confirmed": true
            }
          }
        ],
        "left_out": "The vocabulary cannot require the user's confirmation to have the exact text \"Yes, Proceed.\""
      },
      "new_names": [
        "other:start next build phase"
      ]
    },
    {
      "folder": "FearCleevan__final-project-acme",
      "id": "R85",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "create",
              "path": "tailwind.config.ts"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "FearCleevan__final-project-acme",
      "id": "R88",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:reconnect acmevintagesupply domain"
            }
          }
        ],
        "left_out": "The explanation about overwriting GoDaddy DNS records is not an additional action constraint."
      },
      "new_names": [
        "other:reconnect acmevintagesupply domain"
      ]
    },
    {
      "folder": "FearCleevan__final-project-acme",
      "id": "R89",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:bulk edit shopify stock"
            },
            "when_unmodeled": "stock quantities for existing Shopify products are being updated"
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:csv import shopify stock"
            },
            "when_unmodeled": "stock quantities for existing Shopify products are being updated"
          }
        ],
        "left_out": "The vocabulary cannot model the causal claim that CSV import may create duplicates."
      },
      "new_names": [
        "other:bulk edit shopify stock",
        "other:csv import shopify stock"
      ]
    },
    {
      "folder": "FearCleevan__final-project-acme",
      "id": "R91",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": [
                "create",
                "edit"
              ],
              "has_secret": true
            },
            "when_unmodeled": "the target is a memory file and the secret is a WordPress login credential or password"
          }
        ],
        "left_out": "Memory files are a document category rather than a named path set."
      },
      "new_names": []
    },
    {
      "folder": "Firesofiso__mouse-platformer",
      "id": "R1",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "edit"
            },
            "needs": {
              "after": "run",
              "after_task": "other:diagnose with debug instrumentation"
            },
            "when_unmodeled": "the edited file is project code"
          }
        ],
        "left_out": "The vocabulary cannot verify what instrumentation was added or correlate the diagnosis with the particular problem."
      },
      "new_names": [
        "other:diagnose with debug instrumentation"
      ]
    },
    {
      "folder": "Firesofiso__mouse-platformer",
      "id": "R3",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "edit"
            },
            "needs": {
              "after": "run",
              "after_task": "other:read diagnostic results"
            },
            "when_unmodeled": "diagnostics have been added and the edit writes project code"
          }
        ],
        "left_out": "The vocabulary cannot distinguish console output from execute_code output or verify that the read result came from the newly added diagnostics."
      },
      "new_names": [
        "other:read diagnostic results"
      ]
    },
    {
      "folder": "Firesofiso__mouse-platformer",
      "id": "R4",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "edit"
            },
            "needs": {
              "after": "run",
              "after_task": "other:read diagnostic results"
            },
            "when_unmodeled": "the edit writes fix code"
          }
        ],
        "left_out": "The vocabulary cannot verify that the results belong to the diagnostic investigation for this fix."
      },
      "new_names": [
        "other:read diagnostic results"
      ]
    },
    {
      "folder": "JD-2207__CSI-ISAC",
      "id": "R109",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:cross scene evaluation"
            },
            "when_unmodeled": "the evaluation uses checkpoint joint_los15_az170.pt"
          },
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:cross scene evaluation"
            },
            "when_unmodeled": "cross-scene evaluation is required and uses results/geo_split/100k/geo_geographic.pt as the source model"
          }
        ],
        "left_out": "The run vocabulary has no field for a model or checkpoint argument, and it cannot express the data-leak explanation."
      },
      "new_names": [
        "other:cross scene evaluation"
      ]
    },
    {
      "folder": "JD-2207__CSI-ISAC",
      "id": "R112",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "stage",
              "kind": "file"
            },
            "needs": {
              "path": "src/exp/*.py"
            },
            "when_unmodeled": "a new file is being added while preparing a commit for JD-2207/CSI-ISAC"
          }
        ],
        "left_out": "The vocabulary cannot directly distinguish a newly created file from a modified tracked file at staging time."
      },
      "new_names": []
    },
    {
      "folder": "JD-2207__CSI-ISAC",
      "id": "R113",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "stage",
              "path": "src/data/"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "JD-2207__CSI-ISAC",
      "id": "R114",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "stage",
              "path": "src/checkpoint/"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "JD-2207__CSI-ISAC",
      "id": "R115",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "stage",
              "path": "src/results/"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    }
  ]
}
```