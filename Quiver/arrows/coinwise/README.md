# coinwise

![License](https://img.shields.io/github/license/AliKHaliliT/My-Styles) ![Last Commit](https://img.shields.io/github/last-commit/AliKHaliliT/My-Styles) ![Open Issues](https://img.shields.io/github/issues/AliKHaliliT/My-Styles)

A small, deterministic library measuring the drift a rounding strategy accumulates when many monetary amounts are rounded to whole cents and summed.

coinwise is an arrow of the [Quiver](../../) inquiry that hosts it, built as a full adaptation of the [Keel](https://github.com/AliKHaliliT/My-Styles/tree/main/Keel) template, carrying Keel's architecture, gate, and documentation spine whole under the arrow's own jurisdiction. It exists to produce the evidence behind the inquiry's claims, which pin the exact commit of this tree that produced their numbers.

> **Named incompleteness:** two domain trims are deliberate and must not be "fixed" unprompted. The suites demonstrate the test shape rather than covering the surface, and there is no command-line surface, because this domain does not need one. The spine, the gate, and the law are carried whole.

## The Philosophy: Why Does This Exist?

The inquiry this arrow serves settles claims with evidence, and evidence nobody can rerun is a screenshot. This library is the rerunnable half of those claims, deterministic by construction, so the pinned commit of this tree reproduces the pinned numbers exactly.

It is also the host's first arrow, which makes it the exemplar future arrows are cut from. An arrow teaches whatever shape it has, so this one carries the full Keel form, the spine, the gate, and the law, rather than a summary of it.

## The Domain: Rounding Drift

Monetary code rounds to whole cents constantly, and the two common tie rules, round half up and round half even, differ only on amounts sitting exactly halfway between two cents. Whether that disagreement matters at ledger scale is the hosting inquiry's question, and this library is the instrument that answers it.

Small as the domain is, it still exercises the layers honestly. The strategies and the tie test stay pure and framework-free in `domain`, the measurement logic in `services` knows nothing about how experiments are surfaced, and the public answer crosses the boundary only through the facade's own schemas.

---

## Core Architectural Pillars

coinwise enforces the **Dependency Rule**: inner layers (Business Logic) must not depend on outer layers (Public Surface).

1. **A Machine-Checked Dependency Rule**
   import-linter holds the layer order, `facade` over `services` over `domain`, on every lint run, so the rule survives contributors who never read this file.
2. **Strict Translators**
   Service results never leak through the public surface; `DriftResult` is flattened into the facade's `StrategyReport` by an outbound translator, per the inherited boundary ruling ([Keel's decision 0005](docs/inherited/0005-translate-only-outward-at-the-facade-boundary.md)).
3. **Determinism as a Feature**
   The grid is fixed by construction, every multiple of a tenth of a cent, so tie density is exactly one in ten, no seed exists to lose, and any run of the same count reproduces the same numbers anywhere.
4. **Library Citizenship**
   No global mutable state, no environment reads at import time, a `NullHandler` on the package logger, curated `__init__` exports, and a `py.typed` marker, so the package behaves the same embedded in the inquiry, a notebook, or a server.

---

## Project Structure

```text
coinwise/
├── src/
│   └── coinwise/               # The installable package
│       ├── domain/             # The two strategies and the tie test they disagree on
│       ├── services/           # Summing a stream twice and measuring the drift
│       └── facade/             # Experiment, public schemas, and the outbound translator
│
├── docs/                       # Technical documentation (the annotated map lives at docs/ARCHITECTURE.md)
├── scripts/                    # The docs audit; the Docs verb of the gate
├── tests/                      # Automated test suite mirroring the src structure
├── AGENTS.md                   # Agent entry point and the documentation index
├── STATE.md                    # Living project state
└── pyproject.toml              # PEP 621 metadata, hatchling build backend, tool config
```

---

## Key Features

- **Pure Strategies:** `round_half_up`, `round_half_even`, and `is_tie` are stdlib-only `Decimal` functions with no state and no dependencies.
- **Honest Measurement:** `accumulate` sums a stream twice, rounded per item and exactly, and reports both totals, their difference, and the tie count.
- **One-Call Experiment:** `run_drift_experiment(count)` builds the fixed grid and answers for both strategies over identical amounts.
- **Typed and Gated:** strict mypy, PEP 561 `py.typed`, ruff with docstring presence, warnings as test errors, and the Dependency Rule held by import-linter.

---

## Getting Started

### 1. Local Development (Python)

Ensure you have Python 3.14+ installed. From this arrow's directory:

```bash
# Install the package in editable mode, with the tooling
pip install -e .
pip install --group dev

# Run the gate
pytest
ruff check . && lint-imports
mypy src tests
python scripts/audit_docs.py
```

### 2. Programmatic Usage

```python
from coinwise import run_drift_experiment

report = run_drift_experiment(10_000)
print((report.half_up.drift, report.half_even.drift))
```

---

## Conventions

The project's conventions live in one place, the rulebook at [docs/CONVENTIONS.md](docs/CONVENTIONS.md). It holds the documentation system (a vendor-neutral [AGENTS.md](AGENTS.md) as the agent entry point and the single index of every document, [STATE.md](STATE.md) as the living project state, [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) as the current map, and immutable decision records under [docs/decisions/](docs/decisions/) as the reasoning behind every settled choice), the docstring convention in its code-level section, and the prose law in its Prose section. That file is normative and must not be modified; the rationale behind the system itself is recorded in the style's founding decision record, 0001.

The rulebook is owned at the style level. A project built from this template never changes it locally, and an improvement discovered while refactoring against the template is not kept as a private advantage; [AGENTS.md](AGENTS.md) describes the upstream report that carries it back to the template, where it is verified and, if it holds, adopted for every project that follows the style.

