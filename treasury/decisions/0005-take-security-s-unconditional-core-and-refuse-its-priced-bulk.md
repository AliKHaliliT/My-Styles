# 0005. Take security's unconditional core and refuse its priced bulk

Status: Accepted
Date: 2026-08-23

## Context

Study 0003 catalogued the named vocabulary of software security, 13,764
entries folded to 1,996 in eight families. The question the family then faced
was the same one every study leaves behind, which of these findings become
law and which stay as vocabulary.

Security answers that question differently from the two studies before it,
and the reason is in the findings rather than in anyone's preference. Two
entries in five end by naming what they cost, and every one of those answers
a question the entry cannot ask. Whether certificate pinning earns its price
depends on who the attacker is, what they want, and what breaks when the pin
is wrong. A style template has no threat model, because the threat model
belongs to whatever is built from the template. So the priced bulk of this
vocabulary cannot become style law without the styles pretending to knowledge
they do not have, and study 0001's disposition already refused that shape of
mistake under another name.

The study also produced the boundary that makes the refusal precise. The
unpriced entries, the attacks and weaknesses and properties and models, cost
nothing to know. Some of them can be checked by a machine, and a machine
needs no threat model to see that a hash function is broken or that a string
is being executed.

## Decision

Two things enter the styles, and both are recorded in each style's own
decision records because they land bytes there.

The delivery gate gains **Adversary honesty** as its nineteenth item. A
change that creates or moves a trust boundary names who it is meant to
withstand, and deciding that nobody is attacking it is a decision to write
down rather than an assumption to leave implicit. The item is unconditional
because knowing the adversary is free, and it demands naming rather than
acting, which is what keeps it free.

The toolchains gain the mechanical subset. The two Python styles enable
ruff's security ruleset ported from bandit. The client style enables the core
rules against dynamic execution and javascript URLs together with the sonarjs
rules for hardcoded credentials, clear-text protocols, weak randomness, weak
ciphers and keys, weak hashing, insecure cookies, and intrusive permission
requests. Every rule adopted fires on a construct that is wrong whoever the
attacker is.

## What is refused, and what would reopen it

**Every priced entry in the vocabulary.** No cryptographic choice, no
authentication or authorization mechanism, no isolation architecture, no
network control, and no operational tooling becomes style law. Each is a
decision belonging to a project with a threat model. This reopens for any
single mechanism that stops being conditional, which in practice means one
whose absence is indefensible for every project a style could produce.

**Security demonstrations in the demo code.** The styles teach form rather
than stack, and their demos are deliberately incomplete in named ways. Adding
authentication hardening to the control-plane demo or a content policy to the
client demo would import a threat model the templates do not have and would
teach a stack decision as though it were a form decision. This reopens if a
style's demo ever grows a surface where the missing security is itself
misleading about the form.

**A rewrite of the secrets rule.** The study was checked against the existing
hard rule that no confidential fact enters a tracked byte, backed by the
untracked private ledger and by secret scanning in continuous integration.
The vocabulary adds names for what that rule already does and no mechanism it
lacks, so the rule stands unchanged. This reopens if a study finds a class of
leak the current rule does not cover.

**A coverage or scoring metric of any kind.** Study 0001 refused coverage
thresholds and velocity metrics, and the security vocabulary offers several
more of the same shape, from control counts to maturity levels to
vulnerability scoring as a management target. The earlier refusal governs
them and no new evidence reopened it.

## Consequences

The family now holds security the way it holds optimization, as a discipline
whose unconditional core is law and whose conditional bulk is vocabulary a
project weighs against its own situation. The gate is nineteen items and
remains byte-identical across the three styles.

The children are not touched by this ruling. They receive it the way they
receive every ruling, by being refactored against the latest form of their
style, and until that happens their gate is eighteen items and their
toolchains lack these rules. Nothing in a child is edited to close the gap.

The vocabulary itself is the larger part of what the study produced, and
refusing to legislate it is not the same as ignoring it. It sits in the
treasury for the reason the treasury exists, so that a project reaching a
security decision starts from the field's own names instead of from whatever
its author happened to remember.
