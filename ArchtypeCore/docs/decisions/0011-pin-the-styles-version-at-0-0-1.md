# 0011. Pin the style's version at 0.0.1

Status: Accepted
Date: 2026-08-10

## Context

A style is not a product. Nobody upgrades through releases of a template; a derived project copies the shape once and versions itself. Yet the family's version fields told product stories. This template carried no package version, but its demo API announced version 1.0.0 on its documentation page from a settings default, which is instance metadata pretending to be a claim about the style.

The owner ruled that everything in the family that never releases reads 0.0.1, one rule with no exceptions, so a version field can never again imply a release process that does not exist.

## Options considered

- **Cut releases properly.** Rejected: it would manufacture a release process purely to justify a number, and the changelog work that follows would document upgrades nobody performs.
- **Leave the numbers as decoration.** Rejected: a decoration that looks exactly like a promise is how this was found, since the pending question "what version comes next" only existed because 1.0.0 claimed there would be a next.
- **Pin 0.0.1 everywhere and delete what the pin obsoletes.** Accepted.

## Decision

The settings default for the displayed API version becomes 0.0.1. A real deployment overrides it from its environment, so the field keeps its job while the style stops claiming a maturity it does not measure.

## Consequences

The style never cuts a release, so upgrade-facing summaries have no home and impact lives in commit subjects, which the rulebook already provides for. A derived project starts its own versioning from whatever number it likes, and the attribution line in its README carries the provenance. The number 0.0.1 now means "this is a style" everywhere in the family.
