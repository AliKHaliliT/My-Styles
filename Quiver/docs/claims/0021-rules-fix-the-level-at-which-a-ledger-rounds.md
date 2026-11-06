# 0021. Rules fix the level at which a ledger rounds

Status: Supported
Date: 2026-11-05

## Claim

This record supersedes [claim 0020, Rules fix the level at which a
ledger rounds](0020-rules-fix-the-level-at-which-a-ledger-rounds.md)
after the pass of 2026-11-05 over the tax office's guidance read the
page that applies Australia's statute. The claim gains the office's
names for the statute's two methods and is otherwise unchanged.

The rules a ledger answers to do not share one level of rounding. The
filing rules of the United States and Canada add exact amounts and round
once at the total; the e-invoicing standard EN 16931, as Peppol carries
it, rounds every line to two decimals, sums the rounded lines without
rounding again, computes each VAT amount once from its summed base, and
carries any rounding of the payable amount as a separate amount; the
United Kingdom lets VAT be rounded per line in one of two ways held
consistently and the total rounded down to a penny; the European court
leaves the level at which VAT is rounded to each Member State;
Australia's statute writes both levels into one section, rounding the
tax on a single supply to the nearest cent with half a cent up and, for
several supplies on one invoice, handing the supplier the choice between
rounding the summed unrounded amounts once and summing amounts each
rounded to the decimal places its accounting system allows, half up at
either level, a choice its tax office names the total invoice rule and
the taxable supply rule and lets a supplier and its customers make
differently; and the cash rounding rules of Hungary, Canada and Israel
round the final sum payable and not the prices. A ledger therefore
cannot inherit a level of rounding from arithmetic; it reads one from
the rule it files under. It must convince a maintainer who believes
rounding each line is the only correct ledger, or that every rule asks
for the same thing.

## Evidence

Read evidence, quoted from the works the passes of 2026-10-16 and
2026-11-05 read in full or in their governing sections, with no pin,
since no tree produced it.

The Australian Taxation Office's page on tax invoices, its section on
the rounding of GST, last updated on 18 September 2026 [ato2026]: "Where
an amount of GST includes a fraction of a cent, special rounding rules
apply. Where there is only one taxable sale on a tax invoice, the amount
of GST should be rounded to the nearest cent (rounding 0.5 cents
upwards). Where there is more than one taxable sale on a tax invoice,
there are 2 rules known as the total invoice rule and the taxable supply
rule." The first: "Total invoice rule – total and then round GST for
each taxable sale to the nearest cent (rounding 0.5 cents upwards). Or
if all taxable sales on a tax invoice include an amount of GST exactly
1/11 of the price, add up the GST-exclusive value of each taxable sale,
calculate GST on that amount and then round to the nearest cent
(rounding 0.5 cents upwards)." The second: "Taxable sale rule – work out
the amount of GST for each individual taxable sale. Where the unrounded
amount of GST has more decimal places than your accounting system can
record, round up or down as appropriate. Then add the individual amounts
and round this total to the nearest cent (rounding 0.5 cents upwards)."
And the sentence that closes the section: "You and your customers don't
need to use the same rounding rules."

Australia's statute, section 9-90, in the register's compilation of 1
January 2026, with the asterisks that mark defined terms as printed
[gstact-1999]: "(1) If the amount of GST on a *taxable supply that is
the only taxable supply recorded on a particular *invoice would, apart
from this section, be an amount that includes a fraction of a cent, the
amount of GST is rounded to the nearest cent (rounding 0.5 cents
upwards)." and "(2) If 2 or more *taxable supplies are recorded on the
same *invoice, the total amount of GST on the supplies is: (a) what
would be the amount of GST if it were worked out by: (i) working out the
GST on each of the supplies (without rounding the amounts to the nearest
cent); and (ii) adding the amounts together and, if the total is an
amount that includes a fraction of a cent, rounding it to the nearest
cent (rounding 0.5 cents upwards); or (b) the amount worked out using
the following method statement:" whose steps read "Step 1. Work out, for
each *taxable supply, what would, apart from this section, be the amount
of GST on the supply. Step 2. If the amount for the supply has more
decimal places than the number of decimal places allowed by the
accounting system used to work out the amount, round the amount (up or
down as appropriate) to that number of decimal places. ... Step 3. Work
out the sum of the amounts worked out under step 1 and (if applicable)
step 2 for each supply. Step 4. If the sum under step 3 includes a
fraction of a cent, round the sum to the nearest cent (rounding 0.5
cents upwards)." Subsection (3): "Whether to use paragraph (2)(a) or
paragraph (2)(b) to work out the total amount of GST on the supplies is
a matter of choice for: (a) the supplier if the amount is being worked
out to ascertain the supplier's liability for GST; or (b) the *recipient
of the supplies if the amount is being worked out to ascertain the
recipient's entitlement to input tax credits." Subsection (4) settles
the tie of step 2 upward, where "the last digit of the amount (before
rounding) is 5; the amount is rounded upwards to that number of decimal
places." Section 29-70 requires a tax invoice to show "the amount of GST
(if any) payable in relation to each supply to which the document
relates".

The instructions for the United States individual return, read again on
2026-10-16, say [irs2025]: "If you have to add two or more amounts to
figure the amount to enter on a line, include cents when adding the
amounts and round off only the total."

The Canadian guide for registrants says [cra2026]: "Round off the GST/HST
to the nearest cent as follows: If the amount is less than half a cent,
you may round down. If the amount is equal to or more than half a cent,
round up. If your customer is buying more than one item and tax applies
at the same rate on all items, you can add up the prices of all taxable
supplies of property and services, calculate the GST/HST payable, and
then round off the amount."

Peppol BIS Billing 3.0, section 9 [peppolbis3-2026]: "All document level
amounts shall be rounded to two decimals for accounting. Invoice line net
amount shall be rounded to two decimals. Results from calculations
involving already rounded amounts are not subject to rounding, like
payable amounts and total amounts included VAT." Its business rule BR-CO-17
reads "VAT category tax amount (BT-117) = VAT category taxable amount
(BT-116) x (VAT category rate (BT-119) / 100), rounded to two decimals",
its rule BR-CO-16 reads "Amount due for payment (BT-115) = Invoice total
amount with VAT (BT-112) - Paid amount (BT-113) + Rounding amount
(BT-114)", and section 10.1.2 reads "It is possible to round the expected
payable amount. ... Example: Amount 999.81 rounded to 1000.
PayableRoundingAmount = 0.19". The element it names is defined by the UBL
standard [ubl21-2013] as "The rounding amount (positive or negative)
added to produce the line extension amount."

The United Kingdom's VAT guide, section 17.5 [hmrc2026]: "You may round
down the total VAT payable on all goods and services shown on a VAT
invoice to a whole penny. You can ignore any fraction of a penny."
Section 17.5.1 permits line-level VAT "by rounding in one of the
following ways: down to the nearest 0.1 pence ... to the nearest 1 pence
or 0.5 pence ... Whatever you decide, you must be consistent. The final
total amount of VAT payable may be rounded down to the nearest whole
penny." Section 17.6, for retailers: "If you calculate VAT at line level
or invoice level, you must not round the VAT figure down. But, you may
round (up and down) each VAT calculation."

The Court of Justice held in its operative part that Community law
"contains no specific requirement concerning the method of rounding
amounts of value added tax", that each Member State determines "the level
at which the rounding ... may or must occur", and that tax-inclusive
traders "cannot invoke the principle of fiscal neutrality in order to
claim the right also to round down, at line level and basket level"
[cjeu2009]; a year earlier it had held that Community law "entails no
specific obligation for Member States to permit taxable persons to round
down per item the amount of value added tax" [cjeu2008]. The euro
regulation's Article 5 reads [ec1103-1997]: "Monetary amounts to be paid
or accounted for when a rounding takes place after a conversion into the
euro unit pursuant to Article 4 shall be rounded up or down to the
nearest cent. ... If the application of the conversion rate gives a
result which is exactly half-way, the sum shall be rounded up."

The Hungarian central bank's account of the forint rounding act, p. 16
[leszko2009]: "In practice, retail traders did not re-price articles on
account of the withdrawal of 1- and 2-forint coins ..., but opted
instead for rounding the final sum payable on goods, in line with the
stipulations of the act on rounding." Of the Netherlands, p. 19:
"According to the rule, only the final sum, and not the individual
articles purchased is rounded." The Canadian scheme, pp. 231 to 232
[cheung2018]: "The rounding scheme specifies that if the after-tax total
of a cash purchase ends in (3, 4, 8, 9), then the resulting bill will be
rounded up to the nearest nickel; on the contrary, if the total ends in
(1, 2, 6, 7), the bill will be rounded down to the nearest nickel." The
Israeli scheme, p. 1 [sayag2025]: "In credit card transactions, the
amount paid was exact. In cash transactions, however, the total bill was
rounded to the nearest NIS 0.05".

## Threats

- Coverage. Six jurisdictions and two standards, chosen before the grey
  strand ran and not a census; Australia's statute and the guidance that
  applies it are both read, so no source a pass named stays unread.
- Currency. The guidance pages are living documents, read on 2026-10-16
  and, for Australia's, on 2026-11-05, with the versions the
  bibliography names; a later edition may move a rule, and the pass
  records date what was read.
- Reading. The statute was read in two of its sections, the standards
  and the guidance in their governing sections and the judgments in
  their operative parts, not whole, which is the depth the rulebook
  names full for a standard or a manual.
