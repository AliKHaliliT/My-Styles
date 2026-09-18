# 0049. Land without a remote and check the local deletion

Status: Accepted
Date: 2026-09-18

## Context

The branch protocol lands a change by pushing the branch, waiting for its
run, fast-forwarding main, and deleting the branch on the remote in the
same push, and the workflow fails while a remote branch already merged into
main still stands. A repository with no remote has nothing for three of
those steps to act on, and the family said nothing about it. A child read
on 2026-09-17 had no remote, so its worker committed straight to main, its
workflow had never run, and every check that lived only there was a
sentence in that tree. The em dash count, the vocabulary advisory, and the
spelling advisory have since moved into the docs audit, which the worker
runs. The landed-branches step is the one check the workflow carries beyond
the gate's commands, and its subject, a merged branch left on the remote,
does not exist without one; a merged branch left in the local tree does,
and nothing anywhere checked for it, the guide leaving that half to the
worker.

## Evidence

The protocol bullet in every guide was read on 2026-09-18. It named the
push, the wait, and the remote deletion without a word for a repository
that cannot push, and it left the local deletion to the worker. Whether a
repository names a remote is one git command, and whether a local branch
beside main is already merged into it is another, both decidable in every
tree including the rehearsal's child, which has no remote and one branch.
The measured child carried no stale local branch, since its worker never
branched, which is the other way a protocol with no local form is met.

## Options considered

- Requiring a remote, the audit failing where none is named. Refused,
  because whether a project is hosted is the project's, and a rule that
  reddens a private local project on the day it adopts puts hosting inside
  the style's jurisdiction.
- Leaving the local half to the worker. Refused under the ladder, because
  it is decidable in the terminal and a landed branch outliving its landing
  was the fault the deletion rule was written against.
- Deleting merged branches from the audit. Refused, because an audit
  changes nothing in a tree; it names the branch and the worker deletes it.
- Saying nothing. Refused, because a tree that has never met a run then
  passes for lack of one, which is the passing signal the family's own rule
  on checks warns against.

## Decision

The protocol gains its local form. Where the repository names no remote,
the branch is still merged with main, gated whole in the terminal,
fast-forwarded, and deleted, the push and the wait having nothing to act
on. Every docs audit fails while a local branch beside main, and beside the
branches checked out in any working tree, is already merged into main,
naming the branch, so the local half of the deletion rule is a check
wherever the audit runs; where the tree has no local branch named main the
check names itself as not run. Every docs audit also reports, when the
repository names no remote, that the workflow's landed-branches step ran
nowhere, in the list of checks not run, so the absence is stated on every
run. The rehearsal initialises its child on main, asserts the missing
remote is named, and runs the stale-branch proof there as well as in the
template's own tree, where the proof creates a branch at main's tip,
expects the finding, and removes it. Under the ladder the local half moves
from prose to the check rung; the remote half keeps its workflow step,
whose subject does not exist without a remote.

## Consequences

A worker in a project with no remote follows the same protocol minus the
steps that need one, and the audit tells them on every run which check
never ran and why. A forgotten local branch goes red on the next audit run
in every project, hosted or not, and a worker on a branch is never flagged
for the branch they stand on. Nothing changes for the remote half.
