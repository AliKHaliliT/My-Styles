# 0004. Segregate the server cache from client state

Status: Accepted
Date: 2026-08-03

## Context

The deepest recurring bug class in client applications is treating server data as application state: fetching in effects, copying responses into a global store, then hand-maintaining staleness, deduplication, and race discipline that a cache should own. The two kinds of state have opposite natures. Server data is shared, asynchronous, and stale the moment it arrives; client state is owned, synchronous, and always current. A template that leaves this distinction to convention will watch it erode, one convenient store write at a time.

## Options considered

- **One global store for everything** (the classic Redux shape). Rejected: it re-implements caching by hand, poorly, and makes the store a copy of the backend that must be manually synchronized forever.
- **Fetch in effects with component state.** Rejected: every page re-solves caching, deduplication, cancellation, and retries, which is exactly the boilerplate a server-cache library exists to delete.
- **A server-cache library for server data, small stores for true client state.** Accepted: TanStack Query owns the server cache, and Zustand holds the little that is genuinely the client's.

## Decision

Server data lives in the TanStack Query cache and nowhere else. Each entity defines its query keys and hooks in its `queries.ts`, and all invalidation goes through those exported keys, never through retyped strings. Client state exists only for what the client owns, the session, the theme, form drafts, and UI ephemera, in small Zustand stores or component state. Copying query data into any store is against the rules; a component needing server data subscribes to the query. Mutations invalidate their own slice's keys, and cross-slice invalidation is a feature-layer concern.

## Consequences

Staleness, refetching, deduplication, and request races are the cache's problem instead of every page's, and the stores stay small enough to read in one sitting. The cost is a hard line that occasionally feels ceremonious, such as a feature slice existing mainly to own a cross-entity invalidation, and a second library alongside the store, which the split justifies because each does the job the other is bad at.
