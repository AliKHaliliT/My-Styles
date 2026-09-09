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

The awkward part is the tie. On the grid the experiment walks, every tenth amount sits exactly halfway between two cents, so tie density is a property of the grid rather than a random outcome, and a strategy is judged on what it does there and nowhere else; the drift a rule accumulates is then a count of ties times what the rule does to one, which is why the numbers reproduce anywhere.

---

## Core Architectural Pillars

coinwise keeps Keel's Dependency Rule, inner layers never depending on outer ones, and four decisions carry the rest; [the map](docs/ARCHITECTURE.md) has the detail.

1. **A machine-checked layer order.** import-linter holds `facade` over `services` over `domain` on every lint run.
2. **Translation only outward.** Service results are flattened into the facade's own schemas before a caller sees them, per [Keel's decision 0005](docs/inherited/0005-translate-only-outward-at-the-facade-boundary.md).
3. **Determinism by construction.** The grid fixes tie density at one in ten with no seed to lose, so any run of the same count reproduces the same numbers anywhere.
4. **Library citizenship.** No global state, no environment reads at import, a `NullHandler` on the package logger, curated `__init__` exports, and a `py.typed` marker.

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

The rulebook is owned at the style level. A project built from this template never changes it locally, and an improvement discovered while refactoring against the template is not kept as a private advantage; the project's `UPSTREAM.md` carries it back to the template as [AGENTS.md](AGENTS.md) describes, where it is verified and, if it holds, adopted for every project that follows the style.

