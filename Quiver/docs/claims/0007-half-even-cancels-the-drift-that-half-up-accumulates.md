# 0007. Half even cancels the drift that half up accumulates

Status: Supported
Date: 2026-08-28

## Claim

This record re-pins [claim 0005](0005-half-even-cancels-the-drift-that-half-up-accumulates.md)
after the arrow moved past its pin to complete Keel's library citizenship, a
NullHandler on the package logger, version resolution from package metadata,
and the suite pinning both, work that touched no arithmetic. The claim itself
is unchanged. On the deterministic grid, round half up accumulates drift
linearly in the number of ties, at exactly half a cent per tie, while round
half even cancels to zero drift at every tested scale. It must convince a
maintainer choosing a ledger's rounding policy, and it is the empirical form
of the reason the floating-point standard makes ties-to-even its default
[ieee754-2019].

## Evidence

The experiment re-ran in `arrows/coinwise at bfcb32ce5403` by calling
`run_drift_experiment` at two scales on the grid of amounts i divided by one
thousand. The numbers equal the superseded record's at its old pin, digit for
digit.

- At 10,000 amounts, 1,000 ties. Half up drifts +5.000, which is 1,000 ties at
  half a cent each. Half even drifts 0.000, rounded total equal to the exact
  50,005.00.
- At 100,000 amounts, 10,000 ties. Half up drifts +50.000, again half a cent
  per tie. Half even drifts 0.000 against the exact 5,000,050.00.

Half even cancels on this grid because tie cents alternate parity evenly, so
upward and downward tie breaks balance. The completeness of the scale sweep is
bounded: the two scales above are the whole set run, and behaviour between and
beyond them is interpolation offered as judgment.

## Threats

- External validity. Grid amounts, not market prices; the parity balance that
  gives exactly zero is a property of the grid. Met in part by the mechanism
  being stated, so a reader can check parity balance in their own data;
  conceded beyond that, and the real-distribution line stays open in
  QUESTION.md.
- Confounding of tie density with scale. The grid holds density fixed at one
  in ten across both scales, so scale and density do not vary together here.
