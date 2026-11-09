# 0061. Ask git each question once in every audit

Status: Accepted
Date: 2026-11-09

## Context

A measurement of the desk gate on 2026-11-08 found its time in process
creation and not in the work. The package style's selftest spawned 2,872
git processes and the host's 4,454, at about twenty milliseconds each on
a Windows desk against three on the hosted runner, and four fifths of a
selftest's wall-clock passed inside them. One run of the package style's
audit asked git forty questions, twelve of them for the same list of
tracked files, and one run of the host's asked 146, seventy-eight of
them whether one commit came before another, one pair at a time.
Treasury 0029 had given the host's audit alone a memory of history
answers for the life of a process. The other audits remembered nothing,
and none of them remembered the tree within a run, though a run changes
nothing git reads and the plants of a selftest change it only between
runs.

Measured again on 2026-11-09 with the change in place, on a fresh clone,
every selftest fires every rule, every audit agrees with its tree, and
the type checker and the shape lint pass. One run asks nineteen
questions in the package style, forty-seven in the host and twenty-one
in the client, from forty, 146 and forty-two. The package style's
selftest spawns 501 processes in thirty seconds where it spawned 2,872
in seventy-six, the host's 1,065 in fifty-six where it spawned 4,454 in
110, and the five selftests run one after another in three minutes and
six seconds where they took six minutes and fifty-six.

## Decision

Every seat's audit keeps what git answers for exactly as long as the
answer holds, and asks once per run what it asked once per item. An
answer about committed history, log, show, rev-list, rev-parse and
ls-tree, is kept for the life of the process, because nothing an audit
or its selftest does commits. An answer about the working tree, the
index or the refs is kept for one run, from the moment the run starts to
the moment it ends, because a run changes none of them and the plants
change exactly them between runs; outside a run such a question is
answered fresh. A write is never kept. Whether one commit is before
another is read off one listing of the second's ancestors, and whether
the tree holds a path is read off the one listing of tracked files. The
client's audit is one process per run, so its two memories are one.
Recorded in the package seat's 0125, mirrored into the arrow's inherited
folder, the server seat's 0130, the client seat's 0121 and the host
seat's 0120.

## What is refused, and what would reopen it

- Leaving the cost to the machine. Refused, because the gap was in the
  audits' shape and not in the desk, and the desk is where a tree is
  gated before it is pushed. It would reopen only if a spawn came to
  cost the desk what it costs the runner, and even then the audits would
  be asking one question twelve times.
- Running fewer checks per plant in the selftest. Refused, because the
  proof is that the whole audit fires on a plant, and a selftest that
  runs one check proves one check. It reopens if a selftest grows past
  what a gate can wait for with the whole audit run per plant.
- Keeping answers about the tree for the life of the process. Refused,
  because the plants change the index and the working tree between runs,
  so such an answer outlives its truth. It reopens if the Python
  selftests come to run each plant in a process of its own, as the
  client's does, where the two memories are one.
- Batching the per-token ignore question of the host. Left as it is,
  because it costs under a second per selftest and asks git once per
  token only where a Recorded line names paths. It reopens when a
  measurement puts it above a second.

## Consequences

A selftest at the desk takes less than half its former time and a hosted
job shortens by seconds, the desk gate that runs the five selftests side
by side drops below five minutes, and an audit asks git the way a reader
would, once. The measurement that found this, the spawn count and the
seconds inside it per run, is the one to repeat when a gate slows again.
