# 0124. Raise the pytest floor to the capturing release

Status: Accepted
Date: 2026-10-22

## Context

Record 0123 named pytest nine as the floor the access-log suite's
capture needs, because the suite passed with the boot case first under
the pytest the template runs, and that pytest was a nine. A project
built from this style removed its own capture fixture at re-alignment,
ran the boot case before the middleware suite under pytest 9.0.3 and
watched two cases fail, and sent the ordered result as new evidence. The
evidence held. The capture that reaches a logger with propagation off is
in pytest's source from 9.1.0 and absent from 9.0.3 and from 8.4.2, and
the ordered run fails under 9.0.3 and passes under 9.1.1 on this
template's own tree, so the floor was named one minor release too low.

## Options considered

- Adopt the project's fixture after all. Refused, for the reason record
  0123 gave, that it rebuilds inside the suite what the runner does from
  9.1, and the new evidence changes the version, not the instrument.
- Name the floor as the exact version the template proved. Refused,
  because a floor names the release that carries the behavior, and the
  release notes and the source place it at 9.1.0.

## Decision

The development requirements name pytest 9.1 as the floor, with the
sentence corrected to say that 9.1 is the release that attaches its
capture to a quiet logger and that 9.0 sees nothing. The suite stays as
it is. A project on 9.0 raises it; a fixture of its own stays legal
where it stands.

## Consequences

The floor names the release the behavior arrived in, and the ordered run
that found the gap passes at the floor.
