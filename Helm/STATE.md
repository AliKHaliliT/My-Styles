# Project State

## Now

- The test contract is specified rather than left to the example. Suites mirror `src/`,
  collaborators are substituted only at the wire boundary or behind a hand-written fake, and
  no coverage threshold is imposed; the five existing suites already satisfy all of it, and a
  check confirmed no module mocking anywhere in this template or its derived projects
  (2026-08-05). Decision 0011 carries the reasoning.
- The five documented commands now run in continuous integration on push and on pull request,
  followed by the build, which is what finally makes the ESLint-carried layer and token rules
  enforced rather than merely checkable (2026-08-05). Decision 0012 carries the reasoning.
  Two details in that workflow came from the derived projects rather than from here, since all
  four were already running CI while this template was not. Their trigger fires on every push
  rather than only on the default branch, which catches a feature branch that has no pull
  request yet, and it is adopted as written. Their type-check step called `tsc` directly, which
  this template does not copy, because a workflow should run the command the guide documents so
  the two cannot drift apart (2026-08-05).
- The layer rule is checked by ESLint rather than by review, using the built-in
  no-restricted-imports rule so it costs no new dependency (2026-08-04). Decision 0008
  carries the reasoning.

## Next

- Nothing queued.

## Deferred

- Nothing deferred.

## Blocked

- Nothing blocked.
