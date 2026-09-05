# Tie-breaking in monetary rounding

Date: 2026-09-05

## Slice

First pass over the tie-breaking line of the question, the choice between
round half up and round half even when many monetary amounts are rounded to
whole cents and summed.

## Boundary

The three works the question already cites, read in full for what they say
about ties and accumulated rounding error: the IEEE floating-point standard
in its 2019 edition, Goldberg's 1991 survey of floating-point arithmetic, and
Fowler's 2002 enterprise-patterns treatment of money as a type. No database,
venue, or catalog was searched, and no date range beyond the three works
applies.
Completeness: judgment

## Method

A scoping read of a known corpus, the works in hand read against the slice's
question rather than searched for; named from the field's vocabulary as a
scoping review confined to a seed set, with no snowballing.

## Stages

- Scouting: collapsed, the question's decomposition already names the slice and the works it rests on.
- Enumeration: ran, one passage per work, the standard's stated reason for ties-to-even, the survey's account of error compounding in accumulation, and the pattern book's case for money as a first-class type.
- Checks: ran, every key resolves and every work is entered with its edition.
- Completeness review: collapsed, no completeness is claimed and a search beyond the seed set would extend this pass.
- Fold: collapsed, the ledger did not move.
- Resolution: collapsed, the three works do not disagree on the slice.

## Found

[ieee754-2019], [goldberg1991], and [fowler2002], all already entered.

## Changed

Nothing in the ledger. The pass confirms the framing the question carries,
that the two rules differ only on halfway amounts and that the standard
prefers ties-to-even for freedom from bias in long computations, which the
settled claims already test.

## Left out

Every database and venue, so a numerical-analysis or accounting literature
on tie handling at ledger scale may exist unread. The real-price-distribution
line of the question stays open, and a pass bounded to it would start where
this one stopped.

Cost: one session, with no separate token accounting.
