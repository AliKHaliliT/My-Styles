# 0083. Advise on spelling in the files git tracks alone

Status: Accepted
Date: 2026-09-30

## Context

The spelling advisory ran codespell over the whole directory, so a
generated report, a saved log or an extracted text left beside the tree
was read like source prose, and a project's audit could print more advice
about artifacts than about its documents. The prose law binds a tracked
byte, and a rule binds only where its own text claims to bind, so every
one of those findings was about something no rule governs.

## Evidence

A project built from the host style reported, on 2026-09-18, that one
committed tree produced 48 advisories in a clean checkout and 1,173 in a
workspace holding its saved outputs, the difference being 1,065 matches in
a generated PDF, 50 in a handoff and a quoted audit log, and ten in an
extracted text, none of them tracked. On 2026-09-30 an untracked file with
two misspellings beside the server seat's audit produced two advisories, which the
change below silences, and a misspelling in the tracked README still
prints.

## Options considered

- Passing git's file list to codespell. Refused, because a thousand
  tracked paths exceed a Windows command line and would need batching in
  three languages for the same result.
- Widening the skip list with the artifact names. Refused, since the
  list would chase every project's outputs and never end.
- Keeping the directory scan and dropping every finding whose path git
  does not track. Adopted, one set lookup per line.

## Decision

Every docs audit keeps a spelling finding only when git tracks the path it
names, spelled as git lists it, and drops the rest. The rulebook's Prose
section and the guide's advisory list say the advisory reads the files git
tracks and no other, and the selftest plants a misspelled file git does not
track and expects silence beside the tracked misspelling it already
expects to hear. The family's own workflow keeps its command, since a
hosted checkout holds nothing untracked.

## Consequences

An audit run beside retained outputs reports the same spelling as a clean
checkout, and a person answering the advisory answers only for prose the
law governs. The record is one of four, one per seat whose audit changed,
the demo arrow inheriting the package seat's.
