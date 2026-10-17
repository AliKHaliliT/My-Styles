# Helm Agent Guide

Helm is a strict, AI-ready template for client-side web applications (React, Vite, TypeScript), demonstrated on a harbormaster console for the fictional Port of Saltmere. It is a style template and living blueprint rather than a production deployment, so some gaps are intentional and must not be "fixed" unprompted. Here those are the suites, which pin the seams rather than covering the surface, and the backend, which is answered by an in-browser mock instead of a server. The permanent gaps are the ones named here; anything temporary appears in STATE.md. This guide, [docs/RULES.md](docs/RULES.md) and [docs/CONDUCT.md](docs/CONDUCT.md) are read to their ends before any work, and so are the rulebook, the gate, the state file, the map, the ledger and the baseline where the work touches what they govern; a document is read whole, never by its first and last lines, and the index below names every other document and when it is read.

## Documentation index

This is the single index of the project's technical documentation. A document that is not listed here does not exist as far as this project is concerned: when you create a document, register it here in the same change; when you remove one, delist it here.

| Document | What it is and when to read it |
| --- | --- |
| [README.md](README.md) | Human-facing overview: philosophy, structure, and setup. |
| [STATE.md](STATE.md) | Living project state (Now / Next / Deferred / Blocked). Read first, always. |
| [docs/RULES.md](docs/RULES.md) | The hard rules of the tree, what its code, checks and records must satisfy. Frozen; do not edit. Read whole before any work. |
| [docs/CONDUCT.md](docs/CONDUCT.md) | The hard rules of conduct, how a worker reads, writes, pauses, lands and speaks in this tree. Frozen; do not edit. Read whole before any work. |
| [docs/GATE.md](docs/GATE.md) | The delivery gate, the closed list a change is weighed against before it is delivered. Frozen; do not edit. Read before delivering any change. |
| [docs/ADOPTION.md](docs/ADOPTION.md) | Adopting this style, how an existing repository comes under the law and how a child re-aligns. Frozen; do not edit. Read when adopting or re-aligning. |
| [docs/REPORTING.md](docs/REPORTING.md) | The upstream report, what a project sends its template, in what shape, and how an entry is resolved. Frozen; do not edit. Read before writing an upstream entry. |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | The annotated map of the whole template. Read before any structural change. |
| [docs/INVARIANTS.md](docs/INVARIANTS.md) | What must stay true about the client, one row per claim with the holder that refuses a violation and the rung that says what its green is worth. Read before changing what the product promises; a change to a claim changes its row. |
| [docs/CONVENTIONS.md](docs/CONVENTIONS.md) | The documentation rulebook's core: document species, the spine, the index contract, naming and code-level documentation; its parts are the rows below. Frozen; do not edit. Read before writing or changing any documentation. |
| [docs/LIVING.md](docs/LIVING.md) | The rulebook's rules for living documents and the invariants ledger. Frozen; do not edit. Read before writing or changing a living document. |
| [docs/RECORDS.md](docs/RECORDS.md) | The rulebook's rules for decision records. Frozen; do not edit. Read before writing a record. |
| [docs/PROSE.md](docs/PROSE.md) | The prose law, the rulebook's rules for every tracked byte of prose. Frozen; do not edit. Read before writing prose. |
| [docs/BASELINE.md](docs/BASELINE.md) | The repository baseline: always-present files, never-tracked files, and their modification rules. Read before adding, removing, or reshaping root-level or dot files. |
| [docs/decisions/](docs/decisions/) | Immutable decision records holding the project's "why". Read the relevant record before revisiting a settled topic; never edit an accepted record beyond its status line and a dead link's target. |

There are no assistant-specific instruction files. Every assistant reads this file directly. If a tool genuinely cannot read AGENTS.md, give it a one-line shim that imports or points to this file and nothing more.

## Commands

- Install: `npm install` (Node 24+; also regenerates the untracked msw worker in `public/`)
- Run the offline demo: `npm run dev` (sign in with username "harbormaster", password "saltmere")
- Test: `npm test`
- Lint: `npm run lint` (ESLint holds the layer rule and the function-shape limits; never auto-fix `jsdoc/require-jsdoc`; its generated stubs come out mangled, so doc comments are written by hand)
- Type-check: `npm run typecheck` (it runs `tsc -b`, because the root tsconfig is solution-style and a plain `tsc --noEmit` would check nothing)
- Docs: `npm run docs` (the living documents against the tree and the calendar)
- Prove the audit itself: `npm run docs:selftest` (every rule against a planted defect, because a check that never fires and a check that cannot fire look identical)
- Build: `npm run build`
- Preview the build: `npm run preview`

The checks report at two levels. A failure is a verdict, it stops the
command, and it means a rule the tool fully decides has been broken. A warning is
advice, it leaves the exit status clean, and it comes from a check that cannot
decide its own question and so is not allowed to gate. Advice is not noise and
not optional reading. Every warning is looked at and then either fixed or
dismissed in writing in the commit message of the change that produced it, so
the judgment outlives the run that asked for it, and a warning is never
silenced with a suppression comment to make a run look clean. A finding
printed on every run by design, like a review row of the invariants ledger,
was answered by the record that made it so and needs no repetition. The advisory checks here are the credential and regular-expression heuristics in the lint configuration, which guess from the shape of a string or a pattern and are wrong often enough that they cannot be a gate, the docs audit's vocabulary advisory, which reads an honest domain term the same as a tell and so advises for review, its spelling advisory, which runs where codespell is installed over the files git tracks and no other, reads the project's own terms from `.codespellignore`, and names itself as not run elsewhere, and its form advisory, which counts the references a prose paragraph names and cannot tell an enumeration from an argument, so it advises a list or a table and gates nothing. Its splice advisory names a colon that opens a lowercase clause in a record main does not hold yet, because a list colon and a spliced one look alike to a machine, and it falls silent once the record has landed, since a defect found in a merged record stays. A check the tree gave nothing to run is named as not run, with what it needs, so a clean verdict never hides a check that never looked.
