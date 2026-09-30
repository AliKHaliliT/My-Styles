# 0012. Tie density on real amounts follows the rate and the endings

Status: Conjecture
Date: 2026-09-30

## Claim

When a ledger multiplies a two-decimal price by a rate, a tax, a discount,
a share of a split, the fraction of results that land exactly halfway
between two cents is fixed by the rate's decimal expansion and by which
cent digits the prices cluster on, so the one-tie-in-ten density of the
deterministic grid in
[claim 0009, Half even cancels the drift that half up accumulates](0009-half-even-cancels-the-drift-that-half-up-accumulates.md)
is a property of the grid, and a real ledger may meet ties far more rarely
or far more often. It must convince a maintainer who reads the grid's
drift as the drift a real ledger accumulates.

## Evidence

None.

## Threats

- The arithmetic, not the market. A tie needs a third decimal of exactly
  five, which a price times a rate produces only for rates whose expansion
  allows it, so the sweep an arrow runs must vary the rate as well as the
  distribution of endings drawn from
  [claim 0011, Retail price endings cluster on a few digits](0011-retail-price-endings-cluster-on-a-few-digits.md).
