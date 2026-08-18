# 0008. Check the layer rule instead of reviewing it

Status: Accepted
Date: 2026-08-04

## Context

[Decision 0003](0003-build-the-client-as-one-way-sliced-layers.md) made one-way sliced layers the shape of this template, and the rule that makes them worth anything is that imports point downward only. That rule was left to review, and STATE.md deferred a linter until the rules had proven themselves in practice.

They have now proven themselves, in this template and in three derived projects that adopted the same shape. Review turned out to be the weak link exactly where expected. An import line looks identical whether it points down or up, so catching a violation depends entirely on the reviewer holding the layer order in mind.

## Options considered

- **Leave it to review.** Rejected: the discipline is only as strong as the reviewer's memory of the layer order, and it degrades without anyone noticing.
- **Add a dedicated boundary plugin** (`eslint-plugin-boundaries` or similar). Rejected, though it was the candidate this project's own deferral named and it is a capable tool. It is a new dependency for a rule the project can already express, and a template earns its keep by being thin.
- **Express the rule with ESLint's built-in `no-restricted-imports`.** Accepted.

## Decision

`eslint.config.js` declares the layer order once and derives one config block per layer, each forbidding the layers above it and forbidding any import that reaches past a slice's `index.ts`. Cross-slice imports always travel through the `@/` alias, which is what makes them matchable; a slice's own files use relative paths and are untouched. Suites live outside `src/` and are exempt by construction, which is the same exemption the layer rule already grants them.

Both halves of the rule travel in a single `no-restricted-imports` entry per layer, because a later ESLint config block replaces the same rule rather than extending it; splitting them into separate blocks silently disables the first one. That failure mode is quiet enough to be worth naming here.

## Consequences

An upward import and a reach past a slice door both fail `npm run lint`, so the layer rule holds without depending on who reads the diff. The template gains no dependency, and a project deriving from it inherits the enforcement along with the shape.

The check matches import specifiers, so it has a known blind spot: a deep relative path that climbs out of a slice (`../../other-slice/file`) is not caught. The convention is that anything crossing a slice boundary uses the alias, and the patterns rest on that convention rather than on module resolution.
