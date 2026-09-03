# Documentation Conventions

This file is the rulebook for this project's technical documentation: which documents exist, what species each one is, how each species is written, and where a "why" belongs. It is normative and frozen; do not modify this file. If a rule ever has to change, the change is made deliberately, by the style's owner, inside the template itself in the My-Styles repository, and recorded as a new decision record superseding [0001](decisions/0001-adopt-the-documentation-system-and-extend-it-for-inquiry.md). A project derived from this template never edits its copy and never diverges from it; a case for changing a rule travels upstream through the report described in AGENTS.md.

## The two species of documents

Every technical document is exactly one of two species, and the species dictates all of its rules.

**Living documents** describe the present. They are edited in place, always current, and bounded in size. A living document never contains history: no dates, no "previously", no narration of change. When reality moves, the text is rewritten and the old text disappears; git remembers what it used to say.

**Records** describe one past event. A record is written once, dated, and never edited again, apart from its one legal status edit. When reality moves past a record, a new record supersedes it. This project keeps two kinds of record: decisions, which hold choices, and claims, which hold assertions about the world and the evidence behind them. Any other dated document under `docs/`, a briefing or a progress report, is a record too for the purpose of immutability, though only decisions and claims have a shape the audit holds.

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

Assistant-specific instruction files do not exist here; every assistant reads `AGENTS.md`. Beyond the spine, documentation grows organically. Further documents are added under `docs/` (UPPERCASE markdown, one subject per file, one species per file) and registered in the index. The one exception in location is a directory whose purpose needs stating where a reader stands, which may carry its own `README.md` beside its contents, registered in the index like any other document. A subfolder under `docs/` is a record folder or `arrows/`, nothing else; living organic documents are flat UPPERCASE files at the top of `docs/`, because the naming and budget rules see only that shape. A record folder beyond `decisions/` and `claims/` holds dated documents named `YYYY-MM-DD-short-kebab-title.md`, ordered by date rather than by number, immutable like every record, and registered by its own row in the index. Growth changes the number of documents, never the species rules of an existing one.

## The index contract

`AGENTS.md` holds the single index of all technical documents. A document not listed there does not exist. Creating a document and registering it happen in the same change, as does delisting on removal.

## Rules for living documents

- Present tense only; describe what is, never what was or how it got here.
- No dates and no changelog narration (`STATE.md` entries are the one exception; each carries an absolute date, its last-verified stamp, and an entry older than 90 days is expired until re-verified, an in-flight `Now` entry after 30, since work that has not moved in a month is finished or stalled).
- Record intent and decisions, never inventory the tree can answer.
- A sentence in a living document is a claim, not a fact. Verify a claim before relying on it, and end every change by sweeping `STATE.md`.
- Rewrite in place; never append-and-preserve.
- `AGENTS.md`, `docs/ARCHITECTURE.md`, and `docs/BIBLIOGRAPHY.md` grow with the inquiry rather than against a number, saying everything as briefly as it can be said. Every other living document is bounded at 150 lines, the audit fails one that exceeds its bound, and the remedy is fission by subject. `README.md` stands outside both classes, governed by the README schema in BASELINE.md.
- The mechanical half of freshness is checked by `scripts/audit_inquiry.py`: paths named exist, relative links resolve, no `STATE.md` entry outlives its horizon, no bounded document exceeds its budget, every document under `docs/` is registered or is a dated record in a registered record folder, every root entry has a room in the map or the baseline, a record changes only on its Status line, two claims quoting one figure at one pin agree, each manifest names exactly the current claims on its arrow, names and schemas hold. Records are exempt from every rule in this section; they describe the past, which does not rot.

### The STATE.md schema

`STATE.md` has exactly four sections: `Now` (in flight), `Next` (queued), `Deferred`, and `Blocked`. An entry earns `Now` only while its work is genuinely unfinished. Completing work deletes its entry in the same change. Every entry is one line ending with its date (YYYY-MM-DD), and the audit caps `Now` at five entries. The file is swept at both ends of every change. Execution tracking lives here and never in a record.

## Rules for decision records

Write a decision record when a choice shapes future work and its reasoning would otherwise be lost. Records live in `docs/decisions/`, named `NNNN-short-kebab-title.md`, and follow the family template: Status and Date lines, then Context, an optional Evidence section where the decision rests on something measured or run, Options considered where they existed, Decision, and Consequences. An accepted record is immutable; when a decision changes, a new record supersedes it, and flipping the old `Status:` line is the only edit it may receive. A dead end that cost real effort or could plausibly be retried gets its record when the evidence arrives, naming what killed it and what would reopen it.

## Rules for claim records

A claim is the inquiry's unit of knowledge: one assertion, its evidence, and the exact state of the world that produced it. Claims live in `docs/claims/`, named `NNNN-short-kebab-title.md` in their own sequence, titled by the assertion, and follow this template:

- `Status:` one of `Conjecture`, `Supported`, `Refuted`, `Stale`, or `Superseded by NNNN`, then `Date:`.
- **Claim.** The assertion in plain words, and who it must convince.
- **Evidence.** What ran, in which arrow at which pinned commit, and the results quoted in full, never pointed at; `None.` for a conjecture. A pin is written as `arrows/<name> at <commit-hash>` and names the host commit whose tree produced the results. Evidence gathered by reading rather than running quotes the source's numbers or words in full and cites its bibliography key, and it carries no pin, since no tree produced it. A run whose outcome depends on conditions the pinned tree does not control, such as the model behind an API, a provider's version, or a metered budget, names those conditions in the record, because a pin reproduces only what the tree holds. A run that compares conditions isolates every condition from the operator's own environment, since the sharpest confound is the candidate leaking into its own baseline and being measured against itself. Every figure the claim rests on is also written on its own line as `figure <name>: <value>`, so the audit holds two records that quote one run to one value, and the arrow's manifest names the command that reproduces its figures; a re-pin runs it and quotes the figures digit for digit.
- **Threats.** The named threats and biases most endangering this claim, each with what was done about it or the concession that nothing was.

A claim record is immutable and the `Status:` line is its only legal edit. The trigger for writing or flipping one is evidence arriving or a claim moving, never work completing. A refuted claim names the evidence that killed it, the condition that would reopen it, and the pin that held the attempt. `Stale` means an arrow moved past a claim's pin in the paths that can change a result, its code, its tests, or its project file, so the claim is no longer backed rather than wrong; a person flips it, prompted by the audit's advisory, and the way back is a re-run at a new pin or a superseding claim. Any completeness assertion inside a claim names the enumerable boundary it exhausted or presents itself as judgment.

## Rules for the bibliography

Every work the inquiry consulted is entered, because a source treated as a frame instead of an object silently vanishes from the record. A citation is self-contained: author, year, title, venue, and the edition or dated version actually used, since held knowledge preserves superseded editions without noticing. A DOI or URL may ride as a locator, but the citation must survive its death. Prose cites keys of the form `[authorYYYY]`, or, for a standard with no author's name, the standard's designation with its year suffixed, like `[ieee754-2019]`; the audit verifies every cited key resolves, and bare external links appear nowhere outside this file.

## The arrows and their jurisdiction

An arrow is a complete instance of an artifact style, vendored whole under `arrows/<name>/`. Everything inside that tree is governed by the arrow's own style, its gate, and its conventions; this project's law binds the inquiry layer only and never writes into an arrow. Each arrow has one manifest at `docs/arrows/<name>.md`. An arrow is a full adaptation, carrying its style's entire documentation spine, baseline dotfiles, and inert workflow, so the law an agent needs is in place where jurisdiction binds it and a decision made inside the arrow has a record to land in; named incompleteness in an arrow's README covers domain trims only, never the spine. The LICENSE file alone stays at the host root, since a license answers a repository-level question, and an arrow extracted to stand alone gains its own then, following its style's baseline trigger. Because arrows are vendored, the host history is the only history, which is what makes a pin one hash.

## Proportional rigor

The full spine of an inquiry is question, conjecture, evidence, claim. Any shortening is legal and costs one recorded line, in the claim or in QUESTION.md, saying what was skipped and why. Skipping silently is the only violation.

## Where a "why" belongs

A "why" that fits in a sentence and explains one change goes in the commit message body. A "why" that would be re-litigated goes in a decision record. A "what we hold true" goes in a claim. Chronology itself is never documented; git already is the complete log.

## Naming

Spine and organic documents use UPPERCASE basenames at predictable locations. Decision and claim records use `NNNN-short-kebab-title.md`, each sequence numbered independently, because they are many, ordered, and cited by number. Arrow manifests are lowercase, named exactly after the arrow directory they describe. Other record folders name their files `YYYY-MM-DD-short-kebab-title.md`, since a briefing or a progress report is ordered by when it happened.

## Code inside arrows

This project's inquiry layer carries no code beyond `scripts/audit_inquiry.py`. Code lives in arrows, and each arrow's docstring, testing, and layout rules are its own style's, stated in that style's README and rulebook. An arrow is begun by transplanting the nearest exemplar files from its style and rewriting their words, never by writing fresh from a rule summary. A rulebook names what must exist; only the style's own bytes carry its dialect, so review of a new arrow reads it beside the exemplars it was cut from.

## Prose

Most of this family's prose is written by machines, so the law names the failure modes of machine writing precisely enough for review to check. The rules below govern every tracked byte of living prose and every new record. Words quoted inside this section as examples of what to cut are exempt where they are quoted, and nowhere else.

The house voice is plain declarative sentences that argue their case. Judgment is welcome when it carries its reasons, and the family's idiom of animate machinery, a gate that lives somewhere, a claim that rests, stays. What the voice never does is let a vague actor hide a decision, so "the owner removed the check" beats "the check was removed" and both beat "the decision emerged".

A small census of language-model tells is tolerated one at a time and forbidden stacked: the balanced antithesis, the triadic list, the not-X-but-Y reversal, the em dash aside. At most one such flourish per paragraph, and the rest plain sentences. The clause-colon splice, a sentence shaped as claim, colon, elaboration, is banned outright; in prose a colon introduces only a list, a quote, or a label.

An em dash is legal where it clearly beats the comma, the parenthesis, or the period it replaces, and it spends its paragraph's one flourish. A tracked file carries at most two, because the plague arrives as clusters and a cluster is countable, so CI counts that boundary while the judgment of fit stays with review.

Every sentence must survive the portability test. A sentence that could sit unchanged in another repository's documentation states nothing about this one, so it is cut or bound to this subject with a fact, a mechanism, a consequence, or a judgment this subject earned. The same test condemns the inflated vocabulary that means nothing anywhere, words in the family of delve, tapestry, paradigm shift, game changer, ever-evolving, cutting-edge, supercharge, transformative, multifaceted, meticulous, paramount, embark, empower, and elevate, and the padding phrases in the family of "it's worth noting", "at the end of the day", "in today's world", "let's dive in", and "going forward". CI greps a domain-safe subset of these on living prose, the records and the treasury excluded as quoting ground, and advises; the verdict is review's, because a banned word can be an honest domain term and only a reader knows which.

A claim about the world names its source or dies. "Experts agree", "studies show", and "widely regarded as" are not sources; cite the work or cut the sentence, and when no source exists, say so instead of inventing weight. A specific fact enjoys the same protection, so a number is never smoothed into an adjective and "cuts the run from 40 minutes to 4" never becomes "significantly faster". Plain verbs carry claims best, "is" and "has" beat "serves as", and a trailing participle that pretends to explain, the "highlighting" and "underscoring" family, is replaced by the actual mechanism or dropped.

Theater is cut wherever it appears. That covers throat-clearing openers, setups that flatter the writer as the lone honest expert, rhetorical questions the next sentence answers, importance puffery in the family of "marks a pivotal moment" and "a testament to", negative listing, staccato fragments for drama, and endings that recap what the reader just read. A final line that turns the point into an aphorism or a mic drop is deleted, never rewritten into a better one; the piece ends on its clearest concrete sentence, and when the ending needs more, it gets a plain takeaway or the next action.

Formatting obeys the same law. No emoji in headings, no bold sprinkled mid-sentence for emphasis, no bullet list where two sentences of prose read better, no header over a two-sentence section. Format carries structure the content actually has.

A project adopting this style brings prose it did not write under a law written for prose it will. The law binds the whole tree from adoption, because a gate that excuses a class of files teaches that the class is exempt, and the adopting refactor is where the corpus is brought under it. Inherited prose that cannot be brought under the law in the same change is listed in STATE as debt, one entry per document or group, and paid before the adoption is called done; nothing converges by waiting for someone to edit it next. A path whose bytes another guard hashes or pins, such as data files with manifest digests, is excluded by name in the workflow with the reason beside it, since a comment edit that moves a provenance hash is not a prose fix.

A report to a person opens with one paragraph a reader outside the work could follow, what happened and what it means, before any detail, and every abstract finding is paired with one concrete instance, the input that broke the invariant or the line that carried the drift. This is not a schema and not layman's terms; it is the order in which an expert who did not do the work can check it. Chat replies, upstream reports, and handoffs are reports to a person and follow it.

Before shipping prose, the writer checks its own output against this section: colons only for lists, quotes, and labels; at most one flourish per paragraph and two em dashes per file; every generic sentence bound to the subject or cut; every emphasis argued rather than labeled; a report to a person opened with its plain account; the ending concrete. Beyond the counts named above no tool judges any of this, so the check is the writer's own, and review reads behind it.
