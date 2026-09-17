# 0046. Count the em dash budget in the docs audit

Status: Accepted
Date: 2026-09-17

## Context

The em dash budget, two per tracked file, was counted by a step in the
workflow, and the guide said that CI counts the boundary. A project built
from a template runs the audits, the linter, the type checker, and the tests
in the worker's terminal, because the gate names them as commands, and runs
the workflow only where a remote exists to run it. A project with no remote
has never run the step, and the sentence that says CI counts the boundary is
prose in that tree. The rule was mechanical in form and held nowhere the
worker did not push.

## Evidence

A project built from the host style, read by its history on 2026-09-17, had
no remote, ten files over the budget, one carrying eight em dashes, and
three of them over at its last re-alignment, whose gate the worker ran by
hand. Every count the worker ran held; the one count only the workflow ran
did not. The step needs nothing the audits lack, since it is a count of one
character over the tracked files, and the spelling and vocabulary steps
beside it advise rather than gate and need tools the audits do not carry.

## Options considered

- Requiring a remote. Refused, because whether a project has one is the
  project's, and a rule that depends on it is a rule that holds for some
  projects.
- Keeping the step beside the new check. Refused for the inert workflows,
  because a check has one home and a step that duplicates the audit is a
  second copy of a rule; the family's own root workflow keeps its count,
  since it covers the treasury and the root scripts, which no seat audits.
- Moving the advisory steps too. Refused for now, because they gate nothing
  and one needs a tool the audits do not install; the ruling names them as
  the next candidates if a project shows the same gap there.

## Decision

Every docs audit counts the em dashes in every tracked file that holds no
NUL byte and fails a file over two, naming the file and the count, and the
inert workflow of every seat loses the step, so the count runs wherever the
audit runs, in the terminal and in CI alike. The host's audit leaves the
arrows to their own audits. The guide's bullet and the rulebook's paragraph
now say the docs audit counts the boundary. The plant adds a tracked file
with three em dashes and expects the finding. Under the ladder the rule
keeps the check rung it had and moves the check to the one place a project
always runs.

## Consequences

A project with no remote is held to the budget on its next audit run, and a
project with one loses a redundant step. The audit reads every tracked file
once more per run, a cost measured in milliseconds on the family's seats. The
judgment of whether an em dash beats the comma it replaces stays with review,
as it did.
