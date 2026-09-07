# 0015. Give the upstream report a place and a defect class

Status: Accepted
Date: 2026-09-07

## Context

Four upstream reports reached the family in ten days from three projects,
and no two had the same container: six files with one entry each, one file
for one finding, one dated file with numbered entries, one undated file with
a verification step per entry. The guide fixed what an entry says and never
where a report lives or how it is named. In the same period an adopting
agent found a defect in a template, worked around it, and sent nothing,
because the guide's trigger word was improvement and its qualifying step
asked the agent to be sure a candidate was genuinely better; a small patch
did not read as an improvement, and the adoption gate's "nothing qualified"
deferred to the same judgment.

## Decision

The upstream report is a dated record of the child at
`docs/upstream/YYYY-MM-DD-short-kebab-title.md`, one file per report, never
edited once sent, registered by one index row and held by the folder rule
every style already carries. Its shape is fixed in every guide: an opening
paragraph naming the project, its alignment pin, and its styles; numbered
entries with four labeled parts; the verify line; what the project holds
locally until the reply. The reply is filed beside it as a dated record.

Entries come in two kinds, and only improvements are judged. A defect is
anything worked around, patched, suppressed, or left unmade in
template-owned bytes or template-prescribed behavior, entered whether or not
the child is sure and however small the fix, with uncertainty allowed in
the entry. Every delivery gate gains an upstream-honesty item holding the
workaround written down before delivery, and the adoption gate's report item
asserts both halves. A detector for the marks a workaround leaves was
deferred until a child can know which of its files the template owns.

## Consequences

The maintainer receives one shape, a child's history carries what it sent
and what it was told, and the size of a fix is no longer a reason to keep
it. Each style carries its own record of the rule.
