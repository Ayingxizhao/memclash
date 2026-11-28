```json
{
  "rules": [
    {
      "folder": "Slicon123__JARVIS",
      "id": "R361",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:render film",
              "running": ["other:render film"]
            }
          }
        ],
        "left_out": ""
      },
      "new_names": ["other:render film"]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R372",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:rebuild kurva s files"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": ["other:rebuild kurva s files"]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R404",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:write tts tas assignment content"
            }
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:build tts tas assignment files"
            }
          },
          {
            "type": "may_do",
            "where": {
              "cmd": "run",
              "task": "other:review tts tas assignment"
            }
          },
          {
            "type": "may_do",
            "where": {
              "cmd": "run",
              "task": "other:advise on tts tas assignment"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:write tts tas assignment content",
        "other:build tts tas assignment files",
        "other:review tts tas assignment",
        "other:advise on tts tas assignment"
      ]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R407",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:export rebuilt report pdf"
            },
            "needs": {
              "after": "run",
              "after_task": "other:save report document in word"
            }
          }
        ],
        "left_out": "The vocabulary cannot require the PDF to be exported from the same docx produced by the Word SaveAs step."
      },
      "new_names": [
        "other:export rebuilt report pdf",
        "other:save report document in word"
      ]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R433",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "edit",
              "path": "File terpisah (tidak diunggah)/"
            },
            "needs": {
              "after": "create",
              "after_path": "File terpisah (tidak diunggah)/"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The vocabulary cannot require the earlier created backup to be a copy of the exact file being edited."
      },
      "new_names": []
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R437",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never_hold",
            "where": {
              "path": "**"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R476",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:voice batch",
              "running": ["other:voice batch"]
            },
            "when_unmodeled": true
          }
        ],
        "left_out": ""
      },
      "new_names": ["other:voice batch"]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R479",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:render film",
              "running": ["other:render film"]
            }
          }
        ],
        "left_out": ""
      },
      "new_names": ["other:render film"]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R497",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:run buat_seragam.py"
            },
            "needs": {
              "after": "run",
              "after_task": "other:archive existing same-named buat_seragam outputs"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:run buat_seragam.py",
        "other:archive existing same-named buat_seragam outputs"
      ]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R569",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never_hold",
            "where": {
              "path": "**",
              "has_secret": true
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The vocabulary cannot express the requirement to store the key in a user environment variable."
      },
      "new_names": []
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R580",
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
              "after_task": "other:archive existing same-named build outputs"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": ["other:archive existing same-named build outputs"]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R586",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:run sticker build script"
            },
            "needs": {
              "after": "run",
              "after_task": "other:archive existing sticker versions"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:run sticker build script",
        "other:archive existing sticker versions"
      ]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R590",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:print preview jpg"
            }
          },
          {
            "type": "may_do",
            "where": {
              "cmd": "read",
              "path": "Preview JPG"
            }
          }
        ],
        "left_out": "The vocabulary cannot prohibit every possible non-viewing use of the Preview JPG."
      },
      "new_names": ["other:print preview jpg"]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R594",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never_hold",
            "where": {
              "path": "JARVIS/kuliah/"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R6",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:unggah-sekitar",
              "running": ["other:film session"]
            }
          }
        ],
        "left_out": ""
      },
      "new_names": ["other:unggah-sekitar", "other:film session"]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R611",
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
              "after_task": "other:read reference upload route memory file"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": ""
      },
      "new_names": ["other:read reference upload route memory file"]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R612",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:change windows firewall rules"
            }
          }
        ],
        "left_out": "The vocabulary cannot assign the supplied administrator PowerShell commands specifically to the user."
      },
      "new_names": ["other:change windows firewall rules"]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R633",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "move",
              "path": "GP-100/",
              "kind": "dir"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R646",
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
              "after_task": "other:compare rebuilt and original film sha-256"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": ""
      },
      "new_names": ["other:compare rebuilt and original film sha-256"]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R647",
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
              "after_task": "other:confirm orange rupanya gini channel avatar"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": ""
      },
      "new_names": ["other:confirm orange rupanya gini channel avatar"]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R653",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:schedule tiktok post"
            },
            "needs": {
              "after": "run",
              "after_task": "other:settle every tiktok post detail"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:schedule tiktok post",
        "other:settle every tiktok post detail"
      ]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R67",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never_hold",
            "where": {
              "path": "inspect.py"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R693",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never_hold",
            "where": {
              "path": "**",
              "has_secret": true
            },
            "when_unmodeled": true
          },
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:ask bryan for personal financial figures"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": ""
      },
      "new_names": ["other:ask bryan for personal financial figures"]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R7",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:open social platform to post or schedule film"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": ["other:open social platform to post or schedule film"]
    },
    {
      "folder": "Slicon123__JARVIS",
      "id": "R8",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:pipeline_update upload stage",
              "running": ["other:film session"]
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:pipeline_update upload stage",
        "other:film session"
      ]
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R119",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:autotest audio measurement or verification"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The epistemic statement that silence proves nothing is not an action or repository-state constraint."
      },
      "new_names": ["other:autotest audio measurement or verification"]
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R12",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:run system probe"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The vocabulary cannot express that info() callback implementations must consist only of pure memory access."
      },
      "new_names": ["other:run system probe"]
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R120",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:delete server entity 01"
            },
            "needs": {
              "after": "run",
              "after_task": "other:identify server entity 01 with get clients"
            }
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:start session"
            },
            "needs": {
              "after": "run",
              "after_task": "other:delete server entity 01"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:identify server entity 01 with get clients",
        "other:delete server entity 01",
        "other:start session"
      ]
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R135",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:implement base 15 ssh sftp channel"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": ["other:implement base 15 ssh sftp channel"]
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R137",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:reverse engineer tier5-b1 capabilities advertisement"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": ["other:reverse engineer tier5-b1 capabilities advertisement"]
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R145",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:search for comchan port"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": ["other:search for comchan port"]
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R166",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:migrate webrtc stack to libdatachannel"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": ["other:migrate webrtc stack to libdatachannel"]
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R179",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "test"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R189",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "test"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R193",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "test"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R20",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:debug console"
            },
            "needs": {
              "after": "run",
              "after_task": "other:run shadow native client against same vm"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:debug console",
        "other:run shadow native client against same vm"
      ]
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R214",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:copy libnxbox"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": ["other:copy libnxbox"]
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R217",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "must_do",
            "where": {
              "cmd": "run",
              "task": "other:implement n3 twcc v2 and simplified googcc",
              "after": "run",
              "after_task": "test"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The vocabulary cannot identify the earlier test specifically as the N1+N2 test."
      },
      "new_names": ["other:implement n3 twcc v2 and simplified googcc"]
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R252",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:push switch build"
            },
            "needs": {
              "after": "run",
              "after_task": "restart"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": ["other:push switch build"]
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R259",
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
              "after": "run",
              "after_task": "other:capture desktop plaintext ssl_write"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The vocabulary cannot express that the capture must lock the VST body byte-exact."
      },
      "new_names": ["other:capture desktop plaintext ssl_write"]
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R261",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:implement tier 9 streaming profile trigger"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": ["other:implement tier 9 streaming profile trigger"]
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R27",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:implement sack buffer and retransmit"
            },
            "needs": {
              "after": "run",
              "after_task": "test"
            }
          }
        ],
        "left_out": "The vocabulary cannot identify the earlier test specifically as duplicate-send option 3 or require that its result confirms the packet-loss hypothesis."
      },
      "new_names": ["other:implement sack buffer and retransmit"]
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R302",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:work on shadow port"
            },
            "needs": {
              "after": "run",
              "after_task": "other:validate shadow port environment"
            }
          }
        ],
        "left_out": "The vocabulary cannot separately verify that environment validation included the toolchain, a hello-world build, and nxlink checks."
      },
      "new_names": [
        "other:work on shadow port",
        "other:validate shadow port environment"
      ]
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R314",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:write switch crypto sufp or ctrlchanv2 module"
            },
            "needs": {
              "after": "read",
              "after_path": "ENCRYPTION_AND_FRAMING.md"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The vocabulary cannot require reading the particular section corresponding to the module."
      },
      "new_names": ["other:write switch crypto sufp or ctrlchanv2 module"]
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R320",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "edit",
              "path": "h264_decoder.c"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R321",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "edit",
              "path": "h264_decoder.c"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": ""
      },
      "new_names": []
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R344",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:start spice video stream"
            },
            "needs": {
              "after": "run",
              "after_task": "other:confirm streamer_up true from status"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:start spice video stream",
        "other:confirm streamer_up true from status"
      ]
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R345",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:pivot switch to ngtcp2 quic"
            }
          },
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:port quic stack to switch"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": [
        "other:pivot switch to ngtcp2 quic",
        "other:port quic stack to switch"
      ]
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R35",
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
              "after": "run",
              "after_task": "other:ask for full console reboot"
            },
            "when_unmodeled": true
          },
          {
            "type": "only_if",
            "where": {
              "cmd": "run",
              "task": "other:debug switch code diffs"
            },
            "needs": {
              "after": "run",
              "after_task": "test"
            },
            "when_unmodeled": true
          }
        ],
        "left_out": "The vocabulary cannot require that the prior test is the retest of the same initialization failure, cannot confirm that the requested reboot occurred, and cannot represent the mental act of suspecting a newly linked library."
      },
      "new_names": [
        "other:ask for full console reboot",
        "other:debug switch code diffs"
      ]
    },
    {
      "folder": "Wasabules__Halyard",
      "id": "R361",
      "translation": {
        "status": "ok",
        "clauses": [
          {
            "type": "never",
            "where": {
              "cmd": "run",
              "task": "other:implement quic support for switch"
            }
          }
        ],
        "left_out": ""
      },
      "new_names": ["other:implement quic support for switch"]
    }
  ]
}
```