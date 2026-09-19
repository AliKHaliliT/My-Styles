# 0077. Judge every changed line of a record, list markers included

Status: Accepted
Date: 2026-09-19

## Context

The immutability check reads the diff of every record since its scope
arrived and judges the changed lines in pairs, a Status line free to move and
a link target free to move to one that resolves. It found the changed lines
with a pattern that took a leading minus or plus and refused a second minus
or plus behind it, so that the file headers a diff opens with, three minuses
and three pluses, would not read as lines. A markdown bullet begins with a
minus too. A removed bullet arrives in a diff as two minuses and an added one
as a plus and a minus, so the pattern skipped both, and an edit to any list
line inside an accepted record passed the check in every seat. Records keep
their options considered as bullets, which is the section a later hand is
most tempted to touch.

## Evidence

The hole was found on 2026-09-19 while testing an upstream entry against the
host seat, whose manifest verification line is a bullet and had moved twice
without the check remarking on it. It was then reproduced by hand in the
working tree of the package seat and the client seat, one word added to a
bullet inside an accepted record, and the audit of each reported the tree as
agreeing with its conventions. Reading the diff as the audit reads it showed
the hunk arriving with no lines at all. The header lines the pattern was
written to exclude arrive before the first hunk of a file, so a reader that
opens a hunk at its header and closes it at the next file has no need to
look at what a line's content begins with.

## Options considered

- Excluding only the exact header shapes, three minuses or three pluses and
  a space. Refused, because a removed line whose content is two minuses and a
  space reads the same way, and a rule about content is what failed here.
- Leaving the pattern and documenting the gap. Refused, since a record's
  bullets are the part of it most worth holding.
- Keeping the anchor where it was. Refused, because a check that widens
  reaches behind its arrival, and a bullet edited legally under the old
  reading could never be unmade; the scope sentence changes, so the anchor
  moves forward by construction.

## Decision

Every docs audit reads a record's diff by hunk. A file header resets the
reader, the added-file header names the record, a hunk header opens a hunk,
and inside a hunk every line that opens with a minus or a plus is a removed
or an added line whatever its content begins with. The content pattern is
gone. The scope sentence now says records are held immutable on every line,
so the rule binds from this commit forward and re-judges nothing before it.
The selftest's immutability proof gains a case that adds one word to the
first list line of an accepted record and expects the finding, beside the
body edit that must fail and the Status flip that must pass. Under the
ladder the rule keeps its check rung, and the check now decides the whole
of what the rulebook states.

## Consequences

A bullet edited inside a record goes red on the next audit run in every
seat, in the working tree and in history from this commit on. Nothing older
is re-judged. The host seat's manifests are unaffected, since its own record
keeps them out of the check.
