# The Question

When many monetary amounts are rounded to whole cents and summed, how much
error does the choice of tie-breaking rule accumulate, and does it matter at
ledger scale?

## Why it is worth asking

Monetary code rounds constantly, and the two common tie-breaking rules, round
half up and round half even, agree everywhere except on amounts that sit
exactly halfway between two cents. Folk wisdom treats the choice as taste. The
IEEE floating-point standard defines ties-to-even as its default for a stated
reason, freedom from bias in long computations [ieee754-2019], and the classic
floating-point literature warns that rounding error compounds in accumulation
[goldberg1991], while the enterprise-patterns literature treats money as a
first-class type precisely because representation and rounding choices leak
into totals [fowler2002]. Whether the tie rule alone moves a realistic total
by an amount anyone should care about is an empirical question, and it is the
kind a maintainer decides by recollection unless someone runs it.

## The decomposition

- Open, held as [claim 0001](claims/0001-tie-breaking-choice-is-negligible-at-scale.md):
  over a deterministic grid of ten thousand three-decimal amounts, the choice
  between the two rules moves the accumulated total by less than one cent.
  The experiment lives in the [coinwise](../arrows/coinwise/) arrow.
- Not yet conjectured: how the answer changes when amounts carry more than
  three decimals, and how tie density behaves on real price distributions
  rather than a grid. Both stay open until the first conjecture is settled.

## Recorded shortenings

The spine is shortened in one place. No pilot run precedes the main
experiment, because the grid is deterministic and the full run is as cheap as
any pilot would be.
