# 0038. Refuse a maintained wiki over the treasury and index the names its studies share

Status: Accepted
Date: 2026-09-22

## Context

A published idea file, read on 2026-09-22 and titled LLM Wiki, proposes a
personal knowledge base in three layers. Raw sources stay immutable, an agent
writes and rewrites a wiki of interlinked pages over them, updating entity
pages, revising summaries and flagging contradictions as each source
arrives, and a schema file tells the agent how the wiki is structured and
maintained. Three operations run over it, ingest, query and lint, and two
files navigate it, a content index and an append-only log. The file is
deliberately abstract and reports no measurement.

The treasury already does most of this under other names. The method guide
is the schema, a study is an ingest that folds thousands of names once, a
disposition record is an answer filed back, the README's ledger is the
content index, and the loss audit is a lint inside one study. The two
designs invert each other at one point. The pattern keeps its raw sources
and rewrites its compiled layer. The treasury throws its raw catalogs away
as scaffolding and freezes its compiled layer as immutable records that
never cite one another.

## Evidence

The treasury was measured on 2026-09-22 by extracting every bold name from
the six studies' findings files and intersecting them, then reading every
collision by hand. Six studies hold about 6,500 entries. 178 names appear in
bold in two or more studies. In 98 of them the studies name one thing and
price it separately, with no pointer between the entries. In 80 one word
names different things in different studies. Ten names appear in three
studies. Fuzzing is a primitive priced as opaque cases and a model to
maintain in study 0001, five entries priced as compute, triage and a
coverage plateau in study 0003, and a holder that refuses late in study
0006, and no file of the three mentions the other two.

Overlap with study 0001 is by design and study 0002's guide says so, since a
vocabulary names locally what the primitives name in general. About 48 of
the same-thing names sit between the three vocabularies alone, and that
overlap is stated nowhere. The only cross-study text in the folder is one
section of study 0002's guide relating it to study 0001 at whole-study
grain, and it runs one way, because the older study was frozen before the
younger existed. The scouting stage protects a new study's shape from an
earlier one on purpose and checks content not at all, so nothing in the
method would have noticed.

## Options considered

- Adopting the pattern, with the findings rewritten in place as later
  studies arrive. Refused. A study is a record, dated and measured, and a
  page rewritten by an agent is held by review alone, the weakest rung the
  family named in ruling 0035. The pattern works for its author because a
  person reads every page beside the agent, which is the human doing the
  check, not the design doing it.
- A chronological log file. Refused, because the repository's history and
  the dated rows of the ledger already carry it.
- A search tool over the folder. Refused, because six files answer to one
  search command at this scale, and the index below answers the question a
  search cannot, which is whether two hits mean one thing.
- Keeping the raw catalogs so a later study can re-synthesize. Refused, on
  the folder's standing rule that an unfolded catalog decays into a list
  nobody opens.
- Refusing the index too and writing a trigger for it. Refused, because the
  trigger considered, a study describing what an earlier study already
  described, had by the count above already fired three times, and a bar set
  above a measured number is a refusal fitted to its outcome.

## Decision

The treasury gains one living file above the studies, SHARED-NAMES.md, with
one row per name that two or more studies carry in bold, naming the studies
that hold it and one of two words. The word same says the studies name one
thing and price it separately, so a reader reads every holder's entry. The
word different says one word names different things in different studies,
so a reader picks the sense first. A script at the repository root,
scripts/audit_treasury.py, computes the shared names from the findings files
and holds the rows to them on every run of the family's law job. It fails
when a shared name lacks a row, when a row names a name no two studies
share, when a row's studies differ from the findings, when the rows leave
alphabetical order, or when the third cell is neither word, and it prints
the row a missing name needs. Whether the word is right stays with review,
where ruling 0035 put the truth of every row the family keeps.

The method guide's resolution stage gains the rule that a name an earlier
study already holds stays in the new study's entry and gains its row in the
index once every holder's entry has been read, and the guide's closing
section names the rows among what a study leaves behind. The index is the
folder's one file across studies and never says what a study says, only
where, so the records stay the records.

## Consequences

A reader weighing a technique finds every price the treasury has put on it
from one table, and a reader who meets a word finds out whether the studies
mean one thing by it. The next study lands with its rows written or its
build goes red. The 80 rows marked different are the cross-study form of the
fold rule that one word naming two things becomes two entries, and they stay
rows rather than becoming edits, because the records are immutable. The
pattern refused here reopens only if the family ever decides that its
findings should be rewritten in place, which would be a change to the record
species and not to this index.
