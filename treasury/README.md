# Treasury

A common treasury for the style family: durable research findings that no
single style owns, kept so the next style is designed from evidence rather
than from memory. Each study lives in its own numbered folder. Inside a
folder the files are numbered in reading order, and the research record
always comes before the findings it produced.

## How to use it

Before drafting a new style, read the newest findings end to end and treat
every entry as an option to weigh, never an obligation to satisfy. The point
of the treasury is that every omission becomes a deliberate decision. A study
whose findings need more guidance than this carries its own
uppercase guide beside its records.
[Study 0001's](0001-primitive-reduction/HOW-TO-USE.md) covers what a
primitive is, why primitives oppose one another, and how a project settles
the conflicts.
[Study 0002's](0002-optimization-vocabulary/HOW-TO-USE.md) covers which of
the optimization families hold decisions at all, and the order to move
through them.
[Study 0003's](0003-security-vocabulary/HOW-TO-USE.md) covers why the threat
model has to be settled before any of its priced entries can be weighed, and
the order to move through its families.
[Study 0004's](0004-research-methodology-vocabulary/HOW-TO-USE.md) covers why
the price a method names is the finding rather than a decoration, and how to look
a name up rather than reading the vocabulary through.

Before running a new study, read [the method](HOW-TO-RUN-A-STUDY.md). It
carries the six stages, the checks to write between them, and what the
studies already run paid to learn, so the next study starts from a written
method rather than from anyone's recollection of the last one.

## Ledger

| Study | Date | What it holds |
| --- | --- | --- |
| [0001-primitive-reduction](0001-primitive-reduction/) | 2026-08-11 | 14,765 named software engineering concepts reduced to 125 primitive operations |
| [0002-optimization-vocabulary](0002-optimization-vocabulary/) | 2026-08-17 | 9,188 named optimization concepts folded to a 1,272 entry vocabulary in six families |
| [0003-security-vocabulary](0003-security-vocabulary/) | 2026-08-22 | 13,764 named security concepts folded to a 1,996 entry vocabulary in eight families |
| [0004-research-methodology-vocabulary](0004-research-methodology-vocabulary/) | 2026-08-27 | 22,924 named research-methodology concepts folded to a 2,908 entry vocabulary in thirteen families |

## Family rulings

Rulings no single style owns live in [decisions/](decisions/), one immutable
record each, numbered in their own sequence. A ruling is recorded where its
bytes land: one that changes the styles keeps a record in every style it
changed, and one that changes no style's bytes, a refusal or a study's
disposition, is recorded here once. Before analyzing anything family-wide,
check this folder; the question may already be settled.

| Ruling | What it settles |
| --- | --- |
| [0001](decisions/0001-record-family-rulings-once-in-the-treasury.md) | Where family rulings are recorded, and why refusals never sit in style records |
| [0002](decisions/0002-adopt-thirty-six-primitives-and-refuse-six.md) | Study 0001's disposition: the general thirty-six, the terrain-bound, and the six refusals |
| [0003](decisions/0003-adopt-optimizations-discipline-and-leave-its-techniques.md) | Study 0002's disposition: two gate items and free-win lints in, every priced technique out |
| [0004](decisions/0004-let-the-index-do-what-skill-files-do.md) | Skill files refused; the agent guide and the index already form the two loading tiers |
| [0005](decisions/0005-take-security-s-unconditional-core-and-refuse-its-priced-bulk.md) | Study 0003's disposition: one gate item and the mechanical lints in, every priced mechanism out |
| [0006](decisions/0006-hold-research-methodology-for-the-seat-it-was-gathered-for.md) | Study 0004's disposition: the vocabulary enters no style, and what it hands the research seat it was gathered for |
| [0007](decisions/0007-hold-a-carried-copy-to-its-original-while-they-share-a-roof.md) | Carried copies track their originals inside the host; an extracted child freezes, and no arrow carries the mechanism |
| [0008](decisions/0008-ship-template-workflows-on-tags-and-pin-the-live-one.md) | Template workflows ride major-version tags so children start current; the live workflow pins digests, and hardening is the child's deliberate move |
| [0009](decisions/0009-serve-a-ui-beside-the-server-from-helm.md) | A UI beside an ArchetypeCore server is a Helm instance, co-hosted from `app/static/` or standalone from the same build; the Jinja2 slot leaves the server's form |
| [0010](decisions/0010-defer-the-frontend-seat-that-ships-its-own-server.md) | The server-rendered frontend seat waits for a public-facing product that needs SEO, streaming, or cookie sessions; until then Helm is the whole frontend answer |
| [0011](decisions/0011-dispose-of-the-doctoral-repository-s-upstream-report.md) | The first real upstream report, tested entry by entry: four kept, two adapted with corrected diagnoses, one refused, and the adoption gaps it exposed closed in every style |

## Rules of the folder

- One study, one folder, numbered in order of completion. The research
  record carries the question, the method, and the numbers; the findings
  carry what is meant to be reread; the ledger above indexes every study.
- A study folder may carry one uppercase HOW-TO-USE.md beside its numbered
  records: living guidance for consuming that study's findings, bounded,
  rewritten in place, and never part of the record. Numbered files are the
  immutable records; an uppercase file is living and sorts after them.
- The decisions folder holds family rulings: immutable records of what the
  family adopted, refused, or settled where no single style's bytes carry
  the answer. Every study leaves its disposition there, and a refusal the
  family could plausibly revisit names the condition that would reopen it.
- Guidance on consuming a study belongs to that study. Guidance on producing
  one belongs to the folder, and HOW-TO-RUN-A-STUDY.md is the single
  treasury-level guide: living, rewritten in place as the method sharpens,
  and kept as brief as the method allows. The two are different species,
  which is why one sits beside the records and the other above them.
- Studies are records in the family's document taxonomy. They are exempt
  from the line budget, immutable once merged, and corrected only by a later
  study that names what it supersedes.
- Files are self-contained. The method, the numbers, and the findings live
  in the files themselves, never behind an external link.
- Every byte follows the family prose rules. Written for a public audience,
  colons only for lists, quotes, and labels, em dashes inside the family's
  per-file budget.
- Nothing in here describes the current state of any repository. State rots
  and belongs to STATE files. The treasury holds only findings that stay
  true.
