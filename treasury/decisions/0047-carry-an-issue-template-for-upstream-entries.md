# 0047. Carry an issue template for upstream entries

Status: Accepted
Date: 2026-10-09

## Context

The first upstream entries to arrive as issues, on 2026-10-08, showed
that the family's repository is a channel its law had never described.
The guides now say that the project's owner files an entry and an agent
only proposes it, that an entry names nothing that identifies the
project, and that an entry keeps its dated heading when it leaves the
file. A person filing an issue has read none of that unless the point
of filing shows it, and the point of filing is the one place every
sender passes.

## Decision

The family's repository carries one issue template, `upstream-entry`,
under `.github/ISSUE_TEMPLATE/`. It holds the entry's shape as bytes to
fill, with the dated heading as the body's first line, and two comments
a sender reads before filing, that the owner files and an agent only
proposes, and that the entry names nothing identifying the project and
quotes the template's bytes alone. Blank issues stay allowed, since not
every issue is an entry.

## Consequences

An entry filed from the template arrives in the shape the records are
cut from, and the rule reaches the one reader who never opened a guide.
