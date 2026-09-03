# 0014. Slim the readme and add the prose clauses

Status: Accepted
Date: 2026-09-03

## Context

The README carried a restatement of the documentation system and the prose
rule beside the rulebook that owns them, two homes for one law, and the
review of the doctoral repository surfaced rules with no clause for a case
they met: prose inherited on adoption day, dated supervisor briefings that
were neither spine nor decision nor claim, and reports to a person that an
expert outside the work could not follow.

## Decision

The README keeps one paragraph pointing at the rulebook and one on
ownership; it carries no law of its own, and the baseline's README schema
says so. The Prose section gains two paragraphs. Inherited prose comes
under the law at adoption, tracked in STATE as debt until paid, with a
named exclusion for paths another guard hashes. A report to a person opens
with a plain account a reader outside the work can follow and pairs every
abstract finding with one concrete instance. The species section states
that any dated document under docs/, a briefing or a progress report, is a
record for the purpose of immutability, while decisions and claims stay
the two kinds the audit shapes.

## Options considered

- Letting inherited prose converge when next edited was refused, because
  it is the lenient path that leaves a half-folded repository half folded.
- Adding a third record species for briefings was refused; immutability is
  the one rule a dated document needs, and a species would bring shapes
  nobody asked for.

## Consequences

One home for law and one for welcome. A briefing is left alone once
written, an inherited corpus meets a written rule, and a report is read
in the order an outside expert can check.
