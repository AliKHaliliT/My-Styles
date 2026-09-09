# 0022. Write the README for the product and keep the pin in the upstream file

Status: Accepted
Date: 2026-09-09

## Context

The owner read a Keel child's README and found the template's philosophy
re-skinned as the product's, a forty-character commit hash in the second
sentence, and release comparisons in a living document. The README schema had
asked for all three: its Philosophy and Domain contracts argued for an
architecture because the templates' product is one, the attribution carried
the alignment pin, and the features contract said nothing about history.

## Decision

The schema splits the template's frame from a child's. A child's Philosophy
states its users' problem and the project's stance, its Domain what is harder
than it looks, its Pillars a few decisions in a sentence each with a link into
the map, and its features what is, never what changed. The attribution is one
sentence linking the template by name, and the pin moves to the first line of
the upstream file, `Aligned to <template> at <commit>`, held by the audits and
pointed at by the gate. Each style carries its own record of the rule, and the
demo arrow carries the exemplar.

## Consequences

A product README reads as one, and the pin lives with the entries it governs.
