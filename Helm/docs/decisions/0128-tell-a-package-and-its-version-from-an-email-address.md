# 0128. Tell a package and its version from an email address

Status: Accepted
Date: 2026-11-23

## Context

The docs audit refuses an upstream entry that carries an address,
because an entry is written to leave the repository, and an email is one
of the leaks a tool can decide. Its pattern took any name, an at sign
and a dotted run of letters or digits for an email. A package written
with its version in npm's own form, the name joined to dotted numbers by
an at sign, fits that pattern. A project built from the client style met
it while writing an entry that quoted the style's manifest, and named
the package and its version in words to pass.

## Evidence

Tested on 2026-11-22 at afffa40, the commit the entry pins. The pattern
refused `esbuild@0.28.1` and `msw@2.15.0`, the two approvals the client
style's manifest carries. It refused `@tanstack/react-query@5.105.3` as
the email `react-query@5.105.3`, and the prerelease `react@19.0.0-rc.1`
too. The same entry passed with `esbuild at 0.28.1` written in words.
With the host held to end in a label of letters, each of the four
passed, and `someone@example.invalid` and `someone@163.invalid` were
refused as before.

## Options considered

- Holding the host to the list of top-level domains that exist. Refused,
  because the list grows, and the family would keep a copy that goes
  stale.
- Leaving whatever stands in backticks unread. Refused, because an
  address in backticks leaves the repository as surely as one in prose.

## Decision

An email's host ends in a label of letters, as every top-level domain
does, in the pattern each audit carries. Each audit's selftest plants an
entry that quotes two packages with their versions and requires it to
pass, and plants an email at a host whose first label is digits and
requires its refusal, beside the email it planted already. The pattern
was then broken four ways, the old form among them, and every break
failed a plant in each audit.

## Consequences

An entry quotes a line of a manifest as it is written. A version whose
last dotted label is letters, as `1.0.0-rc.next` has, still reads as an
email, and an entry names that one in words.
