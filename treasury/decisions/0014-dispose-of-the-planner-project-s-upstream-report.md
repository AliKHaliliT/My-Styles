# 0014. Dispose of the planner project's upstream report

Status: Accepted
Date: 2026-09-07

## Context

A project serving a planner over a socket stood ArchetypeCore's delivery
layer up over a real engine and sent three entries, each with the records it
had read named and a verification step written out. Each was tested on the
family's tree before disposition, one by reproduction.

## Decision

- Kept, proven by running it: the request-id middleware admitted websocket
  scopes and then built a `Request`, whose constructor asserts http, so
  every websocket connection died in the middleware. Reproduced against the
  real middleware on a throwaway app. The middleware reads its headers off
  the scope, both observability middlewares are driven as ASGI callables in
  the suite with an http and a websocket scope, and the two docstring
  sentences confessing the untested branch left with the tests that replaced
  them.
- Kept, duplicate: the deprecated 422 constant, the second independent
  report of it in a day, with the same corrected diagnosis as ruling 0013.
- Kept, generalized: the typo. A sweep of the whole family found it to be
  the only misspelling in living prose and code, and the family adopted a
  spell check as an advisory step beside the vocabulary grep, recorded in
  every style.

This report sent a typo and a one-line rename, the small things the
doctoral repository's agent had kept to itself, and the defect class in
ruling 0015 asks every child to send exactly those.

## Consequences

The project reverts its local rename, its middleware patch, and its typo fix
in favor of the template's versions, and re-aligns to the commit that
carries this record.
