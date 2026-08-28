# Quiver Agent Guide

Quiver is a strict, AI-ready template for research-backed projects, demonstrated on a small rounding-drift inquiry. It is a host rather than a fourth peer of the artifact styles. The inquiry layer at the root asks a question and keeps the claims, and complete instances of the artifact styles live whole under `arrows/`, each governed by its own law. It is a style template and living blueprint rather than a finished research project, so some gaps are intentional and must not be "fixed" unprompted. Here that is the demo arrow, which is deliberately incomplete in the ways its own README names. The permanent gaps are the ones named here; anything temporary appears in STATE.md.

## Commands

- Audit the inquiry: `python scripts/audit_inquiry.py` (the living documents, the claim ledger, the citations, and the pins against the tree, the calendar, and git history)
- Prove the audit itself: `python scripts/audit_inquiry.py --selftest` (every rule against a planted defect, because a check that never fires and a check that cannot fire look identical)
- Work on an arrow: use that arrow's own commands, stated in its README; for the demo arrow, `cd arrows/coinwise` then `pip install -e .` with `pip install --group dev`, and its gate commands are `pytest`, `ruff check . && lint-imports`, `mypy src tests`, and `python scripts/audit_docs.py`

The audit reports at two levels. A failure is a verdict, it stops the command, and it means a rule the tool fully decides has been broken. A warning is advice, it leaves the exit status clean, and it comes from a check that cannot decide its own question and so is not allowed to gate. Advice is not noise and not optional reading. Every warning is looked at and then either fixed or dismissed in writing, in the change that produced it, and a warning is never silenced with a suppression to make a run look clean. The advisory check here is the stale-pin scan, which flags every claim still standing as current, its status neither Stale nor Superseded, whose arrow has moved past its pin in the paths that can change a result, the code, the tests, and the project file. Documentation carried inside an arrow executes nothing during a run, so its movement never advises, and only a person can tell whether a flagged movement touched what the claim measured.

## Hard rules

- The jurisdiction split is absolute: everything under `arrows/<name>/` is governed by that arrow's own style, gate, and conventions, and Quiver's law binds the inquiry layer only. Never write into an arrow to satisfy a Quiver rule, and never waive an arrow's own gate because the change came from the inquiry.
- A claim is the only place the inquiry holds a truth. Its evidence quotes results in full and pins the host commit that produced them, per the claim rules in [docs/CONVENTIONS.md](docs/CONVENTIONS.md); an assertion outside a claim record is a working note, not knowledge.
- Follow the documentation rules in [docs/CONVENTIONS.md](docs/CONVENTIONS.md); the rulebook is frozen and must not be edited.
- The documentation rulebook is owned by the style. [docs/CONVENTIONS.md](docs/CONVENTIONS.md) changes only inside the template itself, in the My-Styles repository and by its owner; a project derived from this template never edits its copy and never diverges from it. A derived project that believes a rule is wrong or missing sends the case upstream instead (see [The upstream report](#the-upstream-report)).
- An em dash is legal where it clearly beats the comma, the parenthesis, or the period it replaces, and it counts as its paragraph's one flourish. A tracked file carries at most two; CI counts that boundary, while the judgment of fit and commit messages stay with review.
- Commit history speaks in the owner's voice alone: no attribution trailers, no Co-Authored-By lines, nothing naming a tool or an assistant in a commit message. Held in review, like every commit-message rule.
- A check may never imply more than it decides. A green run is a claim, so a check is named for the question it actually settles, and a check that cannot settle its question advises rather than gates. Whatever it leaves undecided is stated beside the rule as review's work, never left to look automated, because the half no tool reaches is the half that rots and it rots faster behind a passing signal. This is why the family carries no coverage threshold, no maturity score, and no metric standing in for a rule it cannot decide.
- A check that makes a worker damage the work is worse than no check. When a rule fights something real, neither bend the work to earn a green run nor rewrite the rule. Pause the work in a state it can resume from, report the conflict, propose the change, and wait for the owner's explicit approval, because a rule change slipped into a busy diff is a decision nobody made. A length rule cuts filler and never information, a repair is verified for its side effects rather than for its intent, and a warning is answered rather than avoided, since an advisory a worker silences has become a gate.
- A completeness claim names its boundary. Saying that every caller was updated or every usage fixed is a fact only when it names the enumerable list it exhausted, a grep, a file list, a suite run, that a reader can re-derive. A claim over a region the claimant drew itself, such as every edge case considered, is offered as judgment rather than fact, because no boundary exists for it to have reached and the claim reports only that the claimant stopped finding things. Review probes the second kind, and trusts the first only as far as its boundary reaches.
- A rule binds only where its own text claims to bind. A length budget governs the document whose budget it is, the prose law governs a tracked byte, and a stage's cap governs that stage; outside that reach a rule does not apply at all. So nothing is spent applying a convention to material it never named, such as trimming or restyling an untracked working file that will never ship, and a count taken of such material is a measurement rather than a finding to fix.
- All prose must read as if a person wrote it. Never write the clause-colon splice, a sentence shaped as claim, colon, elaboration; in prose a colon may only introduce a list, a quote, or a label. The softer language-model tells (balanced semicolon antitheses, triadic lists, not-X-but-Y reversals) are fine one at a time and forbidden stacked, so allow at most one flourish per paragraph and keep the rest plain declarative sentences. No tool can judge these, so they are held in review, agent and human alike. The full catalog of tells, the vocabulary, and the portability test live in the rulebook's Prose section ([docs/CONVENTIONS.md](docs/CONVENTIONS.md#prose)).
- Every tracked byte is public prose. Confidential facts, private repository names, deployment details, and the description of what was withheld and why never enter a tracked file or a commit message, even in a private repository, because visibility can flip and history is permanent. Such context goes to the untracked `LOCAL.md` at the root (see [docs/BASELINE.md](docs/BASELINE.md)); read it when it exists, create it when first needed, and when unsure whether a fact is sensitive, ask the owner instead of recording it.
- Read [STATE.md](STATE.md) before starting work, and sweep it before starting anything new, deleting every entry that describes finished work and re-verifying or deleting any entry the tree no longer confirms. Its entries are claims to verify, not facts. Completing work deletes its entry in the same change, never adds a narration of the landing, and every change ends with a sweep for entries it completed or invalidated.

## The delivery gate

A task is not delivered while the gate below has findings. Carry these items from the first line written, because they are cheapest to satisfy while the work is still forming and most expensive as after-the-fact repairs; the closing pass exists to confirm, not to redo.

Closing a task follows one loop: run the checking commands above, weigh the change against every item below, fix what an item names, and repeat. One pass with no findings ends the loop. A finding is a concrete disagreement with a listed item, never general unease; the list is closed, and nothing outside it may generate rework. If the same finding survives three honest fix attempts, stop looping, record the finding and the attempts in STATE.md, and say so plainly when delivering.

- **Claim honesty**: every claim states its assertion plainly and names who it must convince, or names itself Conjecture; nothing ships as fact with an empty Evidence section.
- **Evidence honesty**: results are quoted in the record in full, with how they were produced, never pointed at, so the record stays accurate after the tree moves on.
- **Pin honesty**: evidence names the pinned commit of every arrow involved, and a claim whose arrow's evidence paths moved is flipped Stale or superseded, never left implying it is current.
- **Boundary honesty**: any completeness assertion, a literature search, a parameter sweep, an ablation, names the enumerable boundary it exhausted, or is offered as judgment.
- **Threat naming**: every claim names the threats most endangering it, from the field's own vocabulary; naming is free, and no method, design, or standard is ever mandated, because those are priced.
- **Graveyard honesty**: a dead end that cost real effort or could plausibly be retried gets its Refuted record with killing evidence and reopening condition, in the same change that abandons it.
- **Rigor honesty**: any stage of the spine that was skipped is skipped in writing.
- **Jurisdiction**: a change inside an arrow passes that arrow's own style gate; this gate claims only the inquiry layer.
- **The commands**: the audit has passed against the final state of the tree, and every advisory finding printed along the way has been read and then fixed or dismissed in writing.
- **State discipline**: STATE.md swept at both ends of the change; execution tracking lives there and never in a record.
- **Records discipline**: decisions and claims immutable, status-line edits only, dated, self-contained, and every citation key resolving.
- **The institution boundary**: the inquiry layer records the work between meetings and stops where an advisor, committee, or reviewer's jurisdiction starts; it never simulates their approval.

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
| [README.md](README.md) | Human-facing overview: philosophy, structure, setup, and the conventions. |
| [STATE.md](STATE.md) | Living project state (Now / Next / Deferred / Blocked). Read first, always. |
| [docs/QUESTION.md](docs/QUESTION.md) | The root question, why it is worth asking, and its open conjectures. Read before touching any claim or arrow. |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | The map of the inquiry: arrows, and how evidence flows into claims. Read before any structural change. |
| [docs/BIBLIOGRAPHY.md](docs/BIBLIOGRAPHY.md) | Every work consulted, as self-contained citations addressed by key. |
| [docs/CONVENTIONS.md](docs/CONVENTIONS.md) | The documentation rulebook: species, schemas, claims, pins, naming. Frozen; do not edit. Read before writing or changing any documentation. |
| [docs/BASELINE.md](docs/BASELINE.md) | The repository baseline: always-present files, never-tracked files, and their modification rules. |
| [docs/decisions/](docs/decisions/) | Immutable decision records holding the project's "why". Read the relevant record before revisiting a settled topic; never edit an accepted record. |
| [docs/claims/](docs/claims/) | Immutable claim records holding what the inquiry holds true, on what evidence, at which pin. |
| [docs/arrows/](docs/arrows/) | One living manifest per arrow: its style, the part of the question it serves, and the claims resting on it. |
| [arrows/coinwise/README.md](arrows/coinwise/README.md) | The demo arrow: what it measures, its commands, and its named incompleteness. |

There are no assistant-specific instruction files. Every assistant reads this file directly. If a tool genuinely cannot read AGENTS.md, give it a one-line shim that imports or points to this file and nothing more.
