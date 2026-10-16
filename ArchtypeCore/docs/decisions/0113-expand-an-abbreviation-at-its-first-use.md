# 0113. Expand an abbreviation at its first use

Status: Accepted
Date: 2026-10-15

## Context

Every tracked byte is written for a stranger, and the prose law said
nothing of the abbreviations a stranger meets, so a guide could name a
standard, a tool or a design by its letters alone and a reader outside
the project had to guess. A review method the owner keeps outside the
family defines an abbreviation at its first use and refuses to define
one for a term used once, which is the rule technical editors have
held for longer than any of this.

## Options considered

- A list of abbreviations per project. Refused, because a list is a
  second place the term lives, and a reader meets the letters in the
  sentence and not in the list.
- An advisory that greps for capitals. Refused, because the family's
  own names, the seats and the tools among them, are capitals, and the
  advisory would name the tree's vocabulary on every run.

## Decision

An abbreviation a reader outside the project would not know is
expanded at its first use in a document, the words first and the
letters after them, and never introduced for a term the document uses
once. The sentence stands in the rulebook's Prose section, one text
across the family, held in review.

## Consequences

A stranger reads the letters after the words that explain them, and
a term used once keeps its words.
