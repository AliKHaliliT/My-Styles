# 0090. Pin every action a workflow uses to a commit

Status: Accepted
Date: 2026-10-06

## Context

Record 0017 pinned every action the family workflow uses by commit
digest, because the rulebook is pinned by hash since a name can move, and
an action tag is a name that moves. The workflow this template carries
in its own tree, the one a project copies at adoption, kept its tags,
and no check anywhere read a workflow for its pins, so the promise a
child inherited was the one that record had refused. The gap showed on
2026-10-06 while three checks from another project's gate were being
measured against this family, none of which held this rule either.

## Evidence

Measured on 2026-10-06 over the six workflows in the family. The root's
seventeen references name a commit with the version beside it. The five
seat workflows carry twelve references by tag, two in each artifact seat
and the arrow and four in the host's. The tag form entered this seat's
workflow a week before the root was pinned and was never revisited. No
audit read a workflow for anything but the paths prose names.

## Options considered

- Pinning the twelve and leaving the rule to review. Refused, because
  that is the state that drifted, and the next workflow a seat gains
  would start from a tag again.
- A workflow linter from outside. Refused, since the one measured holds
  no pin rule, found nothing else in the six files, and the client seat
  could not carry a current build of it locally.
- Holding the pins in the family audit alone. Refused, because a project
  copies the seat's audit and never the family's.

## Decision

Every action a workflow uses from another repository is pinned to the
commit it runs, forty hex characters with its version named in a comment
beside it, and the docs audit refuses a tag or a bare commit in any
workflow of the tree. The twelve references take the digests the root
already carries. The guide's hard rules state the rule, the selftest
plants a tag and a pin without its version, and the family audit holds
the root's own workflow to the same rule.

## Consequences

A project inherits pinned actions and a check that keeps them so. Moving
an action to a new release means changing a commit and its comment
together, in a change that says why, which is what a pin is for.
