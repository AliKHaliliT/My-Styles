# 0085. Prove the link repair on a record the check can see

Status: Accepted
Date: 2026-09-30

## Context

The selftest proves the link-repair clause by planting three edits on a
record that carries a relative link, a repaired target that resolves, a
target that does not, and a changed link text, and it expects the
immutability check to pass the first and refuse the other two. The check
reads records through git, comparing the working tree with the last
commit, so a record git does not track yet is invisible to it. The proof
chose its record by sorted name alone, so a record written in the working
tree and not yet committed could be the one chosen, and then two of the
three plants raised nothing.

## Evidence

On 2026-09-29 the host seat's selftest went red while a record was being written for a
landing. The record cited another by a relative link, no earlier record of
that seat's own carried one, and the proof planted on it. The ghost target
and the changed text both raised nothing, because the check had no
committed copy to compare against, and the record landed citing by number
and title instead. The same happens in any seat whose first linked record
is new in the working tree, which is every project at its first record
after adoption, since the gate runs before the commit. The rehearsal never
met it because it commits the child before auditing.

## Options considered

- Committing before the gate. Refused, because the gate runs on the tree
  that will be committed, and a proof that needs a commit to pass would
  move the gate behind it.
- Skipping the proof when the chosen record is untracked. Refused, since a
  skipped proof on a tree that holds a tracked linked record proves less
  than it could, and the tracked record is there to be chosen.
- Choosing among tracked records only, and planting on the first of them.
  Adopted.

## Decision

The proof chooses the first record, by name, that git tracks and that
carries a relative link outside its Status line, and it skips with its
reason where none does. It proves the choice itself by writing an
untracked record with a link that sorts before every real one, checking
that the choice falls on another record, and removing it. This seat's selftest asks git for the tracked records the same way. No
sentence of the law changes, because the clause was right and the proof
was reading a record the check could not see.

## Consequences

A project's first linked record no longer turns the selftest red before
its commit, and the immutability clause is proven on a record the check
can see. A record of this defect stands in every seat, and the copies of
the audit stay one text.
