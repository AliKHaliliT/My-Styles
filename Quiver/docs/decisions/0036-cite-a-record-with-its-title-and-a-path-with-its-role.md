# 0036. Cite a record with its title and a path with its role

Status: Accepted
Date: 2026-09-16

## Context

A living document in a project built from the family read "this contract
defines the prescribed calculation, under decision 0072", with the number
linked and nothing else said. The reader had to leave the page to learn what
the sentence rested on, and a reader of the printed text learned nothing at
all. The same document cited paths and symbols the same way, a dotted name
and no word on what it was for. The owner asked that everything cited mid
text carry a short description of what it did or dictated. Describing what a
file does is a claim about the tree, and the rulebook already refuses those
in living documents, because the tree changes through paths that never touch
the document. Describing what a record decided is safe, because a record is
immutable and its title states its decision by the record schema.

## Options considered

- A paraphrase of each record beside its number. Refused. A paraphrase
  drifts from the record it summarises and is rewritten differently in every
  document that cites it, where the title is one text held by the record.
- A description of what each cited file does. Refused. The audit checks that
  a named path exists and nothing about what it does, so the description
  would rot silently; the file's own docstring is where its behaviour lives.
- The rule held by review alone. Refused. The docs audits already resolve
  every link in a living document, so whether a record's title stands beside
  its link is decided, not judged, and a rule that can fire is made to fire.

## Decision

A reference in a living document carries its description. A record is cited
by its number and its title, verbatim from its heading and in the same
paragraph as the link, so the sentence stands without the click and cannot
drift. A path or a symbol is cited with its role in the sentence, what the
reference is for here, and never with its behaviour. The docs audits and the
host audit report a link to a record whose title is absent from the
paragraph, naming the title to add, with a plant in every selftest. The role
stays with review, as it must.

## Consequences

Fourteen citations across the family gained their titles in the same change,
so the rule arrived on a green tree. A sentence that cites a record now reads
as an argument rather than a pointer, in the file and in any copy of its
text. A record's title, which the schema already required to state the
decision, now does that work in every document that leans on it.
