# 0108. Attach nothing to an upstream entry

Status: Accepted
Date: 2026-10-15

## Context

An upstream entry names nothing that identifies the project, quotes
the template's bytes and never the project's own, and the audit
refuses an address, a URL, an email or an absolute path in its text.
The text was the whole of what the rule saw. An owner filing the entry
as an issue can attach a log, a screenshot or an export to show what
the text describes, and the attachment carries the project's paths,
its names and its data, which is what the text was written to leave
out, and no audit reads an attachment. A review method the owner
keeps outside the family checks file names, archives, comments and
metadata before a manuscript goes to anonymous review, because the
text is never where the identity leaks.

## Options considered

- Allowing an attachment the owner has read as a stranger. Refused,
  because the owner's stranger reading is the last line and the rule
  is the first, and a screenshot is not read line by line.
- A check on the channel. Refused, because the issue tracker is the
  template's and the sending is the owner's, and nothing in the tree
  sees either.

## Decision

An upstream entry attaches nothing, no log, screenshot or file; what
it needs to show, it quotes, and the issue template says so beside
the other anonymity rules. The sentence stands in the shared upstream
block of every guide, held in review.

## Consequences

An entry leaves the repository as text alone, and the audit's reading
of that text is the reading of the whole entry.
