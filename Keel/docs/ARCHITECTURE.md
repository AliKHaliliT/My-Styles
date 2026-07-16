# Architecture

This project follows a strict Clean Architecture and Domain-Driven Design (DDD) pattern, adapted to the shape of an installable Python package. The core business logic (`domain` and `services`) is completely isolated from the public surface (`facade`) and the concrete implementations (`adapters`).

Two layout conventions hold throughout the package. First, every directory contains **either** subpackages **or** modules, never a mix; the package root is the sole exception, because Python requires `__init__.py`, `__main__.py`, and the PEP 561 `py.typed` marker to live there beside the layer packages. Second, an `__init__.py` appears **only** where it does real work (re-exporting a subpackage's public names), so the grouping directories are bare [namespace packages](https://peps.python.org/pep-0420/) with no `__init__.py` at all.

A `translators/` package marks a layer boundary: the public-schema-to-domain bridge in `facade/`, mirroring ArchetypeCore's `api/` and `repositories/` translator layers. A leaf adapter's own translation (for example the Anthropic provider's domain-to-wire mapping) instead lives as plain modules beside it, never in a nested `translators/` folder.

```text
my_package/
├── AGENTS.md                   # Agent entry point and the single documentation index
├── CHANGELOG.md                # Curated per-release change summary for consumers
├── pyproject.toml              # PEP 621 metadata, build backend, extras, entry points, tool config
├── README.md                   # Project documentation and setup guide
├── STATE.md                    # Living project state (Now / Next / Deferred / Blocked)
│
├── docs/                       # Technical documentation for maintainers and agents (indexed in AGENTS.md)
│   ├── ARCHITECTURE.md         # This file; the annotated map of the template
│   ├── BASELINE.md             # The repository baseline (always-present files and their rules)
│   ├── CONVENTIONS.md          # The documentation rulebook (frozen; do not edit)
│   └── decisions/              # Immutable decision records; the project's "why" log
│
├── local_util_resources/       # Internal development and repository management scripts
│
├── src/                        # The src layout; prevents importing the uninstalled tree
│   └── keel/                   # The installable package (rename to your package name)
│       ├── __init__.py         # Curated public surface and __version__ resolution
│       ├── __main__.py         # `python -m keel` delegation to the CLI
│       ├── py.typed            # PEP 561 marker; ships the package as typed
│       │
│       ├── facade/             # Public surface: the simplified entry point consumers touch
│       │   ├── engine/         # Engine facade + EngineBuilder (guarded fluent construction)
│       │   ├── cli/            # Argparse CLI wired to the console script and __main__
│       │   ├── schemas/        # Pydantic models for public request/response payloads
│       │   └── translators/    # Bridge public schemas <-> domain schemas (both ways)
│       │
│       ├── core/               # Package-wide infrastructure and configuration
│       │   ├── config/         # EngineConfig (frozen Pydantic model; no env at import)
│       │   ├── logging/        # Package logger with NullHandler (library citizenship)
│       │   └── plugins/        # Entry-point discovery for third-party tools
│       │
│       ├── domain/             # Absolute source of truth: business logic (no frameworks)
│       │   ├── exceptions/     # Pure Python domain-level exceptions
│       │   ├── interfaces/     # Protocols (IReasoner, ITool, IMemory, IEventSink, ...)
│       │   └── schemas/        # Domain models (actions, runs, steps, tools, events)
│       │
│       ├── adapters/           # Concrete implementations of the domain interfaces
│       │   ├── events/         # Event sinks (logging, collecting)
│       │   ├── memory/         # Memory stores (in-memory)
│       │   ├── reasoners/      # One subpackage per reasoner implementation
│       │   │   ├── rule_based/ # Deterministic, fully offline default reasoner
│       │   │   └── anthropic/  # LLM adapter (behind the `anthropic` extra) + translators
│       │   ├── registry/       # ToolRegistry; duplicate-safe registration and lookup
│       │   └── tools/          # Built-in demo tools (calculator, word_count, clock)
│       │
│       └── services/           # Business logic orchestration (coordinates the ports)
│           └── execution/      # AgentRunner; the bounded reason -> act -> record loop
│
└── tests/                      # Automated test suite (mirrors the src structure)
    └── src/
        └── keel/
```
