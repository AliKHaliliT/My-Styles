# 0003. Build the client as one-way sliced layers

Status: Accepted
Date: 2026-08-03

## Context

Client codebases drift structurally faster than servers, because nothing in the React ecosystem enforces where a file goes. The common failure modes are technical-type folders whose `utils/` and `components/` become dumping grounds, and feature folders whose slices import each other freely until every change touches everything. AI agents amplify whichever convention they can pattern-match, so the template needs a placement rule an agent can apply locally, without reading the whole tree, and a boundary rule that makes drift visible in the import path itself.

## Options considered

- **Technical-role folders** (`components/`, `hooks/`, `utils/`). Rejected: they say where a file's kind lives, not where its subject lives, so cohesion decays and cross-imports go unchecked by construction.
- **Atomic design.** Rejected: it organizes only the UI kit, by visual granularity, and says nothing about data, state, or boundaries, which is where client drift actually happens.
- **Full Feature-Sliced Design**, all six layers with the segment liturgy. Rejected: the widgets layer and the mandated per-slice segment taxonomy add ceremony a template of this size cannot justify; the discipline is what earns its keep, not the liturgy.
- **Five one-way layers with slice public APIs**, derived from Feature-Sliced Design. Accepted.

## Decision

The client is five layers, `app`, `pages`, `features`, `entities`, and `shared`, with imports pointing strictly downward and never sideways. Each slice exposes its public surface through an `index.ts` and is entered only through it, deep imports being reserved for the slice itself and for tests. Same-layer slices do not import each other; a concern spanning two slices moves up a layer, so a bare mutation button stays in a page while an interaction with validation, orchestration, or cross-entity effects earns a feature slice. `src/mocks` stands outside the stack the way a real backend would. Feature-Sliced Design is credited as the source of the layer discipline; this template does not claim full FSD compliance.

## Consequences

Placement is decidable locally: name the subject, name the layer, and the path follows. Boundary violations are visible in any diff as an upward or sideways import. The rule is enforced by review for now; a boundary linter can be added if violations recur, and that step is tracked in STATE.md. The cost is ceremony at the edges, since even a small slice carries an `index.ts`, and the occasional judgment call over whether an interaction has earned feature status.
