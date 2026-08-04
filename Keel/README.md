# Keel

![License](https://img.shields.io/github/license/AliKHaliliT/My-Styles) ![Last Commit](https://img.shields.io/github/last-commit/AliKHaliliT/My-Styles) ![Open Issues](https://img.shields.io/github/issues/AliKHaliliT/My-Styles)

A Strict, AI-Ready Clean Architecture Template for Python Packages.

Keel is the package-side sibling of [ArchetypeCore](https://github.com/AliKHaliliT/My-Styles/tree/main/ArchtypeCore). It is a highly structured, installable Python package template built with Pydantic V2 and the modern packaging stack (PEP 621 `pyproject.toml`, src layout, PEP 561 typing). It is designed around **Hexagonal Architecture (Ports and Adapters)** and Clean Architecture's Dependency Rule, keeping the decision logic pure and pushing every piece of IO behind a port in the spirit of the **functional core, imperative shell** school.

## The Philosophy: Why Does This Exist?

In the era of AI coding assistants, a Python package might be a small utility, a client library, or a full runtime that hosts agents, orchestrates tools, and coordinates external providers. Whatever it is, it has to behave like a well-mannered library that other applications embed, and AI assistants suffer from the same **"Architecture Drift"** in packages as they do in services: leaking provider SDKs into business logic, configuring global state at import time, and coupling the public surface to internal representations.

Keel was built to mitigate this. By enforcing explicit boundaries (Translators, Protocols, a guarded Builder), it provides a strict structural foundation that guides AI agents (and developers) toward writing decoupled, maintainable packages. Because AI systems excel at pattern recognition, providing a solid structure from the beginning ensures that even when adding large architectural components, the agent is highly likely to follow the established conventions.

The structure is general-purpose. Your domain logic lives in `domain` and `services`, your concrete IO lives in `adapters`, and your public surface lives in `facade`, the same spine whether you are shipping a parser, an SDK client, or an agent runtime. It ships with an agent-engine demo not because the template is "for agents," but because an agent runtime exercises every seam the architecture defends; delete the demo domain and the skeleton is a rigorous general-purpose package template.

## The Domain Example: Why an Agent Engine?

Many package templates use a generic "string utils" or "image reader" example, which is too simple to demonstrate how an architecture handles real-world complexity.

To demonstrate the utility of Dependency Inversion in the age of AI, Keel implements the domain of an **Agent Engine**: give it a goal, and it runs a bounded reason → act → record loop until the goal is met, a step limit is reached, or the run fails.

Managing an agent runtime forces the architecture to handle practical, complex problems:

- **Pluggable Intelligence:** The loop coordinates decisions through an abstract `IReasoner` interface. The default `RuleBasedReasoner` is deterministic and fully offline; an `AnthropicReasoner` adapter (behind the `anthropic` extra) shows exactly where a real LLM plugs in without the domain ever knowing.
- **Untrusted Execution:** Tools are looked up through a registry, executed under a per-step timeout, and their failures are captured as data (fed back to the reasoner) rather than crashing the run.
- **Bounded Autonomy:** Every run is capped by `max_steps`; exhaustion is a first-class outcome with a full trace, not an exception that loses the work.
- **Extensibility:** Third parties can ship tools via the `keel.tools` entry-point group, discovered at build time by the `EngineBuilder`: opt-in, and a broken plugin is logged and skipped, never fatal.

> ⚠️ **Disclaimer on the Anthropic Implementation:**
> While this template acts as a logically complete agent engine, it serves primarily as an **architectural demonstration**. The `AnthropicReasoner` adapter is a theoretical example of the `IReasoner` interface and is **untested against live API traffic**. The default engine is fully offline and deterministic; validate the LLM adapter against your own account and workloads before production use.

---

## Core Architectural Pillars

Keel enforces the **Dependency Rule**: inner layers (Business Logic) must not depend on outer layers (Public Surface, Providers, IO).

1. **Ports & Adapters (Dependency Inversion)**
   The orchestration service (`AgentRunner`) depends only on pure Python `Protocols` (`IReasoner`, `IToolRegistry`, `IMemory`, `IEventSink`). The `EngineBuilder` injects concrete implementations (like `RuleBasedReasoner` or `AnthropicReasoner`) at construction time.
2. **Strict Translators**
   Domain objects never leak through the public surface; run results are translated into the facade's report schemas before a caller sees them. Provider payloads are strictly for the provider SDK, and the Anthropic adapter carries its own `domain <-> provider` translator pair. There is no inbound mirror schema, because the facade builds domain schemas directly from the primitives its callers pass (see [the boundary decision record](docs/decisions/0005-translate-only-outward-at-the-facade-boundary.md)).
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
├── tests/                      # Automated test suite mirroring the src structure
├── AGENTS.md                   # Agent entry point and the documentation index
├── STATE.md                    # Living project state
├── CHANGELOG.md                # Curated per-release change summary
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

Ensure you have Python 3.13+ installed.

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
pip install -e ".[anthropic]"
```

```python
from keel import EngineBuilder
from keel.adapters.reasoners.anthropic import AnthropicReasoner

engine = EngineBuilder().with_reasoner(AnthropicReasoner()).build()
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

Documentation follows the **NumPy docstring style**, with one house addition: classes carry a `Usage` block (not part of the NumPy standard) that holds a minimal, runnable end-to-end example. `Usage` is not a replacement for NumPy's `Examples` section; the two serve different purposes (`Usage` shows the one canonical way to construct and drive the component, whereas `Examples` illustrates specific behaviors or edge cases), and `Examples` may still be added wherever it is warranted. Where a function warrants a full docstring, all three of `Parameters`, `Returns`, and `Raises` are always present, using the `None.` sentinel when a section is empty (no arguments, or nothing raised); `Raises` otherwise lists every exception raised directly in the body, including the defensive argument-validation guards.

Not everything is documented that heavily, by design. Purely internal helpers and thin mappers, such as the translator functions that bridge schemas across a boundary, keep a one-line summary. Unlike a service with an HTTP edge, this package has no layer whose contract is expressed elsewhere, so the `facade` is documented in full like every other layer: it is the surface an embedding application imports and calls directly, and its docstrings are the only place its failure modes are stated.

The rest of the NumPy vocabulary is used where it fits and omitted where it does not: a caveat becomes a `Notes` section rather than a loose sentence, a generator would document `Yields`, a `warnings.warn` would document `Warns`, and `See Also`/`References` are there for cross-references. Sections you do not see are simply not called for by that code; generated code should add them as it introduces the behavior.

Beyond docstrings, the project's technical documentation is governed by a fixed documentation system: a vendor-neutral [AGENTS.md](AGENTS.md) serves as the agent entry point and the single index of every document, [STATE.md](STATE.md) tracks the living project state, [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) holds the current map of the system, immutable decision records under [docs/decisions/](docs/decisions/) hold the reasoning behind every settled choice, and [CHANGELOG.md](CHANGELOG.md) carries the curated per-release summary for consumers of the package. The full rulebook, including the split between living documents and records and the writing rules for each species, lives in [docs/CONVENTIONS.md](docs/CONVENTIONS.md); that file is normative and must not be modified. The rationale behind the system itself is recorded in [its founding decision record](docs/decisions/0001-adopt-the-documentation-system.md).

Both the rulebook and the conventions above are owned at the style level. A project built from this template never changes them locally, and an improvement discovered while refactoring against the template is not kept as a private advantage; [AGENTS.md](AGENTS.md) describes the upstream report that carries it back to the template, where it is verified and, if it holds, adopted for every project that follows the style.

One further rule applies to every piece of prose in the project, from this README through docstrings to commit messages. Everything must read as if a person wrote it. The clearest machine tell is the clause-colon splice, a sentence shaped as claim, colon, elaboration; no human writes that way outside a slide deck, so in prose a colon may only introduce a list, a quote, or a label. Softer tells, such as a balanced semicolon antithesis or a neat triadic list, are each fine on their own but give the text away when stacked, because a paragraph of polished epigrams reads as machine writing even when every sentence would pass alone. Allow at most one such flourish per paragraph and write the rest as plain declarative sentences.

---

## License

This work is under an [MIT](https://choosealicense.com/licenses/mit/) License.
