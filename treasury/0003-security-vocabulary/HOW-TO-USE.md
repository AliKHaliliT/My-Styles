# How to use the security vocabulary

Living guidance for reading the findings beside this file, rewritten in place
as the practice sharpens. It is not part of the record.

## What the vocabulary is and is not

It is the field's named concepts, folded so a person can hold them. Nothing
here obliges a project to do anything. The point is that a decision made without
knowing a name was still a decision, and after reading the relevant family it
becomes a decision someone made on purpose.

Treat every entry as an option to weigh. An omission then becomes a choice
instead of an accident, which is the whole reason the treasury exists.

## Start with the threat model, not with the list

Security's vocabulary cannot be applied the way a style rule can, because
almost every entry answers a question the entry itself cannot ask. Whether
certificate pinning is worth its cost depends on who the attacker is, what
they want, and what breaks if the pin is wrong. Read the first family before
any other and settle the adversary, the assets, and the trust boundaries.
Without that, the priced entries all look equally attractive and the vocabulary
turns into shopping.

The threat model does here what a profiler does for optimization work. It is
the instrument that says which of these decisions is yours to make today.

## The families, and the order to move through them

1. **What security is and who you are up against.** Properties, the
   design-principle canon, adversary models, threat-modeling methods, risk and
   assurance. Read this one first and read it whole. It is short, almost
   nothing in it costs anything, and everything after it is defined in its
   terms.
2. **How code is broken.** Memory corruption and untrusted input, with the
   mitigations answering each attack. Read when writing code in a language
   that can suffer these, or when reviewing any parser or any boundary that
   accepts input.
3. **Application surfaces.** The browser model, HTTP APIs, mobile apps, and
   model and agent applications. Read the surface you are actually building
   on and skip the rest until you build on it.
4. **Cryptography, from primitives to deployment.** Read before choosing
   anything cryptographic, and note that the misuse material at the end of the
   family is where most projects actually fail. The primitives are largely
   settled and the deployments are where the decisions live.
5. **Identity and authority.** Authentication, federation, access-control
   models, policy, and privilege. The most heavily priced family, because
   almost every entry is a mechanism somebody switches on.
6. **Boundaries and what crosses them.** Isolation, platform and boot
   integrity, the network boundary, and the channels that defeat all three.
   Read when deciding where a wall goes, and read the channel groups before
   assuming a wall holds.
7. **Operations and delivery.** What an adversary does, what a defender sees,
   how an incident is handled, and how software is built and shipped without
   becoming the attack. Mostly unpriced, because an adversary technique is not
   something you install.
8. **Failing safely.** How a system behaves when it breaks. Small, heavily
   priced, and the family most often skipped by people who think they are
   reading a security document.

## Reading a single entry

The names come first and the first one is the name the field uses most. The
bold names after it are the other terms that reach the same entry, whether a
synonym, a competing coinage, or a member folded in. That is what makes the
vocabulary answer to a term someone just heard in a meeting.

A gloss that ends by naming a cost belongs to something a person applies, and
the cost is the honest part of the entry. A gloss that ends at the definition
belongs to something nobody applies, an attack or a property or a failure mode,
and knowing it costs nothing. When scanning for work to do, read only the
priced entries, and read the unpriced ones to understand a report someone
sent you.

## The traps worth naming

- **Do not adopt by family.** No project needs every mechanism in any family
  here, and a project that tries will spend its whole budget on the family it
  happened to read first.
- **Do not read a price as a verdict.** A cost is what the mechanism takes, not
  an argument against it. The argument is the threat model.
- **Do not mistake coverage for security.** The vocabulary is wide because the
  field is wide, and breadth of reading is not depth of protection.
- **Do not treat the newest material as settled.** The model and agent entries
  name vocabulary the field is still fixing, and several carry a competing
  coinage as an alias precisely because nobody has won yet.

## What is deliberately absent

Safety engineering, except fail-safe states and fault containment. The
certification universe governing safety-critical software. Physical security,
though software-observable channels are here. Products, tools, and vendors,
though a named algorithm, format, protocol, or model is here wherever the field
treats the name as a concept.

If a question falls in one of those, this study does not answer it and was not
trying to.
