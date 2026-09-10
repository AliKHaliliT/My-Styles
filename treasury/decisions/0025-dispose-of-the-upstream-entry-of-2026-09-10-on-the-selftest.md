# 0025. Dispose of the upstream entry of 2026-09-10 on the selftest

Status: Accepted
Date: 2026-09-10

## Context

An inquiry project aligned at `d98c75851023` sent one defect entry in its
upstream file: three plants of the Quiver selftest assume the tree the style
has rather than the tree adoption produces. The inherited plant removes a
folder it did not create, the upstream plant deletes the project's own file,
and the immutability plant looks for a record numbered 0001 where a project
that kept its numbers has none, so a rule goes unproven while the command
reports every rule firing. The maintainer reproduced the crash in a scratch
clone shaped like a child before disposing of the entry.

## Decision

Kept, as the reporter fixed it and generalized to every plant: a plant builds
only what the tree lacks and removes only what it built, keeps and restores
any file the project may own, adds an index row only where none exists, and
selects a subject it cannot build by property rather than by number. The
Quiver selftest is now proven in a child-shaped tree as well as in the
template. Quiver record 0032.

## Consequences

The reporting project deletes its entry at its next re-alignment and drops
its private version of the plants for the template's. A selftest that reports
every rule firing means it in every tree that runs it.
