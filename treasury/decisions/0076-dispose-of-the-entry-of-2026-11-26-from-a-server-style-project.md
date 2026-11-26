# 0076. Dispose of the entry of 2026-11-26 from a server-style project

Status: Accepted
Date: 2026-11-26

## Context

One project built from the server style, with a client from the client
style kept in a folder of it, holds one upstream entry in its client's
upstream file, dated 2026-11-26 and pinned at the family's 2ddae38,
which the family's history holds. It says the client's request door
cannot read an answer with no content. The style's owner asked for it
fixed so that the schema stays the only judge. Tested at the family's
964c295, the entry was real, and it reached further than it said, since
a success whose body is not JSON escaped the same way.

## Decision

Kept, and widened. The door reads a success with no body as nothing and
checks it against the caller's schema, and refuses a body that is not
JSON as a broken contract. The client seat's 0147.

## Options considered

- Reading only a 204 or a 205 as nothing. Refused, because a 200 with no
  body and a success that is not JSON would still escape as the JSON
  reader's own error.

## Consequences

The project deletes the entry at its next re-alignment and may answer
its removals with no content.
