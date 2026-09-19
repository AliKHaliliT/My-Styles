# 0052. Read an arrow manifest as the living document it is

Status: Accepted
Date: 2026-09-19

## Context

The rulebook says a subfolder under docs/ is a record folder or the arrows
folder, and that the arrows folder holds one living manifest per arrow. The
immutability check's scope sentence says the same, every file below a
subfolder of docs/ except the arrow manifests. The helper that names the
record a diff touches did not implement that sentence. It called any file
below a subfolder of docs/ a record, manifests included, so the check judged
a manifest's changed lines as it judges a record's and refused them. An
upstream entry of 2026-09-19, sent from a project at pin 4ff17f806f49, named
the gap. The citation rule had reported five untitled citations in three of
its manifests, and the edit that would have answered it was refused as an
illegal edit to a record, so the two rules could not both be met and the
selftest would not run on the red tree.

## Evidence

The helper was read, and its docstring names only the flat living documents
as exempt while the docstring of the function that gathers the diffs quotes
the sentence with the manifests excepted. The defect was reproduced here on
2026-09-19 by changing one word on a citation line of the demo arrow's
manifest, which the audit refused in the working tree. The manifest's
verification line has moved twice since the scope arrived and the audit
passed both times, and reading the diff as the audit reads it showed why:
the pattern that picks out a changed line skips any line whose content
begins with a list marker, and the verification line is a bullet. That is a
second defect, in every seat's audit, and it lands on its own.

## Options considered

- Exempting the manifests from the citation rule instead. Refused, because
  a manifest is a living document and the title beside a citation is what
  lets its sentence stand without the click.
- Superseding a manifest. Refused as a category error, since a living
  document is rewritten in place and only a record is superseded.
- Leaving it, the manifests being appended to in practice. Refused, because
  an append passed only through the second defect, and a rule met by
  accident is a rule not met.

## Decision

The helper returns nothing for a file under the arrows folder of docs/, so
the immutability check never judges a manifest, in the working tree or in
history, and the code now says what its scope sentence has said since it
arrived. The sentence itself does not change, because the scope did not; the
anchor stays where it was. The selftest gains a proof that changes a word on
a manifest's first line, runs the audit, and expects no finding about an
illegal edit, skipping by name in a tree with no arrow. Under the ladder the
rule keeps its check rung and its check now decides what the rule states.

## Consequences

The project titles its five citations at its next re-alignment and its
selftest runs again. A manifest is edited freely, as the rulebook always
said, and the immutability check holds records alone.
