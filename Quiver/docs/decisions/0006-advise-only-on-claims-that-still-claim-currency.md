# 0006. Advise only on claims that still claim currency

Status: Accepted
Date: 2026-08-28

## Context

The stale-pin scan read every claim's pins without reading its Status line, so
a claim already flipped Stale, or superseded by a re-run, kept drawing the
same advisory forever, telling a person to flip what was already flipped. The
advisory's whole purpose is to prompt a decision, and it was prompting for
decisions already made, which is the shape of noise that trains readers to
skip advisories altogether. The wart surfaced when the owner asked what the
standing advisory on the demo's two settled claims actually obliged, and the
answer exposed that neither confirming nor flipping could ever quiet it.

## Decision

The movement advisory fires only for claims still standing as current. A claim
whose status is Stale or Superseded has already said it is not backed by the
present tree, so its pins are history and the scan leaves them in peace. Pin
validity stays gated for every claim regardless of status, because a record's
evidence never gets to point at a commit that does not exist.

The selftest gains three planted claims sharing one genuinely moved pin, drawn
from the repository's own history. The Supported plant must raise the
advisory, and the Stale and Superseded plants must not, so both directions of
the rule are proven to fire and to rest. When a history holds no arrow
movement, the plants are skipped with a printed reason rather than faked.

The rule change was made under the pause-and-propose clause, proposed with the
wart and approved by the owner's delegation.

## Consequences

Flipping a claim Stale now actually settles its advisory, and superseding a
claim with a re-run at a new pin settles it too, so both remedies the advisory
offers now work as remedies. Supported and Refuted claims keep advising when
their arrow moves, which is correct, since they are the ones still asserting
something about the present.

The demo ledger's two standing advisories on claims 0002 and 0003 are now
settleable the lawful way, by superseding claims that re-run the experiment at
a fresh pin, which the next change carries.
