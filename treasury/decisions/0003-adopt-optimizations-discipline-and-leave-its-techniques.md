# 0003. Adopt optimization's discipline and leave its techniques

Status: Accepted
Date: 2026-08-18

## Context

Study 0002 folded 9,188 named optimization concepts into a vocabulary of
1,272 in six families, and the owner asked how the styles should consume
it. This record preserves the family-level disposition; the per-style
records titled "Make growth a choice and speed a measurement" hold the
adopted half's rationale where its bytes landed.

The dividing fact: 939 of the 1,272 entries name a price, and a price means
conditional, a technique that wins in one context and loses in the next. A
style is a table of unconditional rulings, so mandating any priced
technique would be study 0001's definition of an anti-pattern, a primitive
winning a conflict it should have lost. What is general is the discipline
that governs the techniques, and it splits on one further fact: a
measurement sees code on today's data, so it cannot catch a growth-rate
mistake at write time, while growth is the one performance property
readable from the code alone.

## The adopted half

Two gate items, byte-identical across the styles. Growth honesty: what
each loop's or query's cost grows with is a choice, not an accident, and no
change buys a worse growth rate where a construction of equal effort
exists. The measured line: nothing is made faster without a measurement
that demanded it, and every optimization that lands records its measurement
and its price. The pair is the treaty between the two schools the study
catalogs as opposed entries, constant attention governing growth and the
staged approach governing everything priced. The checkable half, at zero
new dependency: the Python styles select PERF and C4 in ruff, and the
client style enables slow-regex from the Sonar plugin it already carries,
catastrophic backtracking being a growth accident inside a regular
expression.

## The refusals

- Technique mandates in the conventions, any caching or batching or layout
  rule. Every such entry is conditional by its own price clause.
- One merged gate item instead of two. The failures point in opposite
  directions and fire at different times, one while writing and one while
  optimizing, and a compound item cannot be weighed in one look.
- Continuous benchmarking with a regression ratchet. The study prices it
  itself, dedicated stable hardware and noise-stalled delivery, which is
  speculative scaffolding for template workloads.
- Complexity annotations on every export's documentation. Burden without a
  reader; the point-of-use truth item already holds any claim actually
  made.

## Consequences

The vocabulary's four technique families stay design-time reading, reached
through the treasury by pointer and never copied into a style. The two
gate items and three lint selections are the study's entire footprint in
the family's law, which is itself a finding: of 1,272 entries, the general
residue is two sentences of judgment and a handful of free-win checks, and
everything else is a decision some project makes against its own terrain.
