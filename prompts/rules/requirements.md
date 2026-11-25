Split ONE rule from a coding agent's memory folder into its single requirements. You get the
rule and the name of the file it came from. Do not translate anything yet. Answer by calling
the tool `list_requirements`.

- A requirement is one thing the rule asks for, forbids or permits, with its condition if it
  has one. "Delete it locally and on the remote" is two requirements. "Before X, do Y" is one.
- `quote`: copy the words of the rule that state the requirement, exactly as written (a piece
  of the rule; you may skip words between requirements, never change them).
- Every part of the rule that asks for, forbids or permits something must be in some
  requirement. A reason ("because ...", "so that ...") is not a requirement.
- `applies_when`: copy the words of the rule that limit when or to what this requirement
  applies (its trigger or scope, e.g. "for non-code changes", "after a merge"), even when
  they sit in the part of the sentence quoted for another requirement; `""` if nothing limits
  it.
- `keep`:
  - `translate`: about git, files, or running a task, including a requirement that limits
    when such an action may happen or what must come before it (only with the user's
    approval, only after tests pass, confirm the files before a push);
  - `vague`: asks for nothing concrete ("keep things tidy");
  - `outside_vocabulary`: concrete, but neither an action on git, files or tasks nor a limit
    on one (code style, which tool to use).
- A prerequisite or order ("before a push, confirm with the user") stays part of its
  requirement; putting "before push" in `applies_when` does not make the requirement
  `outside_vocabulary`.
- `status`: `not_in_scope` if no requirement is `translate`; otherwise `ok`.
- `why`: one short line, only for `vague` and `outside_vocabulary`.
