# 0144. Hand the spelling tool the files git tracks by name

Status: Accepted
Date: 2026-11-26

## Context

The spelling advisory is meant to read the files git tracks and no
other. It did so by walking the whole folder with the tool and dropping
every finding on a path git does not track, the form an earlier record
chose over handing the tool git's list, which it refused as batching in
three languages for the same result. A project built from the host style
reported that the result is not the same in cost, since the walk reads
every file beside the tree before any finding is dropped, and that an
audit beside its retained outputs spent more than two minutes in the
tool before it was stopped.

## Evidence

Measured on 2026-11-26 at 6a35476 on the package seat, whose audit calls
the tool with the arguments this one does. The walk took 0.24 seconds
over the clean tree and 3.5 seconds with 52 megabytes of untracked logs
in a folder beside it, about 63 milliseconds a megabyte, so two
gigabytes of retained text cost two minutes. Handed three files by name,
one under a folder in its skip list and one under a hidden folder, the
tool read all three, where its walk read one, so it applies its skip
list and its hidden rule on a walk and to no file it is handed.

## Options considered

- Keeping the walk and naming the folders to skip. Refused again, since
  the list would chase every project's outputs.
- Handing over every tracked path in one call. Refused, because a
  project of a thousand files outruns a command line, the objection the
  earlier record raised.
- Leaving the tool's skip list and hidden rule to the tool. Refused,
  because it applies neither to a file it is handed, so the immutable
  records and the hidden folders the walk passed over would be read, and
  a record's spelling can be answered by no edit.
- Giving the audit an argument for the length of a run, so the selftest
  could cut a small tree. Refused, because the audit takes no argument
  and the selftest can build a tree whose paths meet the real length to
  the character.

## Decision

The audit hands the tool the tracked files by name and nothing else. It
leaves out a path that is no file on disk and a path with a part that is
hidden or named in the skip list, the two rules the walk applied, and
cuts the rest, in git's order, into runs of at most 7,000 characters of
paths, under the shortest command line a system the family runs on
allows. The filter on findings goes, every path handed over being
tracked. The selftest plants tracked files the pass must read and must
pass over, one of them a folder on disk. Since the audit shows what was
read and not how its runs were cut, the selftest also builds a
repository of its own whose paths meet the limit to the character, hands
the audit there a stand-in for the tool, first on the path, and holds
what the stand-in was handed to the exact runs, saying so where a system
runs only a compiled program by name. On Linux, fourteen breaks, each
one point, each failed a proof, after three that survived showed a sort
git's own order made idle, which went, and a cut no real path reached.
This record supersedes the earlier one on spelling in tracked files
alone.

## Consequences

The pass costs what the tracked tree costs, whatever lies beside it, and
an untracked file is not read, where before its findings were hidden. A
tracked file under a hidden folder or a folder in the skip list stays
unread, as before.
