# 0030. Let the version claim name what CI executes

Status: Accepted
Date: 2026-08-27

## Context

A note about future-proofing prompted a survey of where this client states
which runtime it supports, and the two places disagreed. The `engines` field
in `package.json` claimed `>=20.19`, a floor inherited from Vite's own minimum,
while CI executed Node 24 and nothing ever ran the claimed floor. A range whose
floor no check runs is a completeness claim without a boundary, and here the
claim was three major versions wide with only its top end proven.

The runtime that matters most to this template, the browser, is not part of
this record. The build targets and the platforms the bundle serves are Vite's
territory and are already governed where the build is configured. This record
is about the toolchain runtime only, the Node that installs, tests, and builds.

## Decision

The version story is one number, and the number is the one CI executes. The
`engines` field claims `>=24` now, matching the Node the workflow pins, and
whoever bumps one bumps both.

The ruling is family-wide. Keel and ArchtypeCore carry the same rule in their
own records, shaped to their genres, and their Python trees additionally gate
their test suites on deprecation warnings, since Python's compatibility policy
makes a warning a removal notice at least two releases early.

## Options considered

- Gating the test run on Node's own deprecation warnings would mirror the
  Python trees and is deferred rather than refused. Node emits them, but
  making Vitest fail on them is unproven against this toolchain, and a gate no
  one has watched fire is not a gate. It becomes worth adopting the day
  someone proves it and brings the evidence.
- Keeping Vite's floor as the engines claim was the status quo and is refused,
  because it repeats the upstream author's promise as if it were this
  template's, and this repository never runs Node 20 to back it.
- An upper bound on `engines` is refused permanently, the same way the Python
  trees refuse a `requires-python` ceiling. A ceiling turns a runtime that
  would have worked into an install warning, which is the one genuinely
  anti-future move available here.

## Consequences

The two version fields agree. When the next Node LTS lands in CI, the bump is
one sweep of both fields, and a project built from this template inherits a
claim its own pipeline actually exercises.

The narrowed claim costs nothing real. Anyone on an older Node sees an engines
notice instead of a false promise, and widening the claim back is one CI
matrix entry away for a project that truly supports it.
