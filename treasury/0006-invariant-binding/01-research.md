# Study 0006. How a stated invariant is bound to something that holds it

Date: 2026-09-18

## The question

How do systems state an invariant as a first-class artifact and bind it to
something that holds it?

An invariant here is a claim about a program that is meant to stay true. A
binding is whatever makes the claim more than a sentence, from a type that
will not compile through a checker that refuses, a test that fails, a monitor
that alarms, and a proof that is checked, down to a reviewer who signs.

The question arose from a language whose compiler refuses code that breaks a
law the project declares in a file of its own. The language itself was set
aside. What survived the reading was the shape underneath it, a set of
invariants written down as first-class objects, each bound to something that
refuses. Nothing in the field is called a laws ledger, so the study asked what
the field does call the pieces.

## The boundary, and what was excluded

In scope: ways of writing an invariant down, ways of binding one to a check,
the artifacts that hold the written form, the named roles a binding can play,
and the recurring shapes of claim that practitioners write.

Two candidate territories were scouted and dropped at the boundary. Business
rules engines and decision tables decide an outcome from data rather than hold
a claim true, so nothing in them binds an invariant to a check. Observability
as a whole was excluded except for the part that states a threshold as a
standing claim and alarms on it, because the rest is measurement without a
claim.

Nothing was executed from any source. Every source was read as text.

## The method, and where it departed from the written one

The study followed the six stages. Two departures and one hole are worth
recording.

The scouting pass walked the field's catalogs, taxonomies and standards in ten
searches and returned sixteen territories. Five of the sixteen carry a catalog
that is both published and numbered, which is what makes an exhaustion claim
checkable later. That count is the map's output. No earlier study's shape was
carried forward.

The fold departed from the plan after the loss audit ran. Seven families were
planned, each a decision the shape of a ledger has to make, and the audit
showed that all three published lists of actual invariants in the corpus had
fallen through the gaps between them. The seven families divide the machinery
of stating and binding a claim, and none of them holds the content. An eighth
family was commissioned for the content, and it lifted three groups from 35,
73 and 86 percent survival to 86, 99 and 96.

The hole is named in full below, because the method's standing instruction is
to record the boundary that was excluded rather than to imply the study
reached everything.

## The funnel

| Stage | Count |
| --- | --- |
| Territories scouted | 16 |
| Names enumerated across sixteen passes | 1,948 |
| Additions from five completeness reviews | 332 |
| Names before the fold | 2,280 |
| Sources opened and named | 301 |
| Entries after the fold, across eight families | 166 |
| Names carried into the fold as headwords, alternates or named members | 2,023 |

The fold ratio is roughly fourteen to one.

## Coverage, counted by source

Each pass named the sources it opened with the count of entries taken from
each. Coverage was counted that way and never by volume read, because reading
by position samples whichever source sorts first. The passes opened 301
sources between them. Five sources were opened and credited with nothing,
which is the honest shape for a source that turned out to hold nothing new.

One pass finished without its source accounting and was asked for it rather
than having a number estimated on its behalf. It supplied seventeen sources.

## Verification of the exhaustion claims

Nine territories claimed exhaustion over a published numbered list and named
the list. Seven claimed none, stating plainly that no source they opened was a
closed list, which is the honest outcome for a field whose sources are prose.

Two claims were checked independently, and the two checks disagree in a way
worth keeping.

The claim over a detector's invariant class list was checked by fetching the
same page and counting. The pass reported 207 named classes; the check
reported 175, and the check's own output repeats one name and carries a
placeholder line where entries should be. Neither number is trustworthy. The
findings therefore cite that list by name and never by its size, and no count
from it enters this record as a fact.

The claim over a transaction-anomaly checker's model and anomaly graphs named
a source file rather than a rendered page, so the file was fetched whole,
29,969 bytes, and counted with a script. It carries 24 model names and 38
anomaly names, and the four names the pass said it had surfaced from source
are all present. That claim is verified.

The contrast is the finding. Checking a count by asking a second reader to
count a long page reproduces the first reader's problem instead of testing it.
A count is checkable only when the list can be fetched as bytes and counted
mechanically, and a pass that can choose between a rendered page and the
source behind it should name the source.

## Measuring the reviewers rather than believing them

Each completeness reviewer was given the full name index of its own
territories, told that an addition restating a name already in that index is
an error, and told the rate would be measured. It was measured afterwards by
matching every addition against that reviewer's own index on names and
aliases, with casing and punctuation stripped.

| Reviewer | Additions | Restatements | Rate |
| --- | --- | --- | --- |
| Formal | 64 | 0 | 0.0% |
| Dynamic | 54 | 0 | 0.0% |
| Structural | 83 | 0 | 0.0% |
| Institutional | 63 | 0 | 0.0% |
| Practice | 68 | 2 | 2.9% |

Two restatements in 332 additions. The instruction that the rate would be
measured was given before the work and the measurement was run after it, so
the number is a measurement rather than a self-report.

## Survival, measured group by group

The loss audit read each fold file whole and searched every name with its
aliases against headwords, alternate lines, named members and gloss text,
because an audit reading headwords alone reports a hole for every named member
and its output is worthless.

No group survived at zero. The lowest group before the eighth family was 35
percent and the lowest after it is 64 percent. Of 2,280 names, 257 appear in
no family. Sampling them by hand shows they are individual research tool
names, temporal logic operators, and concepts from adjacent fields such as
fault tolerance and replication, all of which a reader deciding the shape of a
ledger does not need.

## What the study did not reach

**The local moment before history has no name in the corpus.** Pre-commit and
commit hooks appear under no headword anywhere in 2,280 names. Sixteen
enumeration passes and five completeness reviews all missed the most common
place a working programmer meets a refused rule.

The cause is visible in the scouted map, which recorded the bias in advance.
Every catalog this study worked belongs to a field with a conference, a vendor
or a certification authority behind it, and none of them writes down the local
hook, because it is a convention rather than a product, a standard or a
research contribution. The territory that would have held it was the thinnest
in the map and the one the review was pointed hardest at, and even that did
not surface it.

It matters because the local hook is the only moment where a check can refuse
a claim before the claim exists in anyone's history. Every cadence the study
did enumerate acts later, on bytes that already exist somewhere.

The finding stands as a hole rather than being patched, because a name added
after the reviewers were measured would make the coverage figures say
something they did not earn.

Two smaller absences are recorded with it. Continuous conformance checking in
the editor exists in the corpus as a tool name and not as a cadence, so no
entry represents the moment. The oracle problem, the difficulty of judging a
result correct without a known-correct result, was dropped as naming a gap in
the mechanism rather than the worth of a verdict.

## What the instruments cost

Five instrument defects were found, and four were in the study's own tools
rather than in the work. This is the study's most transferable result, so each
is named.

1. A disambiguator cap of twelve words, exceeded by twenty-five entries at
   thirteen to seventeen words. The cap was wrong for the material, because a
   name needing a disambiguator usually needs a clause. Raised to twenty, with
   both numbers recorded, and no pass sent to trim files that never ship.
2. A ban on colons implemented as any colon in any field. Sixteen of its
   eighteen findings were names like `xsd:pattern` and `xsd:keyref`, where the
   colon is part of the published identifier. A repair pass sent against that
   finding would have renamed sixteen real concepts to earn a clean run, which
   is the defect class this method has recorded before. The rule now looks for
   a colon followed by a space, only in the disambiguator, and carries a plant
   that must pass beside the plant that must fire.
3. A ban on em dashes across sweep material, which had no jurisdiction. The
   method fixes what binds scaffolding and says in as many words that the
   sweep is not bound by the house dash rules. It never fired, so it damaged
   nothing.
4. A coverage reader that counted only lines beginning with a bullet, which
   reported a pass as naming no source when it had named thirteen. The
   instrument was measuring its own formatting assumption.
5. A hand check that reported a cluster of nineteen names as homeless when it
   was sitting in a members line seven lines below the heading the check
   printed. The method already warns that a loss audit goes blind where a fold
   keeps a name inside an entry rather than as a title, and tells the reader to
   probe by hand before commissioning a repair. That failure arrived in exactly
   the direction warned about, minutes after an audit script was written to
   avoid it.

Four of the five share one shape. A rule written for one material was pointed
at another, and the fifth was a reading window too small for the thing it
read.

## What this cost to run

Twenty-nine subagent passes, sixteen enumerating, five reviewing, eight
folding, plus one resumed for its source accounting. Wall time about ninety
minutes from the scouting pass to the last fold. Token spend is not recorded
here as a per-stage figure, because the harness reports it per pass rather
than per stage and no honest aggregation was available at the time of writing.
The pass counts and the funnel stand in its place.
