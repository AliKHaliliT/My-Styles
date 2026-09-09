# Keel

![License](https://img.shields.io/github/license/AliKHaliliT/My-Styles) ![Last Commit](https://img.shields.io/github/last-commit/AliKHaliliT/My-Styles) ![Open Issues](https://img.shields.io/github/issues/AliKHaliliT/My-Styles)

A Strict, AI-Ready Clean Architecture Template for Python Packages.

Keel is the package-side sibling of [ArchetypeCore](https://github.com/AliKHaliliT/My-Styles/tree/main/ArchtypeCore). It is a highly structured, installable Python package template built with Pydantic V2 and the modern packaging stack (PEP 621 `pyproject.toml`, src layout, PEP 561 typing). It is designed around **Hexagonal Architecture (Ports and Adapters)** and Clean Architecture's Dependency Rule, keeping the decision logic pure and pushing every piece of IO behind a port in the spirit of the **functional core, imperative shell** school.

## The Philosophy: Why Does This Exist?

A Python package might be a small utility, a client library, or a full runtime that hosts agents, orchestrates tools, and coordinates external providers. Whatever it is, it has to behave like a well-mannered library that other applications embed, and AI assistants suffer from the same **"Architecture Drift"** in packages as they do in services: leaking provider SDKs into business logic, configuring global state at import time, and coupling the public surface to internal representations.

Keel was built to mitigate this. By enforcing explicit boundaries (Translators, Protocols, a guarded Builder), it provides a strict structural foundation that guides AI agents (and developers) toward writing decoupled, maintainable packages. An assistant extends whatever pattern it can see, so a tree whose every seam already shows the right pattern makes the next generated port, adapter, or facade method far more likely to land inside it.

The structure is general-purpose. Domain logic lives in `domain` and `services`, concrete IO in `adapters`, and the public surface in `facade`, whatever kind of package rides that spine. It ships with an agent-engine demo not because the template is "for agents," but because an agent runtime exercises every seam the architecture defends; delete the demo domain and the skeleton is a rigorous general-purpose package template.

## The Domain Example: Why an Agent Engine?

Many package templates use a generic "string utils" or "image reader" example, which is too simple to demonstrate how an architecture handles real-world complexity.

To demonstrate the utility of Dependency Inversion, Keel implements the domain of an **Agent Engine**. Give it a goal, and it runs a bounded reason → act → record loop until the goal is met, a step limit is reached, or the run fails.

Managing an agent runtime forces the architecture to handle practical, complex problems:

- **Pluggable Intelligence:** The loop coordinates decisions through an abstract `IReasoner` interface. The default `RuleBasedReasoner` is deterministic and fully offline; a `GeminiReasoner` adapter (behind the `gemini` extra) shows exactly where a real LLM plugs in without the domain ever knowing.
- **Untrusted Execution:** Tools are looked up through a registry, executed under a per-step timeout, and their failures are captured as data (fed back to the reasoner) rather than crashing the run.
- **Bounded Autonomy:** Every run is capped by `max_steps`; exhaustion is a first-class outcome with a full trace, not an exception that loses the work.
- **Extensibility:** Third parties can ship tools via the `keel.tools` entry-point group, discovered at build time by the `EngineBuilder`; discovery is opt-in, and a broken plugin is logged and skipped, never fatal.

> **On the Gemini implementation:** the default engine is fully offline and deterministic, and the `GeminiReasoner` adapter is the worked example of the `IReasoner` seam. Its wire behavior is pinned by a fixture recorded from one real API call, replayed by the suite so the offline guarantee holds; validate against your own account and workloads before production use.

---

## Core Architectural Pillars

Keel enforces the **Dependency Rule**: inner layers (Business Logic) must not depend on outer layers (Public Surface, Providers, IO).

1. **Ports & Adapters (Dependency Inversion)**
   The orchestration service (`AgentRunner`) depends only on pure Python `Protocols` (`IReasoner`, `IToolRegistry`, `IMemory`, `IEventSink`). The `EngineBuilder` injects concrete implementations (like `RuleBasedReasoner` or `GeminiReasoner`) at construction time.
2. **Strict Translators**
   Domain objects never leak through the public surface; run results are translated into the facade's report schemas before a caller sees them. Provider payloads are strictly for the provider SDK, and the Gemini adapter carries its own `domain <-> provider` translator pair. There is no inbound mirror schema, because the facade builds domain schemas directly from the primitives its callers pass (see [the boundary decision record](docs/decisions/0005-translate-only-outward-at-the-facade-boundary.md)).
3. **Decoupled Exceptions**
   Business logic raises pure Python exceptions (e.g., `ToolNotFoundError`, `StepLimitExceededError`). Nothing in the domain imports a framework or an SDK.
4. **Library Citizenship**
   No global mutable state, no environment reads at import time, a `NullHandler` on the package logger, an immutable `EngineConfig`, curated `__init__` exports, and a `py.typed` marker. The package behaves the same embedded in a server, a notebook, or a CLI.

---

## Project Structure

```text
keel/
├── src/
│   └── keel/                   # The installable package (rename to your package name)
│       ├── facade/             # Public surface (Builder, Engine facade, CLI, public schemas + translators)
│       ├── core/               # Package-wide infrastructure (Config, Logging, Plugins)
│       ├── domain/             # Absolute source of truth (Interfaces, Domain Schemas, Exceptions)
│       ├── adapters/           # Concrete implementations (Reasoners, Tools, Memory, Registry, Event Sinks)
│       └── services/           # Business logic orchestration (the bounded AgentRunner loop)
│
├── docs/                       # Technical documentation (the annotated map lives at docs/ARCHITECTURE.md)
├── scripts/                    # Tracked repository tooling (the docs audit, the fixture recorder)
├── tests/                      # Automated test suite mirroring the src structure
├── AGENTS.md                   # Agent entry point and the documentation index
├── STATE.md                    # Living project state
└── pyproject.toml              # PEP 621 metadata, hatchling build backend, extras, entry points
```

---

## Key Features

- **Guarded Fluent Builder:** `EngineBuilder` validates every injected implementation against its `Protocol` at wiring time, so misconfigurations fail at build, not mid-run.
- **Deterministic Offline Demo:** The default engine needs no network, no API key, and no setup; `keel "calculate (2 + 3) * 4"` works on a fresh install.
- **Structured Observability:** Every run emits typed `EngineEvent`s through the `IEventSink` port; ship them to logs, collect them for assertions, or write your own sink.
- **Plugin Entry Points:** Tools can be discovered from the `keel.tools` entry-point group, with per-plugin failure isolation.
- **Modern Packaging:** src layout, PEP 621 metadata, PEP 561 `py.typed`, PEP 735 dev dependency group, console script plus `python -m` execution, and an optional-dependency extra for the LLM adapter.

---

## Getting Started

### 1. Local Development (Python)

Ensure you have Python 3.14+ installed.

```bash
# Clone the repository
git clone https://github.com/AliKhaliliT/YOUR_REPO.git
cd keel

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install the package in editable mode
pip install -e .

# Run the offline demo through the console script
keel "calculate (2 + 3) * 4"

# Or through module execution, with the full trace
python -m keel "count words in the quick brown fox" --show-trace
```

### 2. Programmatic Usage

```python
import asyncio

from keel import EngineBuilder

engine = EngineBuilder().build()
report = asyncio.run(engine.run("calculate (2 + 3) * 4"))
print(report.output)
```

### 3. The LLM Adapter (Optional)

```bash
pip install -e ".[gemini]"
```

```python
from keel import EngineBuilder
from keel.adapters.reasoners.gemini import GeminiReasoner

engine = EngineBuilder().with_reasoner(GeminiReasoner()).build()
```

### 4. Shipping a Third-Party Tool

Expose an `ITool` implementation from your own package via the entry-point group, then opt in during construction:

```toml
[project.entry-points."keel.tools"]
my_tool = "my_package.tools:MyTool"
```

```python
engine = EngineBuilder().with_discovered_tools().build()
```

---

## Conventions

The project's conventions live in one place, the rulebook at [docs/CONVENTIONS.md](docs/CONVENTIONS.md). It holds the documentation system (a vendor-neutral [AGENTS.md](AGENTS.md) as the agent entry point and the single index of every document, [STATE.md](STATE.md) as the living project state, [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) as the current map, and immutable decision records under [docs/decisions/](docs/decisions/) as the reasoning behind every settled choice), the docstring convention in its code-level section, and the prose law in its Prose section. That file is normative and must not be modified; the rationale behind the system itself is recorded in the style's founding decision record, 0001.

The rulebook is owned at the style level. A project built from this template never changes it locally, and an improvement discovered while refactoring against the template is not kept as a private advantage; the project's `UPSTREAM.md` carries it back to the template as [AGENTS.md](AGENTS.md) describes, where it is verified and, if it holds, adopted for every project that follows the style.

---

## License

This work is under an [MIT](https://choosealicense.com/licenses/mit/) License.
