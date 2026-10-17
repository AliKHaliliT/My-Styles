# 0015. Methods round parts to agree with a total

Status: Supported
Date: 2026-10-16

## Claim

A ledger that must show each line rounded and a total rounded once from
the exact sum has methods for it that the literature has held since the
1960s. Controlled rounding rounds every entry of a table to a
neighboring multiple of the base while every marginal total stays the
rounded total, and is always possible in two dimensions. The largest
remainder rule rounds up the entries with the largest fractional parts
until the parts sum to the total, and in doing so minimizes every
symmetric error at once, in linear time. The standards carry the
difference as its own amount. The choice among them is a design
decision, not a discovery to be made per ledger. It must convince a
maintainer who holds that a ledger must choose between inconsistent
lines and an inconsistent total.

## Evidence

Read evidence, quoted from the works the pass of 2026-10-16 read in full,
with no pin, since no tree produced it.

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

- Depth. The founding papers of controlled rounding, [coxernst1982] and
  [cox1987], and the apportionment seeds [balinski1993] and
  [pukelsheim2014] were read at abstract depth; the methods are quoted
  here from [fagan1988], [fischetti1998], [doerr2006a] and [cont2014],
  which cite them. [berry1976], the earliest statement of distributive
  rounding in commercial code, is read at abstract depth too.
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
