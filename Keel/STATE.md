# Project State

## Now

- Two more reviewed rules became checked rules (2026-08-08). CI greps every tracked byte for
  an em dash, and ruff now verifies docstring presence on public classes, methods, functions,
  and constructors, which surfaced two undocumented properties on `RunState` that are now
  filled. The exemptions mirror the server template: suites, which document themselves
  through case names, and the port stubs in `domain/interfaces`, whose documentation lives
  on their implementations. Commit messages stay with review.
- The Dependency Rule is checked rather than reviewed. Two import-linter contracts keep
  `domain` and `services` free of `facade`, `adapters`, and the Anthropic SDK, and keep
  imports pointing one way through `facade -> services -> domain`. The layer directories are
  bare namespace packages, so the configuration lists them as portions, and the Lint verb now
  runs `ruff check . && lint-imports` (2026-08-08). Decision 0011 carries the reasoning.
- The test contract is specified rather than assumed. Suites mirror `src/`, collaborators are
  substituted only at the ports in `domain/interfaces`, no coverage threshold is imposed, and
  `tests/src/keel/services/execution/test_agent_runner.py` is the worked example holding ten
  cases over the engine loop (2026-08-05). Decision 0009 carries the reasoning.
- The five documented commands now run in continuous integration on push and on pull request,
  with the type checker covering the suites as well as the package (2026-08-05). Decision
  0010 carries the reasoning.

## Next

- Nothing queued.

## Deferred

- The `AnthropicReasoner` adapter is untested against live API traffic; validate it against a real account and workload before production use (2026-07-16).

## Blocked

- Nothing blocked.
