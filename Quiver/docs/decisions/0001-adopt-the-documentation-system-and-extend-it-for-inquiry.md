# 0001. Adopt the documentation system and extend it for inquiry

Status: Accepted
Date: 2026-08-27

## Context

The family's documentation system, the two species, the AGENTS entry point and
index, the bounded living documents, and the immutable records, exists to keep
a project's text truthful as reality moves. An inquiry needs everything that
system provides plus homes for three things a code project does not keep: what
the project currently holds true and on what evidence, which works it
consulted, and which question the whole thing serves.

The design was drawn from treasury study 0004 and its disposition, which fixed
what a research seat must honour. The seat's adversary is self-deception, and
the study named its shapes: a result untraceable to the state that produced
it, a dead end silently re-attempted, a completeness claim over a self-drawn
boundary, a source read but never named, and a superseded edition preserved
without noticing.

## Options considered

- One record species, with claims filed among decisions. Rejected because the
  two have different lifecycles, a decision changes only by a newer decision
  while the world alone can strand a claim, and interleaving would break both
  numbering sequences and bury the rare species under the frequent one.
- References inside each record that uses them. Rejected because a citation
  repeated is a citation that drifts, and because the study showed sources
  vanish when treated as frames rather than objects; one bibliography makes
  the consulted set enumerable.
- A mandatory full method for every inquiry. Rejected as the ceremony disease;
  the study's evidence is that rigor must be proportional or it is evaded.

## Decision

Adopt the family system whole, then extend the spine with four homes. A living
QUESTION.md carrying the root question and its decomposition. A claims record
folder, the second record kind, whose template is Claim, Evidence, and
Threats, whose statuses are Conjecture, Supported, Refuted, Stale, and
Superseded, and whose Evidence quotes results in full and pins the host commit
that produced them. A living manifest per arrow. A living BIBLIOGRAPHY of
self-contained citations addressed by key, each naming the edition actually
used. Proportional rigor is law: the spine is question, conjecture, evidence,
claim, and any shortening costs one recorded line.

## Consequences

Knowledge becomes auditable. The audit script checks what a tool can decide,
the shapes, the budgets, the citation keys, the pins against git history, and
advises on what it cannot, a moved arrow whose claims may be stale. Everything
a tool cannot decide is stated as review's work in the gate.

The seat stays cheap at small scale, because a feature-sized inquiry is one
conjecture, one experiment, one claim, and at most one line of recorded
shortening.
