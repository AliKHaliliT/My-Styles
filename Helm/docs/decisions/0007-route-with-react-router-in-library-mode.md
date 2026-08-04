# 0007. Route with React Router in library mode

Status: Accepted
Date: 2026-08-03

## Context

Two credible routers exist for a client-side SPA in 2026. TanStack Router offers fully typed paths, params, and search state at the cost of a route-tree codegen step and a second ecosystem's idioms; React Router v7 in library mode offers the largest ecosystem and the most widely known API, with types that are merely adequate. The choice matters more for this template than for an ordinary app, because a template's router is read by agents as a pattern to extend, and its guardrails should come from the architecture rather than from any single library's cleverness.

## Options considered

- **TanStack Router.** Rejected, though tempting: its type safety is best in class, but it adds a codegen step to the toolchain and a less universally known API, while this template's defense against drift is the layer discipline rather than route typing. The trade tilts back toward it for apps whose search params carry real state.
- **React Router v7 in framework mode.** Rejected: framework mode brings a server half, which is a different form; the family assigns that shape its own future template rather than stretching this one.
- **React Router v7 in library mode.** Accepted: ubiquitous, stable, agent-familiar, and thin enough that the whole routing surface is one declared table in `app/router.tsx`.

## Decision

Routing is React Router v7 in library mode. The route table is declared once in `app/router.tsx` with `createBrowserRouter`, the basename follows Vite's base so subpath deploys work unchanged, and the auth guard is a layout route. The routing layer stays deliberately thin, so replacing the router touches the app layer and nothing below it.

## Consequences

Any React developer or agent can extend the routes without learning a second idiom, and no codegen step enters the toolchain. The cost is typed-route safety left on the table; params arrive as strings and are guarded by hand, as the vessel detail page does. A derived project whose URL state grows central should revisit this record and may supersede it with TanStack Router, which the thin routing layer makes cheap.
