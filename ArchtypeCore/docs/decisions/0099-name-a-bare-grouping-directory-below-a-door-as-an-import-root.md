# 0099. Name a bare grouping directory below a door as an import root

Status: Accepted
Date: 2026-10-09

## Context

The layout rule keeps grouping directories bare and gives an
`__init__.py` only to a package that re-exports, and the import
contract's roots are the bare layers. The graph reader the contract
runs over walks a bare root whole, nested bare directories included,
but sees a door's subdirectories only through their own doors, so a
bare grouping directory below a package that re-exports is invisible
to it, with no node and no edge. The coverage check already refused
that state, naming the unseen modules without saying why they were
unseen or what to do, and a maintainer of projects built from three of
the family's styles reported on 2026-10-08, as an issue, that removing
an otherwise empty door had turned a checked dependency into an
invisible one, and had kept the empty doors, which the rule forbids.

## Evidence

Measured on 2026-10-09 with the graph reader in fresh interpreters. A
package with a door and a bare directory beneath it yields the package
alone; the same bytes with an empty door in the directory yield the
directory and its module. A bare directory named as a root yields
everything below it, bare subdirectories included, and a door package
inside a bare root hides its own bare subdirectory. The package seat
passes today because its layers are bare and each is a root, and the
server seat because its root is a namespace package the reader walks
whole; neither tree holds a bare directory below a door.

## Options considered

- An empty door in every grouping directory below a door, as the
  issue's workaround. Refused, because a door re-exports, and an empty
  one is a file the rule forbids kept for a reader's sake.
- A reader that covers bare directories below a door. Refused,
  because the reader's own answer to a bare directory is to name it as
  a root, and a reader of our own would be a second graph to keep.
- Forbidding grouping directories below a door. Refused, because the
  layout rule is about purity and doors, and a package that re-exports
  from grouped modules is a legal shape.

## Decision

A bare grouping directory below a door is named as an import-linter
root of its own, as the layers are, because the graph reader walks a
bare root whole and sees a door's subdirectories only through their
own doors. The package seat's layout rule says so, the coverage
finding names that remedy, and the selftest plants a door package
with a bare directory beneath it, the one legal layout the reader
cannot see, which must raise the finding.

## Consequences

A project that groups modules below a re-exporting package lists the
group as a root and keeps its doors honest, and the coverage check
has its first planted proof.
