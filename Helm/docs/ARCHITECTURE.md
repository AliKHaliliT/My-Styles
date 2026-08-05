# Architecture

This project is a client-side single-page application built as one-way sliced layers, with a hexagonal wire boundary and a strict split between the server cache and client state. The layer discipline is derived from [Feature-Sliced Design](https://feature-sliced.design/); the reasoning behind the shape is recorded in [decision 0003](decisions/0003-build-the-client-as-one-way-sliced-layers.md).

## The layers and their one rule

Imports point downward, never up or sideways:

```text
app  ->  pages  ->  features  ->  entities  ->  shared
```

- **app** is the composition root: bootstrap, providers, the route table, the chrome, and the design tokens. It is the only layer allowed to know everything, and all cross-layer wiring (the token provider, the 401 sign-out) is tied here.
- **pages** compose a route's content from features, entities, and shared parts. Ephemeral UI state (a filter, a search box) lives here; logic does not.
- **features** are user interactions with logic of their own: auth, the schedule-arrival form, the departure action. A bare mutation button stays in a page; an interaction earns a feature slice when it carries validation, orchestration, or cross-entity effects.
- **entities** are the domain nouns. Each slice owns its model and pure logic, its wire schemas, its translators, and its query hooks. Raw DTOs never leave the slice.
- **shared** is the base: the HTTP client, typed env access, the UI kit, small libraries, and test helpers. It knows nothing about the layers above.

A slice is entered only through its `index.ts` public API; deep imports are reserved for the slice itself and for tests. Same-layer slices do not import each other; a concern spanning two slices moves up a layer, which is why the departure action is a feature. `src/mocks` stands outside the stack the way a real backend would, and only the bootstrap and the test setup may import it.

```text
helm/
├── AGENTS.md                   # Agent entry point and the single documentation index
├── README.md                   # Project documentation and setup guide
├── STATE.md                    # Living project state (Now / Next / Deferred / Blocked)
├── index.html                  # The single page; mounts src/app/main.tsx
├── package.json                # Manifest: scripts, dependencies, msw worker directory
├── vite.config.ts              # Build, the @ -> src alias, and Vitest configuration
├── eslint.config.js            # Flat ESLint configuration
├── tsconfig.json               # Solution file referencing the app and node configs
│
├── docs/                       # Technical documentation (indexed in AGENTS.md)
│   ├── ARCHITECTURE.md         # This file; the annotated map of the template
│   ├── BASELINE.md             # The repository baseline (always-present files and their rules)
│   ├── CONVENTIONS.md          # The documentation rulebook (frozen; do not edit)
│   └── decisions/              # Immutable decision records; the project's "why" log
│
├── public/                     # Static assets served as-is; holds the untracked msw worker after install
│
├── src/
│   ├── app/                    # Composition root (bootstrap, providers, router)
│   │   ├── layout/             # AppLayout, TopBar, and the theme store
│   │   └── styles/             # Tailwind entry and the design tokens
│   ├── pages/                  # One slice per route; pages compose, they do not own logic
│   ├── features/               # Interactions with logic of their own (auth, forms, departure)
│   ├── entities/               # Domain nouns (vessel, berth): model, wire, translators, queries
│   ├── shared/                 # The base: api, config, lib, ui, testing
│   └── mocks/                  # The pretend backend (MSW); outside the layer stack
│
└── tests/                      # Vitest suites mirroring the src structure
    └── src/
```

## The wire boundary

All HTTP goes through `shared/api`'s `request`, which attaches the bearer token, normalizes failures into `ApiError`, and validates every response body against a zod schema before anything else sees it; a payload that does not match becomes a `WireContractError` instead of a mystery crash three components later. Each entity keeps the boundary in three segments: `dto.ts` describes what the backend actually sends (snake_case, ISO strings), `translate.ts` reshapes it into the domain model (camelCase, real `Date` objects), and `api.ts` composes the two so callers only ever meet domain types. Outbound requests run the same path in reverse through the translators.

## Server cache versus client state

Server data lives in the TanStack Query cache and nowhere else; each entity defines its keys and hooks in `queries.ts`, and invalidation happens through those keys. Client state is only what the client owns (the session, the theme, form drafts, filters) and lives in small Zustand stores or component state. Copying query data into a store is against the rules; the reasoning is recorded in [decision 0004](decisions/0004-segregate-the-server-cache-from-client-state.md). Every consumer renders the cache's lifecycle through `QueryState`, so pending, error, empty, and success are handled once, not per page.

## The demo backend

In mock mode (the default) an MSW service worker answers the same HTTP the client would send anywhere else, with realistic latency, auth checks, and error responses; the handlers speak wire shapes only and share nothing with the client's domain types. Tests run the identical handlers through MSW's node server. Setting `VITE_API_MODE=live` skips the worker entirely and points the client at `VITE_API_BASE_URL`. The trade-offs are recorded in [decision 0005](decisions/0005-run-the-demo-against-an-in-browser-mock-backend.md).

## Theming

`src/app/styles/tokens.css` owns every color as a CSS variable, keyed on the root `data-theme` attribute and mapped into Tailwind utilities through the `@theme` block. Components use only token utilities (`bg-surface`, `text-ink`, `border-line`, `text-signal`, and the status tones); raw palette classes are off limits. The theme store applies the attribute, and `initTheme` runs at bootstrap so the first paint is already correct.

## Testing

Three rules hold however broad the suite is. Suites live in `tests/`, mirroring the source tree, one suite named after the unit it covers. A collaborator is replaced only at an architectural seam, by the MSW handlers answering at the wire boundary or a hand-written fake satisfying the contract it stands in for, never by mocking a module's internals, since a test bound to an implementation voids the substitutability the layering exists to provide. And no coverage threshold is imposed, because a percentage gate buys assertions that assert nothing, so breadth stays a judgment call while placement and substitution do not.

The suites are characterization tests pinning the seams: the translators (pure), the query hooks (against the mock backend), the HTTP client's failure modes (401 and a broken wire contract), the auth store, and the schedule-arrival form end to end. `tests/setup.ts` starts the node mock server, resets the pretend database between cases, and clears the token provider and storage so no test inherits another's session.
