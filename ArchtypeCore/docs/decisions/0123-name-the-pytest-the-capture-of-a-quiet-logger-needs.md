# 0123. Name the pytest the capture of a quiet logger needs

Status: Accepted
Date: 2026-10-22

## Context

The access-log middleware writes to a logger the application configures
at startup with propagation off and a handler of its own, and the
middleware suite reads what it wrote through pytest's capture. A project
built from this style ran its combined suite in a shuffled order and
found two middleware cases empty-handed once the boot case had started
the application, the messages present on the captured output and absent
from the capture, with the suite byte-identical to the template's. The
template's own suite passes in the same order, the boot case first,
because the pytest it runs under attaches its capture to every logger
that does not propagate, which an older pytest does not; the development
requirements named pytest with no version, so the behavior the suite
relied on was a matter of what the installer chose.

## Options considered

- A fixture that attaches a handler to the access logger directly and
  restores it afterward, as the project did. Refused for the template,
  because it rebuilds inside the suite what the test runner already
  does, and a second capture beside the first is one more thing to keep
  in step.
- Leave the middleware suite reading the root logger alone. Refused,
  because the application turns propagation off on purpose, and the
  suite must not depend on which logger a reader happened to configure.

## Decision

The development requirements name the pytest floor the suite was proven
under, nine, with the sentence that says why. The middleware suite stays
as it is, reading through the runner's capture, which reaches a quiet
logger from that version on. A project on an older pytest raises it or
keeps a fixture of its own, and the entry's fixture stays legal where it
stands.

## Consequences

The capture the suite relies on is a named dependency rather than an
installer's choice, and the shuffled suite passes whichever case starts
the application first.
