# 0011. Retail price endings cluster on a few digits

Status: Supported
Date: 2026-09-30

## Claim

The rightmost digit of a retail price is far from uniform. In American
scanner and Internet data and in New Zealand advertisements the digit 9
leads, with 5 and 0 next, and in Chinese advertisements the digit 8 leads,
with 5 and 9 next, so in every sample read three digits carry most of the
endings and the remaining digits share a few percent. It must convince a
maintainer who models the amounts a ledger rounds as uniformly spread over
their last digits.

## Evidence

Read evidence, quoted from the works the pass of 2026-09-30 read in full,
with no pin, since no tree produced it.

From the scanner data of one supermarket chain and the daily prices of 474
Internet products [levy2011]: "In Figure 1, we report the frequency
distribution of the last digit of the prices in Dominick's data. If a
digit's appearance as a price-ending were random, then we should have seen
10 percent of the prices ending with each digit. As the figure indicates,
however, about 69 percent of the prices ended with a "9." The next most
popular ending was "5," accounting for only 12 percent of all price
endings. Only a small proportion of the prices ends with other digits."
and, of the Internet data, ""9" was the most popular terminal digit (33.4
percent), followed by "0" (24.1 percent), and "5" (17.4 percent)."

From 1,188 advertised prices in Palmerston North in 1995 [holdershaw1997]:
"In total, 87% of prices were defined as odd prices. Approximately 60% of
prices ended in the digit 9, with a further 30% of prices ending in the
digit 5. Thus, approximately 90% of prices ended in either "9" or "5".
Three digits (0, 5, 9) accounted for nearly 97% of price endings, with the
remaining seven digits accounting for only slightly over 3%." Its Table 1
gives the digits 0 through 9 as 7.5, 0.26, 0.26, 0.76, 0.26, 28.6, 0.26,
0.4, 1.0 and 60.7 percent.

From 499 prices advertised in Shanghai, Hong Kong and Taiwan in 1996
[simmons2003]: "The distribution of rightmost salient ending digits differs
considerably from chance (X2 [9] = 576.97; p < .001)." and "The occurrence
of three digits (5, 8, and 9) was greater than the 10% chance expectation."
Its Figure 1 gives the digits 0 through 9 as 9.2, 1.6, 7.0, 4.8, 1.4, 14.7,
6.2, 3.4, 39.9 and 11.8 percent.

## Threats

- Selection. Three works read in full out of nine that passed the
  screening, chosen by the existence of an open copy and not by the sample;
  the six unread works are queued and may report other shapes, though the
  three abstracts that state a leading digit all name 9.
- Representation. The three studies count different things, the cent digit
  of a scanner price, the rightmost digit displayed in an advertisement, and
  the rightmost nonzero digit of an integer price in yuan or dollars, so the
  percentages are not one distribution and the claim rests on their common
  shape, a few digits carrying most endings.
- Age. The samples date from 1989 to 2005; endings in a later market or a
  currency without a cent coin may differ, and the claim says nothing about
  them.
