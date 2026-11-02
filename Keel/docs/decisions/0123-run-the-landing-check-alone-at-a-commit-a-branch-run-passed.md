# 0123. Run the landing check alone at a commit a branch run passed

Status: Accepted
Date: 2026-11-02

## Context

A change lands by pushing its branch, waiting for the branch's run, and
fast-forwarding main, and a fast-forward keeps the commit, so the push
that moves main started the whole gate again over a tree the branch run
had already seen whole. The only thing that run could learn was the
state of the remote after the landing, the landed-branches step, which
is one step of one job. The family paid the second run on every landing,
and a project built from a style that meters its runners paid it until
an account-level limit stopped its later checks and sent the finding
here.

## Options considered

- Skip the run on main altogether. Refused, because the landed-branches
  step observes a state only the push that moves main creates, and a
  push to main with no branch run behind it, a direct push, must still
  meet the gate.
- Trust the fast-forward by its shape, a push to main whose commit was
  already on another branch. Refused, because the branch's existence
  says nothing about its run; the evidence that matters is a passed run
  of this workflow at this commit, which the repository's own run
  history holds.

## Decision

Every workflow gains a landing job that carries the landed-branches step
and, on a push to main, asks the repository's run history, through the
token the run already holds with read access to actions, whether this
workflow passed at this exact commit on a branch by a push. Every other
job needs the landing job and runs only without that evidence, so a
fast-forward of a passed branch runs the landing check alone, while a
direct push to main, a failed or missing branch run, a refusal from the
history, a run started by hand and a request from a fork run the gate in
full. Manual dispatch joins the events for that purpose. The rules of
conduct carry the sentence, and the family's own root workflow proved
the design on the landing that brought it.

## Consequences

A landing costs one gate and one landing check, main still never carries
a tree the gate has not seen whole, and a project that copies the
workflow inherits the saving with the evidence rule that bounds it.
