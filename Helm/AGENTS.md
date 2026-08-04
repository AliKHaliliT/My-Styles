# Helm Agent Guide

Helm is a strict, AI-ready template for client-side web applications (React, Vite, TypeScript), demonstrated on a harbormaster console for the fictional Port of Saltmere. It is a style template and living blueprint, not a production deployment: some gaps (test breadth, the absence of a real backend) are intentional, so do not "fix" them unprompted.

## Commands

- Install: `npm install` (Node 20.19+; also regenerates the untracked msw worker in `public/`)
- Run the offline demo: `npm run dev` (sign in with username "harbormaster", password "saltmere")
- Build: `npm run build`
- Preview the build: `npm run preview`
- Test: `npm test`
- Lint: `npm run lint`
- Type-check: `npm run typecheck`

## Hard rules

- The layer rule is absolute: imports point downward through `app -> pages -> features -> entities -> shared`, never up or sideways. A slice is entered only through its `index.ts` (tests excepted), same-layer slices never import each other, and `src/mocks` is imported only by the bootstrap and the test setup.
- All HTTP goes through `shared/api`'s `request` with a zod schema; components never call `fetch`, and raw DTOs never leave their entity slice untranslated.
- Server data lives in the TanStack Query cache only, keyed in each entity's `queries.ts`; never copy query data into a store. Client state (session, theme, drafts, filters) lives in small Zustand stores or component state.
- Colors and status tones come only from the token utilities defined in `src/app/styles/tokens.css` (`bg-surface`, `text-ink`, `text-signal`, and so on); raw palette classes are off limits.
- The environment is read only through `shared/config`; no other module touches `import.meta.env`.
- Follow the doc-comment convention in the [README's Conventions section](README.md#conventions) and the documentation rules in [docs/CONVENTIONS.md](docs/CONVENTIONS.md); the latter is frozen and must not be edited.
- No em dashes anywhere: code, doc comments, documentation, commit messages, UI copy.
- All prose must read as if a person wrote it. Never write the clause-colon splice, a sentence shaped as claim, colon, elaboration; in prose a colon may only introduce a list, a quote, or a label. The softer language-model tells (balanced semicolon antitheses, triadic lists, not-X-but-Y reversals) are fine one at a time and forbidden stacked, so allow at most one flourish per paragraph and keep the rest plain declarative sentences.
- Every tracked byte is public prose. Confidential facts, private repository names, deployment details, and the description of what was withheld and why never enter a tracked file or a commit message, even in a private repository, because visibility can flip and history is permanent. Such context goes to the untracked `LOCAL.md` at the root (see [docs/BASELINE.md](docs/BASELINE.md)); read it when it exists, create it when first needed, and when unsure whether a fact is sensitive, ask the owner instead of recording it.
- Read [STATE.md](STATE.md) before starting work; update it when the state changes.

## Documentation index

This is the single index of the project's technical documentation. A document that is not listed here does not exist as far as this project is concerned: when you create a document, register it here in the same change; when you remove one, delist it here.

| Document | What it is and when to read it |
| --- | --- |
| [README.md](README.md) | Human-facing overview: philosophy, structure, setup, and the doc-comment convention. |
| [STATE.md](STATE.md) | Living project state (Now / Next / Deferred / Blocked). Read first, always. |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | The annotated map of the whole template. Read before any structural change. |
| [docs/CONVENTIONS.md](docs/CONVENTIONS.md) | The documentation rulebook: document species, schemas, naming. Frozen; do not edit. Read before writing or changing any documentation. |
| [docs/BASELINE.md](docs/BASELINE.md) | The repository baseline: always-present files, never-tracked files, and their modification rules. Read before adding, removing, or reshaping root-level or dot files. |
| [docs/decisions/](docs/decisions/) | Immutable decision records holding the project's "why". Read the relevant record before revisiting a settled topic; never edit an accepted record. |

There are no assistant-specific instruction files: every assistant reads this file directly. If a tool genuinely cannot read AGENTS.md, give it a one-line shim that imports or points to this file and nothing more.
