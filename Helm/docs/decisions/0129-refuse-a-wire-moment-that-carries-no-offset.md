# 0129. Refuse a wire moment that carries no offset

Status: Accepted
Date: 2026-11-23

## Context

A project built from the server style sent an entry on stamps that
crossed the wire with no offset, and a browser read each as its own
local time. The client style held the other half of that fault in its
exemplar wire schema, which typed a vessel's arrival time as any string,
while the translator revives it with `new Date`, and `Date` reads a
stamp without an offset as local time. The project had held its own
client's wire schema to an offset and said nothing of the exemplar.

## Evidence

Tested on 2026-11-22 at afffa40. The exemplar schema took
`2026-11-22T01:57:35` and `not a time` as arrival times. Read by
JavaScript's `Date` in a zone seven hours behind UTC, the first became
`2026-11-22T08:57:35.000Z`. Held to an offset, the schema refused both,
and took `2026-11-22T01:57:35Z` and `2026-11-22T01:57:35+00:00`.

## Options considered

- Reviving a stamp without an offset as UTC in the translator. Refused,
  because the client would be guessing what the wire never said, and a
  server that sends its local time would be read wrong without a sound.
- Leaving the schema as it was and trusting the server. Refused, because
  the wire contract is where the client stops trusting, and every other
  field is held there.

## Decision

A vessel's arrival time is an ISO date-time that carries its offset, so
a stamp without one, or a string that is no time, is refused at the
boundary as a broken contract, and the schema's comment says why. Cases
hold both refusals, the stamps the schema takes, and the refusal through
the shared client, and four breaks of the schema were each caught. The
ledger gains the claim that a moment crosses the wire with its offset or
the payload is refused, held by the case at the boundary.

## Consequences

A client cut from the exemplar reads a moment only when the wire says
which one it is. A server that sends a stamp without its offset now
breaks the client loudly at the boundary, where it once moved every
moment by the reader's distance from UTC.
