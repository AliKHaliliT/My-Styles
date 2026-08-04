# 0005. Run the demo against an in-browser mock backend

Status: Accepted
Date: 2026-08-03

## Context

A client template demonstrates nothing without a backend to talk to, but the family's demo philosophy, set by Keel's fully offline rule-based reasoner, is that the default experience must be deterministic, offline, and free of accounts. Those two pulls meet at the wire boundary, which is also exactly the seam the template exists to demonstrate, so whatever answers the demo's HTTP must exercise the real client path rather than bypass it.

## Options considered

- **A hosted demo API.** Rejected: it dies, drifts, costs money, and demands network and possibly keys from every person who clones the template.
- **Hardcoded fixtures imported directly by the query functions.** Rejected: it bypasses the HTTP client, the zod schemas, and the translators, which is the entire boundary under demonstration, and it leaves auth and error states undemonstrable.
- **Vite dev-server middleware.** Rejected: it exists only under the dev server, so the preview build and the test runner would each need a second fake backend.
- **MSW, one handler set for the browser worker and the node test server.** Accepted: the client sends real HTTP through its full stack, the same handlers serve dev, preview, and tests, and requests stay visible in the browser's network tab.

## Decision

The demo backend is MSW. Handlers and the seeded in-memory state live in `src/mocks`, speak wire shapes only (snake_case, ISO strings), enforce auth, inject latency, and answer with realistic errors; they share no types with the client's domain, because the translators are among the things under test. Mock mode is the default; `VITE_API_MODE=live` skips the worker and points the client at a real backend without touching client code. Tests always run against the node server, even in projects that have gone live.

## Consequences

`npm run dev` works on a fresh clone with no network, no account, and no setup, and every seam (auth, pending, error, empty, contract violation) is demonstrable and testable. The worker script is regenerated into `public/` on install and stays untracked. The demo credentials are public by design and guard nothing. The cost is a pretend backend to maintain beside the real contract in derived projects, which the test suite's dependence on it repays.
