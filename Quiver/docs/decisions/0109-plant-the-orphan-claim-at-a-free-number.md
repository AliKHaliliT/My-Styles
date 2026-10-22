# 0109. Plant the orphan claim at a free number

Status: Accepted
Date: 2026-10-22

## Context

The selftest planted its orphan claim, a claim no question links, at the
fixed number 0094, among the single-file plants that each expect one
finding. Record 0075 gave the legal plants and the verified pair numbers
allocated at run time and left every other plant fixed, on the reasoning
that a collision could add a duplicate-number finding and never remove
the plant's own. Question membership is keyed by claim number, so a
project whose ledger reached 0094 and linked it from a question gave the
planted orphan that link, and the finding the plant exists to raise
never appeared. A project built from this template met the case at its
re-alignment, with one rule reported as not working.

## Options considered

- Allocate every single-file plant at run time. Refused, because the
  other plants' findings survive a collision, which only adds a finding
  beside them, and the deliberate duplicate-number proof needs its fixed
  pair.
- Renumber the orphan plant higher. Refused, because a ledger grows past
  any fixed number, and the defect would return the day it did.

## Decision

The orphan plant leaves the fixed list and becomes a proof of its own
that takes the lowest free number from nine hundred, as the legal plants
do, writes the claim, expects the finding under that number and removes
the file. Record 0075's reasoning is narrowed to the plants whose
finding a collision cannot inherit; a plant whose finding depends on
what the real tree links to its number is allocated.

## Consequences

The orphan proof holds in a ledger of any size, and a plant whose needle
a collision could silence is allocated from now on.
