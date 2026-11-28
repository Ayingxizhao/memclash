```json
{
  "rules": [
    {
      "folder": "JD-2207__CSI-ISAC",
      "id": "R125",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:100k run"
            },
            "needs": {
              "after": "run",
              "after_task": "other:10k proxy",
              "after_ok": true
            },
            "when_unmodeled": "the 10k result is a clear signal worth confirming"
          }
        ],
        "left_out": "The vocabulary cannot assess whether a signal is clear or worth confirming; that requirement is retained as an unmodeled condition."
      },
      "new_names": [
        "other:100k run",
        "other:10k proxy"
      ]
    },
    {
      "folder": "JD-2207__CSI-ISAC",
      "id": "R127",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:experiment"
            },
            "needs": {
              "after": "run",
              "after_task": "other:web research"
            },
            "when_unmodeled": "the experiment concerns CSI feedback, NLOS localization, or channel charting"
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:propose experiment"
            },
            "needs": {
              "after": "run",
              "after_task": "other:web research"
            },
            "when_unmodeled": "the proposal concerns CSI feedback, NLOS localization, or channel charting"
          }
        ],
        "left_out": "The vocabulary cannot verify that the research is actual web research into established approaches or that it addresses the same specific problem."
      },
      "new_names": [
        "other:experiment",
        "other:propose experiment",
        "other:web research"
      ]
    },
    {
      "folder": "JD-2207__CSI-ISAC",
      "id": "R150",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "delete",
              "path": "C:\\Users\\javid\\Documents\\Javier\\.claude"
            }
          }
        ],
        "left_out": "The rationale that this is the only pre-crash copy is not represented."
      },
      "new_names": []
    },
    {
      "folder": "JD-2207__CSI-ISAC",
      "id": "R164",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "edit",
              "path": "*.svg"
            },
            "needs": {
              "after": "read",
              "after_path": "*.svg"
            },
            "when_unmodeled": "the SVG is a figure"
          }
        ],
        "left_out": "The vocabulary cannot require that the earlier read covered the exact region being changed or correlate it with the same SVG."
      },
      "new_names": []
    },
    {
      "folder": "JD-2207__CSI-ISAC",
      "id": "R169",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:training"
            },
            "needs": {
              "after": "run",
              "after_task": "other:apply zero-norm ue filter",
              "after_ok": true
            },
            "when_unmodeled": "training uses a newly generated RT dataset"
          }
        ],
        "left_out": "The vocabulary cannot check the dataset's indoor fraction, the min_norm_frac value, or use of build_multitask_feeds."
      },
      "new_names": [
        "other:training",
        "other:apply zero-norm ue filter"
      ]
    },
    {
      "folder": "JD-2207__CSI-ISAC",
      "id": "R178",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:staged training"
            },
            "when_unmodeled": "joint-training negative transfer is being addressed"
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:pcgrad"
            },
            "needs": {
              "after": "run",
              "after_task": "other:staged training"
            },
            "when_unmodeled": "a residual gap remains after staged training"
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:forkmerge"
            },
            "needs": {
              "after": "run",
              "after_task": "other:staged training"
            },
            "when_unmodeled": "a residual gap remains after staged training"
          }
        ],
        "left_out": "The vocabulary cannot determine whether negative transfer or a residual gap exists."
      },
      "new_names": [
        "other:staged training",
        "other:pcgrad",
        "other:forkmerge"
      ]
    },
    {
      "folder": "JD-2207__CSI-ISAC",
      "id": "R196",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:convert channel angle delay"
            },
            "when_unmodeled": "the input is RT-generated CSI already in the delay domain"
          },
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:angular dft"
            },
            "when_unmodeled": "RT-generated CSI is being transformed"
          }
        ],
        "left_out": "The vocabulary cannot inspect the CSI representation or distinguish which transformation is being applied to a particular dataset."
      },
      "new_names": [
        "other:convert channel angle delay",
        "other:angular dft"
      ]
    },
    {
      "folder": "JD-2207__CSI-ISAC",
      "id": "R2",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:csi-representation training"
            },
            "needs": {
              "user_confirmed": true
            },
            "when_unmodeled": "this is the real training run"
          }
        ],
        "left_out": "Whether a run is the real run is retained as an unmodeled condition."
      },
      "new_names": [
        "other:csi-representation training"
      ]
    },
    {
      "folder": "JD-2207__CSI-ISAC",
      "id": "R207",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:pure-nlos test"
            }
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:los-nlos comparison"
            },
            "needs": {
              "after": "run",
              "after_task": "other:pure-nlos test"
            }
          }
        ],
        "left_out": "The need to re-aim the azimuth is explanatory and cannot be represented."
      },
      "new_names": [
        "other:pure-nlos test",
        "other:los-nlos comparison"
      ]
    },
    {
      "folder": "JD-2207__CSI-ISAC",
      "id": "R209",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:single-snapshot self-aiding"
            }
          }
        ],
        "left_out": "The broad notion of pursuing the approach outside a runnable task is not represented."
      },
      "new_names": [
        "other:single-snapshot self-aiding"
      ]
    },
    {
      "folder": "JD-2207__CSI-ISAC",
      "id": "R223",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:implement tr 38.901 hybrid model"
            }
          },
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:cite tr 38.901 hybrid model"
            }
          }
        ],
        "left_out": "The vocabulary cannot inspect content to verify that the cited or implemented model is specifically section 8.4's map-based hybrid channel model."
      },
      "new_names": [
        "other:implement tr 38.901 hybrid model",
        "other:cite tr 38.901 hybrid model"
      ]
    },
    {
      "folder": "JD-2207__CSI-ISAC",
      "id": "R227",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:stochastic-cluster perturbation"
            },
            "when_unmodeled": "the perturbation is being used during training"
          }
        ],
        "left_out": "The vocabulary cannot inspect a training configuration to detect use of this perturbation."
      },
      "new_names": [
        "other:stochastic-cluster perturbation"
      ]
    },
    {
      "folder": "JD-2207__CSI-ISAC",
      "id": "R244",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:build ns-3 5g-lena ns3-rt integration"
            }
          }
        ],
        "left_out": "The vocabulary cannot inspect project content to identify implementation of this integration."
      },
      "new_names": [
        "other:build ns-3 5g-lena ns3-rt integration"
      ]
    },
    {
      "folder": "JD-2207__CSI-ISAC",
      "id": "R264",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "publish"
            },
            "when_unmodeled": "the walkthrough Artifact is being republished using its existing file path"
          }
        ],
        "left_out": "The vocabulary has no path field for publish actions and cannot compare a publication's path with its previous path or verify that its URL is preserved."
      },
      "new_names": []
    },
    {
      "folder": "JD-2207__CSI-ISAC",
      "id": "R3",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:10k proxy"
            },
            "when_unmodeled": "the CSI-representation experiment is being run"
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:100k run"
            },
            "needs": {
              "after": "run",
              "after_task": "other:10k proxy",
              "after_ok": true
            },
            "when_unmodeled": "the 100k run is confirming the CSI-representation result"
          }
        ],
        "left_out": "The vocabulary cannot correlate both runs with the same experiment or result."
      },
      "new_names": [
        "other:10k proxy",
        "other:100k run"
      ]
    },
    {
      "folder": "JD-2207__CSI-ISAC",
      "id": "R7",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:per-layer model retrain"
            },
            "needs": {
              "user_confirmed": true
            },
            "when_unmodeled": "the user's confirmation identifies which lever to pursue"
          }
        ],
        "left_out": "The vocabulary cannot record which lever the user selected."
      },
      "new_names": [
        "other:per-layer model retrain"
      ]
    },
    {
      "folder": "JD-2207__CSI-ISAC",
      "id": "R76",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "delete",
              "path": "F:\\Javier_old\\users-fernando"
            },
            "when_unmodeled": "the new backup has not been verified as trustworthy"
          }
        ],
        "left_out": "Backup trustworthiness cannot be checked by the vocabulary."
      },
      "new_names": []
    },
    {
      "folder": "Jordi-Izquierdo-DDS__rUv_install_test",
      "id": "R11",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "edit"
            },
            "when_unmodeled": "the target is memory content and the operation is a restoration"
          }
        ],
        "left_out": "No path is named, so memory content and restoration context remain unmodeled."
      },
      "new_names": []
    },
    {
      "folder": "Jordi-Izquierdo-DDS__rUv_install_test",
      "id": "R130",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "read",
              "path": "memory.db",
              "running": [
                "other:mcp server"
              ]
            },
            "when_unmodeled": "the read is performed from a node -e debug script"
          }
        ],
        "left_out": "The vocabulary cannot identify the program responsible for a file read."
      },
      "new_names": [
        "other:mcp server"
      ]
    },
    {
      "folder": "Jordi-Izquierdo-DDS__rUv_install_test",
      "id": "R14",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "move"
            },
            "when_unmodeled": "the move renames a memory file during restoration"
          }
        ],
        "left_out": "No memory-file path is named, and the vocabulary cannot distinguish renaming from other moves."
      },
      "new_names": []
    },
    {
      "folder": "Jordi-Izquierdo-DDS__rUv_install_test",
      "id": "R17",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "create",
              "path": "MEMORY.md"
            },
            "needs": {
              "after": "read",
              "after_path": "memory/MEMORY.md"
            }
          }
        ],
        "left_out": "The vocabulary has no copy action and cannot prove that the created file is a copy rather than newly authored content."
      },
      "new_names": []
    },
    {
      "folder": "Jordi-Izquierdo-DDS__rUv_install_test",
      "id": "R204",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "create",
              "path": "scripts/patches/NNN-PATCH-*.sh"
            },
            "when_unmodeled": "the patch file concerns changes to the viz directory"
          }
        ],
        "left_out": "The vocabulary cannot inspect a patch file to determine whether it concerns viz/."
      },
      "new_names": []
    },
    {
      "folder": "Jordi-Izquierdo-DDS__rUv_install_test",
      "id": "R217",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "edit",
              "path": ".claude/helpers/"
            },
            "needs": {
              "after": "run",
              "after_task": "other:bootstrap"
            }
          }
        ],
        "left_out": "The vocabulary cannot distinguish a direct edit from an edit produced by bootstrap or represent source-of-truth status."
      },
      "new_names": [
        "other:bootstrap"
      ]
    },
    {
      "folder": "Jordi-Izquierdo-DDS__rUv_install_test",
      "id": "R55",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "restart",
              "after": "edit"
            },
            "when_unmodeled": "the earlier edit was to a hook script"
          }
        ],
        "left_out": "No hook-script path is named, and the vocabulary cannot represent the explanatory behavior of the next hook invocation."
      },
      "new_names": []
    },
    {
      "folder": "PhoeNox__Phoenox",
      "id": "R68",
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
              "after_task": "other:ask memory scope"
            },
            "when_unmodeled": "the file action saves a memory"
          }
        ],
        "left_out": "The vocabulary cannot inspect the question to verify that it asks whether the memory is project-specific or generally applicable."
      },
      "new_names": [
        "other:ask memory scope"
      ]
    },
    {
      "folder": "PhoeNox__Phoenox",
      "id": "R72",
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
            "when_unmodeled": "the action changes code, the user requested only analysis or review, and the user did not explicitly request implementation"
          }
        ],
        "left_out": "The vocabulary cannot classify files as code or distinguish analysis, review, and implementation requests."
      },
      "new_names": []
    },
    {
      "folder": "PhoeNox__Phoenox",
      "id": "R74",
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
              "user_asked": true
            },
            "when_unmodeled": "the action writes code and the request uses apply, fix, implement, do it, or equivalent explicit wording"
          }
        ],
        "left_out": "The vocabulary cannot classify written content as code or inspect the user's wording."
      },
      "new_names": []
    },
    {
      "folder": "PhoeNox__Phoenox",
      "id": "R76",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "test",
              "after": [
                "create",
                "edit"
              ]
            },
            "when_unmodeled": "the earlier file change implemented a change"
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "lint",
              "after": [
                "create",
                "edit"
              ]
            },
            "when_unmodeled": "the earlier file change implemented a change"
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "build",
              "after": [
                "create",
                "edit"
              ]
            },
            "when_unmodeled": "the earlier file change implemented a change"
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:typecheck",
              "after": [
                "create",
                "edit"
              ]
            },
            "when_unmodeled": "the earlier file change implemented a change"
          }
        ],
        "left_out": "The vocabulary cannot determine whether an earlier file change was an implementation."
      },
      "new_names": [
        "other:typecheck"
      ]
    },
    {
      "folder": "PhoeNox__Phoenox",
      "id": "R77",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:end-to-end verification"
            }
          }
        ],
        "left_out": "The vocabulary cannot determine whether /verify, launching the app, or driving it constitutes the named end-to-end verification task."
      },
      "new_names": [
        "other:end-to-end verification"
      ]
    },
    {
      "folder": "PhoeNox__Phoenox",
      "id": "R78",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "test"
            },
            "when_unmodeled": "the run executes test files written as part of the current implementation"
          }
        ],
        "left_out": "The vocabulary cannot identify who wrote a test file or why it was written."
      },
      "new_names": []
    },
    {
      "folder": "PhoeNox__Phoenox",
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
              "files_shown": true,
              "user_confirmed": true
            }
          }
        ],
        "left_out": "files_shown approximates review but cannot prove that the user reviewed the change; the prior-slice history is explanatory."
      },
      "new_names": []
    },
    {
      "folder": "PhoeNox__Phoenox",
      "id": "R82",
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
              "user_asked": true
            }
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "lint"
            },
            "needs": {
              "user_asked": true
            }
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "build"
            },
            "needs": {
              "user_asked": true
            }
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:typecheck"
            },
            "needs": {
              "user_asked": true
            }
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:verification"
            },
            "needs": {
              "user_asked": true
            }
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:checks"
            },
            "needs": {
              "user_asked": true
            }
          }
        ],
        "left_out": "The vocabulary cannot verify that the request occurred in the same conversation."
      },
      "new_names": [
        "other:typecheck",
        "other:verification",
        "other:checks"
      ]
    },
    {
      "folder": "PhoeNox__Phoenox",
      "id": "R83",
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
              "max_files": 1
            },
            "when_unmodeled": "/tdd is active and the test is part of the red-green loop"
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "test",
              "suite": "all"
            },
            "when_unmodeled": "/tdd is active"
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "build"
            },
            "when_unmodeled": "/tdd is active"
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "lint"
            },
            "when_unmodeled": "/tdd is active"
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:typecheck"
            },
            "when_unmodeled": "/tdd is active"
          }
        ],
        "left_out": "max_files captures a single test file but cannot ensure that the test is targeted; invocation of /tdd and membership in the red-green loop are unmodeled."
      },
      "new_names": [
        "other:typecheck"
      ]
    },
    {
      "folder": "PhoeNox__Phoenox",
      "id": "R84",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "commit"
            },
            "needs": {
              "user_confirmed": true
            }
          }
        ],
        "left_out": "The vocabulary records approval but not the act of asking or waiting for it."
      },
      "new_names": []
    },
    {
      "folder": "PhoeNox__Phoenox",
      "id": "R85",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:close ticket"
            },
            "needs": {
              "after": "commit"
            },
            "when_unmodeled": "the ticket is completed and the earlier commit succeeded"
          }
        ],
        "left_out": "after_ok is available only for earlier run actions, so commit success and ticket completion remain unmodeled."
      },
      "new_names": [
        "other:close ticket"
      ]
    },
    {
      "folder": "PhoeNox__Phoenox",
      "id": "R86",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:verification"
            },
            "needs": {
              "user_asked": true
            }
          }
        ],
        "left_out": "The vocabulary cannot distinguish a harness or skill prompt from a user request or represent prompt precedence."
      },
      "new_names": [
        "other:verification"
      ]
    },
    {
      "folder": "PhoeNox__Phoenox",
      "id": "R87",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "commit"
            },
            "when_unmodeled": "the only purported authorization is a pattern in repository commit history"
          }
        ],
        "left_out": "The vocabulary cannot inspect the reason an action was considered authorized."
      },
      "new_names": []
    },
    {
      "folder": "Robert-Freire__langTeachSaaS",
      "id": "R124",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:investigate blocker bug 71",
              "branch": "hotfix*"
            }
          },
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:fix blocker bug 71",
              "branch": "hotfix*"
            }
          }
        ],
        "left_out": "The vocabulary cannot represent overriding the separate four-day waiting rule, and hotfix* approximates an otherwise unnamed hotfix branch."
      },
      "new_names": [
        "other:investigate blocker bug 71",
        "other:fix blocker bug 71"
      ]
    },
    {
      "folder": "Robert-Freire__langTeachSaaS",
      "id": "R136",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:implement screen"
            },
            "needs": {
              "after": "read",
              "after_path": "docs/design-system.md"
            },
            "when_unmodeled": "the screen is UI work"
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:review screen"
            },
            "needs": {
              "after": "read",
              "after_path": "docs/design-system.md"
            },
            "when_unmodeled": "the screen is UI work"
          }
        ],
        "left_out": "The vocabulary cannot enforce that the document is treated as the single source of truth or assess whether work follows it."
      },
      "new_names": [
        "other:implement screen",
        "other:review screen"
      ]
    },
    {
      "folder": "Robert-Freire__langTeachSaaS",
      "id": "R148",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:docker compose all services"
            },
            "when_unmodeled": "the command is docker compose up --build -d for all services during development"
          }
        ],
        "left_out": "The exact command flags, all-services scope, and development context cannot be inspected by the vocabulary."
      },
      "new_names": [
        "other:docker compose all services"
      ]
    },
    {
      "folder": "Robert-Freire__langTeachSaaS",
      "id": "R15",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "create"
            },
            "when_unmodeled": "the created file is the required e2e test"
          },
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "test"
            },
            "when_unmodeled": "the run executes the required e2e test"
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "pr_create"
            },
            "needs": {
              "after": "create"
            },
            "when_unmodeled": "the earlier created file is the required e2e test"
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "pr_create"
            },
            "needs": {
              "after": "run",
              "after_task": "test",
              "after_ok": true
            },
            "when_unmodeled": "the earlier successful test run is the required e2e test"
          }
        ],
        "left_out": "The vocabulary cannot correlate the created test file, the test run, and the PR, or distinguish e2e tests from other tests."
      },
      "new_names": []
    },
    {
      "folder": "Robert-Freire__langTeachSaaS",
      "id": "R154",
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
              "running": [
                "other:sqlserver",
                "other:api",
                "other:frontend"
              ]
            },
            "when_unmodeled": "an individual e2e test is being run outside Docker with npx playwright test"
          }
        ],
        "left_out": "The vocabulary cannot inspect the test command or determine whether it runs outside Docker."
      },
      "new_names": [
        "other:sqlserver",
        "other:api",
        "other:frontend"
      ]
    },
    {
      "folder": "Robert-Freire__langTeachSaaS",
      "id": "R155",
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
            "when_unmodeled": "the selected test has the SkipIfNoClaudeApiKey decoration"
          }
        ],
        "left_out": "The vocabulary cannot inspect test decorations; user_confirmed approximates explicit opt-in."
      },
      "new_names": []
    },
    {
      "folder": "Robert-Freire__langTeachSaaS",
      "id": "R159",
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
        "left_out": "has_secret does not distinguish the Claude API key from other secrets."
      },
      "new_names": []
    },
    {
      "folder": "Robert-Freire__langTeachSaaS",
      "id": "R172",
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
              "in_worktree": true
            },
            "when_unmodeled": "the target is a task plan file and the worktree is the active worktree"
          }
        ],
        "left_out": "The vocabulary cannot classify task plan files or distinguish the active worktree from another worktree."
      },
      "new_names": []
    },
    {
      "folder": "Robert-Freire__langTeachSaaS",
      "id": "R173",
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
            "when_unmodeled": "the target is a task plan file in the main repository directory"
          }
        ],
        "left_out": "No main-repository path is named, and the vocabulary cannot classify task plan files."
      },
      "new_names": []
    },
    {
      "folder": "Robert-Freire__langTeachSaaS",
      "id": "R174",
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
              "path": "plan/*"
            }
          }
        ],
        "left_out": "The path pattern captures files directly inside plan/ but cannot determine semantically whether each file is a plan file."
      },
      "new_names": []
    },
    {
      "folder": "Robert-Freire__langTeachSaaS",
      "id": "R175",
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
            "when_unmodeled": "the target is a phase plan file not located in that phase's feature subfolder"
          }
        ],
        "left_out": "No feature-subfolder path is named, and the vocabulary cannot correlate a plan file with its phase."
      },
      "new_names": []
    },
    {
      "folder": "Robert-Freire__langTeachSaaS",
      "id": "R176",
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
              "path": "plan.md"
            },
            "when_unmodeled": "the target is a phase overview file located inside that phase's subfolder"
          }
        ],
        "left_out": "The filename requirement is represented, but the vocabulary cannot recognize or correlate the containing phase subfolder."
      },
      "new_names": []
    },
    {
      "folder": "Robert-Freire__langTeachSaaS",
      "id": "R177",
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
              "path": "task*-*.md"
            },
            "when_unmodeled": "the target is an individual task file"
          }
        ],
        "left_out": "The glob cannot require a numeric N, a short description, or placement in the same phase subfolder as the overview."
      },
      "new_names": []
    }
  ]
}
```