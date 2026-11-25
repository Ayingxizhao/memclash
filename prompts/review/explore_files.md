You are one of two independent readers in a class research project. Work read-only: do not
edit, create or delete any file, and do not call any paid API. Your final message is saved as
your report. You will never see the other reader's work.

## Background

Coding agents keep a memory folder of markdown instructions written on different days. Two
instructions **clash** if, in some situation both talk about, no single action satisfies both.
An explicit "you may X" counts: X must stay possible. A pair is **settled** if the text itself
says which one wins (an explicit exception, "this overrides ...", or a later decision recorded
in the folder).

We want to know whether instructions about **files** are common and whether they clash. A file
instruction says that some actor may / must / must not do one of these to some path or kind of
file, possibly only under a condition:
- read, create, edit, delete (move or rename counts as edit)
- commit to git, keep out of git (gitignore), push or publish
- condition examples: only with the user's approval, only by a certain agent, not while X runs

## Folders

Read every `.md` file in each folder listed in the file named below (paths are relative to the
repo root `/Users/yingxizhao/dev/cs2520/projects`). For a folder over about 30,000 words, read
every feedback/rule-like file fully and skim the rest; say which files you skimmed. Do not open
any other folder, never open `data/gold/` or any file named `labels_*`.

## Output: one JSON object (no prose around it)

{
  "reader": "<your name>",
  "folders": [
    {
      "folder": "<owner__repo>",
      "words_read": "full | skimmed: <files>",
      "n_instructions_estimate": <int, rough count of distinct instructions in the folder>,
      "file_instructions": [
        {"file": "<path>", "quote": "<verbatim, short>", "action": "read|create|edit|delete|commit|ignore|push",
         "force": "must|never|may|only_if", "target": "<path pattern or kind of file, as written>",
         "target_is_path": true|false, "condition": "<as written, or empty>"}
      ],
      "clashes": [
        {"a_file": "...", "a_quote": "...", "b_file": "...", "b_quote": "...",
         "topic": "files|git|ask-before-acting|output-format|tools|other",
         "situation": "<the case where no single action satisfies both>",
         "status": "clash|settled", "confidence": "sure|unsure", "why": "<one sentence>"}
      ],
      "other_topics": ["<short names of the main non-file topics in this folder>"]
    }
  ],
  "notes": "<anything a reviewer should know; what you were unsure about>"
}

Rules for the output:
- Report clashes on ANY topic, not only files, but give `topic` honestly.
- Quotes must be verbatim. If you are unsure of a fact, say so in `why` or `notes`.
- Be systematic: within each folder, group the instructions by topic, then check pairs within
  each topic. Do not stop at the first clash.
