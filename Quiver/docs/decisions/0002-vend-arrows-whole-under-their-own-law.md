# 0002. Vend arrows whole under their own law

Status: Accepted
Date: 2026-08-27

## Context

An inquiry that builds anything needs code, and the family already has styles
that know how to build. The question was how a research project carries them.
The options ranged from copying fragments of a style into the inquiry to
referencing external repositories.

The family's own repository is the living precedent. My-Styles hosts three
complete styles plus a research layer above them, with a thin shared law, and
that arrangement has held because each style's law binds its own tree and
nothing reaches across.

## Options considered

- Fragments of a style, trimmed to what the inquiry needs. Rejected because a
  fragment obeys no gate, and code that produces evidence is exactly the code
  that must be held to a law.
- Git submodules or external repositories. Rejected because a claim must pin
  the state that produced its evidence, and a second history makes a pin a
  pair of coordinates that can drift apart. Vendored trees give one history,
  so a pin is one hash and staleness is one git command.
- Quiver rules reaching into arrows, for consistency's sake. Rejected as the
  jurisdiction mistake the family has already refused twice; a rule binds only
  where its own text claims to bind.

## Decision

An arrow is a complete instance of an artifact style, vendored whole under
`arrows/<name>/`, governed entirely by its own style, gate, and conventions.
Quiver's law binds the inquiry layer only. The interface is one living
manifest per arrow at `docs/arrows/<name>.md`, naming the style, the part of
the question served, and the claims resting on the arrow. A pin is the host
commit whose tree produced the evidence, and an arrow has moved when any later
commit touches its path.

A demo arrow may be deliberately incomplete in ways its own README names, the
family's standing pattern for demonstrations, and an incompleteness that is
not named is a defect.

## Consequences

Adding an arrow costs a directory and a manifest. Removing one orphans its
claims visibly, because their pins still name its path. The seat can host
arrows that are not code, since nothing in the manifest or the pin assumes a
language, only a path in the tree.

The shared family law that Quiver replicates in its guide, the checking rules,
the prose law, the public-byte rule, is guarded byte-identically by the
family audit only where anchored blocks exist, today the upstream report;
the delivery gate is deliberately Quiver's own and is not under that guard.
