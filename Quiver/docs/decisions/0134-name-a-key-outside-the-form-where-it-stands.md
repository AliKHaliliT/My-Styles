# 0134. Name a key outside the form where it stands

Status: Accepted
Date: 2026-11-26

## Context

The audit reads a citation and a bibliography entry by one form of key,
an author's name closed by a year or a standard's designation with its
year suffixed. A project built from this template reported that a key
with a word after its year is invisible to both readers, so its entry is
held to no standing and its citations resolve against nothing, and that
only a count in a pass's table, disagreeing with the rows it could see,
gave the omission away.

## Evidence

Run on 2026-11-26 at 6a35476, on files of the probe's own. A
bibliography row with no standing, its bold key carrying a word after
its year, raised nothing from the standing check, and the same key in
brackets raised nothing from the resolving check. A capital in the name
and a hyphen in the name went the same way, while a legal key raised
both findings. Of the family's tracked Markdown, none holds bracketed
text shaped like a key outside the form, and all 105 bullets of the
template's bibliography are legal entries.

## Options considered

- Widening the form to take a word after the year. Refused, because one
  form is what lets one pattern find and resolve every citation, and a
  wider form would leave the next variant, a capital or a hyphen, as
  invisible as this one was.
- Naming a malformed row in the bibliography alone, as the report
  proposed. Refused as the whole fix, because a citation written outside
  the form would still resolve against nothing once its row was mended.
- Holding every record to the form. Refused, because a record merged
  before the rule admits no edit, so the form binds a record from the
  rule's arrival, as the family's other rules over records do.

## Decision

The audit names a bullet at the bibliography's margin that is no entry,
and bracketed text shaped like a key, a name that holds a year, that
stands outside the form, in a living document always and in a record
from the rule's arrival. A key in backticks stays a mention and a
bracket that opens a link stays a link. The two older patterns now read
the form from one text. The rules for the bibliography say so and the
ledger gains the claim. The selftest plants each way a key leaves the
form, in a living document and in a record, each legal shape, seven
bullets, a whole run, and a record older than the rule where the tree
has one. Fifteen breaks, each one point, each failed the proof, after
two that survived showed a plant missing and a reading too loose.

## Consequences

A key the readers cannot see is named on the run that meets it instead
of passing unread. A project whose living documents or bibliography hold
such keys renames them at its next re-alignment, and an older record
that cites one keeps its text, the bibliography free to name the older
spelling in backticks under the entry it became.
