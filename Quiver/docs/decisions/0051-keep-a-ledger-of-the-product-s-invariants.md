# 0051. Keep a ledger of the product's invariants

Status: Accepted
Date: 2026-09-18

## Context

The family states what its products must never do in prose. The README and
the map of every seat carry between four and thirteen sentences with never,
always, guarantee or invariant in them, two to five of those claims sit
beside a tool that refuses a violation, an import contract or a lint rule,
and nothing lists them. Treasury study 0006 read how the field binds a
stated invariant to something that holds it, and found two traditions that
never meet, the formal one binding a single claim with precision about what
a green is worth and the certification one keeping a set of claims complete
and read. No field names the artifact in which an ordinary project writes
its own invariants and binds each to whatever holds it. The family's ruling
on the study, treasury 0035, keeps one.

## Evidence

The seats were measured on 2026-09-18. Across the five, the docs audits
carry 140 checks, all about documents and layout; ten named import contracts
and two property suites hold anything about product behaviour; no document
carries a section listing the claims. The two closest things the family has
are the named import contract, a sentence stating an invariant beside the
tool that refuses it, and the host seat's claim ledger, whose discipline of
status, evidence and threats is the discipline a set of claims needs. Every
seat has holders to point at, so every seat can carry a ledger with honest
rows, which is the condition an addition to the family must meet.

## Options considered

- Deriving the ledger from markers on tests and contracts. Refused, because a
  derived list says which holders exist and cannot carry a claim nobody has
  bound yet, and the unbound claim is the row a reader most needs to see.
- Rows as labelled lines under a heading, the upstream entry's shape.
  Refused for the table, because the rows are parallel facts with three
  fixed cells and the family's form rule puts parallel facts in a table.
- A rung that says proved. Refused, because a sampled property is not a
  proof, a passing test is not a theorem, and the strongest thing the
  family's tools can say is that no counterexample turned up.
- Failing the audit when the ledger is absent. Refused for consistency with
  the state file, whose absence the audit names as a check not run; the
  adoption gate requires the ledger, and a template's rows point at demo
  holders a child deletes, so the child's first audit run forces its own
  rows.
- A ledger held to the line budget. Refused, because the ledger grows with
  the product the way the map does.

## Decision

Every seat carries `docs/INVARIANTS.md`, a living document registered in the
index and the spine, with a table whose columns are the claim, its holder
and its rung. A holder is a tracked path in backticks, with a quoted needle
the file must contain where the path holds more than one thing, or the word
review. A rung is one of five words, impossible, generated cases, listed
cases, advised, and review, each defined in the rulebook's new section, and
a holder of review pairs only with the rung review. The docs audit decides
that every row has its three cells, that every holder path is tracked and
contains its needle, that every rung is on the list, and that review pairs
with review; it prints every review row as an advisory on every run. The
selftest plants a ghost holder, a missing needle, a rung off the list, a
review holder under another rung, a file holder under the review rung, and a
row short of a cell, expects each finding, and plants two legal rows that
must pass, one held by review, whose advisory it expects. The guide gains a
hard rule, a gate item, an adoption item, and an index row; the rulebook
gains the section, a spine row, and a clause in the mechanical-freshness
list; the map draws the file. This seat's rows point at its own contracts
and suites and carry one claim held by review. Under the ladder the
pointers land on the check rung, the truth of a row stays with review, and
the ledger itself is the form the study found no field had named.

## Consequences

A reader who wants to know what the product promises opens one file and
sees for each promise what refuses a violation and what that refusal is
worth. A project built from this seat writes its own rows at adoption and
keeps them as its own document. A claim nothing decides is printed on every
audit run until something does. The cost column and the commit hook the
study also raised are refused in treasury 0035 with the conditions that
reopen them.
