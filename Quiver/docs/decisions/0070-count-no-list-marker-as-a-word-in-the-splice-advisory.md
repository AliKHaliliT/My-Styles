# 0070. Count no list marker as a word in the splice advisory

Status: Accepted
Date: 2026-10-05

## Context

The splice advisory names a colon that closes a clause of three words or
more and opens a lowercase one, in a record main does not hold yet, and
leaves the verdict to the writer because a list colon and a spliced one
look alike to a machine. The block splitter starts a block at a list
marker and keeps the marker in the line, and the clause was counted by
splitting on whitespace, so the hyphen that opens a list item counted as
a word. A two-word label behind a marker reached three words and was
advised, while the same label without the marker was not. A project built from this
template reported it on 2026-10-03, after the first review record it
wrote drew the advisory on the stage line the record form prescribes for
a stage of two words and on no other stage line.

## Evidence

Measured on 2026-10-05 against this template's own review records, where every record draws the
advisory on the line of its two-word stage and on no other stage line,
and against a sample where a one-word stage behind a marker stays silent
and a six-word bullet clause is advised. The template dismissed the same
line in commit messages more than once before the project named the
cause.

## Options considered

- Leaving list items out of the advisory. Refused, because a bullet can
  carry a spliced clause as well as a paragraph can, and the proof plants
  one.
- Raising the word threshold. Refused, since the threshold is right for
  a clause and the defect was in what was counted, not in how many.

## Decision

The advisory drops the list marker the block splitter recognizes before
it counts the clause's words, so a label of two words behind a marker
stays a label and a bullet whose clause runs to three words or more is
still advised. The selftest plants both beside the clauses it already
plants, a two-word stage label behind a marker that must stay silent and
a bullet clause that must be advised.

## Consequences

A stage line in the prescribed form draws no advisory, and a writer who
dismissed one on such a line will see it no more. A spliced bullet is
still named, by its own words.
