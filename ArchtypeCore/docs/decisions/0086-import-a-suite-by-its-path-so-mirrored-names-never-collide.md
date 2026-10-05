# 0086. Import a suite by its path so mirrored names never collide

Status: Accepted
Date: 2026-10-05

## Context

The testing rule places one suite per unit at the mirrored path under
`tests`, named after the unit it covers, and the folder convention gives
no grouping folder an `__init__.py`. Under the test runner's default
import mode a suite's module name is then its bare file name, global to
the tree, so two units that share a name in different layers, a
domain schema and a service named after one concept, cannot both carry
the suite name the rule gives them. A project built from the host style
with an arrow of this style met two such pairs on 2026-10-03 while moving
to one suite per module, and named one suite of each pair after a class
instead, with a comment saying why, because the tree did not say which
form the template intended.

## Evidence

Reproduced on 2026-10-05 on this template's tree with two planted suites
of one name in different folders. The runner refused to collect the
second with an import file mismatch, while the type checker, which already takes the repository root as its
explicit package base, told the pair apart. With the suites imported
by path the runner collected both, and the whole suite passed under
the new mode, 28 tests.

## Options considered

- A naming rule for the collision, a suite named after its class or its
  layer when a name is taken. Refused, because the rule names the suite
  after the unit so a reader finds it by the path alone, and a second
  rule that applies only on the day of a collision is the kind of
  exception the tree cannot explain.
- Package markers under `tests`. Refused, since the folder convention
  gives a grouping folder no `__init__.py`, and a marker in the test tree
  for the runner's sake would be the first.

## Decision

The runner imports a suite by its path, with `--import-mode=importlib`
among the configured options, so two suites may share a file
name across the mirrored tree and each keeps the name of its unit. The
configuration says why beside each setting.

## Consequences

A project moving to one suite per module keeps the rule's names whatever
its units are called. A suite can no longer import another suite as a
module, which no suite in this tree does and the rule never allowed.
