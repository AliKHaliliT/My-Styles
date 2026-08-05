# 0012. Answer the same five commands in every style

Status: Accepted
Date: 2026-08-05

## Context

The styles are meant to differ in form and agree in contract, so a person or an agent arriving at any of them should find the same questions answered. Comparing the `## Commands` blocks showed they did not agree. This template and the package template both listed Lint and Type-check; the server template listed neither, because it had nowhere to configure or install them. The blocks also ordered the same verbs differently, which makes comparing the styles harder than it needs to be.

A second gap was larger and mattered most here. None of the three styles had any continuous integration. [Decision 0008](0008-check-the-layer-rule-instead-of-reviewing-it.md) moved the layer rule out of review and into ESLint precisely so it would be checked rather than remembered, but with no workflow running ESLint the rule was still only checked when somebody typed the command. The reasoning of that decision was therefore only half realized.

## Options considered

- **Leave each block shaped by what its language happens to offer.** Rejected: the differences then read as choices rather than as consequences of the language, and a reader cannot tell which is which.
- **Unify the tools rather than the contract.** Rejected: ESLint is not ruff and vitest is not pytest. Only the contract can be shared.
- **Fix the five verbs and their order, and run them in CI.** Accepted.

## Decision

The five commands are Install, Run, Test, Lint, and Type-check, in that order, in every style. Commands beyond the five, which here are Build and Preview, are listed after them rather than in place of them.

Each style runs the five commands in continuous integration on push and on pull request. The workflow installs, then lints, type-checks, tests, and finally builds, since a template whose build breaks is worse than one whose tests fail.

## Consequences

The layer rule is now genuinely checked rather than checkable, which is what decision 0008 intended. The same holds for the token rule and the wire-boundary rule, both of which ESLint carries.

The styles agree on what a project must be able to answer, and where the answers differ the difference is attributable to the language rather than to an omission.

The cost is a workflow file and a slower feedback loop on pull requests, and the build step makes this style's workflow the slowest of the three. That is the right place to spend the time, because a broken build is the one failure a person copying this template would hit first.
