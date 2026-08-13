# The Primitive Reduction

Recorded 2026-08-11. This record preserves how the primitives list beside it
was produced: the question, the method, the amount of material, and the
filters that reduced it.

## The question

Software engineering coins names faster than it retires them, and the same
operation returns in every field under a different vocabulary. The question
this study answers is how many distinct operations remain when the names are
set aside, and what they are. Answering it took two steps: enumerating the
discipline's named, established concepts as completely as the literature
allows, then reducing the enumeration to the operations underneath it.

## The method

The work ran in six stages in one day, as independent research passes with
mechanical checks between them.

1. Enumeration. Thirteen passes, one per territory of the discipline, each
   sweeping its canonical sources by name, tables of contents, standards
   glossaries, and pattern indexes, with live web verification. Each pass
   wrote its section straight to a file, so no finding was compressed in
   transit. Rules of entry: a proper name and established use; no products,
   no bare algorithms, no coinages that never spread; one bullet per entry
   with a gloss of at most 25 words and an origin only where certain. The
   sweep produced 10,748 entries.
2. Mechanical checks. Every section was checked for banned characters,
   hedge phrases such as "etc.", and malformed entries. All thirteen came
   back clean.
3. Completeness review. Four independent passes, each holding the complete
   name index of its assigned territories and a list of canonical catalogs
   to check, with the sole task of finding omissions. They added 1,402
   entries. The three largest gaps were the pre-microservice service
   lineage (242 entries), the interface pattern vocabulary (171), and
   eighteen language cultures with no idioms catalogued (165).
4. Extension. Two territories the first sweep had not owned were written
   the same way. Systems, embedded, networking, and language implementation
   engineering added 1,101 entries. Research methods, standards, product
   lines, and specialized domains added 1,514.
5. Reduction. Five independent passes each read the complete name lists of
   three territories and clustered entries by the mechanism performed
   rather than the field served, under the mechanism test written below.
   The five reports were merged and deduplicated.
6. Naming. Each surviving operation received the most widely recognized
   term for it. Six had no industry-wide name and received in-house names,
   marked as such in the primitives list.

Final size per territory: principles and laws 512; code-level patterns and
idioms 967; enterprise and distributed patterns 754; architecture and
domain-driven design 788; methodologies 1,070; coding and refactoring 727;
testing 902; operations and reliability 995; security and safety 1,241; data
engineering 1,092; machine learning engineering 1,220; interface and product
design 968; anti-patterns and the human side 914; systems and language
implementation 1,101; research methods, standards, and domains 1,514.

## The numbers

| Stage | Count |
| --- | --- |
| First sweep, thirteen territories | 10,748 |
| Added by the completeness review | 1,402 |
| Added by the two extension territories | 2,615 |
| Final catalog, fifteen territories | 14,765 |
| Set aside in reduction as non-operations | about 1,700 |
| Distinct underlying operations found | about 110 |
| Entries in the named primitives list | 125 |
| Operations that needed an in-house name | 6 |

The named list carries more entries than the operation count because a few
operations keep two established faces that practitioners treat as distinct.
The set-aside entries are measurements, observed laws and phenomena, standards
and certification packaging, role labels, and named failure modes. A named
failure mode reduces to one of the operations misapplied or missing, so the
anti-pattern literature is the same list read backwards.

## The filters

Five filters were applied in order, and each is why the counts fall.

1. Establishment. An entry needed a proper name plus presence in books,
   canonical catalogs, standards, or professional glossaries. Products,
   tools, libraries, bare algorithms and data structures, and coinages that
   never spread were excluded.
2. Form. One bullet per entry, a gloss of at most 25 words, an origin only
   where certain. Nothing entered as a bare name.
3. Completeness before reduction. Omissions were sought by reviewers who
   could see everything already present, so additions could not duplicate.
4. The mechanism test. An entry survived reduction only as an operation,
   constraint, or tradeoff a person can choose to apply, never as a subject
   area, a role, a document type, or a value judgment. Clusters differing
   only in what they are applied to were merged.
5. Recognition. One name per operation, the one most engineers know, with
   genuine ties kept and the six gaps named in house.

## Verification

Every file was machine-checked between stages for banned characters, hedge
phrases, and malformed entries. The completeness reviewers worked from full
name indexes, so their additions could not restate what existed. And because
the reduction ran five ways in parallel, agreement between independent reports
could be measured: spaced retries and batching appeared in five reports of
five, locality, idempotence, and damage containment in four of five. The
primitive set was found by several readers independently rather than proposed
by one.
