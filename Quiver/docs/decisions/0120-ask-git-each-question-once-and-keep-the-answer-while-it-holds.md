# 0120. Ask git each question once, and keep the answer while it holds

Status: Accepted
Date: 2026-11-09

## Context

The audit asked git for the tracked files once per check, for an
ancestry once per pair of commits, and for the standing of a path once
per path, and its selftest reruns the whole audit once per plant, so
one selftest spawned thousands of git processes. A spawn costs about
twenty milliseconds on a Windows desk and three on the hosted runner,
which made the same proof four times slower where every landing is
gated first. Treasury 0029 had given the host's audit a memory of
history answers for the life of a process and the other audits none.
Measured on 2026-11-08, four fifths of a selftest's wall-clock was spent
inside those spawns, many of them repeating a question already answered
in the same run or asking per item what one listing answers.

## Options considered

- Leave the cost to the machine. Refused, because the gap is in the
  audit's shape and not in the desk. The same proof cost four times
  more here than on the runner, and the desk is where a tree is gated
  before it is pushed.
- Run fewer checks per plant in the selftest. Refused, because the
  proof is that the whole audit fires on a plant. A selftest that runs
  one check proves one check.
- Remember every answer for the life of the process. Refused, because
  the plants change the index and the working tree between runs, so an
  answer about them outlives its truth. Only history has one answer
  for a process.

## Decision

The audit keeps what git answers for exactly as long as the answer
holds. An answer about committed history, log, show, rev-list,
rev-parse and ls-tree, holds for the life of the process, because
nothing the audit or its selftest does commits. An answer about the
working tree, the index or the refs holds for one run, because a run
changes none of them and the plants change exactly them between runs,
so it is kept from the moment a run starts to the moment it ends and
never across runs. A write is never kept and never answered from
memory. Two questions once asked per item are now asked once per run.
Whether one commit is before another is read off one listing of the
second's ancestors, and whether the tree holds a path is read off the
one listing of tracked files. The host's audit had the first memory
since treasury 0029; every seat's audit now has both. The selftest
proves every rule as before, on the same plants.

## Consequences

A selftest at the desk takes a fraction of its former time, a hosted
job shortens by seconds, and a check asks git the way a reader would,
once. A question about the tree asked outside a run is answered fresh,
so the selftest's own plumbing never reads a stale answer.
