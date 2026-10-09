# 0095. Pick a tracked record for the immutability plant

Status: Accepted
Date: 2026-10-09

## Context

The selftest proves the immutability rule by editing the body of an
accepted record and expecting the audit to refuse the edit. It picked
the first record whose status line sat between bare line feeds, read
as bytes, so in a checkout that keeps carriage returns, as this seat's
attributes file gives a Windows checkout, no tracked record matched
and the first match was whatever record a script had just written
with bare line feeds, an untracked file the audit's diff cannot see.
The proof then failed on a tree that broke no rule, or skipped on a
tree with no such record and proved nothing, while the bullet plant
beside it already read either line ending.

## Evidence

Measured on 2026-10-09 in a fresh worktree of the family on Windows.
Every tracked record carried carriage returns, a new record written
by a script did not, and the proof chose the new record and reported
that a body edit raised nothing. The same selftest passes on the
family's Linux runner, whose checkout has bare line feeds throughout,
and in this seat's working copy, where records written by earlier
scripts still carry the line feeds they were written with.

## Options considered

- Normalising line endings in the proof's read. Refused as the whole
  answer, because an untracked record would still be chosen wherever
  it sorted first, and an untracked record has no diff to refuse.
- Leaving the proof to Linux. Refused, because a proof that passes
  only where it is not run by hand is a proof nobody reads.

## Decision

The immutability plant and the bullet plant choose among the records
git tracks, read with either line ending, so the record edited is one
the audit's diff can see whatever the checkout's endings are. The
plant's skip, where no tracked accepted record exists, keeps its
printed reason.

## Consequences

The selftest proves the immutability rule on a Windows checkout as it
does on the runner, and a record a script has just written can no
longer be mistaken for the one to edit.
