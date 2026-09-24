# 0041. Dispose of the upstream entry of 2026-09-24 on the spelling advisory's ignore list

Status: Accepted
Date: 2026-09-24

## Context

Three projects built from the client style, re-aligned at 66ba9f5 with
their six earlier entries deleted, each reported the same defect. The
spelling advisory's ignore list is a constant in the docs audit, a
style-owned script a project carries byte for byte, so a project has no
list it may write to, and a real term of its domain prints on every run of
every change with nothing to answer it but the same dismissal in every
commit message. The reports were tested against the template's tree. The
record that brought the check had promised a project its own list in its
own workflow, and the record that moved the check into the audit took the
list into the script without saying so. The constant's two words were the
client style's test hook and a word of the audits' own banned-vocabulary
list, pardoned so the audit would not report its own script.

## Decision

Kept. A project's terms live in `.codespellignore` at its root, one word
per line, present only when a real term exists and never recopied at
re-alignment, and every docs audit passes the file to codespell when it
exists. The client style ships its one term, and every audit skips its own script
as quoting ground instead of pardoning a word everywhere. The baselines, the rulebooks
and the guides name the file, the selftests prove a named term is silent,
and the family's own root workflow reads whatever seat files exist in place
of its hard-coded pair. The records are the package seat's 0082, the server
seat's 0079, the client seat's 0083 and the host seat's 0059.

## Consequences

The three projects delete the entry at their next re-alignment, write their
terms into the file, and their advisories fall silent about them. A shared
dictionary stays refused, since a term of one domain is noise in another.
