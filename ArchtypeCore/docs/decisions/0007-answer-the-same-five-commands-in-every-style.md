# 0007. Answer the same five commands in every style

Status: Accepted
Date: 2026-08-05

## Context

The three styles are meant to differ in form and agree in contract, so an agent or a person arriving at any of them should find the same questions answered. Comparing the `## Commands` blocks showed they did not. Keel and Helm both list Lint and Type-check; this template listed neither, and offered Migrate and Docker in their place. Of the five commands a project needs answered, this one answered three.

The cause was structural rather than an oversight, which is why it went unnoticed. Ruff and mypy read their configuration from a `pyproject.toml`, and an application that is deployed rather than installed has never needed one. The dependency manifest is a flat `requirements.txt`, and the Dockerfile installs exactly that file into the runtime image, so adding a linter to it would ship a linter to production. There was nowhere to put the tooling and nowhere to configure it, so the verbs stayed unanswered.

A second gap sat on top of the first. The block advertised `Test: pytest` while pytest appeared in no manifest, so the command failed on a clean clone.

## Options considered

- **Leave the block honest and short.** Rejected: it is honest about the tooling and dishonest about the contract, since a reader comparing the styles concludes this one chose not to lint rather than that it could not.
- **Make the template an installable package so it gains a `pyproject.toml` naturally.** Rejected: a server is deployed, not imported, and inventing a package identity for it would misrepresent what it is in order to satisfy a config file.
- **Put the tooling in `requirements.txt` and accept it in the image.** Rejected: the image is the artifact this template teaches how to build, and teaching it to carry a type checker is the wrong lesson.
- **Split the manifest by audience and add a `pyproject.toml` carrying tool configuration only.** Accepted.

## Decision

The five commands are Install, Run, Test, Lint, and Type-check, in that order, in every style. Commands beyond the five are listed after them rather than in place of them, which is where Migrate and Docker now sit.

`requirements.txt` keeps only what the application needs at runtime, and stays what the Dockerfile installs. `requirements-dev.txt` includes it and adds pytest, pytest-asyncio, ruff, and mypy. `pyproject.toml` carries `[tool.*]` sections and deliberately has no `[project]` table, because this project is not a package and should not claim to be one.

Ruff runs the same rule set as Keel. Where a finding was real it was fixed, and where a finding marks a deliberate pattern the configuration names the pattern and the reason, so the file teaches rather than merely silences. Mypy checks the whole application, which needs the repository root named as the import base because every grouping directory is a bare namespace package.

Each style also runs the five commands in continuous integration, on the reasoning that a rule checked only when somebody remembers to type it is a reviewed rule wearing a checker's clothes.

## Consequences

The styles now agree on what a project must be able to answer, and a reader comparing them learns from the differences in how each language answers rather than from an absence.

Two costs follow. The root gains two files, which is the price of separating a runtime manifest from a development one without pretending to be a package. And fifteen type-check findings are pinned with a stated reason rather than resolved, because each is a design question rather than an annotation; they are listed in STATE.md under Deferred, and `warn_unused_ignores` is enabled so no pin outlives its cause silently.

Answering a verb is not the same as answering it well. The type checker runs in its default mode rather than strict, since strict reports sixty-four findings against hand-written code that predates it. Tightening it is real work with real design decisions inside, and it belongs to the owner rather than to whoever notices the setting next.
