# Study 0005. The agent-skills ecosystem read against the family's law

Date: 2026-09-16

## The question

Which practices in the published agent-skills ecosystem does the family not
already hold, in a form that adds decidability or completeness to its law?

Not whether the family should carry skill files. That was settled by
[treasury 0004, Let the index do what skill files do](../decisions/0004-let-the-index-do-what-skill-files-do.md),
and this study did not reopen it. The question was about the practices inside
the files. The family's prose section came from one writing skill folded in,
its decidable residue becoming the em dash count and the vocabulary grep, and
the owner asked whether the rest of the ecosystem held more of the same.

## The boundary, as the owner ruled it

The corpus was the official skills repository, the superpowers collection,
four curated lists, the specification repository, and the repositories those
lists named wherever a name looked like engineering process rather than a
product. Crawler and marketplace sites were excluded as noise. Nothing shipped
by any skill was executed. Every file was read as text, because skills ship
scripts, and a study reads.

The fold criterion was the family's own. An adoption adds decidability or
completeness and never a sentence asking for taste, lands separately from
every other law change, and binds every seat or does not enter.

## The method, and where it departed from the written one

The study followed the six stages, with one departure the corpus forced and
one failure the method predicted.

The departure was in enumeration. Every earlier study had to generate names
from held knowledge, territory by territory, across dozens of passes. Here
every name already existed as bytes, in a frontmatter field or a list row, so
a script read all 2,272 in under a second. Enumeration, which had been most of
a study's cost, cost nothing. Jurisdiction was then ruled by class rather than
item by item, since two generated families were 74 percent of the field and
each collapses to one entry under the alias-density rule.

The failure was the exhaustion claim. The first pass read about twenty bodies
of the 580 available in the process territory, judged the rest from a name and
a one-line description, and called the territory covered. The method says a
claim of that shape has been false every time it was tested, and it was false
here. A second pass extracted every rule-shaped line from every body, routed
the normative ones into eight topics matching the family's jurisdiction, and
read them. Reading by position turned out to sample whichever repository
sorted first, so coverage was then measured by source, and the 21 sources
never sampled were read directly.

## The funnel

| Stage | Count |
| --- | --- |
| Frontmatter harvested from the cloned repositories | 898 |
| Entries named by the curated lists | 1,374 |
| Names before deduplication | 2,272 |
| One generated integration template, one entry | 832 |
| One generated SDK-wrapper family, one entry | 851 |
| Named in both a repository and a list | 57 |
| Distinct names remaining | 519 |
| Repositories cloned for the process territory | 40 |
| Files opened in them | 2,799 |
| Rule-shaped lines extracted | 152,060 |
| Distinct normative lines routed into eight topics | 13,116 |
| Candidates after the first pass | 9 |
| Candidates after the completeness pass | 26 |
| Adopted, refused, already held | 10, 10, 6 |

The first pass found nine of twenty-six. What it missed were not the weak
ones. Four of the eight adoptions were in bodies the first pass never opened.

## How verification was done, and its limits

Every verdict was checked against the law surface by a script that grepped
each candidate's vocabulary over every guide, rulebook, map, baseline, record,
audit script, configuration and workflow, and printed the hits with file and
line. The six candidates recorded as already held were found by that script,
not remembered, and two of them had been called absent before it ran. One
candidate was measured rather than judged. Over the family and a project built
from it, 75 of 1,213 prose paragraphs opened with a bare demonstrative, and
every one had a clear antecedent, so the mechanical form of the rule would
misfire and the honest form was taste.

Two tools in the corpus independently derived the family's own proof rule,
that a check is shown to work by planting the defect, watching it fail, and
watching it pass again when the plant is removed. That convergence is the
strongest external evidence the family's audits have had.

Four limits are stated rather than buried. The study ran as one reader without
the independent passes the method calls for, because the owner had not
authorized delegation. Coverage is claimed by source and not by line, since
8,722 of the 10,902 filtered lines were never read individually. The 466 names
whose bodies live in repositories that were never cloned were judged from
their name and description alone. Token spend was not metered per stage; wall
time was.

## What the study found

The family already holds most of the process territory in stricter form, and
the findings record names the convergences one by one. What it lacked was its
own proof instrument extended from the audits to the test suites, one
statement of a preference it already practises, and six small checks. The
findings are in [02-findings.md](02-findings.md) and the disposition in
[treasury 0030, Take eight rules from the skills study and refuse the rest](../decisions/0030-take-eight-rules-from-the-skills-study-and-refuse-the-rest.md).

## What the study paid to learn

Two lessons entered the method.

1. A corpus that is already enumerated is a trap. When the names exist as
   bytes, the harvest is instant, and the speed tempts a single pass that
   skips the reading. The cost moved from enumeration to reading; it did not
   disappear.
2. Coverage is counted by source, never by volume read. A reader who has read
   two thousand lines may have read nothing from half the sources, because
   reading by position samples whichever source sorts first.

## Spend

| Stage | Wall time |
| --- | --- |
| Clone, harvest, jurisdiction sort, dedup | about 25 minutes |
| First body pass and first report | about 30 minutes |
| Completeness pass, extraction through the source-coverage read | about 2 hours |
| Text review of every verdict against the law surface | about 40 minutes |

The times are approximate. Token spend per stage was not recorded, which the
method asks for and the next study should do.
