# 0016. Check doc-comment presence instead of reviewing it

Status: Accepted
Date: 2026-08-10

## Context

The README's convention says every export carries a doc comment, and until now nothing looked. The two Python styles closed the same gap through rules their linter already ships, which cost no dependency, and that left this template as the only one whose documentation rule was held by review. The gap was not hypothetical here. The first run of a checker against this very tree found fifteen undocumented exports, in the theme store, both wire schemas, the auth store, the mock database, and the typed environment, sitting unnoticed in a template whose convention says they cannot exist.

ESLint has no built-in rule for this, so [decision 0008](0008-check-the-layer-rule-instead-of-reviewing-it.md)'s bar, no dependency a built-in can replace, does not decide the question; there is nothing to replace. The owner's criterion was maintenance: a plugin if one is actively maintained, an in-house script otherwise.

## Options considered

- **Stay with review.** Rejected: fifteen misses in the template's own tree is the measurement of how well review carries this rule.
- **An in-house audit script.** Rejected while a maintained plugin exists, because a house script that every fork inherits is code nobody maintains, and export-shape parsing in TypeScript is exactly the kind of edge-case swamp a dedicated project handles better.
- **`eslint-plugin-jsdoc`.** Accepted. It is actively maintained, with a release the day before this decision, and its `require-jsdoc` rule scopes to exported declarations.

## Decision

`eslint-plugin-jsdoc` joins the dev dependencies, and `jsdoc/require-jsdoc` runs as an error over `src/**`, configured for exported functions, classes, variables, interfaces, and type aliases. Suites are exempt by the same rule that keeps them outside the every-export requirement, and they live outside `src` anyway. The fifteen findings were filled with one-sentence comments in the house voice rather than suppressed, and a planted undocumented export was confirmed to fail the Lint verb before this record was written.

## Consequences

An undocumented export now fails `npm run lint` and CI with it, so doc-comment coverage stops decaying silently, which closes the last reviewed-only documentation rule in the family. The cost is one dev dependency, accepted knowingly against the thinness bar because no built-in exists, and a rule whose export-detection contexts may need extending if the template ever exports shapes it does not export today.
