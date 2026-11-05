# 0019. Methods round parts to agree with a total

Status: Supported
Date: 2026-11-04

## Claim

This record supersedes [claim 0015, Methods round parts to agree with a
total](0015-methods-round-parts-to-agree-with-a-total.md) after the pass
of 2026-11-04 read whole the founding papers it quoted through later
works. The claim is unchanged but for its dates.

A ledger that must show each line rounded and a total rounded once from
the exact sum has methods for it that the literature has held for
decades, in commercial code since 1976 and for tables since 1982.
Controlled rounding rounds every entry of a table to a neighboring
multiple of the base while every marginal total stays the rounded total,
and is always possible in two dimensions. The largest remainder rule
rounds up the entries with the largest fractional parts until the parts
sum to the total, and in doing so minimizes every symmetric error at
once, in linear time. The standards carry the difference as its own
amount. The choice among them is a design decision, not a discovery to
be made per ledger. It must convince a maintainer who holds that a
ledger must choose between inconsistent lines and an inconsistent total.

## Evidence

Read evidence, quoted from the works the passes of 2026-10-16 and
2026-11-04 read in full, with no pin, since no tree produced it.

The founding definition, p. 423 [coxernst1982]: "We investigate the
problem of rounding all entries in a one- or two-dimensional tabular
array A to integer multiples of a positive integer base B subject to the
requirements" that "each entry in A is rounded to an adjacent integer
multiple of B" and that "the sum of the rounded values along any row (or
column) of A ... equals the rounded value of the corresponding row (or
column) total entry. We refer to a procedure satisfying (1)-(2) as a
controlled rounding of A and demonstrate that controlled roundings may
always be achieved in a tabular array by standard, computationally
efficient techniques." Why the conventional rule is not enough, p. 424:
"Although conventional rounding achieves minimum data distortion in the
sense of (3) for 1 ≤ p ≤ ∞, it often fails the additivity condition
(2)." The existence results, p. 427, Theorem 3.1: "A controlled rounding
R of A always exists." and Theorem 3.2: "The zero-restricted controlled
rounding problem always has a solution.", the zero-restricted problem
being the one in which, p. 426, "whenever an A-value a is an integer,
the quantity (R*(a) − a) is restricted to equal 0." The method's limit,
p. 429, is "an example that illustrates that controlled roundings cannot
always be obtained with prespecified roundings of the totals entries."

The commercial statement, p. 74 [berry1976]: "As long as rounding is
regarded as a scalar function (applied independently to each element
being rounded, without regard to its context) there is the risk that the
sum of the rounded parts will differ from the expected total. This vexes
accountants; when a small discrepancy is found, one is not certain
whether it arose from the benign effects of rounding, or is a symptom of
some other problem. Moreover, since funds must be accounted exactly,
there remains the question of what to do with the odd amounts missing or
left over." Its requirement, p. 75, is that "rounding must distribute
over summation", and its algorithm, on the same page: "Instead of adding
1 to each element whose fractional part is 0.5 or greater, first
calculate N, the amount by which the sum of the floors +/⌊X falls short
of the sum of the true values (expressing the sum to the nearest
integer). That determines the number of 1's that must be added to ⌊X.
Next for each element of X calculate A, its accuracy ranking. Select the
first N elements of X for which the floor is the least accurate
representation, and add 1 to each of them." Its guarantees, p. 77: "The
total of the components along the indicated axis is exactly equal to the
inital amount (when both are expressed in the same units)." and "The
elements thus obtained never differ from the true value by as much as
one unit in the last place, and never differ from the independently
rounded approximation by more than one unit." Its payroll case, p. 77:
"to make out a weekly paycheck to an employee whose annual salary is
fixed at 10000 (which is not evenly divisible by the 52 and 1/7 weeks in
a year) it is common practice to round down to 191.78, and to accumulate
the fractional underpayment week by week until (roughly every thirteenth
week) an entire penny can be added."

The line between a rule and a method, p. 476 [balinski1993]: "This paper
studies "rules of rounding," that is, procedures that round independent
of the sums that the numbers "should" satisfy. In contrast are "methods
of rounding," procedures that guarantee or force that the rounded
numbers are "justified" ... They are studied in a companion paper [1]."

The method stated for a general readership, p. 47 [wainer1998]: "Step I
of the Webster method is the usual one. With p_i being the exact
proportions, round 100p_i to the nearest integer n_i. If the rounded
numbers sum to 100, they are the final result." and "Step II is called
for only if the Step I results fail to sum to 100. (a) If the sum
exceeds 100, then find a small positive quantity ε and apply Step I to
(100 − ε)p_i until the new rounded numbers do sum to 100. (b) If the sum
stays below 100, apply Step I to (100 + ε)p_i until the rounded numbers
sum to 100." with the tie rule in its bracket, "if the fractional part
is equal to 1/2, then round to the nearest even integer (Eisenhart
1947)."; its Table 5, p. 49, shows the ten yearly distributions that had
summed to 99, 98 or 101 at integer percents all summing to 100 under the
method, at a cost the column puts at "+.08 and −.12" of a percent.

The census report defines the method, pp. 1 to 3 [fagan1988]: "Given a
positive integer b and an additive table of non-negative integers A ...
find an additive table B where [row and column sums are preserved] and
b_ij = [a_ij/b]b or [a_ij/b]b + b ... Such a table B is called a
controlled rounding of A." Fischetti and Salazar, p. 554 [fischetti1998]:
"The (zero-restricted) Controlled Rounding Problem (CRP) then calls for
finding a rounding of each entry a_i, such that M a = b and the
associated total rounding weight ... is minimized", a problem that "can
be solved in polynomial time for k-dimensional tables with marginals if
k <= 2", and their worked table on the same page rounds entries to tens
while its totals stay the totals of the rounded entries. Theorem 1 of
Doerr and others [doerr2006a] states that for any real matrix "a
rounding Y ... such that" the errors in every initial row interval,
every initial column interval and the whole matrix are "< 1 can be
computed in time O(mn log(mn))", and their randomized variant is
"unbiased, that is, for all entries y_ij of our rounding, we have
E(y_ij) = x_ij".

Cont and Heidari, abstract [cont2014]: "Given N real numbers whose sum is
an integer, we study the problem of finding N integers that preserve the
sum while minimizing the rounding error. We first show that every optimal
solution necessarily rounds each coordinate either to its floor or its
ceiling ... rounding upward the largest fractional parts simultaneously
minimizes the L q rounding error for every q >= 1." Their Problem 3,
p. 7, is the ledger's case, "Decimal rounding with exact preservation of
total", which "is equivalent to Problem 1"; p. 4 names the rule: "our
primary rounding rule coincides with the classical largest-remainder
(Hare-Niemeyer) method used in proportional apportionment"; and
Proposition 4.2, p. 25, gives "deterministic worst-case time complexity
O(N)". Coleman writes the same rule for practitioners, pp. 4 and 7
[coleman2025]: "Controlled Rounding: Rounding data to add up to a
control", and "The algorithm then rounds up the x_i corresponding to the
k largest m_i", where m_i is the fractional part. Ichimori measured how
often a divisor method coincides with plain rounding, abstract and
section 5 [ichimori2011]: "the probability that one state satisfies its
rounding-off constraint under the method of Webster is about 97.58%
while that under the method of Hill is about 95.73%".

The same rule runs in money libraries, and its failure mode is known,
Finding and Minimal counterexample [kadirbekov2026]: "Money::allocate()
computes its initial integer shares with exact arithmetic, but converts
the amount and ratios to binary float when ranking fractional
remainders"; for 7 000 000 000 000 000 units allocated 1:2 the library
returned [2333333333333334, 4666666666666666] against the exact
largest-remainder result [2333333333333333, 4666666666666667], and "The
allocated parts still sum to the original amount; the defect is the
proportional ranking of the residual unit."

The standards' device is the separate amount, section 10.1.2 and rule
BR-CO-16 [peppolbis3-2026]: "It is possible to round the expected payable
amount. ... Example: Amount 999.81 rounded to 1000. PayableRoundingAmount
= 0.19", with the amount due for payment defined as the total with VAT
less the paid amount plus the rounding amount. Cegiełka and Łyko, p. 16
[cegielka2017], report the experiment in which, among the divisor
methods read as rounding rules, rounding to the nearest integer is "the
only neutral rounding method", leaving no constituency ahead on average.

## Threats

- Depth. [cox1987], whose procedure makes a controlled rounding
  unbiased, and the apportionment seed [pukelsheim2014] stay at abstract
  depth; a library search on 2026-11-03 found no copy of the first, and
  the claim quotes its result from [doerr2006a] and [fischetti1998],
  which cite it.
- Standing. [cont2014] is a preprint, in its third version of 2026, with
  no published version found on 2026-10-16; [kadirbekov2026] and
  [coleman2025] are self-published, second-tier grey, and the floor this
  bibliography declares is the first tier. The claim rests on them for
  the ledger's case and the practitioner's rule, and on the reviewed
  works for the methods.
- Scope. Which method a ledger should choose, and what each costs in a
  line that moves by a cent, is the conjecture of [claim 0016, The rule
  decides whether the tie rule
  accumulates](0016-the-rule-decides-whether-the-tie-rule-accumulates.md),
  not this claim.
