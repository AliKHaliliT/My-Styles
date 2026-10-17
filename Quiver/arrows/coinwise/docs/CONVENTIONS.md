# Documentation Conventions

This file is the rulebook for this project's technical documentation: which documents exist, what species each one is, how each species is written, and where a "why" belongs. It is normative and frozen; do not modify this file. If a rule ever has to change, the change is made deliberately, by the style's owner, inside the template itself in the My-Styles repository, and recorded as a new decision record superseding the style's record 0001, which is also where the rationale behind this whole system lives. A project derived from this template never edits its copy of this file and never diverges from it, however much better a local rule looks from below; a case for changing a rule travels upstream through the report described in AGENTS.md, and the rule then changes for every project or for none.

The rulebook is read as four documents: this core, the rules for living documents in [LIVING.md](LIVING.md), the rules for records in [RECORDS.md](RECORDS.md) and the prose law in [PROSE.md](PROSE.md); each is frozen as this file is.

## The two species of documents

Every technical document is exactly one of two species, and the species dictates all of its rules.

**Living documents** describe the present. They are edited in place, they are always current, and they are bounded in size. A living document never contains history: no dates, no "previously", no "we changed X to Y" narration. When reality changes, the document is rewritten to match it and the old text disappears; git remembers what it used to say. `AGENTS.md`, `STATE.md`, and `docs/ARCHITECTURE.md` are living documents.

**Records** describe one past event. A record is written once, dated, and never edited again, apart from its Status line and the repair of a link target that no longer resolves, which moves where a citation points and changes nothing a reader sees. It is not updated to stay current, because its job is to remain an accurate account of a moment. When reality moves past a record, a new record is written that supersedes the old one. Everything under `docs/decisions/` is a record, and so is any dated document under `docs/` whatever it is called, a briefing or a progress report included, for the purpose of immutability; decisions are the kind this rulebook shapes. In a project built from this template, the template's own decision records are carried whole in an `inherited/` folder under `docs/`, byte-identical to the template's at the alignment pin and recopied as one folder at every re-alignment, so `docs/decisions/` holds the project's own decisions and nothing else, numbered from 0001 in every project alike; a record cites an inherited one by a relative link into the `inherited/` folder. A re-alignment is itself one of the project's decisions and gets one record, which cites every record the folder gained and says what each did to the tree, so the records stay the changelog for the child's law as well as the template's. The docs audit fails a record in `docs/decisions/` whose body, beyond its heading and its status line, is an inherited record's, because a template record kept under the project's number is the one copy the split forbids, and the remedy is deletion, since the inherited folder carries the record and history keeps the copy.

Nearly every documentation failure is a species violation. A history file that grows until it is unusable is record-species content forced into one ever-growing living file. An architecture document that rots is a living document treated as append-only. Never mix the two species in one file.

## The spine and the organic zone

Every project carries this fixed spine:

| Document | Species | Role |
| --- | --- | --- |
| `AGENTS.md` | Living | Vendor-neutral agent entry point: the commands and the single documentation index. |
| `docs/RULES.md` | Living, frozen | The hard rules of the tree, read whole before any work. |
| `docs/CONDUCT.md` | Living, frozen | The hard rules of conduct, read whole before any work. |
| `docs/GATE.md` | Living, frozen | The delivery gate a change is weighed against before it is delivered. |
| `docs/ADOPTION.md` | Living, frozen | How a repository adopts this style and how a child re-aligns. |
| `docs/REPORTING.md` | Living, frozen | The upstream report, what a project sends its template and how an entry is resolved. |
| `STATE.md` | Living | Current project state: what is in flight, queued, deferred, or blocked. |
| `CHANGELOG.md` | Records | Curated per-release summary for consumers; present only where consumers upgrade through releases (the trigger lives in BASELINE.md). |
| `docs/ARCHITECTURE.md` | Living | The map of the system as it is today. |
| `docs/INVARIANTS.md` | Living | The product's stated invariants, one row per claim, each bound to the holder that refuses a violation and graded by what its green is worth. |
| `docs/CONVENTIONS.md` | Living, frozen | The rulebook's core; its parts follow. |
| `docs/LIVING.md` | Living, frozen | The rulebook's rules for living documents and the invariants ledger. |
| `docs/RECORDS.md` | Living, frozen | The rulebook's rules for decision records. |
| `docs/PROSE.md` | Living, frozen | The prose law, the rulebook's rules for every tracked byte of prose. |
| `docs/decisions/` | Records | The decision log of this project's own choices; the durable home of rationale. |

Assistant-specific instruction files (a `CLAUDE.md`, a `GEMINI.md`, tool rule files) do not exist in this project. Every assistant reads `AGENTS.md` directly. If a tool ever genuinely cannot read `AGENTS.md`, it gets a one-line shim that does nothing but import or point to `AGENTS.md` in whatever include syntax the tool understands. A shim is not a document: it is not indexed, it carries no content of its own, and it never grows a second line.

Beyond the spine, documentation grows organically. Any further document the project needs is added under `docs/` (UPPERCASE markdown, one subject per file, one species per file) and registered in the index. The one exception in location is a directory whose purpose needs stating where a reader stands, which may carry its own `README.md` beside its contents, registered in the index like any other document. A subfolder under `docs/` is a record folder, nothing else; living organic documents are flat UPPERCASE files at the top of `docs/`, because the naming and budget rules see only that shape. A record folder beyond `decisions/`, and beyond `inherited/` where a project carries one, holds dated documents named `YYYY-MM-DD-short-kebab-title.md`, ordered by date rather than by number, immutable like every record, and registered by its own row in the index. Growth changes the number of documents, never the species rules of an existing one.

## The index contract

`AGENTS.md` holds the single index of all technical documents, each with a one-line description of what it contains and when to read it. A document that is not listed there does not exist. No reader can be expected to find it, and no agent will. Creating a document and registering it in the index happen in the same change, as does delisting on removal.

## Where a "why" belongs

Rationale has exactly two homes here, chosen by reach:

1. A "why" that fits in a sentence or two and only explains one change goes in the **commit message body**. When the change fixes a defect, the body also names where else the same defect was looked for and what was found, so the search is a fact a reader can re-derive rather than a claim that everything was checked.
2. A "why" that will shape future decisions, or that would be re-litigated without a record, becomes a **decision record**.

A changelog exists only where consumers upgrade through releases, so a project that versions none maintains none (the trigger lives in BASELINE.md). A versioned artifact, such as a packaged library, adds `CHANGELOG.md` as a third home, carrying the curated per-release summary for its consumers; it summarizes impact, not reasoning.

Chronology itself is never documented. Git already is the complete log, and any document that re-narrates it degenerates into a worse git log.

A reference in a living document carries its description. A record is cited by its number and its title, verbatim from its heading and in the same paragraph as the link, so the sentence stands without the click and cannot drift, because a record is immutable. A path or a symbol is cited with its role in the sentence, what the reference is for here, and never with its behavior, which is the file's own claim and moves when the file moves. The docs audit holds the title; the role stays with review.

## Naming

Spine and organic technical documents use UPPERCASE basenames at predictable locations (`STATE.md`, `docs/ARCHITECTURE.md`), matching the ecosystem convention that uppercase markdown means "meta-document about the project". Decision records use `NNNN-short-kebab-title.md` because they are many, ordered, and cited by number. The inherited folder keeps the template's numbers untouched and a project's own records start at 0001, so a number is unique within its folder and the two sequences never meet. A record's filename stays within seventy-two characters, because the folders a record lives under are deep and a Windows clone has a path limit; the docs audit holds the cap for records written after it arrived. Other record folders name their files `YYYY-MM-DD-short-kebab-title.md`, since a briefing or a progress report is ordered by when it happened.

## Code-level documentation

Docstrings follow the NumPy style with one house addition, a `Usage` block on classes that holds a minimal, runnable end-to-end example. The sections and what each holds:

| Section | Holds |
| --- | --- |
| `Usage` | The one canonical way to construct and drive the component; a house addition, not part of the NumPy standard |
| `Examples` | Specific behaviors or edge cases, added wherever warranted; not a replacement for `Usage`, and not replaced by it |
| `Parameters` | Every parameter, under the name the code gives it |
| `Returns` | The returned value, named only where its type cannot carry the meaning |
| `Raises` | Every exception raised directly in the body, the defensive argument-validation guards included; it has no name to give |
| `Attributes` | Every attribute, under the name the code gives it |
| `Warns` | Every warning issued; it has no name to give |

- Where a function warrants a full docstring, all three of `Parameters`, `Returns`, and `Raises` are always present, using the `None.` sentinel when a section is empty (no arguments, or nothing raised).
- A returned or yielded value is named only where its type cannot carry the meaning, so an opaque `str`, `bool`, or `dict[str, Any]` gets a name that says what it holds while a `RunResult` or an `AuthToken` is left bare, since repeating the type as a name tells the reader nothing twice.
- A pydantic model's docstring is also the description of the JSON schema pydantic generates from it, so a schema a language model reads, a tool's parameters or a structured output, is built by the adapter's translator from fields named for it, or the model drops its docstring from the schema with the reason beside it. The docstring stays written for the reader of the source.

Not everything is documented that heavily, by design. Purely internal helpers and thin mappers, such as the translator functions that bridge schemas across a boundary, keep a summary of one sentence, in the house rhythm. Unlike a service with an HTTP edge, this package has no layer whose contract is expressed elsewhere, so the `facade` is documented in full like every other layer. It is the surface an embedding application imports and calls directly, and its docstrings are the only place its failure modes are stated.

The rest of the NumPy vocabulary is used where it fits and omitted where it does not: a caveat becomes a `Notes` section rather than a loose sentence, a generator would document `Yields`, a `warnings.warn` would document `Warns`, and `See Also`/`References` are there for cross-references. Sections you do not see are simply not called for by that code; generated code should add them as it introduces the behavior.

A module carries no docstring; its name and its room in the map say what it is, and only a script run as a command opens with one.

Test files stand outside the every-export rule, because a suite documents itself through the name of each case and the assertion it makes. A comment belongs in a test only where the reason a case exists is invisible from its name, as with a regression guard that should name the defect it pins.
