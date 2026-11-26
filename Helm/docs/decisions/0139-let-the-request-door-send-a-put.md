# 0139. Let the request door send a PUT

Status: Accepted
Date: 2026-11-25

## Context

The request door is the only way the client reaches its backend, since
the layer rule refuses `fetch` anywhere else, and its options typed the
method as GET, POST, PATCH or DELETE. A project built from this style
reported that a screen changing a stored record by sending it whole,
against a server that takes that change as a PUT, could not send it
through the door.

## Evidence

Read on 2026-11-25 at 05a5f80. The method type named four methods and no
PUT, and the door hands its method to `fetch` unchanged, so the type
alone stood in the way.

## Options considered

- Sending a whole record's replacement as a PATCH. Refused, because the
  method is the server's to choose, and a door that refuses one a server
  takes pushes a caller toward `fetch` outside it.

## Decision

The method type gains PUT. A case sends a PUT through the door to a
pretend backend whose handler for that address answers a PUT alone, and
dropping PUT from the type failed the type check on that case. The
ledger gains the claim that a request goes through the door by any of
the five methods.

## Consequences

A screen that replaces a record whole sends it through the door, and
nothing changes for the methods the door took before.
