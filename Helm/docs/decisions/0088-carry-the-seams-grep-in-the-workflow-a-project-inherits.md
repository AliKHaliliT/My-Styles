# 0088. Carry the seams grep in the workflow a project inherits

Status: Accepted
Date: 2026-10-05

## Context

The testing rule replaces a collaborator only at a declared seam and never
by patching a module's internals, and record 0020 moved the ban from
review into a check, a grep over each style's suites that fails the build
when it matches. That grep runs in the family workflow at the root of the
style repository, and in the host style's job for an arrow. The workflow
this template carries in its own tree, the one a project copies at
adoption, never had the step, so in every derived project the ban stayed
the review that record 0020 had named the weaker form. A project built
from the host style reported it on 2026-10-03, having needed a holder in
its own tree for the ledger claim that no suite patches a module and
found none.

## Evidence

Measured on 2026-10-05 in the family's history. The grep entered the root
workflow with record 0020 and the host's arrow job when the host style
settled the arrow form, and no commit ever added it to the workflow of
this template or of the package and server seats. The root workflow runs it over
this template's suites on every push, which is why the gap never showed
here.

## Options considered

- Leaving the step in the family workflow alone. Refused, because a
  derived project does not run the family workflow, and a rule lands in
  the strongest form its mistake allows in every tree that carries it.
- Writing the ban into the invariants ledger with review as its holder.
  Refused, since a check that exists is the holder, and a row of review
  for a claim a grep decides hides a green behind a verdict nobody gave.

## Decision

The workflow in this tree runs the Seams step after the docs audit, the
same grep over `tests` the family workflow runs for this style, failing
with the same message, and the invariants ledger gains the row that no
suite replaces a collaborator by patching a module's internals, held by
that step at the rung impossible. The package and server seats take the same step
with their own patterns.

## Consequences

A project copies the check with the workflow and has the holder its
ledger needs on the day it adopts. The family workflow keeps its own copy
of the step, so this template's suites are read twice, once here and once
at the root, which costs a second of a run and nothing else.
