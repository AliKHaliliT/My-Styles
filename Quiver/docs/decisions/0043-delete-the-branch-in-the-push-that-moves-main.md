# 0043. Delete the branch in the push that moves main

Status: Accepted
Date: 2026-09-17

## Context

The branch protocol said how a change lands and stopped at the
fast-forward. Nothing said what became of the branch, and thirteen landed
branches stood on the remote and in the working tree after one day of
landings under the protocol, each a name for bytes main already carried.
A stale branch is where the next session starts from the wrong base, where a
second worker pushes a fix nobody will merge, and where a reader of the
remote sees work in flight that finished a week ago. The owner ruled that
once a change is committed, merged and pushed, its branch goes, and asked
that the ruling be law if it was not.

## Evidence

Every guide's protocol bullet was read on 2026-09-17 and none named the
branch after the fast-forward. The remote held thirteen branches beside
main, every one already merged into it, and the working tree held the same
thirteen locally. Git deletes a remote branch and moves main in one push
when both refspecs travel together, so the deletion costs no second round
trip and no window in which main has moved while the branch still stands.
The workflows already fetch full history in their first job, which is what
a merged-branch check needs.

## Options considered

- A sentence alone. Refused under the ladder, because the remote half can
  be checked, since a branch merged into main and still on the remote is a
  fact the workflow reads in one command.
- Deleting the branch before the fast-forward. Refused, because a branch
  deleted before main carries its commits leaves them unreachable if the
  fast-forward then fails.
- Checking local branches. Refused, because no workflow sees a worker's
  machine; the local half stays with the worker, stated in the same bullet.
- Deleting merged branches automatically in the workflow. Refused, because
  a workflow that deletes refs holds write access it does not need and acts
  on a worker's behalf; the check fails and names the branch, and the worker
  deletes it.

## Decision

The protocol bullet in every guide gains the last step, deleting the branch
locally and on the remote in the push that moves main, with its reason. Every
workflow, the family's and each seat's inert copy, gains a step that fetches
every remote head and fails while any branch beside main is already merged
into it, naming the branch and the rule. A run on a branch passes, since the
branch is not yet merged; a run on main after a clean landing passes, since
the push that moved main removed the branch; a run on main after a forgotten
deletion fails with the name. The thirteen stale branches were deleted before
this landing so the check starts from a clean remote. The rule lands as a
check for its remote half and as prose for its local half, the strongest form
each half allows.

## Consequences

Landing a change costs one more refspec on the final push and nothing else. A
remote that carries only main and the branches in flight reads as the state
of the work. A child whose worker forgets the deletion learns it from the
next run on main, with the branch named.
