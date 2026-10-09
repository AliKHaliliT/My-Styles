# 0096. Keep Python 3.14 as the style's floor, not a stack binding

Status: Accepted
Date: 2026-10-09

## Context

The tool configuration is style-owned law, and a line in it that binds
the demo's own stack rather than the style's rule is marked `Stack
binding` so a project may re-adapt it. The project file's floor, the
lint's target and the type checker's version all name Python 3.14 and
carry no mark, so a project tested on an older interpreter read them
as a tested runtime choice dressed as a requirement. A maintainer of
projects built from three of the family's styles reported it on
2026-10-08 as an issue, having lowered the two analyzer targets to the
3.12 the projects run on.

## Evidence

Measured on 2026-10-09 in a 3.12 virtual environment. The package seat
refuses to install there by its own floor, and the server seat, which
installs, fails collection with a name error, because both seats name
a class inside its own annotations unquoted, which only the deferred
annotations of 3.14 allow. The lint at a 3.12 target names seven such
sites in the package seat's builder and three in the server seat's
unit of work; the arrow carried by the host names none. No syntax
above 3.12 appears anywhere, so the floor rests on this one feature.

## Options considered

- Marking the lines as stack bindings, as the issue proposed. Refused,
  because a project that lowers them and keeps the exemplars gets
  analyzers that accept what its interpreter rejects, which is the
  defect the issue describes from the other side.
- Quoting the self-references so the code runs on 3.12. Refused,
  because the unquoted form is the dialect the exemplars carry, and
  the family runs on the newest stable interpreter by choice.

## Decision

Python 3.14 is the style's floor. The project file, the lint's target
and the type checker's version say so in a comment beside each line,
naming the feature the floor rests on, so a project reads them as law
and not as a binding to re-adapt, and a project on an older
interpreter is off the style until it moves.

## Consequences

A project adopting the style runs 3.14 or newer, and the analyzers
read the exemplars the way the interpreter does. The floor moves only
by a record here.
