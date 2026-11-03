# 0128. Audit the dependencies the gate installs as an advisory

Status: Accepted
Date: 2026-11-03

## Context

A project built from the client style ran a dependency audit of its own
and found, in the lint stack the style ships, a path matcher that could
be made to spin, before the family had looked, and the ruling that moved
the lint stack left open whether such an audit joins every seat. Every
gate of the family installs a resolved set on each run, and none asked
the index whether an advisory had been published against what it
installed. A published advisory is a fact about the day and not about
the tree. On the day this landed the server seat's set carried two
without a fix release, both in paths that seat never takes, which is the
shape a gate cannot judge and review can.

## Options considered

- Gate on the audit. Refused, because its verdict follows the index's
  advisories on the day it runs, so a tree that passed goes red with no
  change to it, and a finding in a path the project never takes is not a
  defect of the tree, which is what a gate judges.
- Leave the audit to each project. Refused, because a project found the
  hanging matcher in the family's own lint stack before the family did,
  and a check the family wants at every push is the family's to carry.
- Audit the environment after the install step. Refused, because the
  tool's own tree would join the audited set and a worker's environment
  holds more than the project, while the requirement files are one list
  in the workflow and at the desk.

## Decision

Every seat's workflow carries a dependency-audit step on the advisory
tier, right after the install step and marked continue-on-error as the
credential heuristics are, and a worker runs the same audit at the desk
as the guide names it. The tool is fetched by the step and joins no
dependency group.

Here the step runs `pip-audit -r requirements-dev.txt`, which resolves
the development requirements and the runtime set they include as the
install step does and reads the resolved set against the index. The
package seat audits its declared dependencies and development group the
same way, the client seat runs `npm audit` over the lock, and the host
audits the one tool its gate installs.

The guide names the audit among the advisory checks, and a finding is
review's, fixed or dismissed in writing in the commit that passes the
gate, as every advisory is.

## Consequences

A published advisory against what the gate installs is named at every
push and answered in writing, a tree never goes red for the index's day,
and a project that copies the workflow inherits the step with the tier
that bounds it.
