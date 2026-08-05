# Project State

## Now

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
