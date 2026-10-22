# Documentation Conventions

This file is the rulebook for this project's technical documentation: which documents exist, what species each one is, how each species is written, and where a "why" belongs. It is normative and frozen; do not modify this file. If a rule ever has to change, the change is made deliberately, by the style's owner, inside the template itself in the My-Styles repository, and recorded as a new decision record superseding the style's record 0001. A project derived from this template never edits its copy and never diverges from it; a case for changing a rule travels upstream through the report described in AGENTS.md.

The rulebook is read as seven documents: this core, the rules for living documents in [LIVING.md](LIVING.md), the rules for records in [RECORDS.md](RECORDS.md), the rules for review records and screening logs in [REVIEWS.md](REVIEWS.md), the rules for the bibliography in [SOURCES.md](SOURCES.md), the prose law in [PROSE.md](PROSE.md), and the method of a pass in [METHOD.md](METHOD.md) and [FOLD.md](FOLD.md); each is frozen as this file is.

## The two species of documents

Every technical document is exactly one of two species, and the species dictates all of its rules.

**Living documents** describe the present. They are edited in place, always current, and bounded in size. A living document never contains history: no dates, no "previously", no narration of change. When reality moves, the text is rewritten and the old text disappears; git remembers what it used to say.

**Records** describe one past event. A record is written once, dated, and never edited again, apart from its Status line and the repair of a link target that no longer resolves, which moves where a citation points and changes nothing a reader sees. When reality moves past a record, a new record supersedes it. This project keeps three kinds of record: decisions, which hold choices, claims, which hold assertions about the world and the evidence behind them, and review passes, which hold what was read, within what boundary, and what it changed. Any other dated document under `docs/`, a briefing or a progress report, is a record too for the purpose of immutability, though only decisions, claims, and review passes have a shape the audit holds. In a project built from this template, the template's own decision records are carried whole in an `inherited/` folder under `docs/`, byte-identical to the template's at the alignment pin and recopied as one folder at every re-alignment, so `docs/decisions/` holds the project's own decisions and nothing else, numbered from 0001 in every project alike; a record cites an inherited one by a relative link into the `inherited/` folder. A re-alignment is itself one of the project's decisions and gets one record, which cites every record the folder gained and says what each did to the tree, so the records stay the changelog for the child's law as well as the template's. The docs audit fails a record in `docs/decisions/` whose body, beyond its heading and its status line, is an inherited record's, because a template record kept under the project's number is the one copy the split forbids, and the remedy is deletion, since the inherited folder carries the record and history keeps the copy.

Nearly every documentation failure is a species violation. Never mix the two species in one file.

## The spine and the organic zone

| Document | Species | Role |
| --- | --- | --- |
| `AGENTS.md` | Living | Vendor-neutral agent entry point: the commands and the single documentation index. |
| `docs/RULES.md` | Living, frozen | The hard rules of the tree, read whole before any work. |
| `docs/CONDUCT.md` | Living, frozen | The hard rules of conduct, read whole before any work. |
| `docs/GATE.md` | Living, frozen | The delivery gate a change is weighed against before it is delivered. |
| `docs/PASSES.md` | Living, frozen | Running a review pass and adopting an inquiry that has drafts. |
| `docs/ADOPTION.md` | Living, frozen | How a repository adopts this style and how a child re-aligns. |
| `docs/REPORTING.md` | Living, frozen | The upstream report, what a project sends its template and how an entry is resolved. |
| `STATE.md` | Living | Current project state: what is in flight, queued, deferred, or blocked. |
| `docs/QUESTIONS.md` | Living | The aim of the inquiry and its numbered questions, each with its decomposition into the conjectures and claims that serve it. |
| `docs/ARCHITECTURE.md` | Living | The map of the inquiry as it is today: the arrows and how evidence flows from them into claims. |
| `docs/INVARIANTS.md` | Living | The product's stated invariants, one row per claim, each bound to the holder that refuses a violation and graded by what its green is worth. |
| `docs/BIBLIOGRAPHY.md` | Living | Every work the inquiry consulted, as self-contained citations addressed by key. |
| `docs/CONVENTIONS.md` | Living, frozen | The rulebook's core; its parts follow. |
| `docs/LIVING.md` | Living, frozen | The rulebook's rules for living documents, the questions file and the invariants ledger. |
| `docs/RECORDS.md` | Living, frozen | The rulebook's rules for decision records and claim records. |
| `docs/REVIEWS.md` | Living, frozen | The rulebook's rules for review records and screening logs. |
| `docs/SOURCES.md` | Living, frozen | The rulebook's rules for the bibliography and the standing of a source. |
| `docs/PROSE.md` | Living, frozen | The prose law, the rulebook's rules for every tracked byte of prose. |
| `docs/METHOD.md` | Living, frozen | The method of a pass over the literature from the first seed to the screening, and the demo's field bindings, which a project rewrites at adoption and re-adapts at re-alignment while the rest is recopied like this rulebook. |
| `docs/FOLD.md` | Living, frozen | The method of a pass from its checks to its record and the forms a pass takes, recopied like this rulebook. |
| `docs/BASELINE.md` | Living | The repository baseline: always-present files, never-tracked files, and their modification rules. |
| `docs/decisions/` | Records | The decision log of this project's own choices; the durable home of rationale. |
| `docs/claims/` | Records | The claim ledger; the durable home of what the inquiry holds true, on what evidence. |

Assistant-specific instruction files do not exist here; every assistant reads `AGENTS.md`. Beyond the spine, documentation grows organically, and growth changes the number of documents, never the species rules of an existing one:

- Three folders join the spine with their first entry, a `reviews/` folder under `docs/` holding one record per pass over the literature, a `screening/` folder under `docs/` holding one log per reader of a pass that screened, and an `arrows/` folder under `docs/` holding one living manifest per arrow, each registered by its own row in the index when it appears, because a fresh inquiry has neither a pass nor an arrow yet, and a folder git cannot hold empty is not a folder a project can carry.
- Further documents are added under `docs/` (UPPERCASE markdown, one subject per file, one species per file) and registered in the index.
- The one exception in location is a directory whose purpose needs stating where a reader stands, which may carry its own `README.md` beside its contents, registered in the index like any other document.
- A subfolder under `docs/` is a record folder or `arrows/`, nothing else; living organic documents are flat UPPERCASE files at the top of `docs/`, because the naming and budget rules see only that shape.
- A record folder beyond `decisions/`, `claims/`, `reviews/`, `screening/`, and `inherited/` where a project carries one, holds dated documents named `YYYY-MM-DD-short-kebab-title.md`, ordered by date rather than by number, immutable like every record, and registered by its own row in the index.

## The index contract

`AGENTS.md` holds the single index of all technical documents. A document not listed there does not exist. Creating a document and registering it happen in the same change, as does delisting on removal.

## The arrows and their jurisdiction

An arrow is a complete instance of an artifact style, vendored whole under `arrows/<name>/`. Everything inside that tree is governed by the arrow's own style, its gate, and its conventions; this project's law binds the inquiry layer only and never writes into an arrow. Each arrow has one manifest at `docs/arrows/<name>.md`, naming the style, which fixes the paths the stale-pin scan watches, the question the arrow serves by number and what of it, the command that reproduces its figures, the current claims resting on it, and its verifications, one `NNNN at <commit-hash>` per claim whose figures reproduced after the arrow moved, the latest standing for each. An arrow is a full adaptation, carrying its style's entire documentation spine, baseline dotfiles, and inert workflow, so the law an agent needs is in place where jurisdiction binds it and a decision made inside the arrow has a record to land in; named incompleteness in an arrow's README covers domain trims only, never the spine. The LICENSE file alone stays at the host root, since a license answers a repository-level question, and an arrow extracted to stand alone gains its own then, following its style's baseline trigger. Because arrows are vendored, the host history is the only history, which is what makes a pin one hash. An arrow's `UPSTREAM.md` is the arrow's own, under its own `docs/`, because the divergence and the law it answers to are the arrow's and an arrow extracted to stand alone carries it along; the host's covers the inquiry layer alone.

## Proportional rigor

The full spine of an inquiry is aim, question, conjecture, evidence, claim. Any shortening is legal and costs one recorded line, in the claim or under the question in QUESTIONS.md, saying what was skipped and why. Skipping silently is the only violation.

## Where a "why" belongs

A "why" that fits in a sentence and explains one change goes in the commit message body, and when the change fixes a defect the body also names where else the same defect was looked for and what was found. A "why" that would be re-litigated goes in a decision record. A "what we hold true" goes in a claim. Chronology itself is never documented; git already is the complete log.

A reference in a living document carries its description. A record is cited by its number and its title, verbatim from its heading and in the same paragraph as the link, so the sentence stands without the click and cannot drift, because a record is immutable. A path or a symbol is cited with its role in the sentence, what the reference is for here, and never with its behavior, which is the file's own claim and moves when the file moves. A record cited where no link can stand, in a document or a configuration comment that travels into a project built from the style, names whose record it is, the style's or this project's own, beside its number and its title, because there the same number names an inherited record and one of the project's own; a form kept byte for byte, a serialized string compared as written, keeps its bytes and names the record in a comment on the same line. The docs audit holds the title and the owner; the role stays with review.

A document composed from the ledger, a chapter, a paper, a proposal or a report, is written afterward from the claims, the passes and the bibliography, and where one is kept in the tree it cites a claim by its number and title and a work by its key, so every sentence in it traces to the record behind it, and it holds no finding the ledger does not, because a finding that lives only in the chapter is a claim nobody recorded. The audit holds keys and record titles wherever it reads markdown; a document in another markup is review's.

## Naming

Spine and organic documents use UPPERCASE basenames at predictable locations. Decision and claim records use `NNNN-short-kebab-title.md`, each sequence numbered independently, because they are many, ordered, and cited by number. A record's filename stays within seventy-two characters, because the folders a record lives under are deep and a Windows clone has a path limit; the audit holds the cap for records written after it arrived. Arrow manifests are lowercase, named exactly after the arrow directory they describe. Other record folders name their files `YYYY-MM-DD-short-kebab-title.md`, since a briefing or a progress report is ordered by when it happened.

## Code inside arrows

This project's inquiry layer carries no code beyond `scripts/audit_inquiry.py`. Code lives in arrows, and each arrow's docstring, testing, and layout rules are its own style's, stated in that style's README and rulebook. An arrow is begun by transplanting the nearest exemplar files from its style and rewriting their words, never by writing fresh from a rule summary. A rulebook names what must exist; only the style's own bytes carry its dialect, so review of a new arrow reads it beside the exemplars it was cut from.
