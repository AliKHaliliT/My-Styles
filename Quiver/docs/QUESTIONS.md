# The Questions

The inquiry asks whether the tie-breaking rule in monetary rounding is a
matter of taste or a source of error a ledger must govern. It is answered
when the rule's effect on a total is measured at scale, the density of ties
on real amounts is known, and what a filing rule leaves to the rule is
settled.

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

## The questions

### 1. When many monetary amounts are rounded to whole cents and summed, how much error does the choice of tie-breaking rule accumulate, and does it matter at ledger scale?

- Settled. The negligibility conjecture is refuted in
  [claim 0008, The tie rule moves the total by dollars, not cents](claims/0008-the-tie-rule-moves-the-total-by-dollars-not-cents.md),
  and what the evidence supports is held in
  [claim 0009, Half even cancels the drift that half up accumulates](claims/0009-half-even-cancels-the-drift-that-half-up-accumulates.md).
  The experiment lives in the [coinwise](../arrows/coinwise/) arrow.
- Constrained by what a runtime already does. Two runtimes default to
  opposite tie rules, held in
  [claim 0010, Two runtimes default to opposite tie rules](claims/0010-two-runtimes-default-to-opposite-tie-rules.md),
  so the arrow pins its rule rather than inheriting one.
- Not yet conjectured: how the answer changes when amounts carry more than
  three decimals.
- Shortened. No pilot run precedes the main experiment, because the grid is
  deterministic and the full run is as cheap as any pilot would be.

### 2. How often do real amounts land exactly halfway between two cents, and what fixes that density?

- Conjectured. Tie density on real amounts follows the rate applied and the
  digits prices cluster on, held in
  [claim 0012, Tie density on real amounts follows the rate and the endings](claims/0012-tie-density-on-real-amounts-follows-the-rate-and-the-endings.md),
  resting on the read evidence of
  [claim 0011, Retail price endings cluster on a few digits](claims/0011-retail-price-endings-cluster-on-a-few-digits.md);
  an arrow that sweeps rates over a read distribution of endings would
  settle it.

### 3. Can a ledger that must show each line rounded still report its total rounded once from the exact sum, as a filing rule requires, so that the tie rule becomes a choice about presentation rather than accumulation?

- Not yet conjectured. The filing rule is read in [irs2025]; a conjecture
  waits on whether a line-rounded ledger can carry an exact total beside its
  lines, and a pass over the rules such ledgers follow would open one.
