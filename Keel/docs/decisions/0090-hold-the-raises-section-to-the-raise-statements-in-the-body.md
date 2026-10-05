# 0090. Hold the Raises section to the raise statements in the body

Status: Accepted
Date: 2026-10-05

## Context

Record 0002 settled that a Raises section lists exactly the exceptions a
function's own body raises, the argument guards included, that a callee's
exception stays on the callee, and that a function raising nothing writes
the `None.` sentinel. The rule was chosen because it is the one boundary a
reader can check without leaving the function, and the docs audit, which
holds the decidable half of the docstring convention, never checked it.
A project built from the host style reported on 2026-10-04 that the demo
arrow's one-call experiment lists a `ValueError` its body never raises,
the error coming from the grid function it calls, so the exemplar a child
cuts its experiments from taught the form the record refused.

## Evidence

Measured on 2026-10-05 with a prototype of the rule over the three Python
seats' trees and the family's tooling, 998 functions and 147 Raises
sections. In this template the tool
runner's execution method listed `ToolExecutionError` and raised nothing,
the raise living in the helper that halts a run, the server seat's field
reorderer listed a `TypeError` raised by the helpers its reshaping had
extracted, and the arrow's experiment was the third of three. Read the other way, no function raises by name
outside a guarded try what its section omits, once a raise inside a try
that may catch it is left to review, which is the case record 0002 named
of an exception raised and caught in one function.

## Options considered

- Fixing the three docstrings and leaving the rule to review. Refused,
  because the audit already holds the parameters against the signature,
  the rule's boundary is a `raise` statement the parser sees, and the
  template itself drifted in three places while nobody read.
- Reading the call tree to list what escapes. Refused by record 0002 and
  refused again here, since the set is a property of every callee and
  rots as they change.

## Decision

The docs audit holds a function's Raises section to the exceptions its
body raises by name outside a try that may catch them, in both
directions. A raise that names no class, a bare re-raise or a raise of a
variable, leaves the function's section to review, and a raise inside a
guarded try body is neither demanded nor forbidden. The selftest plants a
section naming what the body never raises, a body raising what the
section omits, and a raise caught in the same body that must stay
silent. The tool runner's method writes the sentinel, and the demo arrow
carries the audit and the fix in its own experiment.

## Consequences

A Raises section that says more or less than the body is a red build,
the sentinel is written where it belongs, and a reshaping that moves a
raise into a helper moves the section with it or fails. A function
raising through a variable keeps the review the rule cannot replace.
