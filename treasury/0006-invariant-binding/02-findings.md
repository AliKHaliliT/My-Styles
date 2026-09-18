# Study 0006. Findings

Date: 2026-09-18

Eight families, 166 entries, folded from 2,280 names gathered across sixteen
territories. Seven families hold the machinery of stating a claim and binding
it to something that refuses. The eighth holds what the claims say.

A reader here is deciding whether to keep a written set of invariants and what
shape to give it. Each family below is a decision that shape has to make, and
each closes with what the field has settled and what it has left open.

## The one finding that reorganizes the rest

Every mechanism in this corpus answers one of two questions, and no field
answers both well.

The first question is how a single claim is bound. The formal traditions
answer it with enormous precision, from clause kinds attached to a routine
through solvers and proof kernels to the exact strength of the resulting
verdict. The second question is how a set of claims stays complete, readable
and honest as the system grows. The certification traditions answer that one,
with registers, numbering, grading, traceability and the review that reads
them, and they answer the first question by naming an authority rather than a
mechanism.

A practice that wants both takes the binding vocabulary from one tradition and
the set discipline from the other. Nothing in the corpus does this on its own,
which is why the field has no single name for the artifact a reader might
build.

## F1. Where the claim is written

The artifacts that hold an invariant as a written sentence, from a clause on
the declaration it governs to a document no build ever opens.

Three choices run through every entry. **Distance** decides survival, since a
clause on a declaration moves when that declaration moves and dies when the
unit is deleted, while a model file, a policy file or an argument document
outlives the code and drifts from it silently. **Readership** decides who can
act, since a schema, a rule file and a test are read by machines and by people,
prose sections and decision records only by people, and a golden file by
neither until a reviewer says what it holds. **Granularity** decides what a
reader can assemble, since one file for the whole system concentrates review
and buries the claim about a single unit, while one artifact per claim
scatters them beyond any list.

## F2. What binds the claim

The kinds of holder, from a type the compiler will not accept through solvers,
fuzzers, monitors, constraint engines and policy gates to the reviewer who
withholds approval.

Three choices sit here. **How early the holder refuses**, since a type refuses
before the code exists, a fuzzer refuses after a sequence runs, and an alarm
refuses after users felt it. **The price of restatement**, since a solver, a
schema and a policy engine each demand the claim in their own language, while
a sanitizer and a reviewer take the system as it stands. **The blind half**,
which is why a claim carries more than one holder, and why a claim held twice
pays twice in build time, runtime or attention.

## F3. What the binding is worth

What a green result licenses a reader to believe, from a violation that cannot
be expressed down to an argument nobody has defeated yet.

This is the family the study was really about, and its entries are the ones a
ledger must not overstate. Three choices sit under them. **The direction of
error a reader will accept**, whether the check may miss a violation or may
report one that cannot happen. **Where the guarantee stops**, since a bound, a
sampled suite, an undefeated argument, and a verified model never tied to the
shipped binary all stop in different places. **What goes unchecked on
purpose**, since axioms, admitted goals, unqualified tools and waived findings
each turn a green into a conditional statement, and the condition is legible
only where it is written down.

The sharpest single distinction in the corpus lives here. A partial
correctness result establishes its conclusion only if the program terminates
and says nothing about whether it does, while a total correctness result
carries termination with it. One published calculus marks the difference in
its own name, calling the weaker form liberal.

## F4. When the claim is checked

The lifecycle in order, from the compiler that refuses a program to the
monitor that watches it serve.

One sentence tested at compile time, at the merge, and under live traffic is
three rules, each seeing what the earlier one could not see. Three choices
follow. **How early the claim is tested**, since an earlier check refuses more
and knows less. **Whether a check runs on a clock or on an event**, since a
clock pays its cost whether or not anything changed and an event leaves every
unnamed occurrence unwatched. **Whether a settled claim expires**, since
without a horizon a claim is re-asked only after something else has already
failed.

## F5. How the link stays honest

The mechanisms that keep a claim and its evidence pointing at each other as
both move, and that report which claims have no evidence and which evidence
has no claim.

Three choices run through them. **Whether a link resolves**, since a pointer a
build resolves on every commit reports its own breakage while a row in a
matrix reports nothing until a person rereads it. **What a passing result is
pinned to**, since a result carrying the version and digest it ran against can
be refused when either moves and a bare pass cannot. **What happens to an
unsupported claim**, since some schemes mark the gap and leave it visible,
some close it by declaration, and some let a green build hide it.

## F6. What happens on violation

The response when a holder finds a claim broken, and the machinery for getting
out of it.

A reader faces five choices. **Where the response lands**, since a compile
error, an admission denial, a merge gate and a revert stop the violation
reaching anyone, while an alert, an audit-mode scan and a graded finding
record one that already arrived. **Whether the machine acts or only speaks**,
since enforcement, repair and degradation change the run and a warning changes
nothing. **How many enforcement levels a rule set carries**, and who overrides
each. **Which escape exists and what it costs**, since a suppression comment
beside the code asks nothing of its author, a deviation record demands
rationale, approver and scope, and a frozen baseline forgives every past
violation at once. **Whether a reported violation carries a status somebody
owes an answer to.**

The frozen baseline deserves its own line. It records the violations a rule
already has so that only new ones fail, which is the answer to the hardest
problem in adopting any claim set into a codebase that already exists. Without
it the first run is red everywhere and the set is switched off on its first
day.

## F7. How the set stays complete

The register that says which claims exist, the numbers and statuses that keep
them findable, the argument that decomposes one goal into many, the catalogs
published for reuse, and the tools that mine claims nobody wrote.

Four choices sit here. **Who writes the set**, since a hand-written register
says what the team meant and stays silent about everything it forgot, while a
mined set proposes what the code does and returns thousands of candidates a
person must accept one by one. **Whether the set is graded**, since grading
buys rigour proportional to harm and invites the grade to be argued down.
**What surfaces a hole**, since a traceability grid and an undeveloped-goal
marker report only holes someone already named, while coverage figures,
surviving mutants and unclaimed files report holes nobody named. **Who reads
the set**, which is why numbering, status values and suppression exist at all,
because an unread register still passes every check it declares.

## F8. What the claims themselves say

The recurring shapes practitioners write down, and the answer to what the rows
of a ledger contain.

Three published lists supply most of the vocabulary. A consistency and
isolation lattice grades what a store guarantees and names, level by level,
the anomaly each one still permits. A detector's invariant templates enumerate
the shapes a claim about program state can take, and a detector that emits
them emits nothing else. A set of token property tables states conservation,
revert and authority claims per standard.

The shapes repeat across fields under different names. A bound is a bound in a
schema, in a gas ceiling and in an interval domain. What the family leaves
open is cost, since some rows cost one comparison and others a model checker,
and no catalog records which.

## What the field has no name for

Three absences are worth as much as the entries.

**The local moment before history.** Pre-commit and commit hooks appear under
no headword in 2,280 names, though they are the most common place a working
programmer meets a refused rule. They are a convention rather than a product,
a standard or a research contribution, and conventions are what nobody
catalogs. The moment matters because it is the only one where a check can
refuse a claim before that claim exists in anyone's history.

**A ledger of a system's own invariants.** Registers exist in the
certification traditions, catalogs of reusable properties exist in the
security traditions, and claim ledgers exist in research practice. No field
names the artifact in which an ordinary project writes its own invariants and
binds each to whatever holds it.

**The cost of a claim.** Every family names what a mechanism decides and what
it leaves undecided. None names what it costs to keep. The corpus grades harm,
grades confidence and grades rigour, and grades effort nowhere.

## Two cautions for anyone folding this further

The fold merges, so it conflates. One entry here carries a property class that
strictly does not belong to it, flagged by the pass that made the merge, and a
reader should expect others it did not catch.

The entries say what a mechanism is worth and never what it proves beyond
that. A sampled property is not a proof, a passing test is not a theorem, and
an undefeated argument is not a demonstration. Any later summary that loses
those three sentences has lost the study's subject.
