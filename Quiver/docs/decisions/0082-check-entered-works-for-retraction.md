# 0082. Check entered works for retraction

Status: Accepted
Date: 2026-10-15

## Context

A bibliography entry closes with its source's standing, reviewed, a
preprint with the day it was last checked for a published version, or
grey in one of three tiers, and the standing advisory names a
Supported claim resting below the declared floor. A publisher's
withdrawal of a work changed nothing in the tree. A reviewed work
stayed reviewed, the claim resting on it stayed Supported, and no
check asked, because the one standing that falls after entry had no
word. A review method the owner keeps outside the family checks every
reference for retraction in each verification pass, against the
registry the publishers feed.

## Options considered

- A checked date on every reviewed entry, re-asked each season like a
  preprint's. Refused, because most works are never withdrawn and a
  date that moves for nothing teaches that the move means nothing.
- A network check in the audit. Refused, because the audit decides
  from the tree and the calendar alone, and a check that fails with the
  network is a check that fails for the wrong reason.
- Silence until a reader notices. Refused, because that is the status
  quo and the claim stands Supported until then.

## Decision

A fourth standing, `Source: retracted, noticed YYYY-MM-DD.`, marks a
work its publisher has withdrawn, with the day the inquiry noticed; the
entry stays and the standing is rewritten in place. The standing
advisory names every Supported claim whose evidence cites a retracted
key, floor or none, until the claim's Threats cite the key or a new
claim supersedes it, and a retracted work ranks below every floor and
may not be one. The Checks line of a pass answers for retraction, none
retracted or the key and the day, on every pass added from the rule's
arrival; the audit holds that the line answers and review holds that
the answer is true. The rule took the form of a standing and an
advisory, because whether a withdrawn work still carries a claim is the
inquiry's to decide and the tree's to show.

## Consequences

A withdrawal has a word in the tree and a claim resting on it cannot
stay green by silence. The three passes in the tree stand without the
answer, since a record admits no edit.
