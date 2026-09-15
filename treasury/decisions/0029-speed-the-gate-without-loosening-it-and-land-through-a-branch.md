# 0029. Speed the gate without loosening it and land through a branch

Status: Accepted
Date: 2026-09-15

## Context

The owner observed that development under the styles takes noticeably longer
between tasks, that the code is better and easier to develop for it, and that
the added time is waiting rather than generation. The question was whether the
process could be faster without loosening the gate. A second question followed,
what happens when two sessions work on one project at once, from record numbers
to refused pushes to an agent finding the tree changed under it.

## Evidence

Where the minutes went in one day of work on the family, in order: the host
audit's selftest, forty full audit runs each repeating the same history
queries; the fresh gate after the last edit, five seats run one after another;
CI, five to eight minutes per push; proof work for reshaped audits; and reading
law before touching it. The immutability check started one git process per
commit that had touched docs since its scope arrived, a cost linear in a
project's age.

After the changes below, on 2026-09-15 in this repository: the host selftest
ran in 5 seconds where the committed version ran in 37, printing the same
lines; the host audit ran in 1 second; the docs audits printed identical
findings to their previous versions over fifteen planted trees across three
seats; Helm's audit did the same over its three groups.

## Options considered

- Skip the checks whose inputs did not change. Refused. Deciding which inputs
  changed is the judgment call the week's stale-perception cases were about.
- A type-check daemon. Refused. It is fast because it keeps state between
  runs, and state kept between runs is stale perception waiting to happen;
  incremental caching is already on.
- Parallel agents in worktrees. Refused as a speed measure. It raises
  throughput, not the latency of one task, and adds merge risk to every
  landing.
- Fewer plants or a lighter rehearsal. Refused. They are the proofs the law
  rests on.
- Not waiting on CI in the foreground. Declined by the owner, who wants the
  outcome reported.

## Decision

Four changes, each its own landing. The gate's commands run concurrently
where they are independent, a practice and not a byte. The immutability
check gathers every commit's patch in one git call behind marker lines
instead of one process per commit, in the docs audits, the host audit, and
Helm's audit, with merges shown as show would. The host audit remembers
answers about committed history for the life of one process, log, show,
rev-list, and rev-parse, never diff or ls-files, because plants change the
working tree and never the history. The host audit gains the duplicate-number
check the docs audits already had, with a plant. And every seat adopts the
branch protocol, one worktree and one branch per session, merge main in, gate
the merged tree, push the branch, wait for green, fast-forward main, merge and
not rebase where records pin commits, with the pause rule's new trigger for a
change the session did not make. The seats record the protocol as Keel 0054,
ArchtypeCore 0051, Helm 0055, and Quiver 0035, identical bodies, and the arrow
inherits Keel's.

## Consequences

The local loop is bounded by the slowest command rather than their sum, the
audits stop slowing down as a project ages, and the host selftest is cheap
enough to run on every change to the audit as its docstring demands. A
scaffolded task stays slower than an unscaffolded one, by the reading, the
records, and the closing pass, and the owner accepts that price by name.
