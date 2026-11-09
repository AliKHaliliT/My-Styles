# 0121. Read only a linked review record as the pass a Slice extends

Status: Accepted
Date: 2026-11-09

## Context

Record 0081 has the audit hold that the date an extending pass starts
from stands before the prior pass's Date line. The check that holds it
walked every Markdown link in the Slice and read each linked document as
a prior pass. A document with no Date line, a living document such as
the method or the bibliography, was given the earliest date there is, so
the comparison failed whatever the pass's date, and a dated record of
another kind was compared as if it were a pass. A project built from
this template linked its prior review and a living document in one
Slice, was refused though its overlap was sound, and moved the second
link to Method to pass. The rules for review records ask the Slice for a
link to the prior pass record and say nothing against a second link.

## Options considered

- Mark the prior pass with a word of its own, the link after Extends or
  a line of its own. Refused, because the reviews folder already says
  which documents are passes, and a marker is a second fact a writer can
  get wrong. It reopens when a Slice needs to link a review record it
  does not extend.
- Correct the comparison and leave the Slice check as it was. Refused,
  because that check takes any linked document for the prior pass, so a
  Slice that links a living document and no review record would pass
  with nothing compared, where it failed before, and a correction must
  not loosen the gate.
- Bind the corrected reading to every pass in history. Refused, because
  the Slice check binds passes older than the extension rule, a merged
  record cannot be edited to meet a reading that arrived after it, and
  the extension rule's arrival is where the pass's identity began to
  matter.

## Decision

From the extension rule's arrival on, the pass a Slice extends is a
review record the Slice links, a document in the reviews folder, and no
other document it links. The audit compares the date an extension starts
from with the Date line of each such record and with nothing else, and a
Slice that links no review record names no prior pass, whatever else it
links. A pass older than the rule keeps the reading it was written
under. A document of another kind linked in a Slice is context, and a
dead link there is the record-link check's to report. The rules for
review records say which links are taken for passes. Two plants hold
both sides, the bibliography linked beside a pass with a sound overlap,
which raises nothing, and the same link alone, which names no pass. No
pass the old reading passed since the rule's arrival is refused by the
new one, and the ledger's row and its holder stand as written.

## Consequences

A Slice may point at the documents that explain it without failing its
overlap, a pass that names no pass is told so in those words, and a
writer who links a second review record in a Slice has said the pass
extends it.
