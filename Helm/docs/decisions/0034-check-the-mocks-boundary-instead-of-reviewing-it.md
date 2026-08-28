# 0034. Check the mocks boundary instead of reviewing it

Status: Accepted
Date: 2026-08-28

## Context

The rule that `src/mocks` is imported only by the bootstrap and by tests
had no checker, so a production import of the pretend backend would ship
if review blinked. The layer rule crossed the same gap in
[decision 0008](0008-check-the-layer-rule-instead-of-reviewing-it.md),
moving from review into ESLint, and this boundary is the same kind of
question, decidable from an import path alone.

## Decision

Every layer's `no-restricted-imports` entry gains a pattern forbidding
`@/mocks`, and a final override exempts the one legal importer inside
`src`, the bootstrap at `src/app/main.tsx`. Suites live outside `src` and
never match the layer globs, so tests stay legal without an exemption.

## Evidence

A planted `import "@/mocks/node"` in a page failed the lint with the
boundary's own message, the revert ran clean, and the bootstrap file
lints clean with the mock import it legitimately carries.

## Consequences

The boundary is a verdict instead of a reading. The cost is the standing
one for this config, that ESLint's later blocks replace earlier
`no-restricted-imports` wholesale, so the bootstrap override must carry
the deep-import pattern too, and any future pattern joins both places.
