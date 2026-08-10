# Project State

## Now

- The WireGuard provider ran live for the first time: `scripts/wg_smoke.py` drove every
  subprocess path, credential generation through provision, stats, config render, and
  revocation, against a real interface inside a NET_ADMIN container, all passing, and on
  Python 3.14 for good measure (2026-08-10). The demo is a working demo now.
- The type checker holds strict with the re-export doors kept implicit, matching the
  package style's bar; all thirty-two findings were ours and are fixed by annotation, and
  the three framework pins survive untouched (2026-08-10). Decision 0013 carries the
  reasoning. `engines/` is stated for what it is, an empty seat for Keel-shaped cores that
  real projects grow, never the style (2026-08-10).
- String delimiters are law where the choice is free: double quotes, switching only to
  avoid escapes, checked by ruff's Q rules (2026-08-10). Decision 0012 carries the rule's
  generality test.
- The style is pinned at 0.0.1: the demo API's displayed version default dropped its 1.0.0
  claim, since a style is not a product (2026-08-10). Decision 0011 carries the reasoning.
- Living documents carry an anti-rot contract (2026-08-10). A STATE date is now a
  last-verified stamp with a 90-day expiry the docs audit enforces in CI, living documents
  record intent rather than tree-derivable inventory, and their sentences are claims to
  verify before relying on, agent and human alike. Decision 0010 carries the reasoning.
- Two more reviewed rules became checked rules (2026-08-08). CI greps every tracked byte for
  an em dash, and ruff now verifies docstring presence on public classes, methods, functions,
  and constructors, which surfaced ten missing docstrings that are now filled. Two exemptions
  are calibrated to the convention rather than to convenience: suites, which document
  themselves through case names, and the port stubs in `app/domain/interfaces`, whose
  documentation lives on their implementations. Commit messages stay with review.
- The Dependency Rule is checked rather than reviewed. Two import-linter contracts in
  `pyproject.toml` keep the core free of frameworks, `api`, `models`, and `repositories`,
  and keep imports pointing one way through `api -> services -> domain`. Both were proven
  by planted violations before landing, and the Lint verb now runs
  `ruff check . && lint-imports` (2026-08-08). Decision 0009 carries the reasoning.
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

- Nothing queued.

## Deferred

- Production routing under real client traffic remains the deployment's own validation;
  the smoke run proves the command paths, not the network (2026-08-10).
- Three type-check findings stay pinned with a stated reason, because each is a limitation in
  a dependency rather than anything this project can correct (2026-08-06). Two are Starlette
  typing an exception handler against `Exception` rather than the subclass it handles, and one
  is pydantic's `create_model` refusing a pre-built field mapping. `warn_unused_ignores` is
  enabled, so if either library tightens its annotations the pins will report themselves.

## Blocked

- Nothing blocked.
