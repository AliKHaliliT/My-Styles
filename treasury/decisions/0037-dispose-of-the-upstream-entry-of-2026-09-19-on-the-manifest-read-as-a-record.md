# 0037. Dispose of the upstream entry of 2026-09-19 on the manifest read as a record

Status: Accepted
Date: 2026-09-19

## Context

A project built from the host style, aligned at `4ff17f806f49`, reported
that the inquiry audit reads an arrow manifest as a record. The rulebook and
the immutability check's own scope sentence call the manifests living
documents, and the helper that names the record a diff touches called every
file below a subfolder of docs/ a record. The citation rule had reported
five untitled citations in three manifests, the edit that would answer it
was refused as an illegal edit to a record, and the selftest would not run
on the red tree.

## Decision

Kept. The helper now excludes the arrows folder, so the code says what the
sentence has said since it arrived, and the selftest proves that a word
changed on a manifest raises nothing. The scope sentence does not move,
because the scope did not change. The record is Quiver 0052, and no other
seat carries manifests.

The entry's diagnosis was tested before it was kept, and the test found a
second defect. The pattern that picks out a changed diff line skips any line
whose content begins with a list marker, so a bullet edited inside an
accepted record passed the immutability check in every seat, which is also
why the project's appended verifications passed and why the family's own
verification line moved twice unremarked. That defect is the family's, not
the entry's, and it is repaired in its own landing with its own records.

## Consequences

The project titles its citations at its next re-alignment, its selftest
runs again, and it deletes the entry. The observation the entry made about a
red tree blocking every proof stands as the family's own design, since a
plant proves nothing against a tree that already fails, and the remedy the
family takes is a check that a tree can satisfy.
