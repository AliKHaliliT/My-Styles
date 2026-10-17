# 0105. Carry up to five prose-only rules in one branch

Status: Accepted
Date: 2026-10-17

## Context

Every change to the law landed alone, one branch, one gate, one push,
one run and one fast-forward per rule, and the conduct rules named the
branch and the gate without saying how many rules a branch may carry. A
series of ten short rules paid that price ten times, most of it waiting
on the remote, while every one of them changed prose alone and none
could break a check.

## Options considered

- Keep one landing per rule. Refused, because the cost fell on waiting
  and not on rigor; the gate reads the merged tree whole whether it
  carries one commit or five.
- Let a branch carry any number of commits of any kind. Refused,
  because a red run over ten changes names none of them, and a change to
  a check or code is the kind that goes red.

## Decision

Each rule is one commit with its own record, so history and the records
stay one to one. A branch carries one such commit, or up to five when
every one of them changes prose alone, no check, no code and no tooling
among them, and the branch is gated whole and pushed once. A change that
touches a check or code travels alone. One branch at a time stands as it
did.

## Consequences

A run of short rules lands in one cycle, the records still answer to
history one to one, and a red run over a prose branch points at five
paragraphs at most.
