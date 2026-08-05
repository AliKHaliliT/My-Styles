# 0008. Specify the test contract and leave its breadth free

Status: Accepted
Date: 2026-08-05

## Context

This template specifies where every production file goes and why. Tests were the one part of it with no rule at all. The frozen rulebook and the repository baseline mentioned tests zero times, AGENTS.md said only that test breadth was an intentional gap, and the architecture map named the folders without saying what belonged in them.

That is the worst place in a codebase to leave unspecified, because a test is written under time pressure, reviewed more loosely than the code it covers, and is where an agent improvises most freely. An improvised suite in a layered architecture tends to reach for patching, and a patched internal passes green while quietly voiding the substitutability the layering was built to provide.

The template also asserted a shape it never demonstrated. `tests/app/` held a single `.gitkeep`, so the folder claimed a convention with no example of it, while the sibling client template backed the same claim with real suites. Every other convention here is taught by a worked example in the demo domain, and this was the sole exception.

A wording defect sat on top of that. AGENTS.md called the gap "test breadth", which describes a thin suite, when in fact there was none. An agent reading it would conclude there was existing work to match and go looking for a house style that did not exist.

## Options considered

- **Leave tests unspecified and let each project decide.** Rejected: the styles exist so a project never has to invent structure, and tests are structure. Leaving the most improvisation-prone part free contradicts the whole premise.
- **Specify tests fully, including a coverage threshold and a naming schema.** Rejected: a percentage gate buys assertions that assert nothing, and a naming schema buys review nitpicks. Both cost more in resentment than they return in quality.
- **Specify the frame and leave the volume free.** Accepted.

## Decision

Three rules bind. Suites live in `tests/`, mirroring the source tree, one suite named after the unit it covers. A collaborator is replaced only at an architectural seam, by a hand-written fake satisfying the interface in `app/domain/interfaces` that it stands in for, and never by patching a module's internals. No coverage threshold is imposed.

The substitution rule is the one that matters most here, because this architecture's entire payoff is that a collaborator can be swapped. A test that patches an internal keeps passing while destroying that property, and no linter will ever report it.

Test files stand outside the every-export documentation rule, since a suite documents itself through the name of each case and the assertion it makes. That belongs in the frozen rulebook, because it is a code-level documentation question, and it is the only part of this decision recorded there.

The rule ships with a worked example rather than as prose alone. `tests/app/services/test_user_service.py` drives the real orchestration of `UserService.create_user_with_device` against fakes for the unit of work, its repositories, and the VPN provider. Writing it was worth more than the rule it demonstrates, because it immediately surfaced a deprecated pydantic config class that had been emitting a warning unnoticed.

The gap sentence in AGENTS.md now states what is true, which is that the suites are a demonstration of the shape rather than a thin version of a real one.

## Consequences

A suite added here has a shape to match and an example to read, and the type checker now covers the tests as well as the application, so a fake that does not really satisfy its interface is reported rather than assumed.

The cost is that a fake is more work than a patch. That is the intended trade, since the work is what proves the interface is honest, and a fake declared against the interface fails to compile when the interface changes, where a patch would silently keep passing.

Breadth remains deliberately narrow. This repository is a blueprint rather than a deployment, so the suite demonstrates the form rather than covering the surface, and that stays a stated gap instead of a hidden one.
