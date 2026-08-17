# Using These Findings

This is study 0001's guidance for consuming the findings beside it, written
for the moment a new style or project is being designed. It explains what a
primitive is, why primitives conflict, and how a project settles those
conflicts. The study's numbered records stay immutable; this file is living
guidance and is rewritten in place as the practice sharpens.

## What a primitive is

A primitive is an irreducible operation: a thing an engineer can choose to do
that cannot be built out of the other entries on the list. Every primitive
carries a price, and the price is not a footnote. It names what applying the
operation forecloses, which is usually another primitive. Read every entry as
a purchase, never as a virtue.

## Irreducible does not mean compatible

Primitives oppose each other constantly, and they must, because most are
positions on a dial where some other primitive is the opposite position.
Caching does work before it is asked for; lazy loading refuses work until it
is asked for. Fail fast dies loudly; graceful degradation limps onward. Retry
insists; load shedding refuses. Locking bets collisions are common; optimistic
concurrency bets they are rare. Type safety rejects what does not fit;
tolerant reading accepts what it does not recognize. Append-only keeps
everything; waste elimination and anonymization exist to remove things. None
of these pairs contains a wrong side. They conflict only when applied to the
same resource at the same point with a finite budget, which is the situation
engineering is always in.

## Treaties

A treaty is a named resolution of one such conflict in one context, and a
large share of the industry's named concepts are exactly this. The
stale-while-revalidate cache is the treaty between caching and freshness. The canary release is
the treaty between the feedback loop and blast radius. The error budget is the
treaty between reliability targets and delivery pace. Expand and contract is
the treaty between changing a shape and staying available. This family has
signed its own: the tiered document budgets are the treaty between bounded
size and a manual's need to grow, the seed-wins fingerprint is the treaty
between single source of truth and a local override, and the split between
checked and review-held rules is the treaty between automation and judgment.

## The craft

Engineering is deciding which primitive wins where, for this project, under
these constraints, and writing the ruling down. A style, in this family's
sense, is a fixed table of such rulings, made once so that derived projects
stop re-fighting the same wars. An anti-pattern is usually a primitive winning
a conflict it should have lost in that context. There is no configuration of
primitives that is simply correct; there are only rulings that fit a project's
constraints and rulings that do not, which is why the same primitive is a cure
in one repository and a disease in the next. One law holds across every
ruling: the checker lives outside the thing it checks, because a watchdog
inside a dead task is no watchdog, and a judge the judged can edit stays
green forever.

## Recommended use

1. Read the findings beside this file end to end before designing anything.
   The goal is not to apply entries; it is to make every omission a decision.
2. Set aside the general subset, which needs no per-project thought. Its
   checkable half is the styles' toolchain law: the import contracts, the
   audits, type checking, linting, and the prose checks. Its judgment half is
   the delivery gate's fifteen primitive items in each style's agent guide
   ([ArchetypeCore](../../ArchtypeCore/AGENTS.md), [Keel](../../Keel/AGENTS.md),
   [Helm](../../Helm/AGENTS.md)). Those places are the single source of truth
   for what counts as general; this file deliberately copies none of it, so
   the two can never drift apart.
3. For each remaining group, ask which entries the project's terrain actually
   touches, then decide which side of each conflict wins where. Prices decide
   this, never fashion.
4. Write each ruling that would otherwise be re-litigated as a decision
   record, including the losing side and why it lost here.
5. Treat the family's standing rejections as context-bound rulings, not
   verdicts. Each names the condition that would reopen it: a team, real
   production traffic, a genuinely published package.
6. When two chosen primitives meet on the same resource, name the treaty
   explicitly instead of letting the collision resolve itself in code nobody
   chose.
