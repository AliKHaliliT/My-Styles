# 0002. Adopt thirty-six primitives and refuse six

Status: Accepted
Date: 2026-08-18

## Context

Study 0001 reduced 14,765 named software engineering concepts to 125
primitive operations, and the owner asked which of them are general enough
to hold in every style regardless of terrain. This record preserves that
disposition, which predates the treasury's decisions folder and until now
lived only in per-style records for its adopted half. The analysis found
36 of the 125 general: 21 that a machine can impose and 15 that need
judgment. The remaining 89 split into 83 terrain-dependent options, which
are what the treasury's findings exist to hold, and 6 the family refuses
outright.

## The adopted halves

The 21 machine-imposed primitives are the styles' toolchain law, and nearly
all were already wired when the analysis ran: encapsulation as door-only
exports, cohesion as folder purity, layering as import contracts,
indirection as boundary homes for environment and wire, convention as the
prose bans, static analysis, type safety, testing through the five verbs,
point-of-use information as docstring presence, the documentation horizon
and budgets, traceability as resolving links, differential checking of
document claims against the tree, read-model consistency as index
completeness, the record and naming schemas, waste as dead-code detection,
input validation behind the schema door, and checksum, replication with
drift detection, and single source of truth, the last three served together
by the pinned rulebook.

The 15 judgment primitives became the delivery gate's core items, weighed
against every change from the first line written: cognitive load,
granularity, ubiquitous language, intent-split placement, decision records,
debt, waste, two hats, change shape, the feedback gate, least privilege and
surface, boundary honesty, loud failure, single source of truth, and test
honesty. The gate items in each style's agent guide are the single source
of truth for this half, and the per-style records titled "Gate delivery on
the general primitives" hold the adoption's rationale where its bytes
landed.

## The six refusals

- Coverage thresholds. The moment a coverage number becomes a target, tests
  get written to touch lines rather than to verify claims. The family
  checks the frame, suites mirroring source and substitution only at seams,
  and leaves breadth free.
- Velocity-style metrics. A one-owner family with machine gates has nothing
  for such numbers to steer, so they would only invite optimizing the
  number.
- Publish and subscribe. Present once in a derived project as an observer
  channel with zero subscribers, purged as dead code. Speculative event
  machinery is waste until a second listener exists.
- Ratcheting, applying a new rule only to touched code. Every new rule is
  applied wholesale in one wave instead, because two coexisting standards
  is drift by another name and the family's doctrine is anti-drift.
- Decentralization. Deliberately inverted: upstream-first is centralization
  by design, the style being the single authority, and letting each child
  decide where information sits is the exact failure the family exists to
  prevent.
- Semantic versioning's signaling. Styles are not products, so a version
  carrying compatibility promises would be a false signal; identity is the
  rulebook hash, which says exactly which text you have.

The common thread: five of the six refuse a proxy or a gradual mechanism in
favor of a direct one, and the sixth refuses speculation. None are bad
primitives; each carries a price that lands exactly where a one-owner,
machine-checked template family is weakest.

## Consequences

The general subset needs no per-project thought and every other primitive
does, which is why the findings list prices instead of prescriptions. The
refusals are context-bound rulings, not verdicts. A team, real production
traffic, or a genuinely published package reopens the one whose condition
it meets.
