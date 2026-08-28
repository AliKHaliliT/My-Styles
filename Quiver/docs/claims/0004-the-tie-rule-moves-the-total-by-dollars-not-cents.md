# 0004. The tie rule moves the total by dollars, not cents

Status: Refuted
Date: 2026-08-28

## Claim

This record re-pins [claim 0002](0002-the-tie-rule-moves-the-total-by-dollars-not-cents.md)
after the arrow moved past its pin for a dialect rewrite and its promotion to
a full style adaptation, work that touched no arithmetic. The claim itself is
unchanged. It settles the line of
[claim 0001](0001-tie-breaking-choice-is-negligible-at-scale.md), which
conjectured that over a deterministic grid of ten thousand three-decimal
amounts the choice between round half up and round half even moves the
accumulated total by less than one cent. The conjecture remains refuted. It
was addressed to a maintainer choosing a ledger's rounding policy, and the
refutation is addressed to the same reader.

## Evidence

The experiment re-ran in `arrows/coinwise at 9c955ac55f26` by calling
`run_drift_experiment(10_000)` on the grid of amounts i divided by one thousand
for i from 1 to 10,000, whose exact sum is 50,005.000 and which contains 1,000
half-cent ties by construction.

- Round half up: rounded total 50,010.00, drift +5.000.
- Round half even: rounded total 50,005.00, drift 0.000.

The numbers equal the superseded record's at its old pin, digit for digit. The
two totals differ by 5.00, five hundred times the conjectured bound of one
cent, and the drift equals one half cent per tie under half up, so the
conjecture dies wherever ties occur at any realistic density.

Reopens for amount populations that carry no half-cent ties, such as prices
already quoted in whole cents, where the two rules coincide on every input and
the choice is genuinely free.

## Threats

- External validity. The grid fixes tie density at one in ten, and real price
  distributions tie less often. Met in part by the per-tie form of the result,
  half a cent of drift per tie under half up, which lets a reader scale to
  their own tie density; the transfer itself remains open in QUESTION.md.
- Mono-operation bias. One accumulation shape and one grid. Conceded; the
  companion claim widens scale but not shape.
