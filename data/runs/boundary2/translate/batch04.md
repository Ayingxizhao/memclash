```json
{
  "rules": [
    {
      "folder": "Robert-Freire__langTeachSaaS",
      "id": "R188",
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
              "after_task": "other:assign issue to self"
            }
          }
        ],
        "left_out": "The vocabulary cannot verify that both actions concern the same selected issue."
      },
      "new_names": [
        "other:start issue work",
        "other:assign issue to self"
      ]
    },
    {
      "folder": "Robert-Freire__langTeachSaaS",
      "id": "R189",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:implement issue"
            },
            "needs": {
              "after": "worktree_add"
            }
          }
        ],
        "left_out": "The vocabulary cannot verify that the worktree and implementation concern the same issue or that the worktree was created with a new branch."
      },
      "new_names": [
        "other:implement issue"
      ]
    },
    {
      "folder": "Robert-Freire__langTeachSaaS",
      "id": "R191",
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
              "after_task": "other:qa acceptance criteria verification",
              "after_ok": true
            }
          }
        ],
        "left_out": "The vocabulary cannot identify the QA agent or correlate the verification with the particular PR."
      },
      "new_names": [
        "other:qa acceptance criteria verification"
      ]
    },
    {
      "folder": "Robert-Freire__langTeachSaaS",
      "id": "R192",
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
              "after_task": "other:code quality review",
              "after_ok": true
            }
          }
        ],
        "left_out": "The vocabulary cannot identify the review agent or correlate its review with the particular PR."
      },
      "new_names": [
        "other:code quality review"
      ]
    },
    {
      "folder": "Robert-Freire__langTeachSaaS",
      "id": "R211",
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
            "when_unmodeled": "the current migration is the real run in Azure mode"
          }
        ],
        "left_out": "The vocabulary cannot distinguish a --dry-run migration from a real migration."
      },
      "new_names": []
    },
    {
      "folder": "Robert-Freire__langTeachSaaS",
      "id": "R243",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:review screen"
            },
            "needs": {
              "after": "read"
            }
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:seed screen"
            },
            "needs": {
              "after": "read"
            }
          }
        ],
        "left_out": "The vocabulary cannot identify an unnamed screen-behavior document or verify that the read document and action concern the same screen."
      },
      "new_names": [
        "other:review screen",
        "other:seed screen"
      ]
    },
    {
      "folder": "Robert-Freire__langTeachSaaS",
      "id": "R66",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "edit"
            },
            "needs": {
              "after": "read"
            }
          }
        ],
        "left_out": "The vocabulary cannot require the earlier read and current edit to target the same otherwise-unnamed file."
      },
      "new_names": []
    },
    {
      "folder": "Robert-Freire__langTeachSaaS",
      "id": "R9",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:npm run dev"
            },
            "when_unmodeled": "the action is part of regular development work"
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:local vite dev server"
            },
            "when_unmodeled": "the action is part of regular development work"
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:npm run dev",
        "other:local vite dev server"
      ]
    },
    {
      "folder": "Sc07713__PLAIOS",
      "id": "R124",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:cross-tool invocation"
            },
            "needs": {
              "after": "read",
              "after_path": "AGENTS.md"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:cross-tool invocation"
      ]
    },
    {
      "folder": "Sc07713__PLAIOS",
      "id": "R126",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:spy systematic options refinement"
            }
          }
        ],
        "left_out": "The stated reason that the area is settled is not a formal condition."
      },
      "new_names": [
        "other:spy systematic options refinement"
      ]
    },
    {
      "folder": "Sc07713__PLAIOS",
      "id": "R129",
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
              "after_task": "other:refine inverse-squeeze short straddle tp50 strategy"
            },
            "when_unmodeled": "the deployment is of the inverse-squeeze short straddle TP50 strategy as a sleeve"
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:refine inverse-squeeze short straddle tp50 strategy"
      ]
    },
    {
      "folder": "Sc07713__PLAIOS",
      "id": "R142",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:re-verify budget event structure"
            },
            "when_unmodeled": "the action occurs in the next session"
          }
        ],
        "left_out": "The prior clean confirmation and its date are explanatory context rather than expressible action fields."
      },
      "new_names": [
        "other:re-verify budget event structure"
      ]
    },
    {
      "folder": "Sc07713__PLAIOS",
      "id": "R148",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:re-verify korea trip savings events"
            }
          }
        ],
        "left_out": "The prior confirmation in PocketSmith is explanatory context rather than an expressible action field."
      },
      "new_names": [
        "other:re-verify korea trip savings events"
      ]
    },
    {
      "folder": "Sc07713__PLAIOS",
      "id": "R182",
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
              "after_task": "test",
              "after_ok": true
            },
            "when_unmodeled": "the deployment concerns a skip-month or buy-month trading claim"
          }
        ],
        "left_out": "The vocabulary cannot distinguish a Bonferroni-corrected test from other tests or correlate it with the deployed claim."
      },
      "new_names": []
    },
    {
      "folder": "Sc07713__PLAIOS",
      "id": "R183",
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
              "after_task": "test",
              "after_ok": true
            },
            "when_unmodeled": "the deployment concerns a skip-month or buy-month trading claim"
          }
        ],
        "left_out": "The vocabulary cannot distinguish a split-sample test from other tests or correlate it with the deployed claim."
      },
      "new_names": []
    },
    {
      "folder": "Sc07713__PLAIOS",
      "id": "R185",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "deploy"
            },
            "when_unmodeled": "the deployment is of the long-strangle book"
          }
        ],
        "left_out": "The reason that the book is not yet deployable is not a separate formal condition."
      },
      "new_names": []
    },
    {
      "folder": "Sc07713__PLAIOS",
      "id": "R200",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "checkout",
              "branch": "main"
            },
            "when_unmodeled": "the repository is trading-tools"
          },
          {
            "type": "must_do",
            "where": {
              "cmd": "checkout",
              "branch": "master"
            },
            "when_unmodeled": "switching branches in the trading-tools repository"
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "Sc07713__PLAIOS",
      "id": "R241",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:max sprints"
            },
            "when_unmodeled": "the readiness gates have not passed"
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:depth jumps"
            },
            "when_unmodeled": "the readiness gates have not passed"
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:max sprints",
        "other:depth jumps"
      ]
    },
    {
      "folder": "Sc07713__PLAIOS",
      "id": "R250",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:activate travel domain"
            },
            "needs": {
              "user_asked": true
            }
          }
        ],
        "left_out": "The vocabulary cannot identify Scott separately from the user."
      },
      "new_names": [
        "other:activate travel domain"
      ]
    },
    {
      "folder": "Sc07713__PLAIOS",
      "id": "R251",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "edit",
              "path": "CLAUDE.md"
            },
            "needs": {
              "user_asked": true
            },
            "when_unmodeled": "the edit adds the travel domain to the top-level PLAIOS domains table"
          }
        ],
        "left_out": "The vocabulary cannot identify Scott separately from the user."
      },
      "new_names": []
    },
    {
      "folder": "Sc07713__PLAIOS",
      "id": "R299",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:rs_vol sleeve",
              "running": [
                "other:spy_top_5 strategy"
              ]
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:rs_vol sleeve",
        "other:spy_top_5 strategy"
      ]
    },
    {
      "folder": "Sc07713__PLAIOS",
      "id": "R3",
      "translation": {
        "status": "ok",
        "clauses": [
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
      "folder": "Sc07713__PLAIOS",
      "id": "R64",
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
              "user_confirmed": true
            }
          }
        ],
        "left_out": "The vocabulary cannot identify Scott separately from the user or cover repository changes that are neither basic file actions nor named git actions."
      },
      "new_names": []
    },
    {
      "folder": "Sc07713__PLAIOS",
      "id": "R65",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "delete",
              "path": "D:\\PLAIOS\\bundle.md"
            },
            "needs": {
              "user_confirmed": true
            }
          }
        ],
        "left_out": "The vocabulary cannot identify Scott separately from the user."
      },
      "new_names": []
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R10",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:upload"
            },
            "needs": {
              "user_asked": true
            },
            "when_unmodeled": "the request in chat is for this one specific upload"
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:schedule upload"
            },
            "needs": {
              "user_asked": true
            },
            "when_unmodeled": "the request in chat is for this one specific upload"
          }
        ],
        "left_out": "The vocabulary cannot identify Bryan separately from the user or represent permission expiration after the single upload."
      },
      "new_names": [
        "other:upload",
        "other:schedule upload"
      ]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R124",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": [
                "edit",
                "move",
                "delete"
              ]
            },
            "needs": {
              "after": "run",
              "after_task": "other:verify changes in scratchpad",
              "after_ok": true
            },
            "when_unmodeled": "the target is the user's real file"
          }
        ],
        "left_out": "The vocabulary cannot correlate the scratchpad verification with the particular real file."
      },
      "new_names": [
        "other:verify changes in scratchpad"
      ]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R140",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "edit",
              "path": "*.pptx"
            },
            "needs": {
              "after": "run",
              "after_task": "other:dump raw run xml"
            },
            "when_unmodeled": "the edit regex-fixes text"
          }
        ],
        "left_out": "The vocabulary cannot correlate the XML dump with the target paragraphs."
      },
      "new_names": [
        "other:dump raw run xml"
      ]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R16",
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
            "when_unmodeled": "the edit fills in the contents of a copied file after the user requested the copy"
          }
        ],
        "left_out": "The vocabulary cannot express that offering the fill-in must be a separate conversational step."
      },
      "new_names": []
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R169",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:export.mjs"
            },
            "needs": {
              "after": "run",
              "after_task": "other:build.mjs",
              "after_ok": true
            },
            "when_unmodeled": "the action is for the animate skill"
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:export.mjs",
        "other:build.mjs"
      ]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R170",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "build"
            },
            "needs": {
              "after": "run",
              "after_task": "other:search github for existing solution"
            },
            "when_unmodeled": "the build creates a new skill, tool, script, or small app from scratch"
          }
        ],
        "left_out": "The additional Hugging Face search required for models or agents cannot be combined with the GitHub prerequisite because the vocabulary records only one earlier run task."
      },
      "new_names": [
        "other:search github for existing solution"
      ]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R172",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:connect higgsfield"
            },
            "needs": {
              "user_confirmed": true
            }
          }
        ],
        "left_out": "The vocabulary cannot identify Bryan separately from the user."
      },
      "new_names": [
        "other:connect higgsfield"
      ]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R173",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:log in to higgsfield"
            },
            "needs": {
              "user_confirmed": true
            }
          }
        ],
        "left_out": "The vocabulary cannot identify Bryan separately from the user."
      },
      "new_names": [
        "other:log in to higgsfield"
      ]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R177",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:install tool"
            },
            "needs": {
              "after": "run",
              "after_task": "other:audit tool",
              "after_ok": true
            },
            "when_unmodeled": "the tool is considered a good fit"
          }
        ],
        "left_out": "The vocabulary cannot verify that the audited and installed tools are the same."
      },
      "new_names": [
        "other:install tool",
        "other:audit tool"
      ]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R187",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:install tool"
            },
            "needs": {
              "after": "run",
              "after_task": "other:ask user about installation"
            },
            "when_unmodeled": "the tool was found in the search"
          }
        ],
        "left_out": "The vocabulary cannot verify that the question and installation concern the same tool."
      },
      "new_names": [
        "other:install tool",
        "other:ask user about installation"
      ]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R188",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:search for existing solution"
            },
            "when_unmodeled": "the user requests creation of a skill, tool, or script"
          }
        ],
        "left_out": "The vocabulary cannot express that the search must be the first step rather than merely an obligatory step."
      },
      "new_names": [
        "other:search for existing solution"
      ]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R193",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:render"
            },
            "needs": {
              "after": "run",
              "after_task": "other:stop at every=3 board",
              "user_confirmed": true
            },
            "when_unmodeled": "the action occurs in a film chat"
          }
        ],
        "left_out": "The vocabulary cannot identify Bryan separately from the user or express that the stop happens exactly once."
      },
      "new_names": [
        "other:render",
        "other:stop at every=3 board"
      ]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R194",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:upload films"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:upload films"
      ]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R218",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": [
                "create",
                "move"
              ]
            },
            "when_unmodeled": "the action places animation pieces in the JARVIS repository"
          }
        ],
        "left_out": "No concrete path for the animation pieces or JARVIS repository is named."
      },
      "new_names": []
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R22",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "create",
              "path": "*.xlsx"
            },
            "needs": {
              "after": "run",
              "after_task": "other:excel formatting feasibility test",
              "after_ok": true
            }
          }
        ],
        "left_out": "The vocabulary cannot verify that the single test covers every formatting technique used by the particular design."
      },
      "new_names": [
        "other:excel formatting feasibility test"
      ]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R230",
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
              "path": "*.pptx"
            },
            "needs": {
              "user_asked": true
            },
            "when_unmodeled": "the presentation is for the Bahasa Inggris presentation project and building it is being started"
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R235",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:submit bahasa inggris work"
            },
            "needs": {
              "after": "run",
              "after_task": "other:ask for grading rubric"
            }
          }
        ],
        "left_out": "The vocabulary cannot correlate the requested rubric with the particular project or assignment."
      },
      "new_names": [
        "other:submit bahasa inggris work",
        "other:ask for grading rubric"
      ]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R244",
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
              "after": "read"
            },
            "when_unmodeled": "the action republishes an existing artifact in a new session"
          }
        ],
        "left_out": "The vocabulary cannot require the earlier read and republication to concern the same artifact."
      },
      "new_names": []
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R28",
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
              "after_task": "other:check for lock file",
              "after_ok": true
            },
            "when_unmodeled": "the edit replaces Bryan's file"
          }
        ],
        "left_out": "The vocabulary cannot express that the check specifically looks for the corresponding ~$ lock file or identify Bryan separately from the user."
      },
      "new_names": [
        "other:check for lock file"
      ]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R29",
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
              "after_task": "other:check file matches backup",
              "after_ok": true
            },
            "when_unmodeled": "the edit replaces Bryan's file"
          }
        ],
        "left_out": "The vocabulary cannot express byte identity or correlate the check, backup, and replaced file; it also cannot identify Bryan separately from the user."
      },
      "new_names": [
        "other:check file matches backup"
      ]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R296",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "move",
              "path": "C:\\Bryan De Great\\GP-100\\",
              "kind": "dir"
            }
          }
        ],
        "left_out": "The shortcut dependency is explanatory context rather than a formal condition."
      },
      "new_names": []
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R318",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:buat_kaos.py"
            },
            "needs": {
              "after": "move"
            },
            "when_unmodeled": "the action rebuilds kaos boards and same-named output files already exist"
          }
        ],
        "left_out": "The vocabulary cannot constrain an earlier move's destination to _Arsip\\ or correlate the moved files with the rebuild outputs."
      },
      "new_names": [
        "other:buat_kaos.py"
      ]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R336",
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
            "when_unmodeled": "the commit contains the sekitar skill"
          }
        ],
        "left_out": "No concrete path for the sekitar skill is named, and the vocabulary cannot identify Bryan separately from the user."
      },
      "new_names": []
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R337",
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
            "when_unmodeled": "the commit contains the riset-sekitar skill"
          }
        ],
        "left_out": "No concrete path for the riset-sekitar skill is named, and the vocabulary cannot identify Bryan separately from the user."
      },
      "new_names": []
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R340",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:bulk-post uploads"
            }
          }
        ],
        "left_out": "The vocabulary cannot count scheduled uploads, so the positive one-at-a-time formulation is represented only by the bulk-post prohibition."
      },
      "new_names": [
        "other:bulk-post uploads"
      ]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R360",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:post first comment"
            },
            "when_unmodeled": "the associated scheduled upload is not yet live"
          }
        ],
        "left_out": "The vocabulary cannot correlate the comment with a particular scheduled upload."
      },
      "new_names": [
        "other:post first comment"
      ]
    }
  ]
}
```