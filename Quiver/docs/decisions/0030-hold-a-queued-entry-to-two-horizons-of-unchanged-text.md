# 0030. Hold a queued entry to two horizons of unchanged text

Status: Accepted
Date: 2026-09-10

## Context

A project built from the family reported that its STATE queue had reached
eleven entries while Now held one, every entry legal: one line, dated inside
its horizon, re-dated on schedule, and none of them ever done. Record 0018
had weighed caps of three, five, and ten for Now and said nothing about Next,
and the horizon bounds abandonment rather than standing still, so a queue can
hold thirty items indefinitely with the audit green throughout. The remedy the
rulebook already carried for an entry that will not move, that a Deferred or
Blocked entry re-affirmed across several horizons is a decision record trying
to be born, was written for those two sections, was prose only, and had never
reached the host style's rulebook at all. A cap on Next would have made the
wrong argument, since the failure is an entry that never moves rather than a
section that is long, and the file cannot show which entries have moved,
because a date is the entry's last-verified stamp and not its birthday.

## Decision

An entry in Next, Deferred, or Blocked whose text has stood unchanged, its
date aside, for two horizons is a decision record trying to be born, so it is
promoted to Now, written as a record and removed, or dropped. The docs audit
reads the entry's age from history, from the first commit that carried the
entry's text, and fails it past two horizons the way it fails an entry past
one. The check reads history, so it binds from the arrival of its own scope
sentence like every such check, and no entry's age is counted from before
that arrival; an adopting project's oldest queue item gets two horizons from
adoption, never an instant verdict over a past that was legal. Rewording an
entry resets its clock, and review sees rewording. The rulebooks of all four
styles carry the sentence, the host's for the first time.

## Options considered

- A cap on Next was refused. Ten never fires and five refuses a legitimate
  queue, which is the argument 0018 already made about Now, and a long queue
  of moving items is not the disease.
- Extending the prose remedy alone was refused, because the reporting
  project had the prose for two sections and a person, not a rule, noticed
  the file; where the fact is decidable the family holds it.
- A birthday stamp beside the verified date was refused, because it would
  put in the file a fact history already holds and invite the two to
  disagree.

## Consequences

A queue tells a reader what is queued, because anything that has stood there
for half a year has become a decision record or has gone. The remedy for a
deferred or blocked item is now the same rule with the same teeth.
