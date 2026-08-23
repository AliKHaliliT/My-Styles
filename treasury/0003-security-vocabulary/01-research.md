# The Security Sweep

Recorded 2026-08-22. This record preserves how the vocabulary beside it was
produced: the question, the method, the amount of material, and the filters
that reduced it.

## The question

The family's existing law makes code auditable, cheap to change, and cheap to
measure, and none of that makes it safe against someone trying to break it.
Security's opponent is an adversary rather than entropy, which is a different
subject with its own vocabulary, and no earlier study had touched it. The
question this study answers is what that vocabulary actually contains.
Answering it took two steps, enumerating the named, established concepts across
every territory that owns part of the subject, then folding the enumeration
into families without losing the names.

## The boundary

Security is here in full. From safety engineering only one slice is here,
fail-safe states and fault containment, because a template family can carry
that much and no more. Out are the certification universe governing
safety-critical software, physical security, and products, tools and vendors as
entries. A channel a program can observe or exploit stayed in even where its
physics is physical, and a named algorithm, format, protocol or model stayed in
wherever the field treats the name as a concept.

## The method

The work ran in six stages in two days, as independent passes with mechanical
checks between them.

1. Scouting. One pass walked the field's canonical structures, the weakness
   taxonomy views, the published top-ten list families, the textbook chapter
   lists for security engineering and for cryptography, the secure-coding rule
   families, the control-family catalogs, the attack taxonomies, and the survey
   literature for memory safety, supply chain, isolation, side channels,
   identity and dependability. It recorded what each one indexes and derived
   the territories from the accumulated terrain. Nineteen raw regions came out
   of the walk. Four were too thin to stand and were merged into the
   literatures they already live in, applied-crypto misuse into the protocol
   territory whose attack face it is, language security into memory safety,
   model and agent security into the application-surface territory, and the
   secure-coding standards across memory safety and injection. Two were too
   dense for one pass and were split, cryptography into primitives and
   deployment, and identity along the seam where authentication and
   authorization divide in the literature. Fourteen territories remained. The
   count was not chosen; it is what the terrain left standing after the merges
   and the splits.
2. Enumeration. Fourteen passes, one per territory, each sweeping its canonical
   sources by name and verifying with live search wherever a pass held a name
   loosely. One contract file carried the rules of entry so every pass returned
   the same shape, and each pass wrote its section straight to its own file.
   The sweep produced 10,004 entries.
3. Mechanical checks. Every file was checked for banned characters, entry
   shape, gloss length, colons inside a gloss, hedge phrases, glosses that
   point at another entry instead of defining themselves, and names repeated
   inside a group. Twelve of the fourteen passes came back clean on everything
   but gloss length. The one structural finding was a false positive in the
   checker rather than a defect in the work, since the checker accepted only a
   single alias and reported a correct two-alias entry as malformed.
4. Completeness review. Six independent passes, each holding the complete name
   index of its own territories and a list of canonical catalogs to work
   through by name, with the sole task of finding omissions. They added 3,760
   entries. An independent measurement of whether their additions restated what
   they had been shown returned a rate of zero. The gaps were whole canons
   rather than thin spots: three entire tactics of the adversary matrix and
   nearly all of the defensive taxonomy facing it; the standards series and the
   textbook definition lists behind cryptography; the verification standards and
   the machine-learning attack taxonomies behind the application surfaces; the
   authenticator and threat tables of the identity guidelines; the
   disclosure-control and privacy-mechanism literature; the operating-system
   forensic artifact catalogs; the framework practice sets behind supply chain;
   and the fault-classification viewpoints and exception structure behind the
   safety slice.
5. The fold. Eight passes, one per family, each reading its territories in full
   under a hard entry budget, because a budget is what forces folding instead
   of copying. Seven of the eight landed exactly on their ceiling and one came
   in under. They produced 1,880 entries.
6. Resolution. Thirty-nine names were a primary entry in two families at once.
   Thirty-two went to the family owning the subject, with the discarded copy's
   synonyms and any content the survivor lacked carried across. Seven were one
   word naming two different things and became two entries each, renamed so a
   reader can tell them apart, among them the evaluation assurance level
   against the identity assurance level, hardware fault injection against fault
   injection testing, and the hardware capability against the capability token.
   Forty-five aliases that duplicated another family's entry were removed.
   Seven name overlaps remain deliberately, each a word the field genuinely
   uses for two things.

## The loss audit and the repair

After the fold, an audit measured survival group by group across the whole
catalog, counting a name as surviving if it appears anywhere in the folded
text, not merely as an entry title. It found 38 groups keeping nothing and 138
under a fifth, and probing those by hand produced the study's sharpest finding
about folding itself. A merged entry that names its members keeps them
findable, and a merged entry that describes its members loses them. The family
that folded hardest of all, at better than nine to one, lost almost nothing
because it names members; the families that lost most had written good prose
about what a group contained without ever saying the words.

Repair passes therefore preferred amending an existing entry to name its
members over adding a new one, and every pass had to report how many absent
names it judged not worth restoring and why. Roughly 1,100 names came back,
and roughly 900 were declined as wire constants, error and alert codes, control
and rule identifiers, message field names, per-platform variants of one
technique, generic descriptors carrying no idea, and second labels for
something already held under a better name. The audit ended at 3 groups keeping
nothing, each explained, and mean survival across the catalog's 519 groups rose
to 62 percent.

The audit is blind wherever the fold kept a name in a phrase rather than
verbatim, and that blindness was not small. Four flagged holes turned out to be
nothing: an entry listing seventeen allocator techniques as a series rather
than by full name, a term present in a neighbouring entry's gloss, a framework's
practice groups named in full in another family, and a taxonomy's decomposition
named as a list. Every flagged hole was probed by hand before any repair was
commissioned, which is the only reason those four did not become busywork.

## The funnel

| Stage | Entries |
| --- | --- |
| Scouting, territories derived from nineteen raw regions | 14 |
| Enumeration, fourteen passes | 10,004 |
| Completeness review, six passes, restatement rate zero | 3,760 |
| Catalogued in total | 13,764 |
| The fold, eight passes against a budget of 1,890 | 1,880 |
| After the loss audit's repairs | 2,028 |
| After resolution removed 32 duplicate entries | 1,996 |

The catalog folds to the vocabulary at 6.9 to 1. The study before this one
folded at 7.2 to 1 in a different field, and the agreement is the evidence that
the two studies catalogued at a comparable grain.

## The filters

- A proper name and established use. No product, tool, or vendor as an entry.
- One entry per line, opening with its name and defining itself rather than
  pointing at another entry.
- A gloss of at most 25 words during the sweep and the review. The cap rose to
  45 at the fold, because an entry that merges a taxonomy has to name its
  members, and to 60 during the repair for the same reason. All three numbers
  are recorded here because a rule written for one stage can be wrong at the
  next, and the honest fix is to change it in the open.
- A clause naming what it costs, for anything a person applies, and no such
  clause for anything nobody applies. The finished vocabulary prices two
  entries in five.
- A hard entry budget per family at the fold, raised by a fifteen percent
  repair allowance only where the loss audit proved a name had been dropped.

## How verification was done

Every check was written before the work it judged and run outside the pass that
produced it, because a pass grading itself reports what it intended. Each check
was proved against a planted defect before any clean result was trusted, and
the clean control had to come back clean, which is how two false positives from
an earlier study stayed fixed and how this study's own alias false positive was
caught. The completeness reviewers were measured rather than believed, by an
independent comparison of their additions against the indexes they had been
given. The fold was measured against its budgets, the repair against the loss
audit, and the resolution by a recount of every name claimed by two families.
The final state of the vocabulary carries no mechanical finding of any kind.

## What this study paid to learn

- A merged entry must name its members. Describing them reads well and loses
  them, and the loss is invisible until something measures it.
- A check run while a pass is still writing measures a half-written file and
  reports defects that were never there. Checks belong between stages.
- A survival audit that matches names literally will call a fold a hole. Probe
  its findings by hand before commissioning any repair.
- Splitting one large repair into two passes cost nothing and finished, where
  the single pass had died against an output limit without writing a line.
- A scout reading density from chapter and catalog structure will undercount a
  field badly, because a canon presents as one region and arrives as two
  hundred names. The scouted estimate here was low by a factor of three, which
  did not damage the study because the territory map, not the estimate, is what
  the passes were assigned from.
