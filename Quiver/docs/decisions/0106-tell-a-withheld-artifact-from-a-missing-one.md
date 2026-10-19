# 0106. Tell a withheld artifact from a missing one

Status: Accepted
Date: 2026-10-19

## Context

Record 0025 made the existence of an artifact a `Recorded:` line names a
verdict, because existence is decidable, and record 0086 held a pass
record's exports the same way. Both assumed every artifact tracked. The
audit tested the working directory, so an artifact that merely lay on
the machine that made it passed there and failed in every other
checkout, and its pass implied a tree that held what it did not. A
project built from this template met the case when its preserved run
reports turned out to carry a substantial share of a licensed dataset
whose terms forbid redistributing it. The owner stopped tracking the
reports and kept them where they lay, under a path the ignore file
names, while the claims quote every result in full and name the reports
on lines that admit no edit.

## Options considered

- Keep existence as the verdict. Refused, because a verdict that changes
  with the machine is not one, and the claims that name a withheld
  artifact cannot be edited to say otherwise.
- Supersede the claims to drop the paths. Refused, because supersession
  is reserved for a change of figures, evidence or belief, and nothing
  changed but custody.
- A new word on the `Recorded:` line marking an artifact withheld.
  Refused, because the line is immutable where the case arises, and the
  ignore file is a living file the owner already writes.

## Decision

The verdict on a recorded artifact is whether the tree holds it, asked
of the index and never of the disk, so an artifact never added fails in
every checkout alike. An artifact the ignore file names is withheld by
declaration and is no verdict either way; the audit names it on every
run as a check not run, with whether it lies on that machine, since no
checkout can vouch for what the tree does not hold. A withheld path
counts as named even where its folder is absent, so a line naming only
withheld artifacts never reads as naming nothing. The rule binds a
claim's line and a pass record's Boundary alike, the selftest plants a
withheld artifact present, absent and never added, and the claims rule,
the review rule and the freshness bullet say so.

## Consequences

A project may keep a preserved artifact it is not allowed to publish,
its claims stand unedited, and every checkout reads the same line about
it. A pass over a licensed index can keep its exports the same way.
