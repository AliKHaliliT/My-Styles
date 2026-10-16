# 0095. Name a read a tool cut short

Status: Accepted
Date: 2026-10-15

## Context

The reading rule says a document the index names is read whole, first
line to last, and says nothing about a read the tool itself cut off.
A file tool returns the first part of a long guide and stops, a fetch
fails on a page the pass needed, and an agent that reads the part it
was given proceeds on half a rulebook without having skipped anything
on purpose. The owner's own tooling cut the guides at a fixed size
during the work that wrote this rule, and only a reader who noticed
the cut re-read them in parts. A review method the owner keeps outside
the family puts every blocked fetch, unreadable file, truncated output
and tool failure in the block of needs at the end of the turn, and
never fills a gap silently.

## Options considered

- Leaving it to the reading rule as written. Refused, because the
  rule binds the reader's intent and a truncation is not the reader's
  intent, so a half read passes the rule as the reader understands it.
- A check on the tool. Refused, because the tool is whatever the
  session runs on and the tree cannot see it.

## Decision

A read a tool cut short, by truncating its output or failing to
fetch, is re-read in parts until it is whole, or the closing note
names the file as not read whole, and every fetch that failed is named
there too. The sentence stands in every guide's reading bullet, held
in review.

## Consequences

A file the agent relied on was read whole, or the owner knows which
one was not, and a failed fetch is a named gap rather than a silent
one.
