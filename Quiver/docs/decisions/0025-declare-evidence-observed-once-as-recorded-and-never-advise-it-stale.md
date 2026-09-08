# 0025. Declare evidence observed once as recorded and never advise it stale

Status: Accepted
Date: 2026-09-08

## Context

The same project carried a claim whose evidence was a single run against a
hosted commercial model. It cost money, could not be re-run for free, and
would not reproduce exactly if paid for again, because the model is a service
rather than a commit. Records 0007 and 0008 had anticipated such runs, but
only as run evidence whose conditions are named in prose that nothing reads,
so the manifest's reproduce field, the re-pin discipline, and the movement
advisory all treated it as a computation and would in time report it stale
and offer supersession, which would mean paying again or quoting the old run
into a new record. Evidence demonstrated once, at a named time, and never
again is a third kind beside the reproducible and the read, and the style had
no place for it.

## Decision

Evidence observed once and never to be re-run declares itself on one line of
the Evidence section, `Recorded:` followed by what was preserved of it, named
by root-anchored path, or the words `nothing preserved`. The audit reads the
line: a recorded claim is never advised stale, because no command's output
could have changed, and every artefact it names must exist, which is
decidable and so a verdict. Reproducible and read evidence stay inferred as
before, from the presence of a pin or of citation keys, so the nine existing
claims remain legal without an edit.

## Options considered

- A declared kind on every claim, as the report proposed, was refused for
  now, because it would mean editing immutable records to retrofit a form,
  and the ledger moves to a form only where the form is new.
- Treating a recorded claim as a conjecture was refused, because it was
  demonstrated, once, and the ledger's value is telling that from an
  assertion.

## Consequences

A reader of a ledger can tell which claims could be checked this afternoon
and which are observations from a particular day, and the audit tells them
apart the same way. A recorded claim is superseded only when a new
observation is made.
