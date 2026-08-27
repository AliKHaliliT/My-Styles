# 0001. Tie-breaking choice is negligible at scale

Status: Conjecture
Date: 2026-08-27

## Claim

Over a deterministic grid of ten thousand three-decimal amounts, the choice
between round half up and round half even moves the accumulated total by less
than one cent. It must convince a maintainer choosing a ledger's rounding
policy, who today chooses by taste.

## Evidence

None.

## Threats

- External validity. The grid fixes tie density at one in ten by construction,
  and real price distributions may tie far less often or not at all. Conceded;
  the grid is chosen for reproducibility, and the transfer to real
  distributions is named as an open decomposition line in QUESTION.md rather
  than claimed.
- Mono-operation bias. One grid, one accumulation shape, one scale. Partly
  met by planning the run at two scales; otherwise conceded.
