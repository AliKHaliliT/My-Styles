# Repository Baseline

This file is the living rulebook for the repository's always-present files: which files must exist, which must never be tracked, and how each may be modified. Unlike [CONVENTIONS.md](CONVENTIONS.md), this document is not frozen: the baseline evolves with tooling, and changes that reshape it are recorded as decision records (its adoption is [0003](decisions/0003-adopt-the-repository-baseline.md)).

## Always present

| File | Role | Modification rule |
| --- | --- | --- |
| `README.md` | Human-facing overview. | Living document. The section order is fixed: title and badges, one-line pitch, Philosophy, Domain Example, Core Pillars, Project Structure, Key Features, Getting Started, Conventions, License. The License section accompanies the `LICENCE` file, so like the file it is present in public repositories only. |
| `.gitignore` | What git must never track. | Append into the matching labeled section (project rules under `Project specific`); never delete inherited rules without an owner decision. |
| `.gitattributes` | Line-ending and binary policy, so repository bytes never depend on a contributor's local git configuration. | Near-frozen; changes are owner decisions, because they silently rewrite every contributor's checkout. |
| `.editorconfig` | Vendor-neutral editor baseline (charset, indentation, final newline). | Near-frozen; same reasoning as `.gitattributes`. |

The documentation spine (`AGENTS.md`, `STATE.md`, `docs/`) is also always present; it is governed by [CONVENTIONS.md](CONVENTIONS.md), not by this file.

## Present when the trigger exists

| File | Trigger |
| --- | --- |
| `LICENCE` | The repository is public. The MIT license text (house spelling: LICENCE), owner-only and effectively immutable; agents never touch it. A private repository or codebase omits it, and should: with no license granted, default all-rights-reserved copyright applies, which is exactly the posture private code wants. |
| `.env.example` | Anything reads a `.env`. Tracked and secret-free, it mirrors every variable the project consumes; the real `.env` stays ignored. |
| `.dockerignore` | A `Dockerfile` exists. |
| `requirements.txt` / `pyproject.toml` | The project's dependency manifest, per project type. |
| `CHANGELOG.md` | The project is a versioned package that consumers upgrade through (see CONVENTIONS.md). |

## Never tracked

- Editor and IDE directories (`.vscode/`, `.idea/`). A setting that matters to everyone is expressed vendor-neutrally in `.editorconfig` or in tool configuration (`pyproject.toml`); a setting that does not is personal and stays on the machine that likes it. This is the assistant-shim doctrine from CONVENTIONS.md applied to editors.
- Secrets and local environments: `.env`, virtualenvs.
- Anything regenerable: caches (`__pycache__/`, `.mypy_cache/`, `.ruff_cache/`, `.pytest_cache/`), build artifacts (`build/`, `dist/`, `*.egg-info/`), coverage output.
- Operating system junk: `.DS_Store`, `Thumbs.db`, `Desktop.ini`.

## Line endings

`.gitattributes` is the single authority: text files are stored normalized (`* text=auto`), shell scripts always check out LF (they run inside Linux containers, where a CRLF shebang breaks them), and Windows script formats (`.bat`, `.cmd`, `.ps1`) always check out CRLF. Local `core.autocrlf` settings must never be load-bearing.
