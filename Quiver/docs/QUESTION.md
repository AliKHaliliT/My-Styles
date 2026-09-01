# The Question

When many monetary amounts are rounded to whole cents and summed, how much
error does the choice of tie-breaking rule accumulate, and does it matter at
ledger scale?

## Why it is worth asking

Monetary code rounds constantly, and the two common tie-breaking rules, round
half up and round half even, differ only on amounts that sit
exactly halfway between two cents. It is tempting to treat the choice as taste. The
IEEE floating-point standard defines ties-to-even as its default for a stated
reason, freedom from bias in long computations [ieee754-2019], and the classic
floating-point literature warns that rounding error compounds in accumulation
[goldberg1991], while the enterprise-patterns literature treats money as a
first-class type precisely because representation and rounding choices leak
into totals [fowler2002]. Whether the tie rule alone moves a realistic total
by an amount anyone should care about is an empirical question, and it is the
kind a maintainer decides by recollection unless someone runs it.

## The decomposition

- Settled. The negligibility conjecture is refuted in
  [claim 0004](claims/0004-the-tie-rule-moves-the-total-by-dollars-not-cents.md),
  and what the evidence supports is held in
  [claim 0005](claims/0005-half-even-cancels-the-drift-that-half-up-accumulates.md).
  The experiment lives in the [coinwise](../arrows/coinwise/) arrow.
- Not yet conjectured: how the answer changes when amounts carry more than
  three decimals, and how tie density behaves on real price distributions
  rather than a grid. Both are open for a conjecture whenever the inquiry
  returns to them.

## Recorded shortenings

The spine is shortened in one place. No pilot run precedes the main
experiment, because the grid is deterministic and the full run is as cheap as
any pilot would be.
