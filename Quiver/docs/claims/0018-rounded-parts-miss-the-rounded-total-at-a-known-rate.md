# 0018. Rounded parts miss the rounded total at a known rate

Status: Supported
Date: 2026-11-04

## Claim

This record supersedes [claim 0014, Rounded parts miss the rounded total
at a known
rate](0014-rounded-parts-miss-the-rounded-total-at-a-known-rate.md)
after the pass of 2026-11-04 read whole the works whose results it
quoted through a restatement. The claim is unchanged.

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

Read evidence, quoted from the works the passes of 2026-10-16 and
2026-11-04 read in full, with no pin, since no tree produced it.

The founding measurement, in the summary of [mosteller1967], reprint pp.
399 to 400: "We find that the probability that the sum of rounded
percentages adds to exactly 100 percent is certain for two categories,
about three-fourths for three categories, about two-thirds for four
categories, and about √(6/cπ) for larger numbers of categories, c, on
the average when categories are not improbable." Its Table 1, reprint p.
403, counts the lines of one study's tables whose percentages, rounded
to the nearest 1 percent, sum to exactly 100 as 72.93, 66.40, 58.73,
58.38, 46.90, 39.54 and 42.65 percent for three to nine categories;
reprint p. 400: "This failure to add to 100 percent occurs so frequently
that, if very many sums of percentages do add to 100 percent in a set of
reported tables, one begins to suspect the reporter of fudging." The
limit, reprint p. 409: "Limiting case. For fixed c, as the grid gets
fine (Δ → 0), it can be shown that the mean of the sum of the rounded
values tends to n in units of Δ, or to 1 in nΔ. The variance tends to
c/12 in units of Δ². This result is fairly reasonable if we assume that
the rounding errors are uncorrelated and uniformly distributed over an
interval of length Δ for each of the c pieces." On ties, reprint p. 401:
"If a number ends in a 5 that must be rounded, our rule is to round to
the nearest even digit, but a high-speed computer often has views of its
own about this, since it may produce 2.5 as 2.4999999, depending on just
how it carried out the calculation. Consequently, we set this rounding
5's problem aside for the moment and regard it as a rare event not worth
special attention in this study of average results."

The proof, p. 360 [diaconis1979], Theorem 1: "Suppose p1, ..., pc are
uniformly distributed over the simplex (1). As the rounding number n
approaches infinity, n{Σ r_n(p_i) − 1} converges in distribution to
r_1(Σ V_i) where V_i are independent and uniformly distributed on [−.5,
.5]." and Theorem 2, that the sum rounds to one "with probability (6/π(c
− 1))^1/2 + O(1/c^3/2)."; on the same page: "The assumption that p1,
..., pc are uniformly distributed over the simplex (1) is not critical.
Any absolutely continuous distribution will do, as shown in Section 4."
The small-sample caveat, p. 362: "MYZ also consider the multinomial
model with p1, ..., pc fixed rather than random. On p. 856 of their
article, MYZ seem to assert that with large samples the multinomial
model behaves like the broken-stick model. The argument of Section 2
shows that this cannot be correct." and p. 363: "MYZ's Table 3 shows,
however, that for samples of size N = 1 to 20, this chance is close to
75 percent." Its reading of a classic table of leading digits, p. 364:
"Direct calculation shows that the entries in columns 3 and 9 have been
incorrectly rounded." and "Thus, rounding to help the data fit the
theory can make a difference."

The generalization to other rules, p. 479 [balinski1993], Theorem 3.1:
"Suppose p is absolutely continuously distributed on the simplex and
ρ^d_t is based on d(k) = k + C, C ∈ [0, 1]. Then, as t → ∞, Pr(x_N = 1)
→ Pr(C − 1 ≤ V_1 + ... + V_{n−1} ≤ C) where the V_i's are independent
and uniformly distributed on [−C, 1 + C]." and "From Theorem 3.1 it
follows that among the stationary divisor rules (or 0-stationary ones)
the MYZ-rule, or Webster's rule ρ^w_t, maximizes the probability that in
the limit as t → ∞ the sum of the roundings is 1."; p. 482, that the
rate in the best case, "≈ √(6/(π(n − 1))) + o(n^−1/2) can be very slow."
For tables, p. 500: "The limit relations (6.3), (6.4) show that the
chance that p = (p_ij) is justified is much smaller than the chance that
the vector of mn entries p_ij is justified".

The restatement the superseded claim quoted stands, p. 18 [janson2013],
Example 7.1: "If a statistical table is presented as percentages, with
all percentages rounded to integers, we have this situation with N =
100; the percentages do not necessarily add up to 100, and the error is
given by Delta 1/2." Its Theorem 7.5, pp. 19 to 20, gives the limit of
the discrepancy for shares with an absolutely continuous distribution,
with an expectation that tends to n(1/2 - rho) + gamma, zero for
standard rounding with gamma equal to zero, and a variance that tends to
n/12 for n of three or more, and its Corollary 7.8 names the standard
case "the result of Diaconis and Freedman".

The column that carried the result to a general readership, p. 46
[wainer1998]: "Sums of rounded proportion often fail to add to 1." and
"Mosteller, Youtz, and Zahn (1967) showed that the probability that
rounded proportions add up to 1 depends strongly on the number of
categories; with a large number of categories, it is about 1.38 ×
c^−1/2." Its Tables 3 and 4, p. 48, give ten years of one test's score
distribution summing to 100.00, 100.01, 99.99, 100.00, 99.97, 99.98,
100.00, 99.98, 100.03 and 99.99 at two decimals and to 99, 101, 99, 98,
98, 101, 99, 98, 101 and 100 at integer percents: "We now see that only
one (1990) of the ten years shown still sums to 100%."

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

- Depth. [happacher2001] and [heinrich2017], which carry the
  discrepancy's distribution and variance in their own words, were read
  at abstract depth, their publishers refusing scripted readers, and no
  person has fetched them; the claim rests for those results on
  [mosteller1967], [diaconis1979] and [balinski1993], read whole.
- Model. The n/12 variance and the vanishing mean hold in the limit of a
  large accuracy for shares with a smooth distribution, and
  [diaconis1979] shows at p. 362 that for a fixed multinomial the chance
  of a correct sum can fall to zero as the sample grows while samples of
  twenty or fewer behave as the limit says; a ledger's lines are
  amounts, not shares of a fixed total, and their fractional parts
  cluster, as [claim 0017, Retail price endings cluster on a few
  digits](0017-retail-price-endings-cluster-on-a-few-digits.md) holds,
  so the rate on real lines is a conjecture until an arrow measures it.
- Edition. [mosteller1967] is quoted from its reprint, whose pages the
  claim cites, and the page of the original that [diaconis1979] answers
  was not checked against the original pagination.
- Units. The discrepancy is counted in rounding units, cents for a
  ledger; what it costs in money follows from the unit and the count,
  not from this claim.
