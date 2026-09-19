# How to use the invariant binding study

Living guidance for reading study 0006's findings and for filling a ledger of
invariants. Rewritten in place as the practice sharpens, and never part of the
record.

## What this study is for

It exists so that a project writing down what must stay true about its product
starts from the field's own shapes rather than from whatever the writer happens
to remember, and so that every row says what its green is worth. The findings
hold eight families. Seven divide the machinery of binding a claim to something
that refuses, and each is a decision a ledger's shape has to make. The eighth
holds what the claims themselves say, and this guide lists it, because that
family is the one a writer walks while filling rows.

## How to write a row

A row carries a claim, a holder, and a rung, and the seats' rulebooks fix the
columns. Write the claim as one plain sentence a reader could test by hand, in
the product's own words rather than the tool's. Name the holder as the tracked
path that refuses a violation, with the quoted name of the test, contract, or
rule where the file holds more than one thing, or write review when nothing
decides it yet. Choose the rung by what a green result licenses a reader to
believe and nothing more. A type or an import contract makes the violation
impossible. A property test has found no counterexample in the cases it
generated. An example test has passed the cases it lists. An advisory has named
the violation and left the decision to a reader. Review means a person reads.
No rung says proved, because a sampled property is not a proof and a passing
test is not a theorem.

Before writing a claim, walk the shapes below and ask which apply to the
product. A shape that applies and has no row is a claim the product makes in
prose or in nobody's head, and a review row is the honest way to write it down
until something holds it.

## The shapes a claim takes

Twenty-two shapes recur across databases, contracts, schemas, detectors, and
specifications, each under many names. They are grouped here by what they
assert.

**About a single value or state.**

- A one-of constraint. The value is always drawn from a named set, an
  enumeration, a pattern, a format. A schema or a type holds it before anything
  runs.
- A range or bound. A quantity stays between stated endpoints, a minimum, a
  cap, a length, a gas ceiling. One comparison checks a state, and a type can
  make the breach impossible.
- A non-null constraint. A location always holds a real value. A type system
  carries it at no runtime cost, and a validator fires only on the paths a
  caller reaches.
- A linear relationship. Two or three variables stay tied by one arithmetic
  law, an equality, an ordering, a modulus. A detector that fits the law
  reports what held on every recorded run, never a proof.

**About a collection or an order.**

- Sortedness and uniqueness. A collection keeps its order, holds no repeats, or
  stays contained in another. A unique constraint or a key holds it in a store,
  and a property test holds it in code.
- A round trip. Applying an operation and its inverse returns the original, and
  its siblings say that repeating changes nothing further or that two
  operations commute. Property tests over generated input are its holder, and a
  translator's row is one of these.
- A metamorphic relation. When no oracle says what one run should return, a
  stated relation between two related runs stands in. Add a constant and the
  output moves so, permute the inputs and it does not. A wrong relation still
  passes, so the row names the relation.

**About accounting and authority.**

- Conservation. Nothing is created or destroyed outside the named operations,
  so the sum of the parts equals the recorded whole. A fuzzer finds a break
  only when it generates one, and a prover discharges the sentence over every
  sequence.
- Revert on condition. A call with stated inputs must fail and change nothing,
  which is the direct way to say a guard exists, and its twin says a read never
  fails. Both are checked by making the call.
- Access control. Only a named principal may cause a state change and every
  other caller is refused. Cheap to check at one entry point and hard to check
  globally, since a second path into the same storage defeats it.

**About time and the whole run.**

- A safety property. Nothing bad ever happens, so one finite trace refutes it
  and no finite trace confirms it. Every state invariant is one, and a monitor
  catches a violation at the step it occurs.
- A liveness property. Something good eventually happens, which no finite
  trace refutes. A checker hunts for a cycle in which it never does, and the
  row names the fairness it assumes.
- Termination. The routine finishes, shown by a measure that strictly
  decreases. Bounds on time, memory, and gas are the same claim with a number
  attached, and the measure has to be supplied.
- Memory safety. No freed or unwritten memory is read, no index or integer
  overflows, no two unsynchronized accesses race. A sanitizer reports the path
  that executed, and an abstract interpreter proves the absence at far greater
  cost.

**About a store's guarantees.** Six shapes grade what a database or a
replicated system promises, and each level is defined by the anomalies it
forbids: linearizability, serializability, snapshot isolation, read committed,
eventual consistency, and the transaction anomaly itself, which names what each
level still permits. A row for a store names the level and the anomaly it
accepts, and its holder is a checker replaying recorded histories, which for
the strongest levels is a hard search.

**Two shapes that grade rather than claim.**

- A quality attribute names a dimension of how well a system works,
  reliability, maintainability, security, and stays an empty bucket until a
  measure and a threshold are attached. A row for one carries the measure, or
  it is prose.
- A requirement keyword, must, should, may, fixes how binding the sentence
  around it is and never states the check, so a must with no holder behind it
  is enforced exactly as much as a may. The ledger's rung column exists so this
  cannot happen quietly.

## Two things the rows never record

The findings say what a mechanism is worth and never what it proves beyond
that, and the claim's wording keeps that boundary. And no catalog in the field
records what a claim costs to keep. The family refused a cost column in
treasury 0035 because the test runner reports a test's duration on every run,
and the refusal names the condition that reopens it.
