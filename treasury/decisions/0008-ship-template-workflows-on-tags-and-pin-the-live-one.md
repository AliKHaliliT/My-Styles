# 0008. Ship template workflows on tags and pin the live one

Status: Accepted
Date: 2026-08-28

## Context

The repository's live workflow pins every GitHub action to a commit
digest, and its header says why, a tag can move and a digest cannot. The
four inert workflows the templates ship use movable major-version tags
like `@v7`. A content review of the family's law asked whether that split
is drift or design, and nothing anywhere recorded the answer.

## Decision

The split is design. The live workflow guards this repository today, so
it pins digests nobody can move out from under it. A template's workflow
is inherited by children born over years, and a digest pinned today ages
into a stale action no child chose; a major-version tag hands each child
the current action at birth, at the price of trusting the publisher of
the tag. That price is the child's to weigh, so each inert workflow
carries one comment naming the trade and inviting the child to pin
digests when its threat model warrants hardening.

## Consequences

The live repository stays pinned and the templates stay current. A child
that hardens its workflow diverges from the template's bytes knowingly,
which is ordinary adaptation rather than drift. The comment is carried
law, so the demo arrow's copy is held to Keel's by the family audit like
every other carried byte.
