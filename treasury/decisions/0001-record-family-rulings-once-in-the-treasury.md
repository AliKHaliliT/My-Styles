# 0001. Record family rulings once, in the treasury

Status: Accepted
Date: 2026-08-18

## Context

Rulings that concern the whole family were being recorded as identical
decision records in every style, one body under three numbers. For rulings
that change each style's bytes this is right, because a record explains the
repository it lives in, and a style cloned alone must carry the reasons for
its own visible law. But a rejection changes no bytes, so a per-style copy
of it explains nothing in that repository, and the practice puts one fact in
three homes. Worse, it hides the family's memory. An author drafting a
fourth style, or anyone re-analyzing an old question, would need to dig
through every style's records to learn that the question was already
settled, and the digging cost grows with every style added, which is the
exact failure this repository exists to prevent.

## Options considered

- Keep triplicating. Rejected: three homes for one fact, a discovery path
  that worsens as the family grows, and per-style histories padded with
  events that never touched them.
- A new decisions zone at the repository root. Rejected: it would need its
  own index, reader instruction, and audit, new machinery for one folder,
  while the treasury already owns the read-before-designing rule that
  delivers every future style author to its door.
- A living status matrix of analyzed-and-rejected items. Rejected: a living
  summary of past events is a record wearing a living document's clothes,
  and the STATE discipline already taught how that species rots. Records
  only accumulate.

## Decision

A ruling is recorded where its bytes land. A ruling that changes the styles
keeps the existing form, one record per style, identical bodies held by
review. A ruling that changes no style's bytes, an analysis that adopts
nothing, or a disposition that concerns the family as a whole, is recorded
once, in `treasury/decisions/`, immutable and numbered in its own sequence,
in the same record format the styles write. Discovery rides the existing
law. Whoever designs a new style already reads the treasury end to end, and
now that walk passes the family's refusals as well as its findings.

The owner accepted the one cost by name, that family records do not travel
with a style cloned alone. A style's bytes already incorporate or omit every
outcome, and a project wanting newer reasoning takes the latest style and
refactors.

## Consequences

The skill-file rejection, first recorded as three style records before any
commit, relocates here as the pattern's first resident. Each treasury study
leaves a disposition record in this folder naming what the family adopted
from it, what it refused, and why. The treasury README indexes the folder
and names the species. Style records stay reserved for rulings a reader of
that style can see in its bytes.
