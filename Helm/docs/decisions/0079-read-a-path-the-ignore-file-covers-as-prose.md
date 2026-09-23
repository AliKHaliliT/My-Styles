# 0079. Read a path the ignore file covers as prose

Status: Accepted
Date: 2026-09-23

## Context

The docs audit holds every backticked path a living document names to the
tree, reading a token whose first segment the root does not know as prose.
The rule looked at the disk. A folder that exists on one machine and not on
another, untracked and ignored, decided whether a token was judged, so the
baseline's sentence naming the harness's working-tree folder failed on a
machine where the harness had made its settings folder and passed everywhere
else, the build included. In the Python seats the same rule stripped the characters
dot and slash one by one from the front of a token, so a dot-rooted path lost
its dot, its first segment was never found at the root, and nothing under
`.github/` or any other dot folder was ever judged.

## Evidence

A project built from this style reported the first defect at a0db0a4 with the
words the audit printed, "which does not exist", present with the folder and
absent without it. It was reproduced on 2026-09-23 in the client seat with an
empty settings folder. The package seat did not reproduce it, and reading its
rule found the second defect, which is why: the dot was gone before the first
segment was looked up. A ghost under `.github/` passed every Python audit
that day and still passes nothing in this one.

## Options considered

- Judging tokens against the tracked tree instead of the disk. Refused,
  because a file a writer has created and named but not yet added would go
  red until the add, and the audit runs on working trees on purpose.
- Renaming the folder in the baseline sentence to a token the audit reads as
  prose, which is what the project did to land. Refused, since it hides a
  defect behind a wording and leaves the rule machine-dependent.
- Dropping the ignore file's entry for the harness folder. Refused, because
  the entry is what the record that added it exists for.

## Decision

A token the ignore file covers is read as prose, asked of git with the
token's trailing slash kept so a directory pattern answers, because an
ignored path is by declaration not part of the tree and a living document
naming one claims nothing the tree can be held to. The client audit already stripped only a leading `./`, and the Python seats' audits now do the same, so a dot-rooted path is judged like any other. The rulebook's
sentence gains the clause. The selftest plants a ghost under `.github/` that
must fire and names an ignored folder under a settings folder made for the
run, which must not. Under the ladder the rule keeps its check rung.

## Consequences

The audit's verdict on a backticked path no longer depends on what an
untracked folder on the machine happens to be. Paths under dot folders are
held from this commit on, and nothing in history is re-judged, since the
freshness rule reads the working tree only.
