# 0060. Prove a test by the failure it catches

Status: Accepted
Date: 2026-09-16

## Context

The family proves every audit rule against a planted defect, and the guide
says why in its commands, that a check that never fires and a check that
cannot fire look identical. The test suites had no such rule. Their bullet in the
guide governed where a suite lives, what it may substitute and at which seam,
and that no coverage threshold binds breadth, and nothing said whether a test
can fail, how its expected value is derived, or what shows that a fix fixed
anything. Treasury study 0005 found the missing rule stated three times in
the published agent-skills ecosystem by writers who had never seen the
family, and the family disposition, treasury 0030, Take eight rules from the
skills study and refuse the rest, adopted it as one law with three clauses,
because a rule stated at three moments is one rule.

## Evidence

The guide's test bullet and the map's testing section carried four rules,
placement, substitution at a seam, no threshold, and both paths of an
optional dependency, and the word failure appeared in neither. The record
that fixed the test contract chose to specify the frame and leave breadth
free, and a rule about proof binds the frame. The three sources agree on the
instrument and differ in emphasis. One asks the writer to name the production
change that would fail the test before writing it, to derive expectations by
hand because a value the code computes for itself passes whatever the code
does, and to mutate the code against a closed list before calling a test file
done. One validates a patch by a test that fails on the unpatched tree and
passes on the patched one, with a marker proving the assertion was reached
and the failure was not a harness that died first. One triages surviving
mutants and holds that a mutant is equivalent only when the types and the
control flow prove it, never because no test noticed. The family's own audit
selftests are the same instrument pointed at checks instead of tests, and
were adopted for the same reason.

## Options considered

- Three landings, one per clause. Refused, because the clauses are one
  principle at three moments, and the shape limits landed three limits as one
  ruling on the same reasoning. A later supersession names the clause it
  changes.
- A mutation-testing tool in the gate. Refused for the template. A campaign
  runs the suite once per mutant, so its cost grows with the suite times the
  code, and its output still needs the equivalence triage the rule asks of
  the writer. A child may run one as a measurement; nothing here gates on it.
- A coverage threshold as the proof a test exists. Refused again, as the test
  contract refused it, because a percentage buys assertions that assert
  nothing.
- Requiring a docstring on every test stating the break. Refused, because the
  rulebook already makes the case name carry that, and a comment belongs in a
  test only where the name cannot.

## Decision

The test bullet in every guide, and the testing section of every map, gain
the rule in three clauses.

1. Before a test is written, its name states the break it catches, and its
   expected value is derived without the code under test. A value the code
   computes for itself, and a test that can fail only on an intentional
   decision, a constant's value or a message's exact wording, are refused.
2. After a test file is written, the code is mutated against a closed list,
   in thought or in a scratch copy: a wrong constant or argument, a wrong
   branch, a missing side effect, an empty or default return, a missing check
   for zero, empty, nil, unauthorized or malformed input. A test fails for
   each. A survivor is a gap in the suite unless the types and the control
   flow show the mutant equivalent; that no test noticed is not the proof.
3. After a fix, the fix is reverted, the regression test is watched failing
   on its assertion and not in its harness, and the fix is restored.

The clauses bind the three code seats and the arrow, which carries Keel's
guide tail; the host carries no suite of its own and reaches its arrows
through their styles. This rule lands as prose. The tool that would
mechanize the second clause was refused above, and the first and third
clauses describe what a writer did before and after a test existed, which no
check on the tree can see.

## Consequences

A worker finishing a test file owes the mutation pass, and a worker fixing a
defect owes the revert. Neither adds bytes to the tree, so the gate is
unchanged and the audits' selftests remain the family's worked example of the
instrument. The mutation list is closed and revisable only by a record, so a
child that finds a mutation class the list misses reports it upstream rather
than extending the list locally. A project re-aligning to the family receives
the three clauses with its guide and map.
