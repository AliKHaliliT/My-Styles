# 0117. Run a pull request's jobs only from a fork

Status: Accepted
Date: 2026-11-02

## Context

Every workflow of the family listens to a push and to a pull request, so
a push to a branch with an open pull request from the same repository
starts two complete gates over one revision. The family's own protocol
never opens a pull request, it pushes a branch, waits for that run and
fast-forwards main, so the family never paid for the second run; every
project built from a style copies the workflow, and one that reviews
through pull requests paid for it until an account-level limit stopped
its later checks.

## Options considered

- Drop the pull-request event, as the project did. Refused, because a
  fork's push never reaches the repository, so a contribution from a
  fork would run no gate at all until an owner carried it onto a branch
  by hand.
- Cancel the earlier of the two runs through a concurrency group.
  Refused, because it cancels a run the protocol is waiting on and still
  starts both.

## Decision

Every job of every workflow runs on a pull request only when the request
comes from a fork, by one condition on the job, that the event is not a
pull request or that the request's head repository is not this one. A
push to a branch of the repository stays that branch's run, a fork's
request still runs the whole gate, and a same-repository request starts
a run whose jobs all skip. The comment above the events says so, and the
rules of conduct carry the sentence.

## Consequences

A project that reviews through pull requests pays for one gate per
revision, and a fork keeps the coverage the request event exists to
give.
