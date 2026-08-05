# Helm Agent Guide

Helm is a strict, AI-ready template for client-side web applications (React, Vite, TypeScript), demonstrated on a harbormaster console for the fictional Port of Saltmere. It is a style template and living blueprint rather than a production deployment, so some gaps are intentional and must not be "fixed" unprompted. Here those are the suites, which pin the seams rather than covering the surface, and the backend, which is answered by an in-browser mock instead of a server. STATE.md holds the current list.

## Commands

- Install: `npm install` (Node 20.19+; also regenerates the untracked msw worker in `public/`)
- Run the offline demo: `npm run dev` (sign in with username "harbormaster", password "saltmere")
- Test: `npm test`
- Lint: `npm run lint`
- Type-check: `npm run typecheck` (it runs `tsc -b`, because the root tsconfig is solution-style and a plain `tsc --noEmit` would check nothing)
- Build: `npm run build`
- Preview the build: `npm run preview`

## Hard rules

- The layer rule is absolute: imports point downward through `app -> pages -> features -> entities -> shared`, never up or sideways. A slice is entered only through its `index.ts` (tests excepted), same-layer slices never import each other, and `src/mocks` is imported only by the bootstrap and the test setup.
- All HTTP goes through `shared/api`'s `request` with a zod schema; components never call `fetch`, and raw DTOs never leave their entity slice untranslated.
- Server data lives in the TanStack Query cache only, keyed in each entity's `queries.ts`; never copy query data into a store. Client state (session, theme, drafts, filters) lives in small Zustand stores or component state.
- Colors and status tones come only from the token utilities defined in `src/app/styles/tokens.css` (`bg-surface`, `text-ink`, `text-signal`, and so on); raw palette classes are off limits.
- The environment is read only through `shared/config`; no other module touches `import.meta.env`.
- Test suites live in `tests/`, mirroring the source tree, one suite named after the unit it covers. A collaborator is replaced only at an architectural seam, by the MSW handlers answering at the wire boundary or a hand-written fake satisfying the contract it stands in for; never `vi.mock` a module's internals, because a test bound to an implementation voids the substitutability the layering exists to provide. No coverage threshold is imposed, so breadth stays a judgment call while the placement and substitution rules do not. The shape is mapped in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md#testing).
- Follow the doc-comment convention in the [README's Conventions section](README.md#conventions) and the documentation rules in [docs/CONVENTIONS.md](docs/CONVENTIONS.md); the latter is frozen and must not be edited.
- The documentation rulebook is owned by the style. [docs/CONVENTIONS.md](docs/CONVENTIONS.md) changes only inside the template itself, in the My-Styles repository and by its owner; a project derived from this template never edits its copy and never diverges from it. A derived project that believes a rule is wrong or missing sends the case upstream instead (see [The upstream report](#the-upstream-report)).
- No em dashes anywhere: code, doc comments, documentation, commit messages, UI copy.
- All prose must read as if a person wrote it. Never write the clause-colon splice, a sentence shaped as claim, colon, elaboration; in prose a colon may only introduce a list, a quote, or a label. The softer language-model tells (balanced semicolon antitheses, triadic lists, not-X-but-Y reversals) are fine one at a time and forbidden stacked, so allow at most one flourish per paragraph and keep the rest plain declarative sentences.
- Every tracked byte is public prose. Confidential facts, private repository names, deployment details, and the description of what was withheld and why never enter a tracked file or a commit message, even in a private repository, because visibility can flip and history is permanent. Such context goes to the untracked `LOCAL.md` at the root (see [docs/BASELINE.md](docs/BASELINE.md)); read it when it exists, create it when first needed, and when unsure whether a fact is sensitive, ask the owner instead of recording it.
- Read [STATE.md](STATE.md) before starting work; update it when the state changes.

## The upstream report

This template is the style's single statement of its form, and it only stays that way if improvements flow back to it. When a refactor against this template surfaces something the template itself should have had, the improvement belongs in the template first and in the refactored project second; an improvement kept privately by one child is a quiet fork of the style.

The order is strict:

1. **Finish the refactor as specified.** The report comes after the template has been properly implemented, never instead of finishing.
2. **Qualify every candidate.** An improvement earns an entry only if it is genuinely better rather than differently shaped, the template does not already have it, and [docs/decisions/](docs/decisions/) shows no record of it being considered and rejected. Read the decision records before writing anything; a rejected idea returning without new evidence is noise, and a report invented to satisfy this section when nothing real was found is worse than no report.
3. **Write each entry as a hand-off.** One entry per improvement, self-contained enough to be pasted verbatim to an agent or handed to the template's maintainer and acted on with no other context. Each entry states what the improvement is, how the refactor surfaced it, why it is believed better than what the template does today, and that the decision records were checked and hold no prior ruling. Each entry ends by telling the receiver to verify the claim with proper research-backed grounding before adopting it, because the report is a lead, not a verdict.
4. **Apply upstream first, then align.** The improvement lands in the template before the child keeps it. Integrating it there often refines it further, so afterwards run a manual final alignment check on the refactored project, confirming it carries the upstream form of each improvement rather than the draft it started from.

Every report opens by saying why the reader is seeing it. The style's owner uses the report to point an agent at the template and improve it directly. Anyone else is holding it because this template is open source, and the right move is to file the report as an issue on the template's repository so the improvement reaches everyone who builds on the style.

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
