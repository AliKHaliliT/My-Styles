# 0014. Rounded parts miss the rounded total at a known rate

Status: Supported
Date: 2026-10-16

## Claim

When n shares of a total are each rounded to the nearest unit, their sum
misses the rounded total with a probability that does not vanish, and
the miss has a known distribution. Under smooth random shares its mean
tends to zero for standard rounding and its variance to n over twelve
units, so a ledger of many lines rounded one by one expects its lines to
disagree with its total by an amount that grows with the square root of
the line count, and the disagreement is a property of rounding parts,
not of any tie rule. It must convince a maintainer who expects rounded
lines to add up to the rounded total as a matter of course.

## Evidence

Read evidence, quoted from the works the pass of 2026-10-16 read in full,
with no pin, since no tree produced it.

Janson states the setting, p. 18 [janson2013]: "Let p1, ..., pn be given
probabilities (or proportions) with the sum of pi equal to 1 and let N be
a (large) integer. Suppose that we want to round N pi to integers, by
standard rounding or, more generally, by rho-rounding for some given rho.
It is often desirable that the sum of the results is exactly N, but this
is, of course, not always the case." His Example 7.1: "If a statistical
table is presented as percentages, with all percentages rounded to
integers, we have this situation with N = 100; the percentages do not
necessarily add up to 100, and the error is given by Delta 1/2. Rounding
to other accuracies correspond to other values of N. This has been
studied by several authors, see Mosteller, Youtz and Zahn and Diaconis
and Freedman." Theorem 7.5, pp. 19 to 20, gives the limit of the
discrepancy for shares with an absolutely continuous distribution. Its
expectation tends to n(1/2 - rho) + gamma, which is zero for standard
rounding with gamma equal to zero, and for n of three or more its variance
tends to n/12. Corollary 7.8 names the standard case "the result of
Diaconis and Freedman", and Example 7.9 states that the asymptotic
probability that standard rounding yields the correct sum is a fixed
Euler-Frobenius ratio, with Remark 7.10 warning that for finite N the
result is only asymptotic because of edge effects.

Cont and Heidari, p. 5 [cont2014]: "As the example x = (2.25, 3.4, 4.35)
shows, componentwise rounding to the nearest integer may fail to satisfy
such a constraint"; and p. 6: "The following problem arises e.g. in
rounding problems encountered in accounting, where one rounds N entries
while leaving the total unchanged up to the nearest dollar".

For tables the failure is structural rather than probabilistic.
Fischetti and Salazar, p. 555 [fischetti1998]: "Cox and Ernst (1982)
proved that the zero-restricted CRP associated to any 2-dimensional
table with row and column marginal totals is always feasible", and
"Causey, Cox, and Ernst (1985) showed that the zero-restricted CRP on
3-dimensional tables with marginal totals is not always feasible, and
gave a simple 2 x 2 x 2 counter-example"; their own finding, p. 553, is
"that 4-dimensional tables often admit no zero-restricted rounding". The
census report says the same of three dimensions, p. 1 [fagan1988]:
"given an arbitrary three dimensional table, a controlled rounding may
not exist."

The forint study measured the rate on receipts, p. 16 [leszko2009]: "the
more items we purchase simultaneously, the more evenly the last digit of
the final sum on the receipt is distributed between 0 and 9", so that
"in the case of purchases of 10 or more items, there is an equal
probability of the cashier rounding the final sum upwards or downwards".

## Threats

- Depth. The classic results are quoted through [janson2013], which
  restates and extends them; [diaconis1979] and [mosteller1967] were
  read at abstract depth, their publishers refusing scripted readers,
  and [happacher2001], [heinrich2017] and [balinski1993], which carry
  the discrepancy's distribution and variance in their own words, at
  abstract depth as well. A person with library access reads them and
  the claim stands or moves on what they say.
- Model. The n/12 variance and the vanishing mean hold in the limit of a
  large accuracy for shares with a smooth distribution; a ledger's lines
  are amounts, not shares of a fixed total, and their fractional parts
  cluster, as [claim 0011, Retail price endings cluster on a few
  digits](0011-retail-price-endings-cluster-on-a-few-digits.md) holds,
  so the rate on real lines is a conjecture until an arrow measures it.
- Units. The discrepancy is counted in rounding units, cents for a
  ledger; what it costs in money follows from the unit and the count,
  not from this claim.
