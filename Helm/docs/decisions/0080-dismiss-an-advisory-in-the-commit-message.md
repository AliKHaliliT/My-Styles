# 0080. Dismiss an advisory in the commit message

Status: Accepted
Date: 2026-09-23

## Context

The checks report at two levels, and the guide has said since the levels
were split that every warning is read and then fixed or dismissed in
writing, in the change that produced it. It named no place for the writing.
A delivery's closing note was the usual place, and a closing note is a
message to the owner that the repository never holds, so the next change met
the same warning with no trace that anyone had judged it, and the only
durable home a project had was a decision record, which is too heavy for a
judgment about one run.

## Evidence

A project built from this style reported the gap at e069bab. It had carried
the advisory rules and asked where a dismissal lives once the change that
dismissed it is committed and its notes are gone, and it proposed a section
of the upstream file or a small ledger beside it. Reading the family's own
history on 2026-09-23 found the same gap at home: dismissals written to the
owner in delivery notes, none of them in the tree.

## Options considered

- A ledger of dismissals. Refused, because a dismissal that persists is a
  suppression with extra steps, and the rule says a warning is re-read on
  every run, so a judgment belongs to the change that made it and never to a
  standing list.
- A section of the upstream file. Refused, since that file carries what the
  project has for its style, and a dismissal is the project's own judgment.
- A decision record for each dismissal. Refused, as the project itself said,
  because a record is for a decision the project will be held to and a
  dismissal is a reading of one run.
- Leaving the place unnamed. Refused, because a rule that asks for writing
  and provides no place for it cannot be followed, and prose is already the
  weakest rung.

## Decision

A warning is fixed or dismissed in writing in the commit message of the
change that produced it, so the judgment travels with the change, is found
by searching history, and outlives the run that asked for it. A finding
printed on every run by design, like a review row of the invariants ledger,
was answered by the record that made it so and needs no repetition. The
two-level paragraph and the gate item name the place. Under the ladder the
rule keeps its prose rung, held in review, since no check can read whether a
message answers a warning; what changes is that review has a place to look.

## Consequences

A reader who meets an advisory finding searches the history for its
dismissal and finds it, or finds that nobody judged it. Nothing mechanical
changes and no file is added.
