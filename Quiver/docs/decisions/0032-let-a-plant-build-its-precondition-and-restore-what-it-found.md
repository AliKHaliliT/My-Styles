# 0032. Let a plant build its precondition and restore what it found

Status: Accepted
Date: 2026-09-10

## Context

A project built from this template ran the selftest after re-aligning and it
crashed in the inherited plant's teardown, which removed a folder it had not
created and found full of the style's records. Past that crash the upstream
plant would have deleted the project's own upstream document, and the
immutability plant, which looked for a record numbered 0001 in the project's
own decisions, had printed a skip and counted no failure since the project
kept its numbers after the inherited ones, so a rule had gone unproven while
the command reported that every rule fires. Three plants had assumed the
tree the style itself has, no inherited folder, no upstream document, own
records from 0001, and adoption is exactly the act that gives a project all
three. Record 0019 had already ruled that a plant builds whatever it names
and restores what it found; these plants breached it in the only tree where
anyone but the style runs them. A fourth cause showed only in a checkout
with Windows line endings, which is the checkout most children have: plants
that compared bytes against text written with bare line feeds matched
nothing, skipped, and counted no failure.

## Decision

A plant that creates a folder records whether the folder existed and removes
it only if it did not. A plant that writes a file the project may own keeps
the file's bytes and writes them back. A plant that adds an index row adds it
only where the guide carries none. A plant that must read the tree selects by
a property rather than by a number: the inherited plant takes the lowest
number its folder does not use, and the immutability plant takes the
lowest-numbered accepted record of the project's own, because immutability
is a fact about history and is the one subject a plant cannot build. The
review plants remove the folder they created and leave one they found. A plant
compares text, never bytes, so a checkout's line endings cannot silence it,
and the bytes it restores are the ones it read. The
selftest is proven in a tree shaped like a child as well as in the style's
own, and it must report every rule firing in both with nothing of the
project's changed afterwards.

## Options considered

- Skipping a plant whose precondition the tree already meets was refused,
  because a skip counts no failure, and the guide's own sentence names the
  hazard: a check that never fires and a check that cannot fire look
  identical.
- Reading subjects from the tree for every plant was refused again, as
  record 0019 refused it; it is right only where the plant cannot build the
  subject, which is the immutability plant alone.

## Consequences

The selftest means the same thing in a child as in the template, and it
leaves a child's tree as it found it. A plant's teardown never knows less
than its setup did.
