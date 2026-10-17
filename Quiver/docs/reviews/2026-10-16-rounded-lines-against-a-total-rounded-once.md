# Rounded lines against a total rounded once

Date: 2026-10-16

## Slice

First pass over the two strands of question 3 that a search can reach,
the rules a ledger, an invoice, a tax return or an e-invoicing standard
sets for rounding line amounts against the total, and what the
literature says about rounding parts against rounding their sum once.
The pass of 2026-09-29 opened the line by hand from four works and
searched no index, so there is no window to overlap and this pass
extends from nothing.

## Boundary

Three open indexes the agent searched itself on 2026-10-16: OpenAlex
through its exact title-and-abstract field, because its stemmed field
reads rounding as round and floods the result with trade rounds and
round tables; Crossref through its bibliographic query, fifty most
relevant records per phrase; and the arXiv API through its
field-prefixed booleans, the first three hundred per query. Semantic
Scholar answered every unkeyed request with a rate limit all day and
dblp with a bot challenge, so neither was searched; their searches are
written out in Left out. Window: works published from 1960 on, because
the slice's classic works are of 1967 and 1979; language English,
applied at screening; document types articles, conference papers, book
chapters, books, reports and preprints, with standards, regulations and
authority guidance in the grey strand.

Criteria, written before screening. A record passes under C-rule when it
states a rule a ledger, invoice, tax return, statement or standard must
follow about rounding line amounts versus the total; under C-compare
when it states, derives or measures how rounding parts, lines, shares,
percentages or cells, compares with rounding their sum once, or how
rounded parts fail to sum to the rounded total; under C-method when it
gives a method for making rounded parts agree with a total, controlled
rounding, apportionment-style rounding, allocation of the rounding
residue or distributive rounding. A record is excluded, with the label,
as Not parts-and-total (a single measurement, a representation or a
function value with no sum of parts), Perception (the psychology of
rounded prices), Price endings (the pass of 2026-09-30), Not money or
counts (rounding in image, signal, filter or control settings),
Duplicate, Related version, Out of window, Wrong document type
(datasets, errata, paratexts, reference entries), Language, or Noise.
The noise the pilot showed, LP and randomized rounding in approximation
algorithms, nurse and leader rounding, cell rounding in biology, sum-up
rounding in optimal control, controlled rounding in digital filters,
statistical reports whose abstracts carry a rounding note beside their
totals, and money as indivisible units in games, was listed before the
screening met it. Two scope rules were added after the pilot and before
the screening. A work on apportionment passes under C-method only where
its title or abstract frames the method as a rounding of proportions,
shares or amounts to a total, and is otherwise excluded as Seat
apportionment; and a record whose copy nobody could open and whose index
record holds no abstract is logged Not decidable at the full-text stage
and queued for a person.

Strings on OpenAlex, each a filter on the exact field with publication
year after 1959, run on 2026-10-16, with the count at the index that day
and the records exported, the first pages by relevance. S1-money:
rounding AND (invoice OR invoices OR VAT OR "sales tax" OR ledger OR
"financial statements" OR monetary OR currency OR cents OR cash OR money
OR prices OR tax OR payroll) AND (total OR totals OR sum OR sums OR
"line item" OR "line items" OR allocation OR allocate OR allocated), 192
records, all exported. S2-parts, the pilot: (rounding OR rounded) AND
(percentages OR proportions OR shares OR apportionment OR "tabular data"
OR tables OR cells OR "line items" OR amounts) AND (sum OR sums OR total
OR totals OR "add up" OR "adds up" OR "add to" OR consistent OR
consistency), 3,122 records, 600 exported. S2b-parts, the corrected run,
adds subtotals to the second block and summation to the third, for the
accumulation strand, 3,143 records, 600 exported. S3-phrases, the pilot:
"controlled rounding" OR "rounded percentages" OR "rounding percentages"
OR "sums of rounded" OR "sum of rounded" OR "rounding proportions" OR
"rounding differences" OR "rounding difference" OR "cash rounding" OR
"currency rounding" OR "penny rounding" OR "rounding residue" OR
"rounding residual", 150 records, all exported. S3b-phrases, the
corrected run, adds "apportionment method", "apportionment methods",
"divisor method", "divisor methods", "largest remainder", "distributive
rounding", "table rounding", "rounding problem", "rounding rule" and
"rounding rules", for the seed pukelsheim2014 and the apportionment
strand, 1,299 records, 600 exported. Crossref, the sixteen phrases of
the pilot and the corrected strings as free-text bibliographic queries,
fifty records each, 800 exported. arXiv, the phrase string and a block
string over abstracts with invoice, VAT, ledger, monetary, currency,
cents and payroll against total, sum and allocation, 71 records
exported. The recall of the pilot is in the seeds line; the corrections
it drove are the b runs.

The records were merged by identifier, then by normalized title, into
one sheet of 1,117 records, which the first screen read whole; the 596
exported records below that sheet's depth were screened afterwards
against the same criteria and stand in the same log. The grey strand ran
beside the academic one with its sources named before it ran, the tax
authorities of the United States, the United Kingdom, Australia, Canada
and the European Union's regulation and court, and the e-invoicing
standards EN 16931 as Peppol BIS Billing 3.0 and OASIS UBL 2.1; each
named source was read once in its governing section, a web search served
only as a tracker to locate a named page, and every page fetched was
archived by the agent. Australia's statute and guidance refused every
fetch and are queued.

Nearest review: [kelly1992], which covers controlled rounding of statistical tables to 1992 in five pages; this pass adds the money and ledger strand, the rules of authorities and standards, the apportionment strand and the window since 1992.
Seeds: 8 fixed, 8 indexed, 6 found, [fowler2002], [diaconis1979], [mosteller1967], [cox1987], [coxernst1982], [balinski1993], [pukelsheim2014], [higham1993]; the strings missed [fowler2002], a book the index holds without an abstract, which no string over abstracts can return, and [higham1993], whose abstract speaks of floating point numbers and not of amounts, where the word the string lacked, floating point, would flood the result with numerical analysis, so the pass went on without it and names the accumulation strand as thin.
Screening: [the log](../screening/2026-10-16-rounded-lines-against-a-total-rounded-once.md)
Recorded: the exports the searches returned, reduced to the fields the screening read, with authorships and locations flattened to names, kept as `util_resources/searches/openalex-S1-money-2026-10-16.json`, `util_resources/searches/openalex-S2-parts-2026-10-16.json`, `util_resources/searches/openalex-S2b-parts-2026-10-16.json`, `util_resources/searches/openalex-S3-phrases-2026-10-16.json`, `util_resources/searches/openalex-S3b-phrases-2026-10-16.json`, `util_resources/searches/crossref-2026-10-16.json`, `util_resources/searches/arxiv-2026-10-16.json`.
Flow: retrieved 1912, screened 91, entered 86, read in full 21
Completeness: judgment

## Method

A multivocal rapid pass, three open indexes over a long window, the grey
strand beside the academic one under one scheme of facets, one reader
with a second look on a sample of 95 records, one snowball round from
the works the claims rest on and the nearest review, full text wherever
a copy opened, and a completeness review against the nearest review's
reference list. Named from the field's vocabulary as a rapid review, its
shortcuts are the depth of the two corrected strings, read to the six
hundredth record by relevance, the sample second look in place of a
second reader over every record, the single snowball round, and the two
indexes it could not reach.

## Stages

- Scouting: ran by the agent (Claude Fable 5.1, named as a condition of the run), over the open indexes with a review filter and review terms; the slice's literature lives in statistical disclosure control, in apportionment theory and in the economics of cash rounding, with the rules in authority guidance and standards rather than in journals, and one review stands near it, [kelly1992].
- Enumeration: ran by the agent (Claude Fable 5.1), over the strings, the exports, the supplement, the snowball round and the grey strand; a second reader in a fresh context, given the records and the criteria and nothing else, screened [95 records](../screening/2026-10-16-rounded-lines-against-a-total-rounded-once-second-look.md), agreeing with the first screen on 89 and differing on 6, which the owner decided; 86 works entered, 21 read in full, the rest at abstract depth where no copy opened, one at secondary depth.
- Checks: ran by the agent (Claude Fable 5.1); every key resolves, every work is entered with its edition, every identifier was resolved at Crossref and at OpenAlex and its title, first author and year compared with the record, none retracted on 2026-10-16; three index records carry a year beside the registry's, the online year against the issue's for [favre2004] and [drton2004] and the second edition's for the seed [pukelsheim2014], and one record's identifier resolves to another work, which the pass reads as a related version; the preprints [cont2014] and [hasan2026] were searched for published versions and none found, and [sayag2025] is cited in its published version.
- Completeness review: ran by the agent (Claude Fable 5.1), against the eight references of [kelly1992]; five were already in the sheet and entered or excluded on their merits, and the three the sheet lacked, a disclosure limitation survey, a simulated annealing bibliography and a hypergraph theorem, fall outside the criteria, so the review found nothing missing from the slice it covers and the boundary still claims judgment, because two indexes were not reached and two strings were read to a depth.
- Fold: ran by the agent (Claude Fable 5.1); three read-evidence claims, on the level at which rules round, on the rate at which rounded parts miss the rounded total, and on the methods that round parts to agree with a total, and one conjecture under question 3 that the rule decides whether the tie rule accumulates.
- Resolution: ran by the agent (Claude Fable 5.1); the rules disagree with one another by design, the e-invoicing standard sums rounded lines while the filing and cash rules round once at the total, and the inquiry follows none of them, reading the disagreement as the finding; the works on methods agree.

## Found

| Key | Depth | Strand | Criterion | Source |
| --- | --- | --- | --- | --- |
| [higham1993] | abstract | accumulation | C-compare | seed |
| [srigadde2021] | full | accumulation | C-compare | string |
| [benkhard1991] | abstract | allocation | C-method | string |
| [berry1976] | abstract | allocation | C-method | string |
| [cont2014] | full | allocation | C-method | snowball |
| [fowler2002] | secondary | allocation | C-method | seed |
| [imf2016] | abstract | allocation | C-method | string |
| [kadirbekov2026] | full | allocation | C-method | string |
| [noguer2026] | abstract | allocation | C-method | string |
| [chande2003] | abstract | cash | C-compare | snowball |
| [cheung2018] | full | cash | C-rule | string |
| [hasan2026] | abstract | cash | C-rule | string |
| [leszko2009] | full | cash | C-rule | string |
| [lombra2001] | abstract | cash | C-rule | string |
| [sayag2025] | full | cash | C-rule | string |
| [demirtas2009] | abstract | imputation | C-compare | string |
| [yucel2008] | abstract | imputation | C-compare | string |
| [cjeu2008] | full | rules | C-rule | grey |
| [cjeu2009] | full | rules | C-rule | grey |
| [cra2026] | full | rules | C-rule | grey |
| [ec1103-1997] | full | rules | C-rule | grey |
| [hmrc2026] | full | rules | C-rule | grey |
| [irs2025] | full | rules | C-rule | prior |
| [nguyen2025] | abstract | rules | C-rule | string |
| [oleary1999] | abstract | rules | C-compare | string |
| [peppolbis3-2026] | full | rules | C-rule | grey |
| [ubl21-2013] | full | rules | C-rule | grey |
| [athanasopoulos1994] | abstract | shares | C-method | string |
| [balinski1989] | abstract | shares | C-method | string |
| [balinski1993] | abstract | shares | C-method | seed |
| [balinski1996] | abstract | shares | C-method | string |
| [balinski1999] | abstract | shares | C-method | string |
| [cegielka2017] | full | shares | C-method | string |
| [diaconis1979] | abstract | shares | C-compare | seed |
| [dorfleitner1999] | abstract | shares | C-method | string |
| [drton2004] | abstract | shares | C-compare | snowball |
| [gassner1988] | abstract | shares | C-method | snowball |
| [gassner1991] | abstract | shares | C-method | string |
| [happacher1996] | abstract | shares | C-method | snowball |
| [happacher2000] | abstract | shares | C-method | snowball |
| [happacher2001] | abstract | shares | C-compare | string |
| [heinrich2004] | abstract | shares | C-compare | snowball |
| [heinrich2005] | abstract | shares | C-method | snowball |
| [heinrich2017] | abstract | shares | C-compare | snowball |
| [ichimori2011] | full | shares | C-method | string |
| [janson2013] | full | shares | C-compare | snowball |
| [meeks1992] | abstract | shares | C-method | string |
| [mosteller1967] | abstract | shares | C-compare | seed |
| [pukelsheim1992] | abstract | shares | C-method | snowball |
| [pukelsheim2006] | abstract | shares | C-method | string |
| [pukelsheim2014] | abstract | shares | C-method | seed |
| [rychlik2000] | abstract | shares | C-compare | snowball |
| [tsitouras2011] | abstract | shares | C-method | string |
| [yamaguchi2015] | abstract | shares | C-compare | string |
| [asano2000] | abstract | tables | C-method | string |
| [asano2003] | abstract | tables | C-method | string |
| [coleman2025] | full | tables | C-method | string |
| [cox1987] | abstract | tables | C-method | seed |
| [cox1989] | abstract | tables | C-method | string |
| [cox2006] | abstract | tables | C-compare | snowball |
| [coxernst1982] | abstract | tables | C-method | seed |
| [doerr2006a] | full | tables | C-method | string |
| [doerr2006b] | abstract | tables | C-method | string |
| [doerr2006c] | abstract | tables | C-method | string |
| [doerr2011] | abstract | tables | C-method | string |
| [fagan1988] | full | tables | C-method | string |
| [favre2004] | abstract | tables | C-method | snowball |
| [fischetti1998] | full | tables | C-method | string |
| [gonzalez2005] | abstract | tables | C-method | string |
| [kelly1990a] | abstract | tables | C-method | string |
| [kelly1990b] | abstract | tables | C-method | string |
| [kelly1990c] | abstract | tables | C-method | string |
| [kelly1992] | abstract | tables | C-method | string |
| [kelly1993a] | abstract | tables | C-method | string |
| [kelly1993b] | abstract | tables | C-method | string |
| [li1986] | abstract | tables | C-method | string |
| [ring1997] | abstract | tables | C-method | string |
| [salazar2004a] | abstract | tables | C-method | string |
| [salazar2004b] | abstract | tables | C-method | string |
| [salazar2005a] | abstract | tables | C-method | string |
| [salazar2005b] | abstract | tables | C-method | string |
| [salazar2006] | abstract | tables | C-method | snowball |
| [sima1999] | abstract | tables | C-method | string |
| [tiwari1993] | abstract | tables | C-method | string |
| [tiwari2012] | abstract | tables | C-method | snowball |
| [tripet2025] | abstract | tables | C-method | snowball |

## Changed

[Claim 0013, Rules fix the level at which a ledger
rounds](../claims/0013-rules-fix-the-level-at-which-a-ledger-rounds.md),
[claim 0014, Rounded parts miss the rounded total at a known
rate](../claims/0014-rounded-parts-miss-the-rounded-total-at-a-known-rate.md)
and [claim 0015, Methods round parts to agree with a
total](../claims/0015-methods-round-parts-to-agree-with-a-total.md)
opened as Supported on read evidence, [claim 0016, The rule decides
whether the tie rule
accumulates](../claims/0016-the-rule-decides-whether-the-tie-rule-accumulates.md)
opened as a conjecture resting on them, and question 3's open line
became that conjecture. The pass found the money and ledger strand thin
in the indexes, 23 works of 86, most of them rules read first-hand and
cash-rounding studies, against a dense literature on tables and shares;
the funnel above measures it.

## Left out

Two indexes the field uses and the pass could not reach, each with its
search written out. Semantic Scholar: the sixteen phrases of the
Crossref run, one query each on the paper search endpoint, limit one
hundred, fields title, year, abstract, externalIds and venue, exported
as returned; dblp: the twelve term queries controlled rounding, rounding
percentages, rounded percentages, currency rounding, monetary rounding,
rounding money, apportionment rounding, rounding proportions,
distributive rounding, table rounding, rounding invoice and rounding
ledger on the publication search endpoint, one hundred hits each,
exported as JSON. The records of S2b-parts and S3b-phrases below the six
hundredth by relevance, 2,543 and 699, and the Crossref records below
the fiftieth per phrase. Every licensed index, none being declared for
this inquiry. Australia's rule, section 9-90 of the GST Act and the tax
office's guidance on tax invoices, which refused every fetch and is
queued for a person with a browser. The full texts of the works entered
at abstract depth whose publishers refused scripted readers or hold them
behind a paywall, among them the seeds [diaconis1979], [mosteller1967],
[cox1987], [coxernst1982] and [balinski1993] and the works [berry1976],
[happacher1996] and [heinrich2017] the claims lean on through threats,
each queued in the state file for a person with library access. The one
record logged Not decidable, Wainer's 1998 column, and the one entered
on its index record alone, [yamaguchi2015], both queued. The second
snowball round, since the first added entries and the method runs rounds
until one adds none.

Cost: one long session of the agent across one day, with no separate token accounting.
