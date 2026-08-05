# Project State

## Now

- The test contract is specified rather than assumed. Suites mirror the source tree,
  collaborators are substituted only at the interfaces in `app/domain/interfaces`, no coverage
  threshold is imposed, and `tests/app/services/test_user_service.py` is the worked example
  (2026-08-05). Decision 0008 carries the reasoning, and writing that suite immediately
  surfaced a deprecated pydantic config class that had been warning unnoticed.
- The five documented commands now run in continuous integration on push and on pull request,
  with the type checker covering the suite as well as the application (2026-08-05).
- The template answers the same five commands as the other styles. Ruff and mypy are
  configured in a `pyproject.toml` that carries tool settings and no `[project]` table, and
  `requirements-dev.txt` holds the tooling so the runtime image never receives it
  (2026-08-05). Decision 0007 carries the reasoning.

## Next

- Populate `engines/` with a first engine when a portable business core emerges (2026-07-16).

## Deferred

- The WireGuard subprocess interactions (`wg` / `wg-quick`) are untested in a live routing
  environment; validate before any production networking use (2026-07-16).
- Fifteen type-check findings are pinned with a `# type: ignore` and a stated reason instead
  of being resolved, because each needs a design decision rather than an annotation
  (2026-08-05). Eight of them are one unexpressed invariant, that a provisioned device
  always carries a `client_identifier` while the schema still permits none, across
  `user_service`, `device_service`, `quota_monitor`, and `peer_sync`; the open question is
  what should happen when that invariant breaks. Two are update schemas widening a required
  base field, which pydantic allows and the type system does not. Two are Starlette typing
  an exception handler against `Exception` rather than the subclass it handles. One is
  pydantic's `create_model` refusing a pre-built field mapping. One is a lookup immediately
  after a create in the same transaction, which cannot miss but is typed as though it could.
  One builds a documentation example from an exception class where the helper wants an
  instance. `warn_unused_ignores` is enabled, so a pin cannot outlive its cause unnoticed.

## Blocked

- Nothing blocked.
