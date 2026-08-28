# Architecture

This arrow follows Keel's Hexagonal Architecture (Ports and Adapters) shape and enforces Clean Architecture's Dependency Rule with import-linter; the reasoning behind the shape lives in the inherited decision records, [0004](decisions/0004-describe-the-architecture-as-hexagonal.md) for the naming and [0005](decisions/0005-translate-only-outward-at-the-facade-boundary.md) for the boundary. The domain holds the two rounding strategies as pure functions, the service accumulates a stream under a strategy, and the facade runs the deterministic experiment and answers through its own schemas, translated outward so no inner layer's object crosses the public surface.

Two layout conventions hold throughout, as in Keel. Every directory contains **either** subpackages **or** modules, never a mix, with the package root as the sole exception, and an `__init__.py` appears **only** where it re-exports, so the grouping directories are bare namespace packages.

```text
coinwise/
├── AGENTS.md                   # Agent entry point and the single documentation index
├── pyproject.toml              # PEP 621 metadata, build backend, tool config
├── README.md                   # Project documentation and setup guide
├── STATE.md                    # Living project state (Now / Next / Deferred / Blocked)
│
├── docs/                       # Technical documentation (indexed in AGENTS.md)
│   ├── ARCHITECTURE.md         # This file; the annotated map of the arrow
│   ├── BASELINE.md             # The repository baseline (always-present files and their rules)
│   ├── CONVENTIONS.md          # The documentation rulebook (frozen; do not edit)
│   └── decisions/              # Immutable decision records, inherited from Keel and appended locally
│
├── scripts/
│   └── audit_docs.py           # The Docs command; checks the living documents mechanically
│
├── src/                        # The src layout; prevents importing the uninstalled tree
│   └── coinwise/               # The installable package
│       ├── __init__.py         # Curated public surface
│       ├── py.typed            # PEP 561 marker; ships the package as typed
│       │
│       ├── domain/             # Absolute source of truth: business logic (no frameworks)
│       │   └── rounding/       # The two strategies and the tie test they disagree on
│       │
│       ├── services/           # Business logic orchestration
│       │   └── accumulation/   # Summing a stream twice and measuring the drift
│       │
│       └── facade/             # Public surface: what an embedding caller touches
│           ├── experiment/     # The deterministic grid and the one-call experiment
│           ├── schemas/        # The public report records
│           └── translators/    # Flatten service results into the public reports (outbound only)
│
└── tests/                      # Automated test suite (mirrors the src structure)
    └── src/coinwise/           # One suite per unit at its mirrored path, plus the citizenship suite test_package.py
```

## Testing

Suites live in `tests/`, mirroring the source tree, one suite named after the unit it covers. Nothing here is substituted, because every collaborator is deterministic and runs in process, so each suite composes the real thing. The seam rule stands unchanged for the day a port reaches outside; a collaborator is then replaced only by a hand-written fake satisfying the port it stands in for, never by patching a module's internals, since a test bound to an implementation voids the substitutability the ports exist to provide. No coverage threshold is imposed, so breadth stays a judgment call while placement and substitution do not.
