# The Primitive Operations

One hundred twenty-five operations that recur across every field of software
engineering under different names, reduced from a catalog of 14,765 named,
established concepts; the research record beside this file preserves how. Each
entry gives the most recognized name, then the operation, then its price. Six
entries carry the mark "(in house)", meaning the operation had no
industry-wide name and the family coined one; the nearest established terms
stay beside them. Read this before drafting a new style, and treat each entry
as an option to weigh, so an omission is a decision rather than an accident.

## When the work happens

- **Caching**, or **precomputation** when it runs ahead of any request: do it before it is needed and keep the result, at the price of staleness and storage.
- **Lazy loading**, also **lazy evaluation**: do it only when something actually asks, at the price of the cost landing during use.
- **Batching**: do it once for a whole group rather than once per item, at the price of added delay and bigger failure units.
- **Incremental processing**, also **delta processing**: do only the part that changed since a recorded marker, at the price of the marker drifting.
- **Pruning**, also **short-circuiting**: look only at what could possibly matter and skip the rest unread, at the price of keeping the summaries that let you skip.
- **Approximation**, and **lossy** when detail is dropped deliberately: accept a close-enough answer inside a declared error band, at the price of the discarded detail being what someone needed.
- **Cascading**, also **two-stage filtering** or **coarse to fine**: filter cheaply first and judge expensively only on survivors, at the price of good candidates lost in the cheap stage.
- **Fast path**, paired with a slow path: optimize for the common case and keep a correct path for the rest, at the price of two paths that must stay equivalent.
- **Concurrency**, and **parallelism** for independent work: start pieces before the earlier ones finish, at the price of coordination and harder reasoning.
- **Streaming**: hand back partial results as they appear, at the price of no global view.
- **Asynchrony**, also **queueing**: answer now and finish the slow part elsewhere, at the price of carrying state across the split.
- **Eliminating waste**, with **YAGNI** as its design-time form: remove work nobody needs at all, at the price of occasionally deleting something still used.

## Where things sit

- **Locality**, and **edge computing** when the move is toward the user: put the work next to the data or the answer next to the asker, at the price of many copies to keep aligned.
- **Shared-nothing**, also **thread-local storage** at small scale: give each worker its own copy so nothing needs coordinating, at the price of duplicated memory and drift.
- **Partitioning**, also **sharding**: divide the whole into non-overlapping pieces chosen by a key, at the price of expensive cross-piece work and uneven pieces.
- **Read-order layout (in house)**: lay data out in the order it will be read, at the price of one layout serving only one access pattern.
- **Denormalization**, also **read model** or **materialized view**: keep a second copy shaped for reading beside the one shaped for writing, at the price of two truths to reconcile.

## Copies, history, and identity

- **Replication**, also **redundancy**: keep more than one copy so losing one loses nothing, at the price of doubled cost and copies that disagree.
- **Single source of truth**: name one copy authoritative and derive every other appearance from it, at the price of that copy becoming a bottleneck.
- **Eventual consistency**, and **bounded staleness** when the limit is numeric: declare how out of date a copy may be, at the price of readers acting on old facts.
- **Append-only log**, called **event sourcing** in applications and **write-ahead log** in databases: append the change instead of overwriting, at the price of unbounded growth.
- **Immutable versioning**, also **content addressing** when the name is a hash: give each version a name that never changes meaning, at the price of permanent storage discipline.
- **Unique identifier**, with **namespacing** for the scheme: give each thing one stable public name so strangers can point at the same thing, at the price of a registry and names that outlive their meaning.
- **Bitemporal modeling**: record a fact's own time separately from when you learned it, at the price of every question needing two time filters.

## Coordination

- **Locking**, also **mutual exclusion**: force an order when two parties touch the same thing, at the price of waiting and deadlock.
- **Optimistic concurrency control**: assume collision is rare, act now, then detect and repair, at the price of visible reversals and rework.
- **Idempotency**: make repeating an act harmless, at the price of keys and remembered history.
- **Transaction**, with **saga** or **compensation** when distributed: group steps so either all take effect or the ones that did are undone, at the price of coordination and reversals that are not always possible.
- **Blocking**, and **await** in modern code: wait for an announced condition instead of polling or guessing, at the price of missed signals and one slow party stalling everyone.
- **Timeout**, with **time to live** for stored facts and **lease** for held claims: put an expiry on every wait and every held fact, at the price of churn when the expiry is chosen badly.
- **Pull**, also **demand-driven**, seen from the other end as **backpressure**: let the receiver signal when work may start, at the price of upstream idling.
- **Publish and subscribe**, also **event-driven** or the **observer** pattern: announce what happened and let whoever cares respond, at the price of nobody owning the whole sequence.

## Boundaries and trust

- **Encapsulation**, also **information hiding**, exposed through an **interface**: hide the inside and publish a narrow promise, at the price of a promise that hardens and leaks.
- **Indirection**: put an intermediary between two parties so neither depends on the other's shape, at the price of a hop to run and maintain.
- **Cohesion**, tied to **separation of concerns**: keep what changes together together and what changes separately apart, at the price of betting on which changes come.
- **Dependency inversion**, with **layering** as its structure: let the volatile depend on the stable and never the reverse, at the price of awkward inversions.
- **Isolation**, with **blast radius** naming what it limits: stop damage at a boundary so it cannot spread, at the price of duplicated resources.
- **Least privilege**: grant only the powers needed and deny by default, at the price of friction and blocked legitimate work.
- **Attack surface reduction**, with **trusted computing base** for the core: shrink what must be trusted and check everything crossing into it, at the price of that core becoming the target.
- **Quotas**, also **resource reservation**: reserve each participant a fixed share of a shared resource, at the price of reserved capacity sitting idle.
- **Digital signature**, and **provenance** or **chain of trust** for the fuller practice: prove where a thing came from and that it has not changed, at the price of key custody.
- **Rotation**, met most often as **key rotation**: give secrets and worn parts a deliberately short life, at the price of renewal machinery that fails at the worst time.
- **Encryption**, and **anonymization** when the goal is unlinkability: make data unreadable or unlinkable while keeping it useful, at the price of lost utility and key loss.

## Load

- **Rate limiting**, also **throttling**, and **load shedding** when you drop accepted work: refuse or slow what you cannot serve, at the price of rejected legitimate work.
- **Control loop**, called **congestion control** in networks and **autoscaling** in operations: adjust the rate continuously from a signal of how the other side is coping, at the price of oscillation and needing a trustworthy signal.
- **Slack**, also **headroom** or **buffer**: keep capacity deliberately unused, at the price of looking like waste until the day it saves you.
- **Budgets**, as in error, performance, and latency budgets: split one scarce limit into named allowances, at the price of allowances argued over and never lent.
- **Retry with exponential backoff**: retry the failure, spaced and capped, at the price of amplifying the very load that caused it.
- **Graceful degradation**: do less rather than stop when you cannot do everything, at the price of partial service masking real breakage.
- **Debouncing**, and **hysteresis** in control contexts: ignore changes below a threshold so noise does not trigger action, at the price of missing real small changes.
- **Watchdog**, listening for a **heartbeat**: require continuous proof of progress and force a harmless state when it stops, at the price of false trips.

## Finding out whether it works

- **Assertion**, generally the **test oracle**: state the expectation apart from the thing, then compare, at the price of the expectation itself being wrong.
- **Regression testing**, with **snapshot** or **golden master** for the frozen reference: freeze current behavior and flag any difference, at the price of blessing today's bugs.
- **Differential testing**, also **N-version** when built independently: run two things that should agree and treat disagreement as the signal, at the price of both being wrong together.
- **Testing**, and **drill** or **rehearsal** for procedures: exercise it deliberately under chosen conditions before it matters, at the price of chosen conditions not matching real ones.
- **Fault injection**, popularized as **chaos engineering**: cause the failure yourself, early and contained, at the price of finding only the failures you imagined.
- **Mocking**, with **stub**, **fake**, and **simulation** as its forms: replace part of the world with a controllable stand-in, at the price of the stand-in drifting from the real thing.
- **Monitoring**, now folded into **observability**: sample it continuously while it runs and reduce that to a few signals, at the price of blind spots between samples.
- **Sampling**, and **equivalence partitioning** in test design: pick a few cases to stand for many by an explicit rule, at the price of whatever hides in the gaps.
- **Fuzzing**, and **property-based testing** when the rule is a stated property: generate the cases mechanically rather than by hand, at the price of opaque cases and a model to maintain.
- **Per-slice evaluation (in house)**, nearest established term **cohort analysis**: judge inside each slice separately because the average hides the failures, at the price of multiplied analysis.
- **Bisection**, also **divide and conquer**, and **ablation** when the variable is a component: change one thing at a time and halve what remains, at the price of many slow cycles.
- **A/B testing**, also **split testing**: vary an input across a real population and read the difference, at the price of exposing some people to the worse arm.
- **Profiling**: measure where the cost actually accumulates before changing anything, at the price of measurement perturbing what it measures.
- **Determinism**, met as **pinning** and **reproducible builds**: pin every input so the same run gives the same result, at the price of pinned things going stale.
- **Code coverage**: track what your checks never touched and treat it as unknown, at the price of touching being mistaken for checking.
- **Quorum** and **voting**, appearing as **consensus**, **peer review**, and **ensembling**: collect judgments formed independently and combine them by a stated rule, at the price of cost multiplied and correlated judges adding nothing.

## Preventing mistakes, and making them cheap

- **Type safety**, sloganized as **make illegal states unrepresentable**: narrow what can be expressed so the wrong thing cannot be written, at the price of blocking legitimate cases.
- **Input validation**, with **sanitization** and **escaping** on the output side: treat incoming data as inert until checked and reshape it per destination, at the price of rejecting valid input.
- **Static analysis**, met daily as **linting** and as **policy as code**: have a machine apply the rule on every change, at the price of checking only what is expressible.
- **Undo**, and **two-way door** at decision level: prefer what can be undone, and where it cannot, add delay or explicit confirmation, at the price of guards that get clicked through.
- **Backup**, with **snapshot** and **checkpoint** as its forms: keep a recoverable earlier state, at the price of restores never exercised until they fail.
- **Checksum**, also **hash** or **cyclic redundancy check**: carry extra derived bits so corruption announces itself, at the price of space and only catching modeled corruption.
- **Canary release**, also **staged rollout**: expose the change to a small slice first and widen only while it holds, at the price of mixed versions coexisting.
- **Strangler pattern**, with **expand and contract** for schemas: add the new beside the old, move across in steps, remove the old last, at the price of a long double-support window.
- **Feature flags**, described as **decoupling deploy from release**: separate the act of building from the act of exposing, at the price of dead paths accumulating.
- **Refactoring**: change shape without changing behavior as an act of its own, at the price of churn with no visible benefit.
- **Stop the line**, also **andon**, with **fail fast** as the automated form: fix the fault at the moment and place it appears, at the price of interrupting whatever you were doing.

## Deciding under uncertainty

- **Feedback loop**: shorten the time between making a choice and learning it was wrong, at the price of favoring what is quick to measure.
- **Small batch size**, also **incremental delivery**: make each unit of work small, at the price of per-unit overhead and losing sight of the whole.
- **Last responsible moment**, also **deferred commitment**: delay commitment to the last moment it can still be made, at the price of some options expiring.
- **Spike**, also **proof of concept** or **prototype**: spend a little to buy information about the largest unknown, at the price of work you throw away.
- **Risk assessment**, named **threat modeling** in security and **failure mode and effects analysis** in engineering: list the ways it can fail, then design against the list, at the price of blindness to what nobody imagined.
- **Root cause analysis**, popularly the **five whys**: follow the chain of causes back and change the earliest link, at the price of being slower than patching the symptom.
- **Reference class forecasting**, also the **outside view**: estimate from recorded outcomes of comparable past cases, at the price of needing history.
- **Confidence interval**, loosely **error bars**: say how uncertain the answer is instead of giving one number, at the price of ranges being read as their midpoint.
- **Prioritization**, and **triage** when the queue is problems: rank by expected value or harm and take the top, at the price of the ranking hiding the long tail.
- **Proportional rigor (in house)**, nearest established phrase **risk-based approach**: set how much scrutiny a thing gets in proportion to what its failure costs, at the price of misjudging the stakes.
- **Metrics**, or **key performance indicators**, with **Goodhart's law** naming the failure: attach a number to a quality so it can be compared, knowing the number will become the target.
- **Technical debt**: take the cheap option now and keep a running account of what it charges later, at the price of an account nobody can actually measure.
- **Cadence**: fix a repeating rhythm so everyone can plan around it, at the price of work being cut to fit the clock.
- **Timeboxing**, explicitly **fixed budget variable scope**: fix the spend in advance and vary what gets built, at the price of silent cuts to quality.
- **Debiasing**, also **decision hygiene**: insert a fixed procedure that corrects a known skew in judgment, at the price of ceremony that slows decisions.

## People, knowledge, and attention

- **Decentralization**, also **delegation** or **subsidiarity**: decide where the information already is, at the price of inconsistency across groups.
- **Conway's law**, applied deliberately as the **inverse Conway maneuver**: draw the boundaries between people to match the boundaries you want in the thing, at the price of reorganizations being slow and painful.
- **Decision records**, formally the **architecture decision record**: write the decision and its reasons where the next person will look, at the price of records that mislead once stale.
- **Knowledge transfer**, with **bus factor** naming the risk: move what is in one head into a form others can act on, at the price of teaching time and decay.
- **Direct collaboration**, as **pair programming** and **workshops**: put the people who each hold part of the answer in contact, at the price of attention and leaving no record.
- **Modeling**, also **diagramming**: externalize the invisible into something inspectable before it is built, at the price of artifacts that drift from reality.
- **Cognitive load**: keep what a person must hold in mind at once small, at the price of more pieces to navigate.
- **Point-of-use information (in house)**, nearest phrases **in-context help** and **just-in-time information**: deliver the fact at the place and moment it can be acted on, at the price of clutter and badly timed interruption.
- **Intent-split content (in house)**, with **Diátaxis** naming the documentation instance: split the same content by what the reader is trying to do, at the price of the same fact maintained in several places.
- **Psychological safety**, practiced as **blameless culture**: remove the personal cost of reporting a problem, at the price of accountability blurring.
- **Ownership**, also **accountability** or **directly responsible individual**: name exactly one party answerable, at the price of a bottleneck and everyone else disengaging.
- **Sensible defaults**, and **choice architecture** for their deliberate use: make the option you want the one that happens when nobody decides, at the price of defaults becoming invisible policy.
- **Convention**, as in **convention over configuration** and **coding standards**: standardize one way of doing a recurring thing, at the price of fitting the average and blocking better local choices.
- **Ratcheting**, popularly **clean as you code** or the **boy scout rule**: apply the new rule to whatever you touch and let coverage grow, at the price of two standards coexisting for years.
- **Cross-training**, also **rotation**: circulate people so no knowledge sits with only one of them, at the price of short-term slowdown.
- **Ubiquitous language**, generally **domain modeling**: match the built thing's vocabulary to the problem's vocabulary, at the price of translation at every edge.
- **Human in the loop**: ask a person to decide where the machine is least trustworthy, at the price of that approval becoming a rubber stamp.
- **Traceability**: make each output point back at the reason it exists, at the price of link maintenance turning into paperwork.
- **Declarative** programming or configuration: say what you want and let a separate mechanism decide how, at the price of opacity when it does the wrong thing.
- **State machine**: represent progress as named states with only declared moves between them, at the price of states multiplying.
- **Polymorphism**, and **table-driven** or **data-driven design** outside object code: replace a decision remade every time with a structure that absorbs the variation, at the price of hidden control flow.
- **Code generation**, serving **don't repeat yourself**: derive the second artifact from the first so the two cannot drift, at the price of a generator that becomes a dependency.
- **Retrieval augmented generation** today, with **query expansion** for its older half: improve the question and put the relevant material in front of whoever must answer, at the price of the rewrite changing the intent.
- **Fuzzy matching**, also **similarity search** or **nearest neighbor**: compare by distance so inexact things can still be matched, at the price of a distance rule that hides assumptions.
- **Granularity**, with **grain** in data modeling and **chunk size** in retrieval: choose the size of a unit deliberately, since it decides both cost and meaning.
- **Progressive disclosure**: reveal a little at a time and let the viewer ask for more, at the price of hidden things going undiscovered.
- **Visibility of system status**, generally **feedback**: show the current state and the result of the last act without being asked, at the price of signals people learn to tune out.
- **Minimizing choices**, with **Hick's law** naming the constraint: reduce the number of options offered, at the price of the removed option being right for someone.
- **Constraint-first design (in house)**, with the **curb-cut effect** naming its payoff and **inclusive design** the surrounding practice: design for the most constrained user, since the constraint exposes what everyone else quietly struggles with.
- **Chargeback**, also **showback**: charge the cost to whoever chooses it, at the price of metering overhead and gaming.
- **Standard**, and **protocol** when it governs communication: fix a shared written definition in advance so strangers interoperate without negotiating, at the price of freezing early mistakes for decades.
- **Reverse engineering**, also **code archaeology**: rebuild intent from the artifact when no surviving description can be trusted, at the price of recovering only part of it.
