# Project State

## Now

- Doc-comment presence is checked rather than reviewed: `jsdoc/require-jsdoc` fails the Lint
  verb on any undocumented export under `src/`, and its first run caught fifteen in this very
  tree, all now filled (2026-08-10). Decision 0016 carries the reasoning and the maintenance
  criterion that picked the plugin.
- String delimiters are law where the choice is free: double quotes, switching only to
  avoid escapes, checked by ESLint's quotes rules (2026-08-10). Decision 0015 carries the
  rule's generality test and the ESLint 10 migration note.
- The style is pinned at 0.0.1 in the manifest, the family-wide marker that a style is not
  a product (2026-08-10). Decision 0014 carries the reasoning.
- Living documents carry an anti-rot contract (2026-08-10). A STATE date is now a
  last-verified stamp with a 90-day expiry the docs audit enforces in CI, living documents
  record intent rather than tree-derivable inventory, and their sentences are claims to
  verify before relying on, agent and human alike. Decision 0013 carries the reasoning.
- The em-dash ban is checked in CI, a grep over every tracked byte that runs before anything
  installs; commit messages stay with review (2026-08-08).
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
