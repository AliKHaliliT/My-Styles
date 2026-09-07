# 0042. Read a refusal's reason from the family's server envelope

Status: Accepted
Date: 2026-09-07

## Context

The client extracted a readable failure from a non-2xx body by reading a
string `message` field and otherwise falling back to the status text. The
demo's mock backend answered with exactly that field, so the template never
met a backend that states its refusal anywhere else. The family's own server
answers every error with `title`, `detail`, `status_code`, and `type`, the
reason living in `detail`, except for validation refusals, which list their
reasons under `detail` and keep the readable text in `title`. The treasury
had ruled that the UI beside that server is this template, and a project
pairing the two saw "Conflict" where the server had said why. The other
seam between the two, the login response, was left alone: the session object
here and the token pair there are demo-domain shapes, not a contract that
crosses every route.

## Decision

The client reads `detail`, then `message`, then `title`, taking the first
non-empty string, and the status line otherwise. The demo's mock backend
refuses in the family's envelope with the server's own titles and types, so
the primary path runs in the demo and `message` stays as the fallback for a
plainer backend. The client suite covers each envelope, the validation
shape, and a body that is not JSON.

## Options considered

- A single named constant for the field, adapted per child, was refused,
  because two siblings of one family should speak to each other without
  adaptation.
- Carrying the whole envelope on `ApiError` was refused as speculative; no
  consumer needs more than the status and the reason today.

## Consequences

Helm and ArchetypeCore talk out of the box, and a refusal's reason reaches
the person reading the screen.
