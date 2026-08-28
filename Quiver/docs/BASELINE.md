# Repository Baseline

This file is the living rulebook for the repository's always-present files:
which files must exist, which must never be tracked, and how each may be
modified. Unlike [CONVENTIONS.md](CONVENTIONS.md), this document is not
frozen; changes that reshape it are recorded as decision records.

## Always present

| File | Role | Modification rule |
| --- | --- | --- |
| `README.md` | Human-facing overview. | Living document; structured by the README schema below. |
| `.gitignore` | What git must never track. | Every rule must correspond to the actual stack; curate on instantiation. |
| `.gitattributes` | Line-ending and binary policy. | Near-frozen; changes are owner decisions. |
| `.editorconfig` | Vendor-neutral editor baseline. | Near-frozen; same reasoning. |

The documentation spine (`AGENTS.md`, `STATE.md`, `docs/`) is also always
present and is governed by [CONVENTIONS.md](CONVENTIONS.md). The `arrows/`
directory is present from the first arrow onward, and each arrow carries its
own baseline per its own style.

## The README schema

The README's sections appear in this order, each with a content contract:
title and badges, the one-line pitch and expansion (a derived project's
expansion carries one sentence linking this template), The Philosophy, The
Domain (headed `The Domain Example: ...` here because the demo inquiry is a
demo, and `The Domain: ...` in a project whose question is real), Core
Architectural Pillars, Project Structure, Key Features, Getting Started,
Conventions (canonical paragraphs inherited verbatim with truth-preserving
edits only), and License (public repositories only, one line). Internal links
are always relative. Badges must state something true about this repository,
never inherited from the template's own.

## Present when the trigger exists

Triggers are bidirectional. The file appears with its trigger and is removed
when the trigger disappears.

| File | Trigger |
| --- | --- |
| `LICENSE` | The repository is public. Owner-only; agents never touch it. |
| `.github/workflows/` | The project runs its checks on a hosted runner. `ci.yml` runs the commands AGENTS.md documents. GitHub reads workflows only from a repository root, so a copy nested inside another repository carries the file inertly. |
| `util_resources/` | The repository carries tracked assets, each kind in a purpose-named subfolder. |
| Arrow manifests and toolchains | Each arrow brings its own conditional files per its own style's baseline; Quiver adds none inside an arrow. |

## Never tracked

- Editor and IDE directories (`.vscode/`, `.idea/`); the vendor-neutral
  settings live in `.editorconfig`.
- Secrets and local environments (`.env`, virtualenvs).
- `LOCAL.md`, the private local ledger. Every tracked byte and every commit
  message is written for a public audience, even while the repository is
  private, because visibility can flip and history is permanent. Confidential
  facts go there, with at most a neutral pointer in tracked text.
- Anything regenerable: caches, build artifacts, coverage output.
- Operating system junk (`.DS_Store`, `Thumbs.db`, `Desktop.ini`).

## Temporary development files

Files created only to support a task in progress are not repository content.
Prefer creating them outside the tree; one that lives inside the tree is
purged in the change that ends its usefulness. A development utility worth
keeping belongs in `local_util_resources/`, which is untracked. When unsure
whether a file is still needed, surface it to the owner.

## Line endings

`.gitattributes` is the single authority: text is stored normalized, shell
scripts always check out LF, Windows script formats always check out CRLF.
Local `core.autocrlf` settings must never be load-bearing.
