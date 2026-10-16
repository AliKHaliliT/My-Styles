# 0083. Write out a search handed to a person

Status: Accepted
Date: 2026-10-15

## Context

A pass names in Left out each search it prepared but could not run,
and queues it in the state file for a person with access. The name was
all the rule asked for. An entry reading that the licensed index was
not searched tells the person to search it and nothing of how, so the
string, the filters and the window are chosen again at the keyboard,
and the next pass enters whatever that guess returned as the search
the first pass meant. A review method the owner keeps outside the
family never hands over a query without its run sheet, the exact
string in the database's syntax, the filters, the export format and
the file name, in the same six moves every time.

## Options considered

- A run sheet file beside the record. Refused, because a search
  written out is a few lines and belongs in the record that prepared
  it, where the next pass reads it.
- Holding the shape in the audit. Refused, because the audit cannot
  tell a string in an index's syntax from a sentence about one, and a
  shape rule it cannot decide would gate on the word search.
- Leaving it to the person's judgment. Refused, because the judgment
  is made under the wrong pass's criteria by whoever happens to hold
  the licence.

## Decision

A search a pass hands to a person is written out whole in its Left
out, the string in the index's own syntax, the filters, the date range
and the export to take, so the person runs it as written and the next
pass enters it as run. The queued entry in the state file names the
pass record whose Left out carries it. The rule stays in prose, held
in review, because nothing decidable separates a string from a wish.

## Consequences

A licensed search runs as the pass that needed it designed it, and the
record of what was asked survives the session that asked.
