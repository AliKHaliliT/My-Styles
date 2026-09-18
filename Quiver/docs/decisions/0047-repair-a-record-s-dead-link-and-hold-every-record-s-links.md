# 0047. Repair a record's dead link and hold every record's links

Status: Accepted
Date: 2026-09-18

## Context

An accepted record was immutable beyond its Status line, and the docs audit
held that byte by byte, in the working tree and in every commit since the
rule arrived. Superseding was the remedy when reality moved past a record.
Nothing said what to do with a record whose account was true and whose link
did not resolve, a relative path short by one level, a filename corrected
after the link was written, a path counted from the wrong root. The link
check read the living documents alone, because records describe the past
and the past does not rot, so a dead link in a record was neither caught
nor repairable. An upstream entry of 2026-09-17, sent from three seats of
one project at pin ec94df4405f3, named the gap, having repaired thirty-two
such links across twenty-seven records and reverted the repair when the
audit refused it.

## Evidence

The rulebook said a record is never edited again and that the status line
is the only edit it may receive; the guide's index row said never edit an
accepted record. Every docs audit's link check ran over the living
documents and the flat files under docs/, and none read a record. The
family's own trees carried no dead link in any record on 2026-09-18, so
holding records to the link rule reddens nothing here. The immutability
check judged each changed diff line alone, so a line whose only change was
inside a link's parentheses looked like any other edit. Whether two lines
differ inside link targets alone, and whether a target resolves, are both
decidable in one read. The treasury's own erratum of 2026-08-24 drew the
same line already, immutability protecting a record's account and
reasoning and not a miscount.

## Options considered

- Superseding the record. Refused, because a new record saying the decision
  changed, when only a path was wrong, is a false entry in the ledger, which
  is the entry's own argument and it holds.
- Leaving dead links in records. Refused, because a record a reader cannot
  follow has stopped doing its job, and history holding the right bytes is
  no help to a reader of the tree.
- Repairing by hand under the owner's word, as the treasury's erratum was.
  Refused as the general form, because the question is decidable and a
  decidable rule may not stay a permission a person grants.
- Holding records to the link check without the repair clause. Refused,
  because it would gate a tree on a defect the worker is forbidden to fix.
- Holding inherited records to the link check. Refused, because they are
  byte-identical to the template's and checked where they were written;
  a child cannot repair them and must not try.

## Decision

A record may be edited beyond its Status line at a link target alone, and
the docs audit decides the edit, holding that the changed lines of a record
differ inside link targets only, the text a reader sees staying
byte-identical, and that every new target resolves, in the working tree
against the files and in a past commit against that commit's tree. Every
other change beyond the Status line stays illegal, as before. Every docs
audit also holds that every relative link in a record of the project's own
resolves, the inherited folder excepted, so a dead link is caught the day it
is written and repaired under the clause once it is found. The rulebook
states both halves and the index row's warning names the two legal edits.
The immutability check's scope sentence names the repair, so the rule binds
from this commit forward like every history-reading check. Under the ladder
both halves take the check rung. The proof repairs a real link in an
accepted record to another resolving target and expects a pass, changes the
link's text and expects a refusal, points the target at a ghost and expects
a refusal, and plants a dead link in the project's own records and in the
inherited folder, expecting the first caught and the second left alone.

## Consequences

A worker who finds a dead link in a record fixes the path and nothing else,
and the audit passes the fix. A record written with a dead link goes red
before it is committed. Yesterday's record on template copies said a
citation of a deleted copy stays as written; it now has a remedy, the
citation re-pointed at the inherited record, which resolves. The three
seats that sent the entry find it adopted at their next re-alignment and
repair their links under the clause.
