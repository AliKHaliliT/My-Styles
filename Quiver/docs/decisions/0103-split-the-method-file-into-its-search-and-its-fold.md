# 0103. Split the method file into its search and its fold

Status: Accepted
Date: 2026-10-17

## Context

The method file ran to two thousand six hundred words, past what a
reader takes in whole, and it was read whole before every pass by the
guide's own rule. Its steps fall in two halves a pass runs at different
times. The first half runs before and during the search, the seeds, the
strings, the screening and the field bindings that name the indexes and
the noise. The second runs after it, the checks, the completeness
review, the fold, the record and the forms a pass takes.

## Options considered

- Leave the file whole and trust the reader to skip to the stage at
  hand. Refused, because the rule says whole, and a rule the reader is
  trusted to bend is a rule the record cannot hold.
- Move the field bindings out as a file of their own. Refused, because
  the bindings are the search's indexes, noise and reasons, rewritten
  per project, and they belong beside the steps that use them.

## Decision

The method file is read as two documents, each frozen as the rulebook
is: `docs/METHOD.md` with the preamble, the steps before the search,
the search, the screening and the demo's field bindings, and
`docs/FOLD.md` with the checks, the completeness review, the fold, the
record and the forms a pass takes. Every paragraph moved as it stood.
The pass document, the rules for review records, the spine, the index,
the README's tree and the map name both.

## Consequences

A pass reads the half it is in whole, and the budget the family moves to
next has two documents to hold instead of one it could not.
