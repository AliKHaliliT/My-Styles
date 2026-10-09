# 0075. Allocate the selftest's claim numbers above the ledger

Status: Accepted
Date: 2026-10-09

## Context

The selftest plants claims to prove each rule, and two of its proofs
demand silence, the legal plants that must raise nothing and the
verified pair whose numbers may appear in no finding. Those plants
took fixed numbers, 0085, 0086, 0088 and 0089, on the assumption that
a young project's ledger never reaches them, which the comment beside
them said. A ledger that does reach them makes the duplicate-number
check fire on a plant, and the two proofs then fail on a tree that
breaks no rule. A maintainer of projects built from three of the
family's styles reported it on 2026-10-08 as an issue, having
reproduced two failures against occupied numbers and none with
numbers allocated at plant time.

## Evidence

Measured on 2026-10-09. The host audit's plants named twenty-three
fixed claim numbers, and the two proofs that read every finding, or
every finding naming their numbers, were the legal plants and the
verified pair; every other plant looks for its own needle, so a
collision adds a finding it does not read. The three docs audits
already allocate their record plants with a free-number helper, and
the host audit carries the same helper for its record plants.

## Options considered

- Allocating every plant's number. Refused for now, because a plant
  that reads its own needle is proven whatever else the collision
  raises, and the deliberately twinned plant must keep sharing one
  number to prove the duplicate check.
- Reserving a band of numbers the ledger may not use. Refused,
  because a rule on a project's own numbering for the selftest's
  convenience is the wrong way round.

## Decision

The legal plants and the verified pair take their claim numbers from
the free-number helper when the proof runs, the lowest numbers from
0900 the ledger does not use, and the verified pair's links, manifest
lines and the number of the claim that must not be current follow the
allocation. The comment beside the legal plants says so.

## Consequences

The selftest proves every rule on a ledger of any size, and a project
whose claims pass 0085 no longer fails two proofs for having claims.
