# Architecture

This project follows a strict Hexagonal Architecture (Ports and Adapters), adapted to the shape of an installable Python package and enforcing Clean Architecture's Dependency Rule throughout. The domain holds deliberately plain data records and pure decision logic, with every piece of IO behind a port in the spirit of the functional-core school; the reasoning behind this naming is recorded in [decision 0004](decisions/0004-describe-the-architecture-as-hexagonal.md). The core business logic (`domain` and `services`) is completely isolated from the public surface (`facade`) and the concrete implementations (`adapters`).

Two layout conventions hold throughout the package. First, every directory contains **either** subpackages **or** modules, never a mix; the package root is the sole exception, because Python requires `__init__.py`, `__main__.py`, and the PEP 561 `py.typed` marker to live there beside the layer packages. Second, an `__init__.py` appears **only** where it does real work (re-exporting a subpackage's public names), so the grouping directories are bare [namespace packages](https://peps.python.org/pep-0420/) with no `__init__.py` at all.

A `translators/` package marks a layer boundary. In `facade/` it holds the outbound bridge that flattens domain results into the public report schemas; there is no inbound counterpart, because the facade builds domain schemas directly from the primitives its callers pass (see [decision 0005](decisions/0005-translate-only-outward-at-the-facade-boundary.md)). A leaf adapter's own translation (for example the Anthropic provider's domain-to-wire mapping) instead lives as plain modules beside it, never in a nested `translators/` folder.

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
│       │   ├── schemas/        # Pydantic models for the public report payloads
│       │   └── translators/    # Flatten domain results into the public reports (outbound only)
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
├── tests/                      # Automated test suite (mirrors the src structure)
│   └── src/
│       └── keel/
│           └── services/
│               └── execution/  # The loop's contract, with fakes at the outward ports
│
└── util_resources/             # Tracked repository assets
    └── readme/                 # Every image the repository embeds (logo, screenshots, figures)
```

## Testing

Three rules hold however broad the suite is. Suites live in `tests/`, mirroring the source tree, one suite named after the unit it covers. A collaborator is replaced only at an architectural seam, by a hand-written fake satisfying the port in `domain/interfaces` that it stands in for, never by patching a module's internals, since a test bound to an implementation voids the substitutability the ports exist to provide. And no coverage threshold is imposed, because a percentage gate buys assertions that assert nothing, so breadth stays a judgment call while placement and substitution do not.

`tests/src/keel/services/execution/test_agent_runner.py` is the worked example, and it shows the two ways a port pays off. The registry, the transcript, and the event sink are the shipped adapters, since each is already deterministic and runs in process, so a test composes the real thing. Only the reasoner and a tool are stood in for, because those are what reach a model and the outside world in production. The suite pins the loop's contract rather than its internals: a finish action completes the run and records one step, a tool result reaches the next decision, a failing tool becomes data unless the configuration says to halt, an unknown tool is reported without ending the run, the step budget bounds a reasoner that never stops, and a broken event sink never takes the run down.
