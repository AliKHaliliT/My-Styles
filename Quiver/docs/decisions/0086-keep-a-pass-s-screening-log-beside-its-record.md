# 0086. Keep a pass's screening log beside its record

Status: Accepted
Date: 2026-10-15

## Context

A pass counted its funnel, retrieved, screened, entered and read in
full, and Found named the works entered. The records screened and the
reason each was dropped lived nowhere. The pass of 2026-09-30 examined
sixty records and entered nine, and what excluded the other
fifty-one, and on which criterion, ended with the session, so a reader
who doubts a criterion has nothing to re-read and a later pass over
the slice screens the same sixty again. A review method the owner
keeps outside the family keeps a screening workbook with a decision
and a reason code per record, the second screener's decisions beside
the first, and the raw exports unmodified, as the audit trail a
systematic review stands on.

## Options considered

- A table inside the pass record. Refused, because a record is read
  whole when it is cited, and five hundred rows of decisions bury the
  account of the pass under its data.
- Exports and spreadsheets beside the record, as the method keeps
  them. Refused for the decisions, because a subfolder of `docs/` holds
  dated records and a spreadsheet is nobody's prose; kept for the raw
  exports, under `util_resources/searches/` and declared generated, so
  the prose law does not read an index's titles.
- Titles in the log. Refused, because a title carries whatever the
  index put in it, an em dash among other things, and an immutable
  record over the budget admits no edit; the identifier is the
  record's identity and the export keeps the title.
- Both readers in one table. Refused, because the audit counts the
  rows a stage passed against the funnel, and two readers' rows over
  one record count it twice.

## Decision

A `screening/` folder under `docs/` joins the spine with its first log
and holds one immutable record per reader of a pass that screened,
named after the pass, opening with a title, a Date line and a link to
the pass, and holding one table of stage, identifier, first author and
year, decision and reason, one row per record per stage, unsure
standing at the abstract stage alone and every exclusion naming a
criterion's label or a standard reason. The pass's Boundary links the
log of the decisions the pass settled on, or says none, a second
look's decisions are a log of their own linked from the Stages line,
and the Boundary may name the raw exports kept under
`util_resources/searches/`, which the attributes file declares
generated. The audit holds the line, that the linked log exists in the
folder and that the rows its abstract stage passed equal the funnel's
screened count, every log's header, decision words, reasons and place
of unsure, and that what a Recorded line names exists, from the rule's
arrival on; the root workflow's em dash count leaves generated files
alone, as the seat audits already did. The rule took the form of a
record shape held by the audit, because a decision's presence and its
reason's presence are decidable and its rightness is not.

## Consequences

A screening can be re-read, doubted at one row, and extended without
screening the same records twice, and a disagreement between two
readers stands in two records. The three passes in the tree stand
without a log, since a record admits no edit, and the folder appears
with the first pass that keeps one.
