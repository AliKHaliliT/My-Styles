# Keel Agent Guide

Keel is a strict, AI-ready Clean Architecture template for installable Python packages, demonstrated on a fully offline agent-engine domain. It is a style template and living blueprint, not a production library: some gaps (test breadth, the untested Anthropic adapter) are intentional, so do not "fix" them unprompted.

## Commands

- Install (editable): `pip install -e .` (Python 3.13+; add the LLM adapter with `pip install -e ".[anthropic]"`)
- Run the offline demo: `keel "calculate (2 + 3) * 4"` or `python -m keel "count words in the quick brown fox" --show-trace`
- Lint: `ruff check .`
- Type-check: `mypy src` (strict mode is configured in `pyproject.toml`)
- Test: `pytest`

## Hard rules

- The Dependency Rule is absolute: `domain` and `services` never import from `facade`, `adapters`, or any SDK; layer-owned objects cross a layer boundary only through translators.
- Library citizenship: no global mutable state, no environment reads at import time, and a `NullHandler` on the package logger.
- Every directory holds either subpackages or modules, never a mix (the package root is the sole exception); an `__init__.py` exists only where it re-exports.
- Follow the docstring convention in the [README's Conventions section](README.md#conventions) and the documentation rules in [docs/CONVENTIONS.md](docs/CONVENTIONS.md); the latter is frozen and must not be edited.
- No em dashes anywhere: code, docstrings, comments, documentation, commit messages.
- All prose must read as if a person wrote it. Never write the clause-colon splice, a sentence shaped as claim, colon, elaboration; in prose a colon may only introduce a list, a quote, or a label. The softer language-model tells (balanced semicolon antitheses, triadic lists, not-X-but-Y reversals) are fine one at a time and forbidden stacked, so allow at most one flourish per paragraph and keep the rest plain declarative sentences.
- Read [STATE.md](STATE.md) before starting work; update it when the state changes.

## Documentation index

This is the single index of the project's technical documentation. A document that is not listed here does not exist as far as this project is concerned: when you create a document, register it here in the same change; when you remove one, delist it here.

| Document | What it is and when to read it |
| --- | --- |
| [README.md](README.md) | Human-facing overview: philosophy, structure, setup, and the docstring convention. |
| [STATE.md](STATE.md) | Living project state (Now / Next / Deferred / Blocked). Read first, always. |
| [CHANGELOG.md](CHANGELOG.md) | Curated per-release summary for consumers of the package. Add an entry when cutting a release. |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | The annotated map of the whole template. Read before any structural change. |
| [docs/CONVENTIONS.md](docs/CONVENTIONS.md) | The documentation rulebook: document species, schemas, naming. Frozen; do not edit. Read before writing or changing any documentation. |
| [docs/BASELINE.md](docs/BASELINE.md) | The repository baseline: always-present files, never-tracked files, and their modification rules. Read before adding, removing, or reshaping root-level or dot files. |
| [docs/decisions/](docs/decisions/) | Immutable decision records holding the project's "why". Read the relevant record before revisiting a settled topic; never edit an accepted record. |

There are no assistant-specific instruction files: every assistant reads this file directly. If a tool genuinely cannot read AGENTS.md, give it a one-line shim that imports or points to this file and nothing more.
