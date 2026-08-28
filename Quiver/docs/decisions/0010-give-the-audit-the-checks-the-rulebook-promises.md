# 0010. Give the audit the checks the rulebook promises

Status: Accepted
Date: 2026-08-28

## Context

A content review of the family's law read every rule against the tree it
governs. The rulebook's freshness section promised that the audit verifies
relative links and that every document under `docs/` is registered, and the
audit did neither; it walked a fixed list of eight documents, so a new
organic document or an arrow manifest was invisible to the budgets, and no
link anywhere was resolved. Its registration check also accepted a
parenthesized path anywhere in the agent guide, which a prose link satisfies,
rather than a row in the index table the rule is about. Separately, the
ledger's most-cited key, `ieee754-2019`, matched neither citation pattern,
because a standard's designation carries digits inside the name. The key was
defined and cited correctly, and the audit passed by seeing neither side,
which is the failure the family names first, a check implying more than it
decides.

## Decision

The audit does what its rulebook says. Living documents are enumerated
rather than listed: the spine, every `docs/*.md`, and every arrow manifest,
with the manifests registered by their folder's index row. Registration
means a row in the index table, not a mention anywhere in the guide. Every
relative link in a living document must resolve, and every root-anchored
path one names in backticks must exist, a token whose first segment the
root does not know being read as prose. Records stay exempt end to end.

The citation-key form widens by one case. A standard with no author's name
is cited by its designation with the year suffixed, `[ieee754-2019]`, and
both patterns accept digits inside the name. The immutable claims already
citing that key are the reason the form moves to the ledger rather than
the ledger to the form.

Each new rule enters the selftest with a plant that proves it fires: an
unregistered organic document, a dead link, a named path that does not
exist, an over-budget document outside the old list, and a cited
standard-form key with no bibliography entry.

## Consequences

A document created under `docs/` without a row in the index now fails the
audit instead of silently not existing. The arrow manifests join the
150-line budget. The rulebook's description of the audit is true again,
and the one sentence that changed meaning, the citation-key form, is this
record's to answer for.
