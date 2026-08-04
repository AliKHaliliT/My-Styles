# 0001. Adopt the documentation system

Status: Accepted
Date: 2026-08-03

## Context

Helm is the third template in the My-Styles family, after ArchetypeCore (the server) and Keel (the package), and the family's documentation system predates it. The system exists because earlier projects degraded in two recurring ways: append-only history files grew until they were unusable, and living overviews accumulated stale narration beside fresh fact. Being born under the system, Helm's question was not whether to document but whether to adopt the shared rulebook unchanged or adapt it to an application's shape.

## Options considered

- **Adopt the system with a changelog, as Keel did.** Rejected: a changelog is a record for consumers who upgrade through releases, and an application template has no such consumers; a changelog with no audience becomes a second history file.
- **Diverge from the family rulebook where an app differs.** Rejected: the species rules, the index contract, and the record format are stack-agnostic, so divergence would create differences without a difference.
- **Adopt the system unchanged, with the changelog trigger simply unfired.** Accepted.

## Decision

Adopt the documentation system specified in [CONVENTIONS.md](../CONVENTIONS.md): a vendor-neutral `AGENTS.md` as the agent entry point and the single documentation index, `STATE.md` for the living project state, `docs/ARCHITECTURE.md` as the living map of the system, and immutable decision records under `docs/decisions/` as the durable home of rationale, with per-species writing rules (living documents are rewritten in place and size-budgeted; records are dated and never edited). No `CHANGELOG.md` exists here, because nothing versions releases; a small "why" goes into the commit message body and a decision-shaping "why" becomes a decision record.

## Consequences

No document has a reason to grow without bound, rationale survives in a form both humans and agents can load selectively, and the entry point works across assistants instead of being tied to one vendor. The cost is discipline: the index must be maintained with every documentation change, the species rules must be respected, and superseding a decision means writing a new record rather than editing the old one. A derived project that does version releases adds `CHANGELOG.md` under the trigger in BASELINE.md.
