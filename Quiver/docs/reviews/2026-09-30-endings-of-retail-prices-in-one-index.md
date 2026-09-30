# Endings of retail prices in one index

Date: 2026-09-30

## Slice

First pass over the real-price-distribution line of the question, how the
rightmost digits of retail prices are distributed, because the tie density
a ledger meets depends on the amounts it rounds and the grid fixes one tie
in ten by construction.

## Boundary

One index, OpenAlex, searched on 2026-09-30 for works published from
1990-01-01 on, with the filter
`title_and_abstract.search:"price endings"|"price ending"|"9-ending"|"nine-ending"|"just-below pricing"|"odd pricing"`
as run, sorted by citation count, the sixty most cited of 460 records
examined at title and abstract. The criteria were written before the
screening. A work passes when it reports an observed distribution of the
rightmost digits of advertised or transaction prices in a currency. A work
is excluded when it studies perception or demand without reporting a
distribution, when its prices are not retail prices, securities, real
estate and fuel among them, or when its abstract could not be read. A work
that passed was read in full where an open copy could be fetched and
entered at abstract depth where it could not.
Flow: retrieved 460, screened 9, entered 9, read in full 3
Completeness: judgment

## Method

A systematic search of one index followed by title-and-abstract screening
against written criteria and full reading of the open copies, named from
the field's vocabulary as a rapid review bounded to one index and its
sixty most cited records, one screener, no snowballing.

## Stages

- Scouting: ran, the index's most cited works on price endings sit in consumer research and marketing journals with a few in economics, and a search of the same index on 2026-09-29 for the tie-breaking terms themselves returned nothing on point, so the slice's literature is the price-endings literature.
- Enumeration: ran, the nine works that passed the criteria were entered, three read in full at their tables of endings and six at abstract depth.
- Checks: ran, every key resolves and every work is entered with its edition.
- Completeness review: collapsed, the pass examined sixty of 460 records in one index and claims judgment.
- Fold: ran, one read-evidence claim on the clustering of endings, one conjecture on tie density under a rate, and the decomposition moved.
- Resolution: ran, the three works read in full agree that endings are far from uniform and differ on which digit leads, nine in the American and New Zealand samples and eight in the Chinese advertisements, which the claim states rather than settles.

## Found

- [levy2011] full
- [holdershaw1997] full
- [simmons2003] full
- [schindler1997] abstract
- [stiving1997] abstract
- [mace2012] abstract
- [strulovshlain2022] abstract
- [bray2006] abstract
- [nguyen2007] abstract

## Changed

[Claim 0011, Retail price endings cluster on a few digits](../claims/0011-retail-price-endings-cluster-on-a-few-digits.md)
opened as Supported on read evidence, and
[claim 0012, Tie density on real amounts follows the rate and the endings](../claims/0012-tie-density-on-real-amounts-follows-the-rate-and-the-endings.md)
opened as a conjecture resting on it; the decomposition's open line on real
price distributions became that conjecture.

## Left out

The 400 records the pass did not examine, below the sixtieth by citation
count; every other index; works published before 1990; and the full texts
of the six works entered at abstract depth, each queued in the state file
for a person with library access, from which the next pass over this slice
extends.

Cost: one session, with no separate token accounting.
