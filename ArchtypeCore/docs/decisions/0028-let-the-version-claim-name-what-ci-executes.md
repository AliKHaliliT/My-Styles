# 0028. Let the version claim name what CI executes

Status: Accepted
Date: 2026-08-27

## Context

A note about future-proofing prompted a survey of where this application
states which Python it runs, and the answer was four places. Ruff's
`target-version` and mypy's `python_version` checked the 3.13 dialect, the
Dockerfile built from `python:3.13-slim`, and CI executed 3.14. So the tools
vetted one interpreter, the image shipped it, and the checks ran on another.
An application has no version range to negotiate the way a package does. It
runs exactly one interpreter, the one its image pins, which makes a split
story here not a half-proven range but a plain disagreement.

The wider question the note asked is how code stays workable on interpreters
that do not exist yet. Python answers that itself. The backwards-compatibility
policy deprecates loudly for at least two releases before removing anything,
so every future removal announces itself as a `DeprecationWarning` years
early. This suite ran with those warnings scrolling past unread.

## Decision

The version story is one number, and the number is the one CI executes. The
linter target, the type-checker target, the Dockerfile base image, and the CI
pin all say 3.14 now, and whoever bumps one bumps them all.

The test suite treats every warning as an error through
`filterwarnings = ["error"]`. Gating on the warning converts a breakage on a
future interpreter into a red test today, while the fix is cheap and
unhurried. An exception must be a named ignore for one specific message with a
reason beside it, never a blanket, the same honesty PGH already demands of
lint suppressions. This tree leans on frameworks, so the first named ignore
will likely arrive from a dependency rather than from `app`, and the rule is
the same either way.

The ruling is family-wide. Keel and Helm carry the same rule in their own
records, shaped to their genres, since a package claims a floor and a client
claims an engine range.

## Options considered

- `from __future__ import annotations`, the era's famous future-proofing
  import, is refused. Python 3.14 evaluates annotations lazily by default, so
  the import now selects the superseded dialect, the one that broke runtime
  introspection in libraries like pydantic, and this application is built on
  pydantic and FastAPI. On this interpreter every annotation form the house
  writes is already native.
- An advisory CI job on the next interpreter's release candidate is refused
  for the template. It is recurring maintenance for a showcase, and the
  warnings gate gives earlier notice anyway, because a warning on 3.14 names a
  removal roughly two releases out while an rc job only reports a breakage
  once it exists.
- A version-range claim with a CI matrix belongs to the package genre and is
  refused here, because an application deploys one runtime and pretending to
  support several would be a claim nothing ships.

## Consequences

The four version fields agree. When 3.15 releases, the bump is one sweep of
the same four fields, image included, and any deprecation the suite started
failing on has been fixed long since.

The warnings gate makes the suite stricter than the code it tests, which is
the point. The first framework release that starts warning turns the suite red
without any change to this repository, and that is the gate working, since the
alternative was learning the same fact from a broken image build two releases
later.
