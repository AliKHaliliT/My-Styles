# Helm

![License](https://img.shields.io/github/license/AliKHaliliT/My-Styles) ![Last Commit](https://img.shields.io/github/last-commit/AliKHaliliT/My-Styles) ![Open Issues](https://img.shields.io/github/issues/AliKHaliliT/My-Styles)

A Strict, AI-Ready Template for Client-Side Web Applications.

Helm is the client-side sibling of [ArchetypeCore](https://github.com/AliKHaliliT/My-Styles/tree/main/ArchtypeCore) (the server) and [Keel](https://github.com/AliKHaliliT/My-Styles/tree/main/Keel) (the package). It is a highly structured single-page application template built with React 19, TypeScript, Vite, TanStack Query, Zustand, zod, and Tailwind, and it builds to plain static files any host can serve. It is designed as **one-way sliced layers**, after [Feature-Sliced Design](https://feature-sliced.design/)'s layer discipline, with a guarded hexagonal wire boundary and a strict split between the server cache and client state.

## The Philosophy: Why Does This Exist?

Client codebases drift structurally faster than anything else in a stack, because nothing in the ecosystem enforces where code goes. Fetch calls scatter through components, server responses get copied into global stores and rot there, colors get hardcoded past the design system, and the folder tree decays into dumping grounds. AI assistants amplify all of it, since they extend whatever pattern they can see.

Helm was built to mitigate this. By enforcing explicit boundaries (one-way layers, schema-checked responses, translators at the wire, a cache that is not a store), it provides a strict structural foundation that guides AI agents (and developers) toward writing decoupled, maintainable clients. An assistant extends whatever pattern it can see, so a tree whose every seam already shows the right pattern makes the next generated slice, query hook, or translator far more likely to land inside it.

The structure is general-purpose. Dashboards, SaaS frontends, internal tools, and browser utilities all share this skeleton, with routing declared in one place, data entering through a guarded boundary, and state split by who owns it. The demo domain sits on top and peels off cleanly.

## The Domain Example: Why a Harbormaster Console?

Many frontend templates use a to-do list, which is too small to force the architecture to show its seams.

Helm implements the console of a small fictional harbor, the Port of Saltmere: sign in as the harbormaster, watch the fleet, schedule arrivals, and record departures. The domain is deliberately modest, but it exercises every seam a real client application has:

- **Authentication:** a login flow, a guarded route tree, bearer tokens injected at the boundary, and automatic sign-out when the backend answers 401.
- **Server State:** lists and detail views served from the query cache, mutations that invalidate exactly the right keys, and a cross-entity effect (a departure frees a berth) that shows where such logic belongs.
- **Async Reality:** pending, error, empty, and success as first-class rendering states, plus a wire-contract failure mode for backends that answer with the wrong shape.
- **Forms:** schema-validated input with field-level messages and backend rejections surfaced under the form.

> **Disclaimer on the Demo Backend:**
> The harbor office is an in-browser mock (MSW) with realistic latency, auth, and errors. It exists so the template runs fully offline and so the tests exercise the real wire path. It guards nothing; the demo credentials are public by design.

---

## Core Architectural Pillars

Helm enforces one-way dependencies: layers import downward, never up or sideways.

1. **One-Way Sliced Layers**
   The client is five layers (`app`, `pages`, `features`, `entities`, `shared`), each sliced by subject. A slice is entered only through its `index.ts` public API, same-layer slices never import each other, and a concern spanning two slices moves up a layer. Placement is decidable locally, and violations are visible in any diff as an upward or sideways import.
2. **A Guarded Wire Boundary**
   Nothing outside `shared/api` calls `fetch`. Every response body is validated against a zod schema at the boundary, then translated from wire shapes (snake_case, ISO strings) into domain models (camelCase, real `Date` objects). A payload that breaks the contract becomes a typed `WireContractError` instead of a mystery crash three components later.
3. **Server Cache Is Not App State**
   Server data lives in the TanStack Query cache, keyed and invalidated through each entity's exported keys. Client state exists only for what the client owns (the session, the theme, drafts, filters) in small Zustand stores or component state. Copying query data into a store is against the rules.
4. **A Deterministic Offline Demo**
   The default mode answers all HTTP from an in-browser mock backend with latency, auth, and errors, so a fresh clone runs with no network, no account, and no setup. Flipping `VITE_API_MODE=live` points the same client at a real backend without touching client code, and the tests keep running against the mock either way.

---

## Project Structure

```text
helm/
├── src/
│   ├── app/                    # Composition root: bootstrap, providers, router, chrome, tokens
│   ├── pages/                  # One slice per route; pages compose, they do not own logic
│   ├── features/               # Interactions with logic of their own (auth, forms, departure)
│   ├── entities/               # Domain nouns: model, wire schemas, translators, queries
│   ├── shared/                 # The base: api client, config, ui kit, lib, test helpers
│   └── mocks/                  # The pretend backend (MSW); outside the layer stack
│
├── tests/                      # Vitest suites mirroring the src structure
├── scripts/                    # Tracked repository tooling (the docs audit)
├── docs/                       # Technical documentation (the annotated map lives at docs/ARCHITECTURE.md)
├── AGENTS.md                   # Agent entry point and the documentation index
├── STATE.md                    # Living project state
└── package.json                # Scripts, dependencies, and the msw worker directory
```

---

## Key Features

- **Schema-Checked Responses:** every response body is parsed with zod before the app sees it, so a drifting backend fails loudly at the boundary.
- **Four-State Rendering:** the `QueryState` component renders pending, error (with retry), empty, and success once, so pages never re-implement the ladder.
- **Session Discipline:** a guarded route tree, tokens injected into the client at bootstrap through dependency inversion, and cache-level hooks that sign out on any 401, query or mutation, because a rejected call means the session died server-side.
- **Token-Owned Theming:** every color is a CSS variable mapped into Tailwind utilities, with dark and light themes switched by one root attribute.
- **Typed Environment:** exactly one module reads `import.meta.env`; everything else imports a frozen, typed object.
- **Test Seams Included:** the same mock handlers serve the browser demo and the Node test server, and the suites pin the translators, the query hooks, the client's failure modes, and a form end to end.

---

## Getting Started

### 1. Local Development

Ensure you have Node.js 24+ installed.

```bash
# Clone the repository
git clone https://github.com/AliKhaliliT/YOUR_REPO.git
cd helm

# Install dependencies (also generates the msw worker into public/)
npm install

# Run the offline demo
npm run dev
```

Sign in with username `harbormaster` and password `saltmere`.

### 2. Checks

```bash
npm test           # Vitest suites against the mock backend
npm run lint       # ESLint
npm run typecheck  # tsc -b
npm run build      # Type-check plus production build to dist/
```

### 3. Pointing at a Real Backend

Create a `.env.local` (see `.env.example`):

```bash
VITE_API_MODE=live
VITE_API_BASE_URL=https://api.your-backend.example
```

The client code does not change. The mock backend stays in the tree, because the test suite runs against it regardless of mode.

### 4. Co-Hosting Inside an ArchetypeCore Image

The same build also ships inside an [ArchetypeCore](https://github.com/AliKHaliliT/My-Styles/tree/main/ArchtypeCore) server when one deploy unit is wanted. The server copies `dist/` into its `app/static/` and mounts it under a prefix such as `/dashboard` with single-page fallback, while its API keeps `/api/v1`, so set `VITE_API_BASE_URL` to the relative `/api/v1` and the client shares the server's origin with no CORS and plain cookies. A multi-stage Dockerfile builds this project in one stage and copies `dist/` into the server image in the next. This tree stays under its own law either way; the server serves the artifact and never imports the source.

---

## Conventions

The project's conventions live in one place, the rulebook at [docs/CONVENTIONS.md](docs/CONVENTIONS.md). It holds the documentation system (a vendor-neutral [AGENTS.md](AGENTS.md) as the agent entry point and the single index of every document, [STATE.md](STATE.md) as the living project state, [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) as the current map, and immutable decision records under [docs/decisions/](docs/decisions/) as the reasoning behind every settled choice), the doc-comment convention in its code-level section, and the prose law in its Prose section. That file is normative and must not be modified; the rationale behind the system itself is recorded in the style's founding decision record, 0001.

The rulebook is owned at the style level. A project built from this template never changes it locally, and an improvement discovered while refactoring against the template is not kept as a private advantage; [AGENTS.md](AGENTS.md) describes the upstream report that carries it back to the template, where it is verified and, if it holds, adopted for every project that follows the style.

---

## License

This work is under an [MIT](https://choosealicense.com/licenses/mit/) License.
