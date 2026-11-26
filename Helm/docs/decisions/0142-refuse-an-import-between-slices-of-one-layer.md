# 0142. Refuse an import between slices of one layer

Status: Accepted
Date: 2026-11-26

## Context

The layer rule says that imports point downward and that slices of one
layer never import each other. The lint configuration held the first
half, a pattern per layer refusing the layers above it, beside a pattern
refusing a reach past a slice's door. A project built from this style
reported that an import of one slice's door from another slice of the
same layer, written with the alias, matched neither pattern and passed,
in entities, features and pages alike.

## Evidence

Run on 2026-11-26 at 6a35476. The linter, handed one import under a path
of the probe's own, passed `@/entities/beta` from a file of
`src/entities/alpha`, and the same in features and in pages, while it
refused an import pointing up a layer and one reaching past a door. No
file of the template imports its own layer by the alias, and no suite
asked the configuration anything, so the ledger's claim that imports
point downward rested on patterns nothing had proven.

## Options considered

- Adding each sliced layer to its own list of the layers above it, as
  the reporting project did. Refused in that form, because the refusal
  would read that imports point downward only for an import that points
  sideways, so the same pattern carries a message of its own.
- Resolving each import to a file and comparing slices. Refused, because
  it needs a resolver plugin for a rule the built-in rule states, the
  dependency the style's record on checking the layer rule declined.
- Refusing as well a relative path that climbs into a sibling slice.
  Refused, because a pattern on a specifier cannot tell a climb from a
  slice's own relative import, a limit that record names already.

## Decision

A layer cut into slices, pages, features and entities, names itself in
the configuration, and inside it the alias to the layer is refused whole
with a message of its own, since a slice reaches its own files by
relative path. A suite of the configuration's own hands the linter one
import at a time under a path of the case's own and reads the refusal,
ten cases over the sideways rule in each sliced layer, the upward rule,
the door rule and four imports the rule allows, and the ledger gains the
claim. Nine breaks, each one point, each failed a case, among them each
layer's own entry, the pattern's wiring, and the two older patterns as
controls. A second pattern for the paths under the alias survived its
break, the first pattern covering them, so it was dropped.

## Consequences

A sideways import by the alias fails the lint in every sliced layer, and
the downward rule and the door rule have cases behind them. A project
that imported a slice's own files by the alias from inside that slice
moves those imports to relative paths at its next re-alignment.
