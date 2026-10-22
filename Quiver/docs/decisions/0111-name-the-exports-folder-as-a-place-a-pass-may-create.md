# 0111. Name the exports folder as a place a pass may create

Status: Accepted
Date: 2026-10-22

## Context

The pass document and the rules for review records named the place a
pass keeps its raw exports as one token, `util_resources/searches/`, and
the audit reads a backticked path under a root the tree knows as a claim
that the path exists. In this template the folder holds the demo's
exports, so the claim held. A project built from this template adopted
the method before any pass kept an export, copied the two frozen
documents as the law requires, and its audit named the folder as missing
on every run, a finding the project could neither fix, since the
documents are frozen, nor answer, since no export existed to keep. The
rules for screening logs had met the same case first and named their
folder as the `screening/` folder under `docs/`, which the audit reads
as a place and not a claim.

## Options considered

- Teach the audit that a token in a frozen document is a specification.
  Refused, because the rulebook names many paths every tree holds, and
  the audit holding them is what keeps the law honest about the tree.
- Ship the folder empty in the template. Refused, because an empty
  folder is a tracked nothing, and a project would carry it for a pass
  it never ran.

## Decision

The three sentences name the place the way the screening rules do, as
the `searches/` folder under `util_resources/`, which appears with the
first pass that keeps an export, in the pass document, the rules for
review records and the map. The audit's reading of paths stands
unchanged. A pass record that names an export it kept still names it by
its full path, and the audit holds that one as before.

## Consequences

A project adopts the method without a folder it has no use for yet, and
the law names a place that may not exist the one way the audit already
reads as a place.
