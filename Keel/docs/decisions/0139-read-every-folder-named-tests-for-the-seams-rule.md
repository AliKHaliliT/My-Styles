# 0139. Read every folder named tests for the seams rule

Status: Accepted
Date: 2026-11-25

## Context

The Python styles share one docs audit, and its seams check read only
the tracked files under the root's `tests` folder. A project built from
the server style reported that an engine there keeps its suites in a
`tests` folder of its own, which the check never read, so an engine
suite could patch a module and pass every check the gate runs.

## Evidence

Read on 2026-11-25 at 05a5f80. The check skipped every path that did not
begin with `tests/`. This package keeps its suites under its root
`tests` folder alone, so the check missed nothing here.

## Options considered

- Naming the server style's engine folders in the check. Refused,
  because a folder named `tests` is a suite folder wherever a layout
  puts it, and the shared text should not need to know each style's
  layout.

## Decision

The seams check reads every tracked file in a folder named `tests`,
whatever the folder sits under, in all three copies of the audit, and a
plant under an engine's `tests` folder proves it. Breaking the check
back to the root's folder alone failed the plant.

## Consequences

In this package the check reads what it read before. A suite folder a
project adds anywhere in its tree is held to the seams rule.
