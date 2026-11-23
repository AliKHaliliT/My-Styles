# 0131. Read the address before the page fetches

Status: Accepted
Date: 2026-11-23

## Context

The page exemplar called its two hooks with whatever the address gave,
an empty string when it gave nothing, and only then returned its error
state for a missing id, so the hooks had already sent requests whose
answers the page never showed. A project cuts its pages from this one,
so each of them inherited the requests. A project built from the client
style met it while cutting a detail page for a resource whose ids are
numbers, where the address had to be read into a number before any hook
could take it, and sent the case as an entry.

## Evidence

Measured on 2026-11-22 at afffa40 in the page's own suite. With no id in
the address, the page sent `GET /api/vessels/` and `GET /api/berths` and
showed neither answer. With the change it sent nothing. Against the page
as it stood, the new case failed in each of five runs.

## Options considered

- Disabling the queries while the id is empty. Refused, because the hook
  would still take a string that may be empty, a page cut from the
  exemplar for a numeric id would still need a placeholder, and the
  disabled queries would still sit in the cache.
- Testing the inner part alone, with the id passed in. Refused, because
  the page reads the address and stays the tested unit, mounted under
  its route as the suite's exemplar shows.

## Decision

The page reads its id first and returns its error state for an address
without one. Otherwise it renders an inner part that takes the id and
calls the hooks, so no hook is called with a value the page already
knows to be wrong. The suite's case for an address without an id now
also asserts that the backend was asked nothing, noting every request at
the mock backend for the run, and the case failed against the page as it
stood.

## Consequences

A page cut from the exemplar asks nothing for a bad address, and the
hook it calls can take the id's own type. The case waits a twentieth of
a second to see that nothing was asked, and a page suite cut from this
one copies the wait with the case.
