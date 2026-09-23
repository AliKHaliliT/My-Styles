# 0058. Advise on a colon splice before a record lands

Status: Accepted
Date: 2026-09-23

## Context

The prose law bans the clause-colon splice and leaves the verdict to review,
because a list colon and a spliced one look alike to a machine. On
2026-09-23 four records landed across the seats with a splice that review
had missed, and the rulebook then said in words that a defect found in a
merged record stays. That moved every remedy to before the merge, and
nothing spoke there.

## Evidence

Measured on 2026-09-23 over the family's 346 records. A colon followed by a
space and a lowercase letter marks 408 lines, most of them the label that
opens an option's verdict, `Rejected` followed by its reason. Requiring a
clause of three words or more before the colon leaves 241 lines, about
seven in ten records, a mix of list intros written on one line, labels of
two words or more, and true splices. No rule can tell them apart, so the
finding is advice. Each of the four splices of that day would have printed
once. The scope was measured against main. A record new or changed in the
working tree, or held by a commit main lacks, is one main does not hold
yet; the remote's main serves where the checkout has no local one, and the
working tree alone where neither exists.

## Options considered

- Gating on the pattern. Refused, because a list intro and a splice are one
  shape to a pattern, so a gate would refuse honest lists or grow an
  exception list.
- Advising over every record forever. Refused, since a merged record's
  defect stays by rule, and a standing finding about it would demand a
  dismissal in every commit message for a thing nobody may fix.
- Advising over living documents too. Refused for now, because a living
  document is fixable and the advisory there would be a nag over list
  colons; it reopens if splices land in living documents at the rate they
  landed in records.

## Decision

The docs audit advises on every line of a record main does not hold yet
where a colon closes a clause of three words or more and a lowercase letter
follows, naming the clause, and it prints nothing for a record that has
landed. The selftest plants a record with a splice, a label and a list intro
on three lines and expects one line of advice, for the splice. The guide's
list of advisories and the rulebook's Prose section name it. Under the
ladder the rung is advised, since the writer decides, and the rule the
advisory serves keeps its place in review.

## Consequences

A writer sees the candidate lines at the gate before the commit, rewrites
the splices and dismisses the list colons in the commit message, as every
advisory is answered. Once the record has landed the audit is silent about
it, so no list of tolerated lines ever forms.
