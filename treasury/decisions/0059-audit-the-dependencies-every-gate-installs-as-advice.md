# 0059. Audit the dependencies every gate installs, as advice

Status: Accepted
Date: 2026-11-03

## Context

The ruling that disposed of the entries of 2026-11-02 moved the client
style's lint stack after a project built from that style ran a
dependency audit of its own and found a path matcher that could be made
to spin, and it left open whether such an audit joins every seat.
Measured on 2026-11-03 over what each gate installs, the package seat's
declared dependencies and development group, the arrow's, the host's one
spelling tool and the client's lock audited clean, and the server seat's
development requirements carried two published advisories without a fix
release, one on its token library's handling of an asymmetric key in
HMAC verification, which the seat never performs since it verifies with
a shared secret under the one algorithm its settings name, and one on
timing in the ECDSA signing of a library the token library carries as a
fallback, which the seat never calls. Both were dismissed in writing in
the commit that landed the step, which is the shape the advisory tier
exists for.

## Decision

Every seat's workflow carries a dependency-audit step on the advisory
tier, right after its install step and marked continue-on-error as the
credential heuristics are. The package seat and the arrow run `pip-audit
-r` over a list written from the declared dependencies and the
development group, the server seat over its development requirements,
which include the runtime set, the client seat runs `npm audit` over the
lock, and the host runs `pip-audit -r` over the one tool its gate
installs. The tool is fetched by the step and joins no dependency group.
Each guide names the audit among its advisory checks, and a finding is
review's, fixed or dismissed in writing in the commit that passes the
gate. Recorded in the package seat's 0124, mirrored into the arrow's
inherited folder, the server seat's 0128, the client seat's 0119 and the
host seat's 0118.

## What is refused, and what would reopen it

- Gating on the audit. Refused, because its verdict follows the index's
  advisories on the day it runs, so a tree that passed goes red with no
  change to it, and a finding in a path a project never takes is not a
  defect of the tree. It reopens if every seat comes to fix its set by a
  lock and keep its dismissed advisories as a list in the tree, so that
  the verdict becomes a fact of the tree and a finding is answered where
  the tree holds it.
- Leaving the audit to each project. Refused, because a project found
  the hanging matcher in the family's own lint stack before the family
  did, and a check the family wants at every push is the family's to
  carry.
- Auditing the environment after the install step in the Python seats.
  Refused, because the tool's own tree would join the audited set and a
  worker's environment holds more than the project, while the declared
  set is one list in the workflow and at the desk.
- Raising the client audit's level so only the higher findings print.
  Refused, because the tier already carries every finding to review, and
  a filter on severity decides for review what review has not read.

## Consequences

The question the ruling of 2026-11-02 left open is closed. A published
advisory against what a gate installs is named at every push in every
seat and answered in writing, and no tree goes red for the index's day.
