# 0081. Overlap a pass with the pass it extends

Status: Accepted
Date: 2026-10-15

## Context

A later pass over a slice extended the last one from the date it
stopped, so the two met exactly. An index enters a work after its date,
by days for some and by months for others, so a work dated before the
first pass's day and entered after it is returned by neither pass, and
the chain of records over the slice carries a gap nobody can see. A
review method the owner keeps outside the family re-runs an update
from one month before the last search date for this reason.

## Options considered

- A fixed overlap of one month. Refused, because the lag is the
  index's and differs between them, so the rule names the mechanism and
  the pass names the figure it chose.
- No overlap, the chain meeting exactly. Refused, because the gap is
  real and silent, which is the one kind of gap the records exist to
  prevent.
- Holding the overlap's size in the audit. Refused, because the size is
  a judgment about an index the audit cannot see; the audit holds that
  an overlap exists and review weighs it.

## Decision

The Slice of an extending pass names the date it extends from, written
as `from YYYY-MM-DD` and set before the day the prior pass ran by the
lag of the index it searches. The audit holds, on every pass added from
the rule's arrival, that an extending pass names the date and that the
date stands before the prior pass's Date line; the size of the overlap
stays with review. The rule took the form of a check over the record's
shape, because a date is decidable and a lag is not.

## Consequences

A slice's chain of passes covers its dates without a gap, at the price
of re-examining the few works the overlap returns twice. The three
passes in the tree are first passes and stand as written.
