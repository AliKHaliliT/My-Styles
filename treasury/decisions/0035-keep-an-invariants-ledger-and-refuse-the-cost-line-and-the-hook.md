# 0035. Keep an invariants ledger and refuse the cost line and the hook

Status: Accepted
Date: 2026-09-18

## Context

Study 0006 asked how systems state an invariant as a first-class artifact
and bind it to something that holds it. The question arose from a language
whose compiler refuses code that breaks a law the project declares in a file
of its own. The language was set aside on the day it was read, and what
survived was the shape underneath it, a written set of invariants each bound
to something that refuses. The study gathered 2,280 names from 301 sources
across sixteen territories and folded them to 166 entries in eight families,
each family a decision the shape of such a set has to make.

Its reorganizing finding is that every mechanism in the field answers one of
two questions and no field answers both. The formal traditions bind a single
claim with precision about what a green result is worth. The certification
traditions keep a set of claims complete, numbered and read, and bind each
one by naming an authority. No field names the small artifact in which an
ordinary project writes its own invariants and binds each to whatever holds
it, with the strength of the holder stated beside it.

## Evidence

The family was measured on 2026-09-18 by counting what it holds. Across the
five seats the docs audits carry 140 checks, every one about document shape,
record immutability, naming or layout. Ten named import contracts and two
property suites hold anything about what the products do. Every seat writes
between four and thirteen sentences about its product in prose that contain
never, always, guarantee or invariant, and no document in the repository
carries a section listing them. The family's checking effort sits on its own
law, and its claims about its products are sentences.

The two closest things the family already has are the named import contract,
a sentence stating an invariant beside the tool that refuses a violation, and
the host seat's claim ledger, whose rows carry a status, the claim in prose,
evidence pinned to a commit and the threats to it. The first is the shape of
a row and the second is the discipline of a set.

The study also found three things the field has no name for. The commit
hook, the only moment a check can refuse a claim before it exists in anyone's
history, appears under no headword in the corpus. A ledger of a project's own
invariants has no name. And no tradition records what a claim costs to keep,
though every one grades harm, confidence or rigour.

## Options considered

- Deriving the ledger from markers on the tests and contracts instead of
  writing it. Refused, because a derived list says which holders exist and
  cannot carry a claim nobody has bound yet, and the unbound claim is the row
  a reader most needs to see.
- Mining the invariants from the code with a detector. Refused, because the
  corpus shows a miner returns thousands of candidates a person must accept
  one at a time, and the family's ledger is meant to be read.
- A cost column on every row, saying what keeping the claim costs per run.
  Refused for now. Where cost varies, the row's holder is a test and the test
  runner already reports its duration on every run, so the column would copy
  a number that goes stale and no audit can check; a contract row always
  costs one lint pass and a review row costs attention nobody can measure.
  It reopens the day a holder arrives whose cost no runner reports, such as
  a model checker run outside the suite.
- A commit hook running the fast checks before every commit. Refused. The
  branch protocol gates the same tree minutes later before anything is
  pushed, the hooks folder is untracked so every clone would install it by
  hand, and one flag skips it. The family's history has no red push a hook
  would have prevented. It reopens if the owner rules that every commit,
  rather than every push, must be green.
- Shipping the ledger's form without rows in the templates. Refused, because
  the family teaches by exemplar bytes and a form with no worked rows is how
  a style drifts at its first adoption.
- Any rung that claims proof. Refused, on the study's own caution that a
  sampled property is not a proof, a passing test is not a theorem, and an
  undefeated argument is not a demonstration.

## Decision

Every seat carries a living document, the invariants ledger, listing what
must stay true about its product. Each row names the claim in plain words,
the holder that refuses a violation, and the rung the holder sits on. A
holder is a tracked path, with a quoted needle the file must contain where
the path holds more than one thing, or the word review. A rung is one of five
words: impossible, where a type, an import contract or a check over the whole
tree refuses the violation before anything ships; generated cases, where a
property test fails on a counterexample drawn from generated input; listed
cases, where an example test fails on the cases it lists; advised, where a
check names the violation on every run and a reader decides; and review,
where nothing decides it. The docs audit decides four things, that every
row has its three cells, that every holder path is in the tree and contains
its needle, that every rung is one of the five words, and that a holder of
review pairs only with a rung of review. It prints every review row as an
advisory on every run, so an unbound claim cannot hide behind a green. Whether a row is
honest stays with review, which is where the study says it has to stay.

The templates carry a small honest set each, three or four rows over holders
they already have, because the rows are the exemplar. A project built from a
template writes its own rows at adoption, cut from that exemplar, and a
child's ledger is the child's own document, re-adapted at re-alignment like
its state file and never recopied. Review rows are how a project adopts with
honest gaps and a green build, which is the frozen baseline the study found
to be the answer to adopting any claim set into a codebase that already
exists.

The ledger lands as its own law change, one landing across every seat with a
record in each. This record disposes of the study and rules on the refusals
above. The method guide gains the study's instrument lessons, since four of
the five defects the study found in its own tools shared one shape and the
next study should not pay for them again.

On the word novel. The study proves absence from the catalogs it worked, not
from practice; it missed the commit hook for exactly that reason, since a
convention is used everywhere and written up nowhere. The family's records
say the artifact has no published name and never that nobody keeps one.

## Consequences

The family gains a document that lists its products' claims where before it
had sentences, and a check that holds the pointers while review holds the
truth. The cost column and the hook are recorded here with the condition that
reopens each. The eighth family of the study, the recurring shapes a claim
takes, is the vocabulary a writer walks when filling the ledger, and the
study's records are where to find it.
