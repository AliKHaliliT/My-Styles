# Keel Agent Guide

Keel is a strict, AI-ready Clean Architecture template for installable Python packages, demonstrated on a fully offline agent-engine domain. It is a style template and living blueprint rather than a production library, so some gaps are intentional and must not be "fixed" unprompted. Here those are the suites, which demonstrate the test shape rather than covering the surface, and the Gemini adapter, whose one live validation is recorded as a fixture the suite replays so the offline guarantee holds. The permanent gaps are the ones named here; anything temporary appears in STATE.md.

## Commands

- Install (editable): `pip install -e .` (Python 3.13+; add the tooling with `pip install --group dev`, and the LLM adapter with `pip install -e ".[gemini]"`; if an import fails after the tree moves, check where the editable install points with `pip list` before debugging code)
- Run the offline demo: `keel "calculate (2 + 3) * 4"` or `python -m keel "count words in the quick brown fox" --show-trace`
- Test: `pytest`
- Lint: `ruff check . && lint-imports` (ruff checks style and docstring presence; import-linter checks the Dependency Rule)
- Type-check: `mypy src tests` (strict mode is configured in `pyproject.toml`)
- Docs: `python scripts/audit_docs.py` (the living documents against the tree and the calendar)

## Hard rules

- The Dependency Rule is absolute: `domain` and `services` never import from `facade`, `adapters`, or any SDK; layer-owned objects cross a layer boundary only through translators, a clause no import graph can see, so it is carried in review by the agent writing a change and the human reading it alike.
- Library citizenship: no global mutable state, no environment reads at import time, and a `NullHandler` on the package logger.
- Every directory holds either subpackages or modules, never a mix (the package root is the sole exception); an `__init__.py` exists only where it re-exports.
- Test suites live in `tests/`, mirroring the source tree, one suite named after the unit it covers. A collaborator is replaced only at an architectural seam, by a hand-written fake satisfying the port in `domain/interfaces` that it stands in for; never patch or monkey-patch a module's internals, because a test bound to an implementation voids the substitutability the ports exist to provide. No coverage threshold is imposed, so breadth stays a judgment call while the placement and substitution rules do not. The shape is mapped in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md#testing).
- Follow the docstring convention in the [README's Conventions section](README.md#conventions) and the documentation rules in [docs/CONVENTIONS.md](docs/CONVENTIONS.md); the latter is frozen and must not be edited.
- The documentation rulebook is owned by the style. [docs/CONVENTIONS.md](docs/CONVENTIONS.md) changes only inside the template itself, in the My-Styles repository and by its owner; a project derived from this template never edits its copy and never diverges from it. A derived project that believes a rule is wrong or missing sends the case upstream instead (see [The upstream report](#the-upstream-report)).
- No em dashes anywhere: code, docstrings, comments, documentation, commit messages. CI greps every tracked byte for the character; commit messages stay with review.
- Commit history speaks in the owner's voice alone: no attribution trailers, no Co-Authored-By lines, nothing naming a tool or an assistant in a commit message. Held in review, like every commit-message rule.
- All prose must read as if a person wrote it. Never write the clause-colon splice, a sentence shaped as claim, colon, elaboration; in prose a colon may only introduce a list, a quote, or a label. The softer language-model tells (balanced semicolon antitheses, triadic lists, not-X-but-Y reversals) are fine one at a time and forbidden stacked, so allow at most one flourish per paragraph and keep the rest plain declarative sentences. No tool can judge these, so they are held in review, agent and human alike.
- Every tracked byte is public prose. Confidential facts, private repository names, deployment details, and the description of what was withheld and why never enter a tracked file or a commit message, even in a private repository, because visibility can flip and history is permanent. Such context goes to the untracked `LOCAL.md` at the root (see [docs/BASELINE.md](docs/BASELINE.md)); read it when it exists, create it when first needed, and when unsure whether a fact is sensitive, ask the owner instead of recording it.
- Read [STATE.md](STATE.md) before starting work, and sweep it before starting anything new, deleting every entry that describes finished work and re-verifying or deleting any entry the tree no longer confirms. Its entries are claims to verify, not facts. Completing work deletes its entry in the same change, never adds a narration of the landing, and every change ends with a sweep for entries it completed or invalidated.

## The delivery gate

A task is not delivered while the gate below has findings. Carry these items from the first line written, because they are cheapest to satisfy while the code is still forming and most expensive as after-the-fact repairs; the closing pass exists to confirm, not to redo.

Closing a task follows one loop: run the checking commands above, weigh the change against every item below, fix what an item names, and repeat. One pass with no findings ends the loop. A finding is a concrete disagreement with a listed item, never general unease; the list is closed, and nothing outside it may generate rework. If the same finding survives three honest fix attempts, stop looping, record the finding and the attempts in STATE.md, and say so plainly when delivering. The names below index a wider literature; where a name's common usage and the rule beside it differ, the rule governs.

- **Cognitive load**: nothing in the change is harder to hold in mind than the task requires.
- **Granularity**: the size of every new unit (function, file, document, the change itself) is a choice, not an accident.
- **Ubiquitous language**: new names use the vocabulary the tree already speaks.
- **Single source of truth**: the change introduces no second copy of any fact, and anything derived points at its source.
- **Least privilege and surface**: nothing gains more access, exports, or dependencies than the task needs.
- **Boundary honesty**: no data crosses a boundary unchecked, and checking happens at the door, once.
- **Loud failure**: every new failure path raises a typed error; nothing is swallowed or silently defaulted.
- **Two hats**: shape changes and behavior changes are separate steps, and no incidental reformatting rides along.
- **Waste**: nothing speculative and nothing the change orphaned is left behind.
- **Test honesty**: substitutes stand in only at the declared seams, and time, randomness, and order are controlled.
- **Point-of-use truth**: the doc comment or docstring each export carries is true, not merely present.
- **Intent-split placement**: every documentation change lands in the document whose reader it serves, per the rulebook's species.
- **Decision records**: any choice made here that would be re-litigated without a record gets one now.
- **Debt**: every shortcut taken is written in STATE.md before delivery, never carried in memory.
- **The commands**: every checking command above has passed against the final state of the tree.
- **The hard rules**: the change disagrees with no review-held clause of this guide's Hard rules, re-read now, not recalled.

## The upstream report

This template is the style's single statement of its form, and it only stays that way if improvements flow back to it. When a refactor against this template surfaces something the template itself should have had, the improvement belongs in the template first and in the refactored project second; an improvement kept privately by one child is a quiet fork of the style.

The order is strict:

1. **Finish the refactor as specified.** The report comes after the template has been properly implemented, never instead of finishing.
2. **Qualify every candidate.** An improvement earns an entry only if it is genuinely better rather than differently shaped, the template does not already have it, and [docs/decisions/](docs/decisions/) shows no record of it being considered and rejected. Read the decision records before writing anything; a rejected idea returning without new evidence is noise, and a report invented to satisfy this section when nothing real was found is worse than no report.
3. **Write each entry as a hand-off.** One entry per improvement, self-contained enough to be pasted verbatim to an agent or handed to the template's maintainer and acted on with no other context. Each entry states what the improvement is, how the refactor surfaced it, why it is believed better than what the template does today, and that the decision records were checked and hold no prior ruling. Each entry ends by telling the receiver to verify the claim with proper research-backed grounding before adopting it, because the report is a lead, not a verdict.
4. **Apply upstream first, then align.** The improvement lands in the template before the child keeps it. Integrating it there often refines it further, so afterwards run a manual final alignment check on the refactored project, confirming it carries the upstream form of each improvement rather than the draft it started from.

Every report opens by saying why the reader is seeing it. The style's owner uses the report to point an agent at the template and improve it directly. Anyone else is holding it because this template is open source, and the right move is to file the report as an issue on the template's repository so the improvement reaches everyone who builds on the style.

## Documentation index

This is the single index of the project's technical documentation. A document that is not listed here does not exist as far as this project is concerned: when you create a document, register it here in the same change; when you remove one, delist it here.

| Document | What it is and when to read it |
| --- | --- |
| [README.md](README.md) | Human-facing overview: philosophy, structure, setup, and the docstring convention. |
| [STATE.md](STATE.md) | Living project state (Now / Next / Deferred / Blocked). Read first, always. |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | The annotated map of the whole template. Read before any structural change. |
| [docs/CONVENTIONS.md](docs/CONVENTIONS.md) | The documentation rulebook: document species, schemas, naming. Frozen; do not edit. Read before writing or changing any documentation. |
| [docs/BASELINE.md](docs/BASELINE.md) | The repository baseline: always-present files, never-tracked files, and their modification rules. Read before adding, removing, or reshaping root-level or dot files. |
| [docs/decisions/](docs/decisions/) | Immutable decision records holding the project's "why". Read the relevant record before revisiting a settled topic; never edit an accepted record. |

There are no assistant-specific instruction files: every assistant reads this file directly. If a tool genuinely cannot read AGENTS.md, give it a one-line shim that imports or points to this file and nothing more.
