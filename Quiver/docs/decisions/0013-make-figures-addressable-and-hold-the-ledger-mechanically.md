# 0013. Make figures addressable and hold the ledger mechanically

Status: Accepted
Date: 2026-09-03

## Context

A doctoral repository adopting this style re-executed its whole ledger and
found nine recorded figures that no longer reproduced, two of them
material: transposed site labels, and a thirty-scenario run's numbers
quoted against a hundred-and-sixty-scenario pin. Two pairs of its claims
also disagreed about one run, and in each pair the figure that reproduced
was the one the other claim carried, so the information needed to catch
the error was already in the tree in a record nothing compared. The same
review found the audit walking only the top of the docs zone, verifying the
map in one direction, holding no record immutable, treating an in-flight
STATE entry like a deferred one, and letting an arrow's manifest name
superseded claims as current.

## Decision

A figure a claim rests on is also written on its own line as
`figure <name>: <value>`, so the audit can hold two records that quote one
run to one value; where two claims name the same pin and the same figure
with different values, the audit fails. Each arrow's manifest names the
command that reproduces its figures, and a re-pin runs it and quotes the
figures digit for digit. The manifest is held to the current ledger: every
claim still standing that pins the arrow is listed and no superseded claim
is. The docs audit walks the whole docs zone, holds every root entry to a
room in the map or the baseline, holds records immutable beyond their
Status line in the working tree and in every commit since the check
arrived, and expires an in-flight STATE entry after thirty days. Every new
rule enters the selftest with a plant that proves it fires and, where the
rule allows something, a plant that proves it rests.

## Options considered

- Verifying every number against its run was refused, because no template
  can execute an arbitrary experiment; what it can do is make figures
  addressable and hold them consistent, which is the class that bit.

## Consequences

Two records disagreeing about one run fail the gate. A claim's figures
are addressable, so a re-pin has a mechanical target and a manifest that
lists a superseded claim is caught the same day.
