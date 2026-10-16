# 0085. Name the nearest review in a pass's boundary

Status: Accepted
Date: 2026-10-15

## Context

Scouting walked the field's catalogs and review papers to see where a
slice's literature lived, and what it found of the reviews themselves
went nowhere in the record. A pass could repeat a review that already
covered its slice over a recent window and nothing in its shape would
show it, and the reviews it had found, whose reference lists are the
best start for a snowball and the best published list for a
completeness review, were kept in the writer's memory. A review method
the owner keeps outside the family runs an existing-reviews check
before the protocol and closes it with a delta statement, what the
planned review adds to the nearest one.

## Options considered

- A separate record of the reviews found. Refused, because the
  bibliography already enters them with their standing, and a second
  list beside it would rot.
- Leaving the delta to the Method section's prose. Refused, because a
  sentence that may be anywhere is a sentence a reader cannot check
  for, and the audit cannot hold what it cannot find.
- Requiring the line only when a review exists. Refused, because a
  pass that found none must say it found none, or the line's absence
  cannot be told from a pass that never looked.

## Decision

The Boundary of a pass carries a nearest-review line. It names, by
key, the review, survey or mapping study that already covers most of
the slice, with the window it covered and what this pass adds, or it
says that none was found in the indexes searched. Scouting looks for
the reviews before the criteria are written and keeps them aside to
seed the snowball and the completeness review. The audit holds the
line's presence and its shape, a key or the words none found, on every
pass added from the rule's arrival; whether the review named is the
nearest stays with review. The rule took the form of a check over the
record's shape, because nearness is a judgment and absence is not.

## Consequences

A pass that would repeat a standing review says so in its own
Boundary before it runs, and the reviews a slice already has are
entered where the next pass finds them. The three passes in the tree
stand without the line, since a record admits no edit.
