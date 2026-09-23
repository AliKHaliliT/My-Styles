# 0074. Prove the link-repair clause on a line the clause binds

Status: Accepted
Date: 2026-09-23

## Context

The selftest proves the link-repair clause of record immutability on the
first relative link it finds, reading the project's own records in filename
order and taking the first link whatever line it sits on. A superseded record
carries a link on its Status line, in the form the rulebook prescribes,
`Superseded by [NNNN](NNNN-the-new-record.md)`, and a Status line is free to
move. In a project whose first own record has been superseded, the proof
therefore edits the one line the clause does not bind. The plant that points
the link at a ghost and the plant that changes the link's text both pass as
legal Status edits, the selftest reports two rules not working, and the plant
that repairs the target passes for the wrong reason. The template's own first
record is accepted, so its run never meets the case.

## Evidence

Three projects built from the client style reported it in their upstream files at the
template's commit a0db0a4, one of them holding its re-alignment until the
plant was fixed rather than landing a patched copy of a style-owned script.
The report was tested on 2026-09-23 by giving the adoption rehearsal's child
a first own record superseded in the prescribed form, and every seat's
selftest reported the two plants raising nothing. Reading the choosers found
each taking the first link of the first record with no regard to its line.
The same reading found that the template's own superseded records, three in
this seat, carry `Superseded by NNNN` on their Status lines, the number
without the link the rulebook prescribes, which is one more reason no
template tree had ever met the case.

## Options considered

- Choosing the first accepted record instead. Refused, because an accepted
  record may link nothing while a later one does, and the clause binds every
  record's body whatever its status.
- Making the selftest step advisory in a tree the plant cannot fit. Refused,
  since a proof that may fail proves nothing.
- Changing the rulebook to the bare form the template's records used.
  Refused, because the link is what lets the link check hold the pointer, and
  a project that followed the rulebook is not the one to change.

## Decision

The chooser skips every line that opens with `Status:` and takes the first
relative link on any other line, and the plants edit that line and no other,
so the proof lands in the body the clause binds. The adoption rehearsal's
child carries a first own record superseded in the prescribed form, with a
superseder that links it from the body, so the proof meets the case a project
meets. The template's own superseded records take the prescribed form on
their Status lines, the one edit an accepted record allows, and the link
check holds the targets. Under the ladder the clause keeps its check rung;
what changes is that the proof of it now fires where it did not.

## Consequences

A project whose first record was superseded runs the selftest green. A record
superseded from now on links its superseder as the rulebook says, and the
older ones now do. Nothing about what the immutability check accepts or
refuses has changed.
