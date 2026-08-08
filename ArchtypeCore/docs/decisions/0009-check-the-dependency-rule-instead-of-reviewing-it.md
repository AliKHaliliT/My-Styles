# 0009. Check the Dependency Rule instead of reviewing it

Status: Accepted
Date: 2026-08-08

## Context

The first hard rule of this template says the Dependency Rule is absolute, with `domain` and `services` never importing from `api`, `models`, or any framework. Nothing enforced it. A service importing `fastapi` to raise an `HTTPException`, or reaching for a database model to skip a translator, passes ruff, passes mypy, passes the suite, and goes green in CI, because every one of those tools answers a different question. The only thing standing between the template and that commit was a reviewer noticing an import line, and an import line looks identical whether it honors the boundary or breaks it.

The client style closed the same class of gap in its [decision 0008](https://github.com/AliKHaliliT/My-Styles/blob/main/Helm/docs/decisions/0008-check-the-layer-rule-instead-of-reviewing-it.md), moving the layer rule from review into ESLint. That left this template's most important rule as the one absolute in the family still held by memory, and STATE.md recorded the gap as an open decision on 2026-08-06, because closing it needed a tool rather than a configuration change.

## Options considered

- **Leave it to review.** Rejected: the discipline is only as strong as the reviewer's attention, and the violation is exactly the change an agent makes under pressure, since raising a framework error from a service is the shortest path to a status code.
- **Express the boundaries in ruff.** Rejected, and it was the first candidate examined because the tool is already here. Ruff's banned-import rules apply to the whole project at once and cannot say that `domain` may not import `models` while `api` may, so the one shape this rule needs is the one shape ruff cannot express.
- **Write a custom checker.** Rejected: a hand-rolled AST walker is a second implementation of a solved problem, and it would itself be the least-reviewed code in the repository.
- **Adopt import-linter.** Accepted. It is purpose-built for exactly this, it reads its contracts from the `pyproject.toml` this template already carries, and it analyzes the import graph statically, so the check needs no environment and executes nothing.

## Decision

Two contracts in `pyproject.toml` state the rule the agent guide has always claimed. "The core is framework-free" forbids `app.domain` and `app.services` from importing `fastapi`, `starlette`, `sqlalchemy`, `alembic`, `app.api`, `app.models`, and `app.repositories`. The repositories entry goes one step past the rule's letter, because the concrete implementations reach the services only by injection, and a service importing one directly would hollow out the ports while satisfying the written sentence. "The Dependency Rule points one way" is a layers contract over `app.api`, `app.services`, and `app.domain`, so an upward import at any depth breaks it.

The Lint verb becomes `ruff check . && lint-imports`, keeping the five commands at five, and CI runs the documented command. The tool joins `requirements-dev.txt`, so the runtime image still never carries it, and its cache directory joins the ignore file beside the other checkers' caches.

Both contracts were proven live before this record was written. A planted import of a database model inside a service broke the first contract, a planted import of a service inside a domain schema broke the second, and the tool reported the full chains, including the transitive one, since the model import pulled `sqlalchemy` into the core two hops away and the report said so. Both plants were then reverted and the run went green again.

One clause of the hard rule stays outside the contracts. Engines never import from `app/`, and there is no engine package yet to name, so that contract is written when the first engine lands. The translators clause also stays with review, because whether data crossed a boundary through a translator is not a fact an import graph can see.

## Consequences

The rule that makes this architecture worth copying is now checked on every push, in the same sense as the client style's layer rule, so the framework-free core stops depending on who reads the diff. The transitive analysis turned out stronger than the client side's specifier matching, since a violation hiding behind an intermediate module is still reported with its full chain.

The costs are one development dependency and a Lint verb that runs two tools. The check is also only as complete as its forbidden list, so a new framework adopted by the application belongs in the contract in the same change that adds it to the manifest.
