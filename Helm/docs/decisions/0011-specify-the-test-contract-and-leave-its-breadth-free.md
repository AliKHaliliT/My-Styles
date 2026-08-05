# 0011. Specify the test contract and leave its breadth free

Status: Accepted
Date: 2026-08-05

## Context

This template specifies where every production file goes and why. Tests were the one part of it with no rule. The frozen rulebook and the repository baseline mentioned tests zero times, and while this template was the only one of the three that actually demonstrated a test shape, with five suites mirroring `src/` and a shared setup file, nothing anywhere stated what that shape was. The practice existed and the rule did not, so a project copying this template inherited an example without the reasoning behind it.

Tests are the worst place in a codebase to leave unspecified, because they are written under time pressure, reviewed more loosely than the code they cover, and are where an agent improvises most freely. In a layered client the improvisation is usually `vi.mock` aimed at a module, which passes green while voiding the substitutability the layering was built to provide.

The layer rule already carried a test-specific clause, since a slice may be entered past its `index.ts` from a test. So the template was already constraining tests, but incidentally and in one place, rather than deliberately.

A wording defect sat on top of that. AGENTS.md listed "test breadth" as an intentional gap, in a sentence copied to all three styles. Here it is accurate. In the two Python styles it was not, because those had no suites at all, and the phrasing was written where it was true and copied where it was not.

## Options considered

- **Leave tests unspecified and let the example speak.** Rejected: an example without a stated rule is copied without its reasoning, and the first pressure to cut a corner has nothing to push back with.
- **Specify tests fully, including a coverage threshold and a naming schema.** Rejected: a percentage gate buys assertions that assert nothing, and a naming schema buys review nitpicks.
- **State the rule this template already follows, and leave the volume free.** Accepted.

## Decision

Three rules bind. Suites live in `tests/`, mirroring the source tree, one suite named after the unit it covers. A collaborator is replaced only at an architectural seam, by the MSW handlers answering at the wire boundary or a hand-written fake satisfying the contract it stands in for, and never by mocking a module's internals. No coverage threshold is imposed.

Test files stand outside the every-export documentation rule, since a suite documents itself through the name of each case and the assertion it makes. That belongs in the frozen rulebook, because it is a code-level documentation question, and it is the only part of this decision recorded there.

The existing suites already satisfy all three rules, and a check confirmed there is no `vi.mock` anywhere in this template or in any project derived from it. So this record describes practice rather than requiring a migration, which is the strongest form such a rule can take.

## Consequences

The rule and its example now travel together, so a project copying this template inherits both. The reasoning is available when someone is tempted to reach for a module mock, which is the moment the rule exists for.

Because the wording of the intentional-gaps sentence was accurate here and inaccurate elsewhere, it is now conditional in all three styles, with the per-project truth living in the repository baseline where a project is allowed to state facts. That follows the same principle as [decision 0010](0010-word-the-rulebook-so-copies-stay-true.md), extended from the frozen rulebook to the agent guide.

The cost is that a fake is more work than a module mock. That is the intended trade, since a fake satisfying a contract stops compiling when the contract changes, where a mock would silently keep passing.
