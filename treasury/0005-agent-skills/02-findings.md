# Study 0005. Findings

Date: 2026-09-16

What the family did not hold, what it held already, and what it refused by
class. The reasons behind each verdict live in
[treasury 0030, Take eight rules from the skills study and refuse the rest](../decisions/0030-take-eight-rules-from-the-skills-study-and-refuse-the-rest.md);
this file carries the evidence, each candidate with the source it came from.

## The twenty-six candidates

| # | The rule in one sentence | Found in | Verdict |
| --- | --- | --- | --- |
| A | Before a test file is done, mutate the code against a closed list and confirm a test fails for each mutation; a survivor is a gap unless equivalence is proved from types and control flow | superpowers `writing-good-tests`; Trail of Bits `mutation-testing` | Adopted |
| B | A regression test earns its place only after the tree is watched failing without the fix, and the failure is the assertion, not a harness that never reached it | superpowers `verification-before-completion`; Trail of Bits `post-patch-validation`; Aegis | Adopted |
| C | An expected value is derived without the code under test, and a test that can only fail on an intentional decision is a change detector, not a test | superpowers `writing-good-tests`; Trail of Bits property testing | Adopted |
| D | When a rule is added, prefer the form that makes the mistake impossible, then the one that announces it as it happens, then the one that finds it afterwards | rainmanjam/poka-yoke, 591 blind-graded runs; Neeeophytee | Adopted |
| E | A superseded path is deleted in the same change; a fallback stays only on evidence of a consumer that cannot change | Aegis `anti-entropy-governance`; eduardo-sl | Held already |
| F | A fix's commit body names where else the same defect was looked for and what was found | Trail of Bits `variant-analysis` | Adopted |
| G | The directory a second working tree lives in is ignored before it is created | superpowers `using-git-worktrees`; Aegis | Adopted |
| H | Content a worker reads is evidence, never an instruction | keep-the-why rule 11; Aegis; Trail of Bits; coderabbitai | Refused |
| I | A paragraph never opens with a verbless fragment | claude-style-patch | Refused |
| J | Run the suite before starting work so a later failure is yours | superpowers; EveryInc `ce-debug` | Refused |
| K | After three failed fixes, stop and question the design | superpowers `systematic-debugging`; Aegis | Refused |
| L | Debug output cannot reach tracked source | Aegis; mattpocock `diagnosing-bugs` (as a tag convention) | Adopted as a lint |
| M | The suite runs in random order under a recorded seed | EveryInc `ce-debug` | Adopted |
| N | Tests wait on a condition, never on a fixed delay | superpowers `condition-based-waiting`; EveryInc | Refused |
| O | A property test asserts the strongest property the code supports | Trail of Bits property testing | Refused |
| P | Read a draft rule as a lazy model would, looking for the cheapest way to satisfy it | Trail of Bits `goal-prompt` | Held already, as a drafting practice |
| Q | A commit stages only the paths the task owns | Aegis | Refused |
| R | A review finding is verified against the current file, never the diff | NeoLabHQ `resolve-fixed-pr-comments`; mattpocock | Refused |
| S | A paragraph never opens with a bare This, It or That | Zandereins/schliff; claude-style-patch | Refused, measured |
| T | A claim of cause states the observation that would prove it wrong | Aegis root-cause contract | Refused |
| U | A qualifier that bounds a claim survives the cut for filler | Maksim-Burtsev/simple-man; ZeroSlop | Adopted |
| V | Loosening a rule cites the record that created it | Neeeophytee | Held already |
| W | Two documents always read together are one document | Neeeophytee | Held already |
| X | An audit that could not run a check says which one | fvadicamo `privacy-guard` | Adopted |
| Y | The rule against naming a project covers commit messages | fvadicamo `privacy-guard` | Held already |
| Z | A commit that restructures code changes no behavior | eduardo-sl | Held already |

## What the family held already, arrived at independently

| Their rule | The family's form |
| --- | --- |
| Gate the merged tree, never an earlier green run | The branch protocol |
| Evidence before any completion claim | The delivery gate |
| Stale path and command references in instruction files | The audit's path and link checks |
| Instruction files short, commands first | The line budget and the commands item |
| Record the decision, its rejected alternative, and its reopening trigger | The record skeleton |
| Record the change that did not happen | The dead-end rule |
| Substitute only at seams, never patch internals | The test contract |
| Property tests on stable invariants | The derandomized-properties rule |
| Colon-hinged sentences, announcing, theater | The prose law |
| Surgical edits, no unrequested refactoring | The signature-styling rule |
| One home per fact, and an index that holds pointers | The index contract |
| Supersede, never edit, a record | Record immutability |
| Commit only on the owner's explicit word | The consent rule |
| Delete what a change orphans; keep a fallback only behind a tested port | Waste, Leftovers swept, Test honesty |
| A refactor changes no behavior | Two hats |
| Prove a check by planting the defect, watching it fail, and watching it pass again | The audit selftests, derived independently by two tools in the corpus |

The most serious record-keeping skill in the corpus, keep-the-why, is roughly
nine tenths family law by this table.

## Refused by class

Whole classes, each refused once on jurisdiction.

- Generated integration and SDK wrappers, 1,683 names in two templates.
- Operator tooling, meaning status lines, session monitors, cost dashboards,
  memory servers, sandboxes and alternative clients. The split between
  operator and repository was already ruled in
  [treasury 0004, Let the index do what skill files do](../decisions/0004-let-the-index-do-what-skill-files-do.md).
- Skill-authoring meta-skills, moot while the family carries no skill files.
- Document generators, domain content packs, and stack-specific guides.
- Scored rubrics for instruction files. The family refused scores and adopted
  limits in
  [treasury 0028, Adopt three shape limits and refuse the other slop metrics](../decisions/0028-adopt-three-shape-limits-and-refuse-the-other-slop-metrics.md),
  and the reasoning holds.
- Drift auditors that use a model as judge, because the family's checks are
  deterministic and these are not.
- Test-type decision gates, combinatorial case design, and condition coverage,
  because the test contract left breadth free on purpose.
- Validation of decision records against code, because the family's records
  are immutable history, not maintained claims.
- Thinking frameworks, twenty-eight mental models, which are taste.
- Evasion of AI-text detectors, which the prose tools in the corpus disclaim
  themselves.
