# The Optimization Sweep

Recorded 2026-08-17. This record preserves how the vocabulary beside it was
produced: the question, the method, the amount of material, and the filters
that reduced it.

## The question

Optimization reaches most programmers twice under one word, first as the
analysis of growth rates and later as a hundred unrelated practices, with
nothing saying that these are different subjects and that only some of them
are decisions anyone makes. The question this study answers is what the
discipline's optimization vocabulary actually contains. Answering it took two
steps: enumerating the named, established concepts across every territory that
owns part of this vocabulary, then folding the enumeration into families
without losing the names.

## The method

The work ran in five stages in one day, as independent passes with mechanical
checks between them.

1. Enumeration. Fifteen passes, one per territory of the vocabulary, each
   sweeping its canonical sources by name: textbook chapter and index
   structures, published compiler and runtime pass lists and option
   references, vendor optimization manuals, standards and professional
   glossaries, and the established practitioner literature, with live web
   verification where a pass held a name loosely. Each pass wrote its section
   straight to a file, so no finding was compressed in transit. Rules of
   entry: a proper name and established use; no product, tool, or library as
   an entry; no algorithm named for what it computes rather than for the
   optimization it performs; one bullet per entry, a gloss of at most 25
   words, and, for anything a person applies, a clause naming what it costs.
   The sweep produced 7,057 entries.
2. Mechanical checks. Every section was checked for banned characters, hedge
   phrases, malformed entries, gloss length, and repeated names. Twenty one
   flags came back, of which two were real defects: an entry that pointed at
   another entry instead of defining itself, and one loop technique
   catalogued twice under two of its own names. The rest were faults in the
   checks. Eleven read a price clause as a hedge, and eight reported one
   idiom priced separately by two language cultures, which is correct in a
   catalog organized by culture. The checks were narrowed until they accepted
   the legitimate forms while still catching the defects, and both narrowed
   checks were proved against planted copies of what they had to catch.
3. Completeness review. Five independent passes, each holding the complete
   name index of its own territories and a list of canonical catalogs to work
   through, with the sole task of finding omissions. They added 2,131
   entries. The gaps were whole canons rather than thin spots: the string,
   geometry, and graph technique vocabularies; transaction and concurrency
   control internals; the approximate membership filter families; the
   operating system scheduler and block layer; audio and video pipelines;
   mobile and native platform performance; the dynamic loop self scheduling
   family; hardware description and high level synthesis, which the sweep had
   not touched at all; and on the discipline side a published performance
   antipattern catalog together with the named failure modes of overload.
4. The fold. Six passes, one per family, each reading its territories in full
   under a hard entry budget, because a budget is what forces folding instead
   of copying. They produced 1,156 entries. A loss audit then measured
   survival group by group across the whole catalog, which is how a hole is
   told apart from a fold, and it showed that most apparent losses were
   entries surviving inside another family's glosses. Three repair passes
   covered what was genuinely lost: the parameterized and satisfiability
   search techniques; the practices that keep an optimization honest,
   together with clock mechanics and the named antipattern catalogs; and
   device programming with constrained system memory. Each repair discarded
   part of its own brief on finding the material already covered.
5. One home per name. Twenty five entries were claimed by two families at
   once. Each went to the family that owns its subject, laws with the laws,
   layout with the machine, compiler transformations with the toolchain, and
   the genuine synonyms of the discarded copy were carried across. One word,
   checkpointing, named two unrelated techniques and became two entries.

Final size per territory, sweep plus review: asymptotic and cost model
analysis 504; complexity classes and hardness 533; algorithm design paradigms
492; space, time, and representation tradeoffs 642; machine independent
compiler optimizations 578; loop, vector, and parallel transformations 427;
code generation, link time, and runtime compilation 642; memory hierarchy and
data layout 423; instruction level and concurrency performance 659;
allocation, input output, and data systems 830; measurement, profiling, and
latency 656; the discipline of optimization 442; language and runtime idioms
704; delivery, rendering, and interactive performance 867; distributed, cloud,
and machine learning performance 789.

## The numbers

| Stage | Count |
| --- | --- |
| First sweep, fifteen territories | 7,057 |
| Added by the completeness review | 2,131 |
| Full catalog | 9,188 |
| Produced by the six folding passes | 1,156 |
| Added by the three repair passes | 141 |
| Removed as claimed by two families | 25 |
| Entries in the vocabulary beside this record | 1,272 |
| Entries of those that name a price | 939 |

The entries that name no price are the measurements, models, laws, and classes
of problem, which cost nothing to know. Their share, one entry in four, is the
study's plainest finding: a quarter of what the industry calls optimization
vocabulary describes cost rather than changing it.

## The filters

Six filters were applied in order, and each is why the counts fall.

1. Establishment. An entry needed a proper name plus presence in books,
   published toolchain and runtime documentation, standards, canonical
   catalogs, or professional glossaries. Products, tools, and libraries were
   excluded as entries, though a tool name may sit inside a definition as the
   place a technique is implemented.
2. Form. One bullet per entry, and a gloss capped at 25 words during the
   sweep. The fold raised that cap to 45, because an entry that folds five
   dependence tests or six optimization levels into one line cannot say what
   it holds inside the sweep's cap. Both numbers are machine checked at their
   own stage.
3. The boundary. Mathematical optimization, the discipline of minimizing
   objective functions, shares the word with this study and belongs to a
   different field. Gradient descent, linear and convex programming, the
   simplex method, and the metaheuristics were excluded by the entry rules
   rather than by later judgement.
4. Completeness before folding. Omissions were sought by reviewers who could
   already see every name in their own territories, so an addition could not
   restate what existed there.
5. The fold test. An entry survives when a person deciding what to do is
   helped by it. Obscurity was never a reason to drop an entry and
   unhelpfulness always was. Two names for one technique became one entry
   with the alternates riding along, a technique named separately by several
   language cultures became one entry, and a taxonomy nobody needs item by
   item became one entry naming its members.
6. One home. A name belongs to one family, so the reader who looks it up
   finds one ruling on it rather than two that differ in detail.

## Verification

Every stage was machine checked, and the checker ran outside the passes it
judged. That is why the review's error rate is a measured number rather than a
self report: 32 of the 2,131 additions restated a name their own author had
been shown, and 151 more duplicated a name held in a territory that author
could not see, which is the unavoidable price of splitting the index so each
reviewer could hold all of it. The fold was audited the same way, by measuring
how much of each source group survived, and the audit's own blind spot was
found before it was trusted: it counted a name as lost when the fold had kept
it inside another entry, so its findings were probed by hand before any repair
was commissioned, and roughly a dozen reported losses proved to be present.
The two narrowed checks from the second stage were proved against planted
defects. Nothing in the vocabulary beside this record rests on a single pass
having been careful.
