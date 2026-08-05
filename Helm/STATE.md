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
- The layer rule is checked by ESLint rather than by review, using the built-in
  no-restricted-imports rule so it costs no new dependency (2026-08-04). Decision 0008
  carries the reasoning.

## Next

- Nothing queued.

## Deferred

- Nothing deferred.

## Blocked

- Nothing blocked.
