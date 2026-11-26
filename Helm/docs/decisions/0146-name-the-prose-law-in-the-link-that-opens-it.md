# 0146. Name the prose law in the link that opens it

Status: Accepted
Date: 2026-11-26

## Context

The rules of conduct close their bullet on prose with a link to the
rulebook's Prose section. When the rulebook was split into documents
read whole, the prose law moved to a file of its own and the link's
target moved with it, while the link's text kept the name of the file
the law had left. A project built from this style reported it after
comparing the rules of conduct it carries with the template's, link by
link.

## Evidence

Read on 2026-11-26 at 2ddae38. The link's text named the rulebook's core
and its target was the prose law, in this seat, in the other three and
in the copy the demo arrow carries, and the host's guide held one more
link of the same kind. A scan of every tracked Markdown file in the
family for a link whose text names one file and whose target is another
found those six and no other, none of them in a record. The text and the
target parted at 776e5c3, the commit that split the rulebook.

## Options considered

- Adding a check to every docs audit that refuses a link whose text
  names a file other than its target. Refused, because the six are one
  slip at one split, copied, and each link still opened the right page,
  so a check would bind every project's links for a class seen once.

## Decision

The link's text names the prose law, the file it opens, in the rules of
conduct of every seat and of the arrow's carried copy, and the host's
guide names it the same way.

## Consequences

A reader who goes by the link's text finds the clause where the text
says. Nothing holds the next rename's links to their names but the
review that missed this one, and a second slip of the kind is the
evidence that reopens the check.
