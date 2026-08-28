# coinwise

![License](https://img.shields.io/github/license/AliKHaliliT/My-Styles) ![Last Commit](https://img.shields.io/github/last-commit/AliKHaliliT/My-Styles) ![Open Issues](https://img.shields.io/github/issues/AliKHaliliT/My-Styles)

A small, deterministic library measuring the drift a rounding strategy accumulates when many monetary amounts are rounded to whole cents and summed.

coinwise is an arrow of the [Quiver](../../) inquiry that hosts it, built as a full adaptation of the [Keel](https://github.com/AliKHaliliT/My-Styles/tree/main/Keel) template, carrying Keel's architecture, gate, and documentation spine whole under the arrow's own jurisdiction. It exists to produce the evidence behind the inquiry's claims, which pin the exact commit of this tree that produced their numbers.

## The Philosophy: Why Does This Exist?

The inquiry this arrow serves settles claims with evidence, and evidence nobody can rerun is a screenshot. This library is the rerunnable half of those claims, deterministic by construction, so the pinned commit of this tree reproduces the pinned numbers exactly.

It is also the host's first arrow, which makes it the exemplar future arrows are cut from. An arrow teaches whatever shape it has, so this one carries the full Keel form, the spine, the gate, and the law, rather than a summary of it.

## The Domain: Rounding Drift

Monetary code rounds to whole cents constantly, and the two common tie rules, round half up and round half even, agree everywhere except on amounts sitting exactly halfway between two cents. Whether that disagreement matters at ledger scale is the hosting inquiry's question, and this library is the instrument that answers it.

Small as the domain is, it still exercises the layers honestly. The strategies and the tie test stay pure and framework-free in `domain`, the measurement logic in `services` knows nothing about how experiments are surfaced, and the public answer crosses the boundary only through the facade's own schemas.

---

## Core Architectural Pillars

coinwise enforces the **Dependency Rule**: inner layers (Business Logic) must not depend on outer layers (Public Surface).

1. **A Machine-Checked Dependency Rule**
   import-linter holds the layer order, `facade` over `services` over `domain`, on every lint run, so the rule survives contributors who never read this file.
2. **Strict Translators**
   Service results never leak through the public surface; `DriftResult` is flattened into the facade's `StrategyReport` by an outbound translator, per the inherited boundary ruling ([decision 0005](docs/decisions/0005-translate-only-outward-at-the-facade-boundary.md)).
3. **Determinism as a Feature**
   The grid is fixed by construction, every multiple of a tenth of a cent, so tie density is exactly one in ten, no seed exists to lose, and any run of the same count reproduces the same numbers anywhere.
4. **Library Citizenship**
   No global mutable state, no environment reads at import time, curated `__init__` exports, and a `py.typed` marker, so the package behaves the same embedded in the inquiry, a notebook, or a server.

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

Documentation follows the **NumPy docstring style**, with one house addition: classes carry a `Usage` block (not part of the NumPy standard) that holds a minimal, runnable end-to-end example. `Usage` is not a replacement for NumPy's `Examples` section; the two serve different purposes (`Usage` shows the one canonical way to construct and drive the component, whereas `Examples` illustrates specific behaviors or edge cases), and `Examples` may still be added wherever it is warranted. Where a function warrants a full docstring, all three of `Parameters`, `Returns`, and `Raises` are always present, using the `None.` sentinel when a section is empty (no arguments, or nothing raised); `Raises` otherwise lists every exception raised directly in the body, including the defensive argument-validation guards. A returned or yielded value is named only where its type cannot carry the meaning, so an opaque `str`, `bool`, or `dict[str, Any]` gets a name that says what it holds while a `RunResult` or an `AuthToken` is left bare, since repeating the type as a name tells the reader nothing twice. `Parameters` and `Attributes` always carry the name the code gives them, and `Raises` and `Warns` have no name to give.

Not everything is documented that heavily, by design. Purely internal helpers and thin mappers, such as the translator functions that bridge schemas across a boundary, keep a one-line summary. Unlike a service with an HTTP edge, this package has no layer whose contract is expressed elsewhere, so the `facade` is documented in full like every other layer. It is the surface an embedding application imports and calls directly, and its docstrings are the only place its failure modes are stated.

The rest of the NumPy vocabulary is used where it fits and omitted where it does not: a caveat becomes a `Notes` section rather than a loose sentence, a generator would document `Yields`, a `warnings.warn` would document `Warns`, and `See Also`/`References` are there for cross-references. Sections you do not see are simply not called for by that code; generated code should add them as it introduces the behavior.

Beyond docstrings, the project's technical documentation is governed by a fixed documentation system: a vendor-neutral [AGENTS.md](AGENTS.md) serves as the agent entry point and the single index of every document, [STATE.md](STATE.md) tracks the living project state, [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) holds the current map of the system, and immutable decision records under [docs/decisions/](docs/decisions/) hold the reasoning behind every settled choice. The full rulebook, including the split between living documents and records and the writing rules for each species, lives in [docs/CONVENTIONS.md](docs/CONVENTIONS.md); that file is normative and must not be modified. The rationale behind the system itself is recorded in [its founding decision record](docs/decisions/0001-adopt-the-documentation-system.md).

Both the rulebook and the conventions above are owned at the style level. A project built from this template never changes them locally, and an improvement discovered while refactoring against the template is not kept as a private advantage; [AGENTS.md](AGENTS.md) describes the upstream report that carries it back to the template, where it is verified and, if it holds, adopted for every project that follows the style.

One further rule applies to every piece of prose in the project, from this README through docstrings to commit messages. Everything must read as if a person wrote it. The clearest machine tell is the clause-colon splice, a sentence shaped as claim, colon, elaboration; no human writes that way outside a slide deck, so in prose a colon may only introduce a list, a quote, or a label. Softer tells, such as a balanced semicolon antithesis or a neat triadic list, are each fine on their own but give the text away when stacked, because a paragraph of polished epigrams reads as machine writing even when every sentence would pass alone. Allow at most one such flourish per paragraph and write the rest as plain declarative sentences.

One rule governs string delimiters in code, and it is general on purpose. Where a language offers a free choice of delimiter with identical semantics, use double quotes, switching only where it avoids escapes; where the delimiters differ in meaning, as they do in SQL or a shell, the meaning decides. The rule binds only where the choice is actually free, which is what lets it hold in every language the family touches without ever fighting a syntax, and where a checker for it exists, the Lint verb carries it.

One rule governs the shape of a code file, and it is judgment rather than a gate. A file holds one idea. A file grown past easy reading is a prompt to ask whether it still does; when its sections have earned names, it is a folder wearing a file's name, and the split follows those names rather than any count, with a re-exporting `__init__.py` keeping the import surface unchanged so no caller pays for the move. Size is the symptom and never the verdict, so no line limit exists for code and none may be added, because a cap would decide by count what only structure can decide and would breed wrapper files written to duck under it. A file with no nameable sections, a generated table or one long linear procedure, is one idea at its honest size and stays whole.

One rule governs the Python version story. The floor in `pyproject.toml`, the classifiers, the linter and type-checker targets, and the CI pin all tell one story, the docs audit holds every floor claim in living prose to that same number, and the story claims only the interpreter CI actually executes. A real package widens the floor for its users by adding that floor to the CI matrix, so the claim grows exactly as far as the proof does. In the same spirit the test suite treats every warning as an error, because a deprecation warning is a removal notice at least two releases early, and hearing it today buys an unhurried fix instead of a broken upgrade.
