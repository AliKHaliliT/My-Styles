# Running a Study

The treasury exists so the next design starts from evidence rather than from
memory, and the method that produces the evidence has to meet the same
standard. This file is that method, written from the two studies that have run
under it. It is living guidance, rewritten in place as the practice sharpens,
and it is the only treasury-level guide; guidance on consuming a particular
study's findings stays beside that study.

## When a study is worth running

Run one when the question outlives the session that asked it, when the answer
would otherwise be re-derived from recollection every time it comes up, and
when the finding will still be true after the code changes. The cost is large
and paid once.

Do not run one to describe what any repository currently does, since that rots
and belongs to a STATE file. Do not run one to settle a rule for a single
style, since that is a decision record. Do not run one for a question a single
search answers.

## The five stages

1. Enumeration. Split the subject into territories, one pass per territory,
   sized so a pass can be exhaustive inside its own borders. Fix the rules of
   entry in one contract file that every pass reads, rather than restating
   them per pass, so the entries come back in one shape and can be checked
   mechanically. Seed each territory with a floor of names showing the
   expected granularity, and say plainly that the floor is not a ceiling.
   Every pass writes its section straight to its own file. Nothing of value
   returns through a summary.
2. Mechanical checks. Run between every stage, never only at the end. The
   checker is written before the work it judges and runs outside the pass that
   produced it, because a pass grading itself reports what it intended.
3. Completeness review. Independent passes whose only task is finding
   omissions, each holding the complete name index of its own territories, so
   an addition cannot restate what is already there. Give each reviewer a list
   of canonical catalogs to work through by name. An instruction to look for
   gaps produces brainstorming; an instruction to work through a published
   catalog produces findings. A book that numbers its rules is itself a
   completeness test, and so is any published index that claims to be
   complete.
4. The fold. One pass per family, each holding a hard entry budget. The budget
   is the instrument, because a fold without one becomes a copy. Two names for
   one thing are one entry with the alternates riding along, a thing named
   separately by several cultures is one entry, and a taxonomy nobody needs
   item by item becomes one entry naming its members. Drop an entry for being
   unhelpful to a reader who is deciding something, never for being obscure.
5. Resolution. Where two families claim one name, it goes to the family that
   owns the subject, and the genuine synonyms of the discarded copy are
   carried across. Where one word names two different things, it becomes two
   entries.

## The checks worth writing every time

- Banned characters and hedge phrases, since both spread once one pass uses
  them.
- Entry shape, so every entry opens with its name and defines itself.
- A gloss cap, enforced at the stage it belongs to rather than globally.
- Repeated names, scoped to the group rather than the file, so one idea priced
  differently in two contexts is not reported as a duplicate.
- Entries that point at another entry instead of defining themselves.
- Per-file counts at every stage, which is where the funnel numbers come from.
- A name index emitted for the next stage to consume.
- An independent pass confirming that additions do not restate what their
  author was shown, which turns a reviewer's error rate into a measurement.
- A loss audit after the fold, measuring survival group by group across the
  catalog. A group that keeps a third of its entries was folded. A group that
  keeps none is a hole.

Two cautions about the checks themselves. Prove each one against a planted
defect before trusting a clean result, because a check that never fires and a
check that cannot fire look identical. And expect the loss audit to be blind
where the fold kept a name inside another entry's gloss rather than as a
title, so probe its findings by hand before commissioning any repair.

## What the two studies paid to learn

- Write to disk first. Interruption at this scale is normal rather than
  exceptional, and a pass that holds its work until the end loses all of it. A
  spend limit once ended five reviewers in the same minute, and only the work
  already flushed survived.
- Give a reviewer everything already found, or its additions will restate it.
- A budget is what makes a fold happen. Instructions to be concise are not.
- Measure the reviewers instead of believing them. Self-reported error rates
  come back lower than measured ones.
- A rule written for one stage can be wrong at the next, and the honest fix is
  to change the rule in the open and record both numbers, not to damage the
  work into compliance.
- Record the boundary that was excluded, in one line, so a later reader knows
  the omission was a decision.

## What a study leaves behind

One folder, numbered records in reading order, the research record before the
findings it produced. The record carries the question, the method, the funnel
counts at every stage, the filters that explain why the counts fall, and how
verification was done. The findings carry what is meant to be reread. A study
whose findings need more guidance carries one uppercase guide beside its
records, and the ledger in the README gains its row.

The raw catalog is not kept. It is scaffolding, it is too large to reread, and
an unfolded catalog decays into a list nobody opens. What the record keeps is
its size at every stage, which is what lets a reader judge the fold. Anyone
wanting the catalog itself runs the study again, which is why this file exists.
