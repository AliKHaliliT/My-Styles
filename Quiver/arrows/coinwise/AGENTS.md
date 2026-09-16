# coinwise Agent Guide

coinwise is a Keel-style installable Python package, an arrow of the Quiver inquiry that hosts it, measuring the drift a rounding strategy accumulates when many monetary amounts are rounded to whole cents and summed. It is a full adaptation of the Keel template under that style's own law, and this guide is Keel's guide with the words rewritten. Some gaps are intentional and must not be "fixed" unprompted. Here those are the suites, which demonstrate the test shape rather than covering the surface, and the command-line surface, which this domain does not need. The permanent gaps are the ones named here; anything temporary appears in STATE.md.

## Commands

- Install (editable): `pip install -e .` (Python 3.14+; add the tooling with `pip install --group dev`; if an import fails after the tree moves, check where the editable install points with `pip list` before debugging code)
- Test: `pytest`
- Lint: `ruff check . && lint-imports` (ruff checks style, docstring presence, and the function-shape limits; import-linter checks the Dependency Rule)
- Type-check: `mypy src tests` (strict mode is configured in `pyproject.toml`)
- Docs: `python scripts/audit_docs.py` (the living documents against the tree and the calendar)
- Prove the audit itself: `python scripts/audit_docs.py --selftest` (every rule against a planted defect, because a check that never fires and a check that cannot fire look identical)

The checks report at two levels. A failure is a verdict, it stops the
command, and it means a rule the tool fully decides has been broken. A warning is
advice, it leaves the exit status clean, and it comes from a check that cannot
decide its own question and so is not allowed to gate. Advice is not noise and
not optional reading. Every warning is looked at and then either fixed or
dismissed in writing, in the change that produced it, and a warning is never
silenced with a suppression comment to make a run look clean. The advisory checks here are the credential heuristics, run as `ruff check --select S105,S106 .`, which read any suggestive string as a possible secret and are wrong often enough that they cannot be a gate, the prose-vocabulary grep in CI, which reads an honest domain term the same as a tell and so advises for review, and the docs audit's form advisory, which counts the references a prose paragraph names and cannot tell an enumeration from an argument, so it advises a list or a table and gates nothing.

## Hard rules

- The Dependency Rule is absolute. `domain` and `services` never import from `facade`, `adapters`, or any SDK; layer-owned objects cross a layer boundary only through translators, a clause no import graph can see, so it is carried in review by the agent writing a change and the human reading it alike.
- Library citizenship: no global mutable state, no environment reads at import time, and a `NullHandler` on the package logger.
- Every directory holds either subpackages or modules, never a mix (the package root is the sole exception); an `__init__.py` exists only where it re-exports.
- A function stays within three shape limits, ten paths through it, five nested blocks, and fifty statements, and the linter gates all three with the rest of the lint, the audit scripts included. A finding is answered by splitting the function, moving a repeated block into one helper, or turning a branch chain into a table, never by removing a guard; a function that genuinely needs more is a conflict for the owner under the pause rule, never a suppression.
- Test suites live in `tests/`, mirroring the source tree, one suite named after the unit it covers. A collaborator is replaced only at an architectural seam, by a hand-written fake satisfying the port in `domain/interfaces` that it stands in for; never patch or monkey-patch a module's internals, because a test bound to an implementation voids the substitutability the ports exist to provide. No coverage threshold is imposed, so breadth stays a judgment call while the placement and substitution rules do not. The shape is mapped in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md#testing). An invariant with no observable output, such as work done once rather than twice, is observed through a counting fake at the seam it crosses, and where no seam exists the invariant is asking for one. A test is proved by the failure it catches. Before it is written, its name states the break it catches and its expected value is derived without the code under test, so a value the code computes for itself and a test that can fail only on an intentional decision are both refused. After it is written, the code is mutated, in thought or in a scratch copy, against a closed list, a wrong constant or argument, a wrong branch, a missing side effect, an empty or default return, a missing check for zero, empty, nil, unauthorized or malformed input, and a test fails for each, a survivor being a gap unless the types and the control flow show the mutant equivalent. After a fix, the fix is reverted, the regression test is watched failing on its assertion and not in its harness, and the fix is restored.
- Follow the docstring convention in the rulebook's code-level section and the documentation rules in [docs/CONVENTIONS.md](docs/CONVENTIONS.md); the latter is frozen and must not be edited.
- The documentation rulebook is owned by the style. [docs/CONVENTIONS.md](docs/CONVENTIONS.md) changes only inside the template itself, in the My-Styles repository and by its owner; a project derived from this template never edits its copy and never diverges from it. A derived project that believes a rule is wrong or missing sends the case upstream instead (see [The upstream report](#the-upstream-report)).
- An em dash is legal where it clearly beats the comma, the parenthesis, or the period it replaces, and it counts as its paragraph's one flourish. A tracked file carries at most two; CI counts that boundary, while the judgment of fit and commit messages stay with review.
- Commit history speaks in the owner's voice alone: no attribution trailers, no Co-Authored-By lines, nothing naming a tool or an assistant in a commit message. Held in review, like every commit-message rule.
- A check may never imply more than it decides. A green run is a claim, so a check is named for the question it actually settles, and a check that cannot settle its question advises rather than gates. Whatever it leaves undecided is stated beside the rule as review's work, never left to look automated, because the half no tool reaches is the half that rots and it rots faster behind a passing signal. This is why the family carries no coverage threshold, no maturity score, and no metric standing in for a rule it cannot decide. A check that reads history binds from the arrival of its own scope, found in the tree's own history and dated by the sentence that states the scope, never by a name or a date a child's past could already carry, because a commit cannot be unmade and a rule that reaches behind its arrival can never go green; when the scope changes, the sentence changes with it.
- A rule lands in the strongest form its mistake allows. Where a type the checker rejects, an import the linter refuses, or a copy the family audit holds byte-identical can make the mistake impossible, the rule lands there and needs no sentence. Where nothing can make it impossible, it lands as a check that decides its own question and gates. Where no check can decide it, it lands as an advisory or as a clause held in review. Prose is the last form, because a rule that lives only in a sentence binds only a reader who already agrees with it, and the em dash count and the form advisory both began as sentences somebody had to remember. The form is chosen before the rule is written, and the record of the rule names the form it took and why no stronger one was available.
- A check that makes a worker damage the work is worse than no check. When a rule fights something real, neither bend the work to earn a green run nor rewrite the rule. Pause the work in a state it can resume from, report the conflict, propose the change, and wait for the owner's explicit approval, because a rule change slipped into a busy diff is a decision nobody made. A length rule cuts filler and never information, a repair is verified for its side effects rather than for its intent, and a warning is answered rather than avoided, since an advisory a worker silences has become a gate. A question to the owner, here or in a closing note, is posed as numbered options, each stating in one sentence what the agent will do if it is chosen, with the recommended one marked, so the answer can be a number or a word; a reply that matches no option is restated in one sentence at the top of the next message, as what was understood and is about to be done, before anything is done. A change in the tree this session did not make, a file edited, added, or moved by no act of its own, is another actor, a session or a tool, and is reported and left alone rather than repaired, because a repair of what one did not break undoes someone's work.
- One working tree and one branch per session, never two sessions in one tree. A second tree created inside the repository lives under `.worktrees/`, which the ignore file names, so it is never a nested checkout in the tracked tree. A change lands by merging main into the branch, running the gate on the merged tree, pushing the branch, waiting for its run to pass, and fast-forwarding main, so main never carries a tree the gate has not seen whole; integration is a merge and not a rebase where records pin commits, because a rebase rewrites the commits they name.
- A completeness claim names its boundary. Saying that every caller was updated or every usage fixed is a fact only when it names the enumerable list it exhausted, a grep, a file list, a suite run, that a reader can re-derive. A claim over a region the claimant drew itself, such as every edge case considered, is offered as judgment rather than fact, because no boundary exists for it to have reached and the claim reports only that the claimant stopped finding things. Review probes the second kind, and trusts the first only as far as its boundary reaches.
- A rule binds only where its own text claims to bind. A length budget governs the document whose budget it is, the prose law governs a tracked byte, and a stage's cap governs that stage; outside that reach a rule does not apply at all. So nothing is spent applying a convention to material it never named, such as trimming or restyling an untracked working file that will never ship, and a count taken of such material is a measurement rather than a finding to fix.
- All prose must read as if a person wrote it. Never write the clause-colon splice, a sentence shaped as claim, colon, elaboration; in prose a colon may only introduce a list, a quote, or a label. The softer language-model tells (balanced semicolon antitheses, triadic lists, not-X-but-Y reversals) are fine one at a time and forbidden stacked, so allow at most one flourish per paragraph and keep the rest plain declarative sentences. No tool can judge these, so they are held in review, agent and human alike. The full catalog of tells, the vocabulary, and the portability test live in the rulebook's Prose section ([docs/CONVENTIONS.md](docs/CONVENTIONS.md#prose)).
- Every tracked byte is public prose. Confidential facts, private repository names, deployment details, and the description of what was withheld and why never enter a tracked file or a commit message, even in a private repository, because visibility can flip and history is permanent. Such context goes to the untracked `LOCAL.md` at the root (see [docs/BASELINE.md](docs/BASELINE.md)); read it when it exists, create it when first needed, and when unsure whether a fact is sensitive, ask the owner instead of recording it.
- Read [STATE.md](STATE.md) before starting work, and sweep it before starting anything new, deleting every entry that describes finished work and re-verifying or deleting any entry the tree no longer confirms. Its entries are claims to verify, not facts. Completing work deletes its entry in the same change, never adds a narration of the landing, and every change ends with a sweep for entries it completed or invalidated.

## The delivery gate

A task is not delivered while the gate below has findings. Carry these items from the first line written, because they are cheapest to satisfy while the code is still forming and most expensive as after-the-fact repairs; the closing pass exists to confirm, not to redo.

Closing a task follows one loop: run the checking commands above, weigh the change against every item below, fix what an item names, and repeat. One pass with no findings ends the loop. A finding is a concrete disagreement with a listed item, never general unease; the list is closed, and nothing outside it may generate rework. If the same finding survives three honest fix attempts, stop looping, record the finding and the attempts in STATE.md, and say so plainly when delivering. The names below index a wider literature; where a name's common usage and the rule beside it differ, the rule governs.

- **Cognitive load**: nothing in the change is harder to hold in mind than the task requires.
- **Granularity**: the size of every new unit (function, file, document, the change itself) is a choice, not an accident.
- **Growth honesty**: what each loop's or query's cost grows with is a choice, not an accident, and no change buys a worse growth rate where a construction of equal effort exists.
- **Ubiquitous language**: new names use the vocabulary the tree already speaks.
- **Single source of truth**: the change introduces no second copy of any fact, and anything derived points at its source.
- **Least privilege and surface**: nothing gains more access, exports, or dependencies than the task needs.
- **Adversary honesty**: every change that creates or moves a trust boundary names who it is meant to withstand, and deciding that nobody is attacking it is a decision to write down rather than an assumption to leave implicit.
- **Boundary honesty**: no data crosses a boundary unchecked, and checking happens at the door, once.
- **Loud failure**: every new failure path raises a typed error; nothing is swallowed or silently defaulted.
- **Two hats**: shape changes and behavior changes are separate steps, and no incidental reformatting rides along.
- **Waste**: nothing speculative and nothing the change orphaned is left behind.
- **The measured line**: nothing is made faster without a measurement that demanded it, and every optimization that lands records its measurement and its price.
- **Test honesty**: substitutes stand in only at the declared seams, time, randomness, and order are controlled, the suite runs in a shuffled order under a seed the run prints so a test leaning on its neighbour fails on the day it is written and the run that caught it can be replayed, and where an optional dependency sits behind a port with a fallback implementation, the suite executes both paths and holds them to a tolerance a decision record states with the measurement that set it, over a fixture on which the two can disagree.
- **Point-of-use truth**: the doc comment or docstring each export carries is true, not merely present.
- **Intent-split placement**: every documentation change lands in the document whose reader it serves, per the rulebook's species.
- **Decision records**: any choice made here that would be re-litigated without a record gets one now.
- **Debt**: every shortcut taken is written in STATE.md before delivery, never carried in memory.
- **Upstream honesty**: every workaround of template-owned bytes or template-prescribed behavior, and every improvement that qualified, is an entry in the project's `UPSTREAM.md` before delivery, nameless as to the project, and the closing note names each entry added by its heading, or says there is none.
- **The commands**: every checking command above has passed against the final state of the tree, which is the tree that gets pushed, so a merge or a rebase after the last run makes a new final tree and the commands run again on it, and every advisory finding printed along the way has been read and then fixed or dismissed in writing.
- **The hard rules**: the change disagrees with no review-held clause of this guide's Hard rules, re-read now, not recalled.

## The upstream report

This template is the style's single statement of its form, and it only stays that way if what a child learns flows back to it. When work against this template surfaces something the template itself should have had, the improvement belongs in the template first and in the project second; an improvement kept privately by one child is a quiet fork of the style. The same road carries defects. A child that works around something in the template's own bytes or behavior and tells nobody leaves every later child to hit it, so the road is also where a workaround is confessed.

A project built from this template carries one living document for this, `UPSTREAM.md` at the top of `docs/`, registered by one index row and present from adoption on; the template itself has none, being the style. It is a document of the same kind as `STATE.md`. It holds what is pending between the project and its style, an entry is written when the work that produced it closes, and an entry is deleted when it is resolved, with anything worth keeping written into a decision record. Its schema is fixed:

- The file opens with its title, one line naming the template and the commit the project is aligned to, `Aligned to <template> at <commit>`, or at the host's own commit for an arrow carried inside its style's repository, and one sentence saying that every entry is a lead and not a verdict, to be verified against the template's own tree before it is adopted.
- One section, `## Open`, holds either the words `Nothing open.` or entries.
- Each entry is a heading of the form `### YYYY-MM-DD` followed by a title, then a `Kind:` line reading `improvement` or `defect`, and a `Pin:` line naming the template commit the entry was written against.
- Each entry carries four parts under the bold labels **What it is**, **How the work surfaced it**, **Why it is believed better** or **What was worked around**, and **Records checked**.

An entry names nothing that identifies the project, no project name, no person, no host, no path or address that points at the project, and no fact about its domain beyond what the entry needs, because the file is handed to the template's public repository and may be quoted verbatim into its records, whatever the visibility of the project that wrote it.

The shape, as bytes to copy rather than a sentence to interpret:

```markdown
# Upstream

Aligned to <template> at <commit>.

Every entry below is a lead, not a verdict; verify it against the template's own tree before adopting it.

## Open

### 2026-09-09 A title in plain words

Kind: improvement
Pin: <commit>

**What it is.** One paragraph.

**How the work surfaced it.** One paragraph.

**Why it is believed better.** One paragraph, or **What was worked around.** for a defect.

**Records checked.** One paragraph.
```

Entries come in two kinds, and only the first is judged:

- **An improvement** earns an entry only if it is genuinely better rather than differently shaped, the template does not already have it, and the template's decision records, [docs/decisions/](docs/decisions/) here and the `inherited/` folder under `docs/` in a project built from this template, show no record of it being considered and rejected. Read the decision records before writing anything; a rejected idea returning without new evidence is noise, and an improvement invented to have something to send is worse than none.
- **A defect** is never judged. Anything the child worked around, patched, suppressed, or could not make work in template-owned bytes or template-prescribed behavior gets an entry, whether or not the child is sure it is a defect and however small the fix was. An entry may say plainly that the child could not tell a defect from its own misunderstanding, because the maintainer decides that, and size is not a criterion; a one-line rename a child needed is exactly the kind of entry that must arrive.

The order is strict. The work is finished as specified first, and an entry is never written instead of finishing. Each entry is written as a hand-off, self-contained enough to be pasted to an agent or handed to the template's maintainer and acted on with no other context, in the same change that closes the work which produced it, and the closing note of that delivery names each entry added by its heading, or says none was. The style's owner reads the file and points an agent at the template. Anyone else holding it is holding an open-source template's feedback, and the right move is to file each entry as an issue on the template's repository.

No reply is owed, and nothing waits for one. Every open entry is resolved by the child at its next re-alignment, against the new pin, the records the template gained since the old one, and the treasury's dispositions, which name reports by pin and date and are public, so a refusal is found there without anyone writing a letter. An entry the template now carries is deleted and the template's form taken. An entry a record refuses is deleted, the child conforming, or turned into the child's own decision record where the matter is the child's to decide. An entry the template is silent on stays. An entry older than ninety days is re-verified against the current template and re-dated, or made the child's own decision and deleted, because silence for a season is the style's answer for now and the child owns its divergence. A reply from the maintainer, when one comes, is a message that speeds this up and is filed nowhere; what was sent and what became of it is the file's own history in git.

## Adopting this style

An existing repository adopts this style through one refactor, and the refactor is done when the gate below holds, not when the tree looks similar. Three rules govern the work.

The adopting agent folds, moves, rewrites, and deletes on its own authority. Ten documents that say one thing become one document that says it; a folder with no room in the map is given one, folded into a room that exists, or removed; code is rewritten into the convention rather than left beside it. Git is the archive, so none of this needs asking. What the owner reviews is content that leaves the repository, and it is reviewed once, at the end, from the inventory the agent keeps: every tracked path classified as kept in its room, folded into a named document, moved to a named room, or deleted with its reason. The pause-and-propose rule stays reserved for a conflict with a rule; a routine refactor decision never pauses.

The demo is the authority on dialect and never on scope. Every artifact the refactor produces is cut from the exemplar the map's Exemplars section names for its kind, a docstring from the exemplar docstring, a translator from the exemplar translator, a suite from the exemplar suite, because a rule names what must exist and only the style's own bytes carry how it reads. What the demo leaves out is its named incompleteness, not a ceiling. The tool configuration is dialect too. The lint, type-check, and import-contract settings the style ships, with the comments that give their reasons, are style-owned law like the rulebook; a child copies them and changes only the names that must be its own, such as the packages a contract lists, because a selection the style refused, docstring-format codes among them, forbids the very rhythm the exemplars carry. Inside those blocks, a line that binds the demo's own stack rather than the style's rule is marked in the style's configuration with a comment beginning `Stack binding`, the type checker's plugin for the demo's validation library, the test runner's async mode, an SDK the import contract forbids by name, and a child re-adapts or removes such a line freely; everything unmarked is law.

The template's decision records travel as one folder. They are carried whole into an `inherited/` folder under `docs/`, registered by one index row, byte-identical to the template's at the pin, and never edited or added to; the project's own decisions live in `docs/decisions/` from 0001, the adoption itself being the first of them, and a record cites an inherited one by a relative link into the `inherited/` folder. A number is unique within its folder, so the template grows without ever colliding with a child, and a reader knows whose record they hold from where it sits.

The adoption is done when every item below holds, and the agent says so by naming the boundary it exhausted rather than by feeling finished. The gate decides what a check can decide; what it cannot, it names as review's, so a passing gate is never read as the whole.

- **Inventory exhausted**: every tracked path is classified, and no path is left undecided.
- **Audits green**: the docs audit, the lint, the type-check, and the tests pass on the final tree, which holds that every directory has a room, every document under `docs/` a species and a row, every record its immutability, and every documented parameter its name.
- **Debt paid**: the STATE debt list the adoption opened, inherited prose or inherited structure that could not be brought under the law in one change, is empty.
- **Leftovers swept**: every rule the adoption or re-alignment retired has had what it required removed from the tree, and the inventory names the sweep.
- **Pin recorded**: the first line of `UPSTREAM.md` names the template commit the project was aligned to, and the inherited folder holds that commit's records whole and nothing else.
- **Upstream present**: `UPSTREAM.md` exists at the top of `docs/` with its row in the index and its aligned line, holding every improvement that qualified and every workaround as entries, or the words Nothing open.
- **Upstream resolved**: every open entry has been resolved against the new pin, adopted and refused ones deleted, kept divergences written as the project's own decision records, and silent ones re-verified and re-dated where past their horizon.
- **Residue named**: whether folding preserved meaning, whether docstrings say true things, and whether prose is good are review's questions against the exemplars, and the closing note says so instead of implying the gate covered them.

Re-alignment is the same refactor in miniature. The child reads the decision records the template gained since its pin, because every rule change carries one; recopies the files the style carries verbatim, the rulebook, the baseline, the docs audit, the inherited records as one folder, the editor and attribute files, the tool-configuration blocks with their project names re-adapted, and this guide from its shared tail; re-adapts from a diff whatever it adapted at adoption; for every rule its own configuration had and the style's does not, sweeps out what that rule required, because the rule's absence in the template is a refusal rather than an oversight; resolves every open entry of its `UPSTREAM.md` against the new pin, reply or none, by the diff of the files the entry touches, the records since the pin, and the treasury's dispositions, deleting an entry the template now carries and taking the template's form, deleting an entry a record refuses or turning it into the child's own decision record where the matter is the child's to decide, and leaving an entry the template is silent on in place, re-dated once re-verified; runs the gate above; and moves the pin. A history-reading check binds the child from the commit its scope sentence arrived in, the re-alignment commit itself, so a red gate over older commits is a defect in the check to send upstream, never a reason to rewrite history. No changelog is kept, because the records are the changelog and a summary would be a lossy copy of them.

## Documentation index

This is the single index of the project's technical documentation. A document that is not listed here does not exist as far as this project is concerned: when you create a document, register it here in the same change; when you remove one, delist it here.

| Document | What it is and when to read it |
| --- | --- |
| [README.md](README.md) | Human-facing overview: philosophy, structure, and setup. |
| [STATE.md](STATE.md) | Living project state (Now / Next / Deferred / Blocked). Read first, always. |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | The annotated map of the whole template. Read before any structural change. |
| [docs/CONVENTIONS.md](docs/CONVENTIONS.md) | The documentation rulebook: document species, schemas, naming. Frozen; do not edit. Read before writing or changing any documentation. |
| [docs/BASELINE.md](docs/BASELINE.md) | The repository baseline: always-present files, never-tracked files, and their modification rules. Read before adding, removing, or reshaping root-level or dot files. |
| [docs/decisions/](docs/decisions/) | This arrow's own immutable decision records. Read the relevant record before revisiting a settled topic; never edit an accepted record. |
| [docs/inherited/](docs/inherited/) | Keel's decision records, carried whole and byte-identical at the host's pin. Read for the reasoning behind every carried rule; never edited or added to here. |
| [docs/UPSTREAM.md](docs/UPSTREAM.md) | What this arrow has for its style: improvements to offer and workarounds to confess, each an entry until re-alignment resolves it. Read before re-aligning. |

There are no assistant-specific instruction files. Every assistant reads this file directly. If a tool genuinely cannot read AGENTS.md, give it a one-line shim that imports or points to this file and nothing more.
