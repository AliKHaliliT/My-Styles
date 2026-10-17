# 0016. The rule decides whether the tie rule accumulates

Status: Conjecture
Date: 2026-10-16

## Claim

Whether the tie-breaking rule reaches a ledger's total depends on the rule
the ledger files under, not on the arithmetic. Under a rule that sums
rounded lines, EN 16931 as Peppol carries it, the total is the sum of n
roundings and the tie rule accumulates as
[claim 0009, Half even cancels the drift that half up accumulates](0009-half-even-cancels-the-drift-that-half-up-accumulates.md)
measured; under a rule that adds exact amounts and rounds once, the
United States and Canadian filing rules and the cash rounding acts, the
tie rule touches one rounding and is a matter of presentation. A ledger
can serve both at once by keeping exact amounts, showing lines rounded,
reporting the total rounded once, and carrying the difference either as
the standards' rounding amount or by the largest remainder rule of
[claim 0015, Methods round parts to agree with a total](0015-methods-round-parts-to-agree-with-a-total.md),
whose adjustment moves at most one unit per line. The conjecture is that
such a ledger's total differs from a line-summed total by the amount
[claim 0014, Rounded parts miss the rounded total at a known rate](0014-rounded-parts-miss-the-rounded-total-at-a-known-rate.md)
predicts, and that the tie rule's share of that difference is the drift
of claim 0009 and nothing more. It must convince a maintainer who reads
the grid's drift as a property of the tie rule rather than of the level
at which the rule rounds.

## Evidence

None.

## Threats

- Rules. The rules read are five jurisdictions and two standards, held in
  [claim 0013, Rules fix the level at which a ledger rounds](0013-rules-fix-the-level-at-which-a-ledger-rounds.md);
  a rule that both sums rounded lines and forbids a rounding amount would
  leave no room for the exact total, and none read does so, but Australia
  is unread and queued.
- Measurement. No arrow has built the two ledgers side by side; the
  conjecture settles when one does, over the rate and endings sweep that
  [claim 0012, Tie density on real amounts follows the rate and the endings](0012-tie-density-on-real-amounts-follows-the-rate-and-the-endings.md)
  asks for, so that the tie density is the real one.
- Presentation. A reader may hold that a line shown rounded and a total
  that does not equal the sum of the lines shown is itself an error a
  rule forbids; the standards answer it with the rounding amount, and the
  filing rules with the instruction to round only the total, but a
  jurisdiction that demands both may exist outside the five read.
