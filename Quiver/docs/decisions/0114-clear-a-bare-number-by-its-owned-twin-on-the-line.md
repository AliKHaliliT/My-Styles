# 0114. Clear a bare number by its owned twin on the line

Status: Accepted
Date: 2026-10-22

## Context

The audits read a record cited by its number alone as a defect, since in
a project built from the style the same number names an inherited record
and one of the project's own. A project met a string that carries such a
number as part of a serialized form, compared byte for byte by its
producer and an independent reader, so the bytes could not change for a
prose rule, and the owner and title it wrote in a comment on the same
line were read as nothing, because the check judged each mention on its
own.

## Options considered

- Exempt string literals from the check. Refused, because no reading of
  a line decides what is a literal in every language the family carries,
  and a bare number in a string is the same ambiguity.
- Keep the check as it stands and let the project suppress the finding.
  Refused, because the family silences no finding with a suppression; a
  finding is fixed or the rule learns the case.

## Decision

A line that names the same record with its owner, the style's, this
project's own or an inherited one, clears a bare mention of that number
on the line, in every seat's audit alike, so a form kept byte for byte
keeps its bytes and the comment beside it answers. Each selftest plants
such a line and expects silence. The citation rule says so.

## Consequences

A serialized form that carries a record number lives with the check, and
the comment that names the record stays on the line the reader sees.
