# 0065. Fail a template record kept under the project's own number

Status: Accepted
Date: 2026-09-17

## Context

The rulebook says the project's own decisions folder holds the project's own
decisions and nothing else, and the record that split the two folders said a
project that had mixed the sequences fixes itself by moving the template's
records into the inherited folder as pure renames. A template record a
project had already renumbered cannot be renamed into the inherited folder,
because the inherited copy must be byte-identical to the template's and the
renumbered heading is not, and the immutability check refuses the edit that
would make it so. So a project in that state added the byte-identical copies
to the inherited folder and left the renumbered ones where they were, under
its own numbers, and every check passed. A later record of that project cited
one of the copies as the project's own decision. The rule was prose, the
checks around it shaped the outcome, and the commit body asserted the rule
as held.

## Evidence

A project built from the host style, read by its history on 2026-09-17,
carried twenty-two of its templates' records under its own numbers across
four seats, each differing from its inherited twin by the heading line alone,
or by the heading and a status line the template had since changed. The docs
audits hold name shape, unique numbers within a folder, and immutability, and
none of those sees a copy, because a copy is well named, uniquely numbered,
and unedited. Whether a record's body equals another's beyond its heading
and its status line is decidable in one read of each folder.

## Options considered

- Prose alone, as it stood. Refused under the ladder, because the question
  is decidable and a decidable rule may not stay a sentence.
- Comparing slugs. Refused, because a project may name its own decision the
  way the template named one, and a body is the record.
- Comparing whole files. Refused, because the copy's heading carries the
  project's number and its status line may carry the status the template's
  record had when it was copied, and both differences are the copy's, never
  the project's decision.
- Renaming the copy into the inherited folder. Refused, because the inherited
  copy already stands there byte-identical and the rename would edit a
  record's heading, which immutability forbids.

## Decision

Every docs audit fails a record in the project's own decisions folder whose
body, beyond its heading and its status line, equals an inherited record's,
naming both, and says the remedy, deletion, because the inherited folder
carries the record and history keeps the copy. The rulebook's paragraph on
records states the check and the remedy. The gate's audits item names it.
Under the ladder the rule takes the check rung, since it needs no history and
no judgment; a copy edited beyond those two lines is not a copy the check
can see and stays review's. The plant writes one body under two headings,
one to each folder, and expects the finding, building the inherited folder
where the template has none and removing it after.

## Consequences

A project that kept the template's records under its own numbers goes red at
its next audit run and deletes the copies, and a citation of a deleted copy
inside one of the project's own records stays as it was written, a dead link
in an immutable record pointing at bytes history still holds; the record
that cites it is not edited for that. Nothing changes for a project that
carried its records into the inherited folder as pure renames.
