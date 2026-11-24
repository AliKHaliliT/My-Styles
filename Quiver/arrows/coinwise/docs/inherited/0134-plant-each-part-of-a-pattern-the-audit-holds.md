# 0134. Plant each part of a pattern the audit holds

Status: Accepted
Date: 2026-11-23

## Context

Two patterns of the docs audit are proven by plants, the one the Python
styles' audit reads for a suite that patches a module and the one every
audit reads for an email in an upstream entry. A project built from the
server style found three breaks of a timestamp fix that passed the suite
meant to hold it, because the breaks that proved that suite had been
made several points at a time. The same batch of changes had proven both
patterns the same way, and breaking them one part at a time found six
parts that no plant held.

## Evidence

Run on 2026-11-23 at 6c9473b. With `mock\.patch` or `MonkeyPatch`
dropped from the seams pattern, the Python audit's selftest passed, and
with `monkeypatch` or `unittest\.mock` dropped, it failed. In the
address pattern, letting a last label of one letter end an email's host,
or letting the last label run on into digits, passed every audit's
upstream proof. Under the first an entry quoting `some-tool@1.4.b` was
refused, and under the second one quoting `some-tool@1.4.beta2`. Proving
the new plants one part at a time found two more. Requiring three
letters of an email's last label passed, since no planted email ended in
two, and letting the last label run on into a hyphen passed, since no
planted version carried one.

## Options considered

- Holding a pattern by a test of its text. Refused, because a check of
  the pattern's text holds the words and not what the audit reads.

## Decision

Each alternative of the seams pattern has a plant of its own, a
decorator from `mock.patch` and an import of `MonkeyPatch` beside the
two plants there were. Each part of the address pattern has a plant in
all three audits. Entries quoting `some-tool@1.4.b`,
`some-tool@1.4.beta2` and `some-tool@1.4.rc-1` must pass, and an email
at `example.zz`, a two-letter name that is never handed out, must be
refused. The patterns were then broken one part at a time, four breaks
of the seams pattern and ten of the address pattern in each audit that
carries it, and each break failed a plant.

## Consequences

A pattern changed in any part fails its selftest, and a reader of the
selftest sees each part the pattern holds. A part added to a pattern
needs its plant in the same change.
