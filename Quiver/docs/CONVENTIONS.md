# Documentation Conventions

This file is the rulebook for this project's technical documentation: which documents exist, what species each one is, how each species is written, and where a "why" belongs. It is normative and frozen: **do not modify this file**. If a rule ever has to change, the change is made deliberately, by the style's owner, inside the template itself in the My-Styles repository, and recorded as a new decision record superseding [0001](decisions/0001-adopt-the-documentation-system-and-extend-it-for-inquiry.md). A project derived from this template never edits its copy and never diverges from it; a case for changing a rule travels upstream through the report described in AGENTS.md.

## The two species of documents

Every technical document is exactly one of two species, and the species dictates all of its rules.

**Living documents** describe the present. They are edited in place, always current, and bounded in size. A living document never contains history: no dates, no "previously", no narration of change. When reality moves, the text is rewritten and the old text disappears; git remembers what it used to say.

**Records** describe one past event. A record is written once, dated, and never edited again, apart from its one legal status edit. When reality moves past a record, a new record supersedes it. This project keeps two kinds of record: decisions, which hold choices, and claims, which hold assertions about the world and the evidence behind them.

Nearly every documentation failure is a species violation. Never mix the two species in one file.

## The spine and the organic zone

| Document | Species | Role |
| --- | --- | --- |
| `AGENTS.md` | Living | Vendor-neutral agent entry point: the operating manual and the single documentation index. |
| `STATE.md` | Living | Current project state: what is in flight, queued, deferred, or blocked. |
| `docs/QUESTION.md` | Living | The root research question, why it is worth asking, and its current decomposition into open conjectures. |
| `docs/ARCHITECTURE.md` | Living | The map of the inquiry as it is today: the arrows and how evidence flows from them into claims. |
| `docs/BIBLIOGRAPHY.md` | Living | Every work the inquiry consulted, as self-contained citations addressed by key. |
| `docs/CONVENTIONS.md` | Living, frozen | This rulebook. |
| `docs/BASELINE.md` | Living | The repository baseline: always-present files, never-tracked files, and their modification rules. |
| `docs/decisions/` | Records | The decision log; the durable home of rationale. |
| `docs/claims/` | Records | The claim ledger; the durable home of what the inquiry holds true, on what evidence. |
| `docs/arrows/` | Living | One manifest per arrow: the style it follows, the part of the question it serves, and the claims resting on it. |

Assistant-specific instruction files do not exist here; every assistant reads `AGENTS.md`. Beyond the spine, documentation grows organically. Further documents are added under `docs/` (UPPERCASE markdown, one subject per file, one species per file) and registered in the index. Growth changes the number of documents, never the species rules of an existing one.

## The index contract

`AGENTS.md` holds the single index of all technical documents. A document not listed there does not exist. Creating a document and registering it happen in the same change, as does delisting on removal.

## Rules for living documents

- Present tense only; describe what is, never what was or how it got here.
- No dates and no changelog narration (`STATE.md` entries are the one exception; each carries an absolute date, its last-verified stamp, and an entry older than 90 days is expired until re-verified).
- Record intent and decisions, never inventory the tree can answer.
- A sentence in a living document is a claim, not a fact. Verify a claim before relying on it, and end every change by sweeping `STATE.md`.
- Rewrite in place; never append-and-preserve.
- `AGENTS.md`, `docs/ARCHITECTURE.md`, and `docs/BIBLIOGRAPHY.md` grow with the inquiry rather than against a number, saying everything as briefly as it can be said. Every other living document is bounded at 150 lines, the audit fails one that exceeds its bound, and the remedy is fission by subject. `README.md` stands outside both classes, governed by the README schema in BASELINE.md.
- The mechanical half of freshness is checked by `scripts/audit_inquiry.py`: paths named exist, relative links resolve, no `STATE.md` entry outlives its horizon, no bounded document exceeds its budget, every document under `docs/` is registered, names and schemas hold. Records are exempt from every rule in this section; they describe the past, which does not rot.

### The STATE.md schema

`STATE.md` has exactly four sections: `Now` (in flight), `Next` (queued), `Deferred`, and `Blocked`. An entry earns `Now` only while its work is genuinely unfinished. Completing work deletes its entry in the same change. Every entry is one line ending with its date (YYYY-MM-DD), and the audit caps `Now` at five entries. The file is swept at both ends of every change. Execution tracking lives here and never in a record.

## Rules for decision records

Write a decision record when a choice shapes future work and its reasoning would otherwise be lost. Records live in `docs/decisions/`, named `NNNN-short-kebab-title.md`, and follow the family template: Status and Date lines, then Context, an optional Evidence section where the decision rests on something measured or run, Options considered where they existed, Decision, and Consequences. An accepted record is immutable; when a decision changes, a new record supersedes it, and flipping the old `Status:` line is the only edit it may receive. A dead end that cost real effort or could plausibly be retried gets its record when the evidence arrives, naming what killed it and what would reopen it.

## Rules for claim records

A claim is the inquiry's unit of knowledge: one assertion, its evidence, and the exact state of the world that produced it. Claims live in `docs/claims/`, named `NNNN-short-kebab-title.md` in their own sequence, titled by the assertion, and follow this template:

- `Status:` one of `Conjecture`, `Supported`, `Refuted`, `Stale`, or `Superseded by NNNN`, then `Date:`.
- **Claim.** The assertion in plain words, and who it must convince.
- **Evidence.** What ran, in which arrow at which pinned commit, and the results quoted in full, never pointed at; `None.` for a conjecture. A pin is written as `arrows/<name> at <commit-hash>` and names the host commit whose tree produced the results. Evidence gathered by reading rather than running quotes the source's numbers or words in full and cites its bibliography key, and it carries no pin, since no tree produced it.
- **Threats.** The named threats and biases most endangering this claim, each with what was done about it or the concession that nothing was.

A claim record is immutable and the `Status:` line is its only legal edit. The trigger for writing or flipping one is evidence arriving or a claim moving, never work completing. A refuted claim names the evidence that killed it, the condition that would reopen it, and the pin that held the attempt. `Stale` means an arrow moved past a claim's pin, so the claim is no longer backed rather than wrong; a person flips it, prompted by the audit's advisory, and the way back is a re-run at a new pin or a superseding claim. Any completeness assertion inside a claim names the enumerable boundary it exhausted or presents itself as judgment.

## Rules for the bibliography

Every work the inquiry consulted is entered, because a source treated as a frame instead of an object silently vanishes from the record. A citation is self-contained: author, year, title, venue, and the edition or dated version actually used, since held knowledge preserves superseded editions without noticing. A DOI or URL may ride as a locator, but the citation must survive its death. Prose cites keys of the form `[authorYYYY]`, the audit verifies every cited key resolves, and bare external links appear nowhere outside this file.

## The arrows and their jurisdiction

An arrow is a complete instance of an artifact style, vendored whole under `arrows/<name>/`. Everything inside that tree is governed by the arrow's own style, its gate, and its conventions; this project's law binds the inquiry layer only and never writes into an arrow. Each arrow has one manifest at `docs/arrows/<name>.md`, and an arrow whose named incompleteness matters states it in its own README. Because arrows are vendored, the host history is the only history, which is what makes a pin one hash.

## Proportional rigor

The full spine of an inquiry is question, conjecture, evidence, claim. Any shortening is legal and costs one recorded line, in the claim or in QUESTION.md, saying what was skipped and why. Skipping silently is the only violation.

## Where a "why" belongs

A "why" that fits in a sentence and explains one change goes in the commit message body. A "why" that would be re-litigated goes in a decision record. A "what we hold true" goes in a claim. Chronology itself is never documented; git already is the complete log.

## Naming

Spine and organic documents use UPPERCASE basenames at predictable locations. Decision and claim records use `NNNN-short-kebab-title.md`, each sequence numbered independently, because they are many, ordered, and cited by number. Arrow manifests are lowercase, named exactly after the arrow directory they describe.

## Code inside arrows

This project's inquiry layer carries no code beyond `scripts/audit_inquiry.py`. Code lives in arrows, and each arrow's docstring, testing, and layout rules are its own style's, stated in that style's README and rulebook. An arrow is begun by transplanting the nearest exemplar files from its style and rewriting their words, never by writing fresh from a rule summary. A rulebook names what must exist; only the style's own bytes carry its dialect, so review of a new arrow reads it beside the exemplars it was cut from.
