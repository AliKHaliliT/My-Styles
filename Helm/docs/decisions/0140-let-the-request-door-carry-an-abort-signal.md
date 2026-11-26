# 0140. Let the request door carry an abort signal

Status: Accepted
Date: 2026-11-25

## Context

The request door offered no way to end a request its caller no longer
needs. A project built from this style held one request open at a time,
waiting on the server until something changed, and had to end it when
the component holding it went away, which the door could not do, while
`fetch` outside the door is what the layer rule refuses.

## Evidence

Read on 2026-11-25 at 05a5f80. The door's options carried a method and a
body, and it called `fetch` with no signal and no way to pass one. The
style's record that segregates the server cache from client state names
cancellation among the cache library's duties and says nothing of the
door.

## Options considered

- Leaving cancellation to the cache library alone. Refused, because the
  library cancels a query by aborting the signal it hands the query
  function, and a door that cannot carry that signal leaves the request
  running.
- Making every query of the demo hand the door the cache library's
  signal. Refused, because what the door must offer is the option, while
  whether a query passes it is that query's choice.

## Decision

The door's options gain an abort signal, which the door hands to
`fetch`, so a caller can end a request and the request rejects with the
AbortError `fetch` raises, and a caller that passes none is served as
before. A case starts a request a handler holds, aborts it once the
handler has it, and sees the request reject with the AbortError and the
handler see its request end, and the ledger gains the claim. Dropping
the signal from the call to `fetch` left the request hanging and failed
the case, and dropping it from the options failed the type check.

## Consequences

A component that goes away can end the request it held, and a query can
hand the door the signal the cache library passes it.
