# 0081. Read a paragraph, not a line, for the splice advisory

Status: Accepted
Date: 2026-09-24

## Context

The splice advisory read a record one line at a time and asked, for each
colon opening a lowercase clause, whether three words or more stood before
the colon on that line. Records wrap near eighty columns, so a colon that
falls early on a wrapped line has its clause on the line above, and the
test saw one word and stayed silent. The rule was a day old when it passed
exactly that shape in a record of this seat, found by the writer's own scan
after the advisory had said nothing.

## Evidence

The record that declared this seat's models with `Mapped` carried the
sentence "Reproduced in a fresh environment with the seat's development
requirements: the revealed type" across a wrap, with the colon second on
its line. The advisory printed nothing for it on 2026-09-24. Joining the
paragraph first finds the clause of nine words and names the line the
colon sits on.

## Options considered

- Lowering the word threshold to one. Refused, because a label like
  `Rejected:` opens most option bullets and would print on every record.
- Reading the whole file as one text. Refused, since a sentence never
  crosses a heading, a table row, a fence or a list marker, and joining
  across them would invent clauses.

## Decision

The advisory reads a record as blocks of prose, a block ending at a blank
line, a heading, a table row, a fence or a list marker, joins a block's
lines, matches over the joined text, and reports the line the colon sits
on. The selftest's planted record gains a spliced sentence wrapped across
two lines and expects the advice at the colon's line. The rung stays
advised.

## Consequences

A splice hidden by a wrap prints like any other before the record lands.
Nothing already landed is re-read, since the advisory falls silent once
main holds a record.
