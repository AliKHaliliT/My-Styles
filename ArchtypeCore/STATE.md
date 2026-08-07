# Project State

## Now

- Twelve of the fifteen pinned type-check findings are resolved rather than suppressed, and
  the three that remain are limitations in Starlette and pydantic with nothing here to fix
  (2026-08-06). The largest group was a real defect: the device column is `NOT NULL` while the
  domain schema declared `client_identifier` optional, so the schema claimed a value the
  database had already forbidden, and correcting one annotation cleared eight pins. The device
  and admin update schemas now stand alone instead of inheriting and widening a required
  field, which is the shape `UserUpdate` already used. Reading a user back after creating it
  raises `EntityNotFoundError` instead of returning a value typed as though it could be
  missing. And the documentation helper's signature now admits the exception class it has
  always special-cased.
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
- Three type-check findings stay pinned with a stated reason, because each is a limitation in
  a dependency rather than anything this project can correct (2026-08-06). Two are Starlette
  typing an exception handler against `Exception` rather than the subclass it handles, and one
  is pydantic's `create_model` refusing a pre-built field mapping. `warn_unused_ignores` is
  enabled, so if either library tightens its annotations the pins will report themselves.
- The Dependency Rule is enforced by review alone. `domain` and `services` are forbidden from
  importing `api`, `models`, or any framework, and nothing checks it, unlike the equivalent
  layer rule in the client style which ESLint carries (2026-08-06). Closing this needs a tool
  ruff does not provide, so it is an open decision rather than a configuration change.

## Blocked

- Nothing blocked.
