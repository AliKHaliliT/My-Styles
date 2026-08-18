# Using These Findings

This is study 0002's guidance for consuming the vocabulary beside it, written
for the moment someone is about to make a program faster. It explains what the
six families are for, which of them hold decisions, and the order to move
through them. The study's numbered records stay immutable; this file is living
guidance and is rewritten in place as the practice sharpens.

## Three kinds of vocabulary wear one word

The catalog splits by who acts, and the split matters more than any single
entry.

Analysis names cost without changing it. Every entry in the first family is a
way of saying what something costs or proving what it cannot cost less than.
None of it speeds anything up, and knowing it is free, which is why those
entries carry no price. Its use is deciding what deserves effort at all.

The toolchain acts without being asked. Almost everything in the third family
happens on every optimized build. Reading that family is not shopping for
techniques to apply, it is learning what is already done so as to stop
hand-writing it, and learning what a compiler cannot do through code that
hides a fact from it. Where such an entry names a legality condition, that
condition is the actionable half of the entry.

The remaining families hold decisions. Choosing a cheaper computation, fitting
work to the machine, delivering work to someone, and measuring and deciding
are the four families where an entry is a choice with a price, and the price
is the part to read first.

## The order that keeps this honest

1. Establish that something is too slow against a stated number, not against
   an impression. The sixth family holds the vocabulary for stating it.
2. Measure where the cost is. A profile decides which family to open next, and
   the sixth family's clock, warmup, and sampling entries decide whether the
   measurement means anything.
3. Reduce the work before speeding it up. The second family changes what is
   computed, which is where the largest wins live and where nothing else can
   act on your behalf.
4. Stop obstructing the toolchain before replacing it. Read the third family
   and remove what blocks a transformation, rather than performing the
   transformation by hand.
5. Only then fit the work to the machine. The fourth family's techniques are
   real and often large, and they are also the ones that hardest resist being
   changed later.
6. Measure again, and keep the measurement. The sixth family's practices for
   holding a gain exist because an unheld gain returns to where it started.

## Both maxims, not one

The vocabulary contains a maxim against optimizing too early and a maxim
against pessimizing by default, and the pair is the actual discipline. The
first forbids spending effort and complexity before a measurement justifies
them. The second forbids choosing the slower construction when the faster one
costs nothing extra to write. Quoting either one alone produces a familiar
failure: a codebase tuned in places nobody waits on, or a codebase uniformly
slow by a thousand small defaults that were never decisions at all.

## Prices, and what they mean here

Every entry that names a technique names what applying it forecloses. Read the
price as the deciding half of the entry, because the technique half is what
makes it sound attractive and the price half is what makes it a choice. Two
entries whose prices cancel each other are not a contradiction in the catalog,
they are the two positions of one dial, and [study
0001's guidance](../0001-primitive-reduction/HOW-TO-USE.md) covers how a
project settles that kind of conflict and writes the ruling down.

## How this sits beside study 0001

Study 0001 reduced the discipline's named concepts to the operations
underneath them. This study did the opposite on one subject. It kept the names.
Much of what appears here is one of those primitive operations applied in a
single setting and named locally, which is why a reader who knows the
primitives will recognize the mechanism behind a name they have never seen.
Use 0001 to decide what a technique really is, and use this vocabulary to find
what a field already calls it, what its established alternatives are, and what
its practitioners have learned it costs.

## Recommended use

1. When facing a specific slow thing, open the family that owns it rather than
   reading the whole vocabulary. The families are ordered as a decision passes
   through them.
2. When designing something new, read the second and fourth families once for
   their prices alone, so the defaults chosen at the start are chosen.
3. When a name appears in a discussion and its meaning is contested, prefer
   this file's entry over the local usage, and say which is meant.
4. When an optimization lands, record the measurement that justified it and
   the price that was accepted. An optimization without a recorded price
   becomes a mystery constraint to whoever meets it next.
5. When tempted by a technique from the fourth or fifth family before the
   second family has been read, treat that as the signal it is, that work is
   about to be made faster instead of smaller.
