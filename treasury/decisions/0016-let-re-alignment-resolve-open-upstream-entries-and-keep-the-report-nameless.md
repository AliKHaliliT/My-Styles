# 0016. Let re-alignment resolve open upstream entries and keep the report nameless

Status: Accepted
Date: 2026-09-07

## Context

Ruling 0015 gave the upstream report a place and a defect class and left two
things implicit. The section still read as if a reply were owed, telling the
child to hold its items until one arrived, so a child whose maintainer said
only that the report was reviewed and the latest should be fetched had no
written procedure for what it held, and could not later tell a silently fixed
entry from an ignored one, or explain to a reader why it differed from its
style. And the section asked the report to name the project, although the
report is the one artifact that leaves a project for this public repository,
where it is quoted into records and commits; the first two reports named or
described their projects, and rulings 0013 and 0014 repeated them. A host
project also asked whether its arrows should hold their own reports or leave
them all at the host.

## Decision

No reply is owed. Re-alignment resolves every open entry of the child's
reports against the new pin, by the diff of the files each entry touches and
the records since the pin: adopted where the template now carries it, dropped
or turned into the child's own record where a record refuses it, and open
with the child's version in place where the template is silent. One dated
resolution record beside the report carries the outcome, and the adoption
gate holds it. The report names nothing that identifies its sender, no
project, person, host, path, address, or domain fact beyond what a finding
needs, and the delivery gate holds that; this treasury's dispositions and the
maintainer's replies name a report by its date and pin alone. In the host
seat, an arrow's report is the arrow's own record under the arrow's `docs/`,
the host's report covers the inquiry layer, and one letter may bundle them.
Each style carries its own record of the rule.

## Consequences

A child can be told nothing and still re-align correctly, with its history
showing the fate of every divergence. A report can be pasted into this
repository without redaction. Rulings 0013 and 0014 keep the words they
carry, because records are immutable and pushed history is not rewritten.
