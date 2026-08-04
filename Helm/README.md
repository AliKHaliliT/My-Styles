# Helm

![License](https://img.shields.io/github/license/AliKHaliliT/My-Styles) ![Last Commit](https://img.shields.io/github/last-commit/AliKHaliliT/My-Styles) ![Open Issues](https://img.shields.io/github/issues/AliKHaliliT/My-Styles)

A Strict, AI-Ready Template for Client-Side Web Applications.

Helm is the client-side sibling of [ArchetypeCore](https://github.com/AliKHaliliT/My-Styles/tree/main/ArchtypeCore) (the server) and [Keel](https://github.com/AliKHaliliT/My-Styles/tree/main/Keel) (the package). It is a highly structured single-page application template built with React 19, TypeScript, Vite, TanStack Query, Zustand, zod, and Tailwind, and it builds to plain static files any host can serve. It is designed as **one-way sliced layers**, after [Feature-Sliced Design](https://feature-sliced.design/)'s layer discipline, with a guarded hexagonal wire boundary and a strict split between the server cache and client state.

## The Philosophy: Why Does This Exist?

Client codebases drift structurally faster than anything else in a stack, because nothing in the ecosystem enforces where code goes. Fetch calls scatter through components, server responses get copied into global stores and rot there, colors get hardcoded past the design system, and the folder tree decays into dumping grounds. AI assistants amplify all of it, since they extend whatever pattern they can see.

Helm was built to mitigate this. By enforcing explicit boundaries (one-way layers, schema-checked responses, translators at the wire, a cache that is not a store), it provides a strict structural foundation that guides AI agents (and developers) toward writing decoupled, maintainable clients. Because AI systems excel at pattern recognition, providing a solid structure from the beginning ensures that even when adding large architectural components, the agent is highly likely to follow the established conventions.

The structure is general-purpose. Dashboards, SaaS frontends, internal tools, and browser utilities all share this skeleton, with routing declared in one place, data entering through a guarded boundary, and state split by who owns it. The demo domain sits on top and peels off cleanly.

## The Domain Example: Why a Harbormaster Console?

Many frontend templates use a to-do list, which is too small to force the architecture to show its seams.

Helm implements the console of a small fictional harbor, the Port of Saltmere: sign in as the harbormaster, watch the fleet, schedule arrivals, and record departures. The domain is deliberately modest, but it exercises every seam a real client application has:

- **Authentication:** a login flow, a guarded route tree, bearer tokens injected at the boundary, and automatic sign-out when the backend answers 401.
- **Server State:** lists and detail views served from the query cache, mutations that invalidate exactly the right keys, and a cross-entity effect (a departure frees a berth) that shows where such logic belongs.
- **Async Reality:** pending, error, empty, and success as first-class rendering states, plus a wire-contract failure mode for backends that answer with the wrong shape.
- **Forms:** schema-validated input with field-level messages and backend rejections surfaced under the form.

> ⚠️ **Disclaimer on the Demo Backend:**
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
├── docs/                       # Technical documentation (the annotated map lives at docs/ARCHITECTURE.md)
├── AGENTS.md                   # Agent entry point and the documentation index
├── STATE.md                    # Living project state
└── package.json                # Scripts, dependencies, and the msw worker directory
```

---

## Key Features

- **Schema-Checked Responses:** every response body is parsed with zod before the app sees it, so a drifting backend fails loudly at the boundary.
- **Four-State Rendering:** the `QueryState` component renders pending, error (with retry), empty, and success once, so pages never re-implement the ladder.
- **Session Discipline:** a guarded route tree, tokens injected into the client at bootstrap through dependency inversion, and a cache-level hook that signs out on any 401.
- **Token-Owned Theming:** every color is a CSS variable mapped into Tailwind utilities, with dark and light themes switched by one root attribute.
- **Typed Environment:** exactly one module reads `import.meta.env`; everything else imports a frozen, typed object.
- **Test Seams Included:** the same mock handlers serve the browser demo and the Node test server, and the suites pin the translators, the query hooks, the client's failure modes, and a form end to end.

---

## Getting Started

### 1. Local Development

Ensure you have Node.js 20.19+ installed.

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

---

## Conventions

Documentation follows **TSDoc**, carrying the family's docstring discipline into TypeScript. Every exported symbol opens with a one-sentence summary. Where a function warrants full documentation, `@param` (one per parameter) and `@returns` are always present, writing `Nothing.` for a void return, and `@throws` lists every error thrown directly in the function's own body, including the defensive guards; an error that merely propagates from a callee is documented on the callee, and the absence of `@throws` on a fully documented function is itself the assertion that nothing is thrown directly. Complex components and services carry an `@example` block with a minimal, runnable snippet, serving the role the family's `Usage` section serves in Python.

Not everything is documented that heavily, by design. Thin mappers such as the translators keep a one-line summary, page components carry a single sentence stating what they compose, and props are documented as field comments on the props interface rather than in a tag block. The boundary is documented in full where its failure modes live, so `shared/api` states both wire failures and each entity segment says what it fetches and translates.

The rest of the TSDoc vocabulary is used where it fits and omitted where it does not: a caveat becomes a `@remarks` block rather than a loose sentence, cross-references use `@see`, defaults use `@defaultValue`, and retirement uses `@deprecated`. Tags you do not see are simply not called for by that code; generated code should add them as it introduces the behavior.

Beyond doc comments, the project's technical documentation is governed by a fixed documentation system: a vendor-neutral [AGENTS.md](AGENTS.md) serves as the agent entry point and the single index of every document, [STATE.md](STATE.md) tracks the living project state, [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) holds the current map of the system, and immutable decision records under [docs/decisions/](docs/decisions/) hold the reasoning behind every settled choice. The full rulebook, including the split between living documents and records and the writing rules for each species, lives in [docs/CONVENTIONS.md](docs/CONVENTIONS.md); that file is normative and must not be modified. The rationale behind the system itself is recorded in [its founding decision record](docs/decisions/0001-adopt-the-documentation-system.md).

Both the rulebook and the conventions above are owned at the style level. A project built from this template never changes them locally, and an improvement discovered while refactoring against the template is not kept as a private advantage; [AGENTS.md](AGENTS.md) describes the upstream report that carries it back to the template, where it is verified and, if it holds, adopted for every project that follows the style.

One further rule applies to every piece of prose in the project, from this README through doc comments to commit messages. Everything must read as if a person wrote it. The clearest machine tell is the clause-colon splice, a sentence shaped as claim, colon, elaboration; no human writes that way outside a slide deck, so in prose a colon may only introduce a list, a quote, or a label. Softer tells, such as a balanced semicolon antithesis or a neat triadic list, are each fine on their own but give the text away when stacked, because a paragraph of polished epigrams reads as machine writing even when every sentence would pass alone. Allow at most one such flourish per paragraph and write the rest as plain declarative sentences.

---

## License

This work is under an [MIT](https://choosealicense.com/licenses/mit/) License.
