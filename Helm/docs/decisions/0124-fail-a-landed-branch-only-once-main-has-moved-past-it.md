# 0124. Fail a landed branch only once main has moved past it

Status: Accepted
Date: 2026-11-19

## Context

The protocol ends a landing by deleting the branch locally and on the
remote in the push that moves main, and every workflow's landing job
failed a run while any remote branch beside main was already merged into
it. That step decided less than its name said. A branch standing at
main's own commit is merged into main whether it landed anything or not,
so the step failed a branch a worker had made and not yet committed to,
and it failed every run on main after a landing by a worker whose remote
refuses a deletion. Hosted agent sessions are such workers. The route
they push through rejects the deletion of a branch, so the run on main
after each of their landings failed by construction, and a project built
from them changed the step in its own workflow and sent the case as an
entry.

## Evidence

Run on 2026-11-19 against a bare repository standing in for the remote,
each step run as a hosted runner runs it. With a branch ahead of main
the old step and the new both passed. With main fast-forwarded to the
branch, which then stood at main's own commit, the old step failed and
named the branch, and it failed again on a second branch made at main's
commit that never carried a commit of its own, while the new step passed
both. With main one commit past the branch both steps failed and named
it, and with the branch merged up to main and ahead again both passed.
Each of the new step's two conditions was watched failing with the
condition removed, the first on a branch at main's own commit and the
second on unlanded work on an older base. The refusal itself could not
be run from the template's own desk. The project's record holds it, an
HTTP 403 on the deleting push, and the documentation of the sessions'
provider, read on the same day, says that its proxy rejects branch
deletions and does not limit which branches a push can update.

## Options considered

- The owner deletes the branch after every such landing and reruns the
  failed check. Refused, because it spends two acts of the owner on
  every landing and leaves main red between them, over a branch that
  carries nothing main lacks.
- Passing branches by a pattern in their names. Refused, because a name
  says nothing about where a branch stands, and a session's branch that
  main has moved past is the stale branch the step exists to catch.
- Deleting merged branches from the workflow. Refused when the step
  arrived, because a workflow that deletes refs holds write access it
  does not need, and nothing here changes that.
- Leaving the step as it was and the case to each project. Refused,
  because the step's name claimed more than it decided for every worker,
  and each project built from hosted sessions would meet the same red
  run.

## Decision

The landing job's step fails a remote branch main has moved past and
passes one that stands at main's own commit, in the family's workflow
and in each seat's inert copy, and it is renamed for the question it
settles, that no landed branch is left behind main. The rules of conduct
say what the step holds and what a worker does whose remote refuses the
deletion. It stays on its branch and leaves it at main's own commit
until its next change moves it ahead or the owner deletes it when the
session ends, and a worker who meets a branch left behind reports it to
the owner. Those words were read back through a weaker model before they
landed, which asked what becomes of the local branch and who answers for
one left behind. A worker that can delete still deletes in the push that
moves main, and the docs audit's local half is unchanged, since it
already leaves a checked-out branch alone. The rule keeps its form, a
check for the half a remote's state can show. Two halves stay with
review, that a worker able to delete does so, and that the owner deletes
a session's branch at its end.

## Consequences

A landing from a hosted session leaves main's run green, and a branch
made and not yet committed to no longer fails one. A deletion forgotten
on the remote is caught when main next moves and no longer on the
landing's own run, which is the price, and until then a branch at main's
commit reads on the remote as work in flight when none is.
