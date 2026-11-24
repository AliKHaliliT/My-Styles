# 0069. Hold every line of the state file in every seat

Status: Accepted
Date: 2026-11-24

## Context

The style's owner brought the state file of a project built from the
host style, which kept thirteen paragraphs of finished work above its
`Now` section while its audit passed, and asked for a check in every
seat that holds the whole schema. Planted files showed what each seat
let through. No seat read a line outside the entries. The host held the
four headings by their presence and skipped any entry naming Nothing
from the cap and the date check, the artifact seats passed an entry with
no date, and the host's selftest planted none of its rules for the file.
The host's rulebook carried a shorter form of the schema's bullets than
the other seats'.

## Decision

- The schema says the file holds its title and its four sections in
  order and nothing else, every line in a section an entry closed by its
  date or the section's empty line alone, and its table names the four
  empty lines. It is shared law, so every seat carries it.
- One check in every seat reads every line. A line above the sections
  beside the title, a line in a section that is not an entry, an entry
  whose date does not close it, an empty line beside other lines, a
  section with no line and a fifth or reordered section each fail. The
  package seat's 0135, the server seat's 0143, the client seat's 0135
  and the host seat's 0130.
- The host's rulebook carries the artifact seats' bullets for the schema
  beside its own two.

## Options considered

- A length cap on entries, to catch one line carrying several tasks.
  Refused, as a length rule was refused before, because it cuts filler
  and never information.
- A new rule telling a project to sweep its state file before each
  change. Refused, because the schema already asks for the sweep at both
  ends of every change, and the miss was a line no check read.

## Consequences

A project re-aligning to this commit finds the lines its schema does not
shape in red. The project whose file prompted the change sweeps its own
file, which is its work and not the family's.
