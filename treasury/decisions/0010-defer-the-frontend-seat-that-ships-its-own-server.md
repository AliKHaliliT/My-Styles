# 0010. Defer the frontend seat that ships its own server

Status: Accepted
Date: 2026-09-01

## Context

A frontend deploys in one of three shapes. Static files served by the API
server, static files served from any host, or an application that needs a
server of its own running, rendering pages, holding sessions in cookies,
and standing between the browser and the API as a backend for the frontend.
Helm covers the first two, and ruling 0009 settles how it rides beside the
server. The third is a different form, with a server-only zone that client
bundles must never import, a wire boundary that doubles into server-side and
browser-side calls, and sessions and caching the static forms never meet.
The owner asked whether it should exist.

## Decision

The seat is deferred, and the trigger is written down. It is built when a
public-facing product needs what only a frontend server gives, search
indexing and social previews of rendered pages, streamed rendering, or
sessions held in cookies the browser cannot read. Until then, Helm with
co-hosting is the family's whole frontend answer, because an internal
dashboard behind a login needs none of those, and a rendering server in
front of an API server is a second server doing work the first should do.

When the trigger arrives, the seat is a fifth style named for its form, a
web application that ships its own server, a sibling of Helm rather than a
Helm mode, since a template whose form flips with a configuration flag would
violate the family's naming honesty. It inherits Helm's layers and adds the
server-only zone and the doubled boundary. The stack is chosen at build time
from Helm's own lineage, React Router in framework mode, the same router
Helm already runs in library mode with loaders and server rendering switched
on, or TanStack Start beside the TanStack Query Helm already uses.

## Consequences

Nobody builds a server-rendered frontend for an internal tool by default.
The record names the conditions that reopen it, so the question is not
re-argued from scratch, and the two stack candidates are noted where the
decision will be made rather than made now.
