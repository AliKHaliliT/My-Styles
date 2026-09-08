# 0024. Re-verify a claim in its arrow's manifest and supersede only when something changes

Status: Accepted
Date: 2026-09-08

## Context

A project built from this template reported that one pair of its claims had
been rewritten five times in four days and had produced identical figures at
each of the first four pins, so that fourteen of its twenty-three claims were
superseded and the supersession chain recorded the arrow's commit history
rather than any change of belief. The law left a moved arrow exactly two
answers, flip the claim Stale or supersede it, and the advisory's "confirm
the claim" had no written form other than a full new record. The demo ledger
shows the same thing: seven of its nine claims are superseded, and the
current one says in its own first paragraph that it re-pins its predecessor
after work that touched no arithmetic and that the claim is unchanged.

## Decision

Supersession is reserved for a change of figures, of evidence, or of belief,
the same line decision records already draw. A moved arrow whose reproduction
prints the same figures is answered by one line in the arrow's living
manifest, `NNNN at <commit-hash>` under a Verified field, the latest standing
for each claim. The audit advises only when the evidence paths moved past the
latest verification rather than past the claim's pin, holds that a
verification names a commit this history holds, no older than the claim's
pin, and a claim that is current on this arrow, and the claim keeps the pin
that produced its quoted figures, so reproducibility is untouched. The gate's
pin item names the three answers. The demo arrow's manifest carries its first
verification, made by running the reproduce command at the recorded commit
and reading the same figures.

## Options considered

- A verification line appended inside the claim was refused. The Status
  line is the record's only legal edit, the audit holds that byte by byte,
  and the family re-anchored that rule days ago.
- The audit re-running the experiment to learn whether the figures moved was
  refused, because an audit never runs experiments, and a check that spends
  time or money to decide its question is the wrong kind of check.
- Leaving the law as it stood was refused, because a ledger that records
  commits instead of knowledge fails the one reader it exists for.

## Consequences

A ledger's supersessions mean something again. The manifest, which already
names the claims resting on an arrow, now also says at which commit each was
last seen to reproduce, which is a present-state fact and belongs in a living
document. The nine demo claims stay as they are, since records are immutable
and the history they record is real.
