# 0130. Approve the install script the lock installs

Status: Accepted
Date: 2026-11-23

## Context

The manifest approves install scripts under `allowScripts`, one of them
for esbuild at 0.28.1, while the lock installed 0.28.2. The lock moved
when the style's dependencies were brought to their current patches, and
the list did not move with it. On every install npm warned that esbuild
at 0.28.2 carried an install script the list did not cover, and named
its postinstall. A project built from the client style met it while
renaming its package, and sent the case as an entry. When npm wrote that
project's lock again, it also dropped four entries the style's lock
marked extraneous.

## Evidence

Installed on 2026-11-22 from the lock at afffa40 with npm 11.17.0 on
Windows, the warning named `esbuild@0.28.2 (postinstall: node
install.js)`, and the hosted run of the same commit printed it under the
npm that runner carries. npm writing the lock again removed the four
entries marked extraneous, for ajv, fast-uri, json-schema-traverse and
require-from-string, 51 lines, and changed nothing else. With the
approval at 0.28.2, a clean install printed no warning.

## Options considered

- Approving esbuild by its name alone. Refused, because an approval
  without a version approves whatever a later lock installs under that
  name, and the review the list exists to force would never happen again
  for it.
- Holding the other direction too, every installed package that carries
  a script approved. Left to npm's own warning, because which packages
  carry a script depends on the system that installs them, fsevents
  among them on macOS alone, and npm names each one it meets. It reopens
  when an install runs a script the list never decided without npm
  saying so.

## Decision

The manifest approves esbuild at 0.28.2, the version the lock installs,
and the lock is the one npm wrote again from the installed tree, without
the four extraneous entries. The docs audit now holds that every
approval belongs to a package the lock installs, at the version the lock
installs where the approval names one, and the ledger gains the claim.
Its selftest plants an approval for a package the lock installs at
another version and one for a package the lock never installs, and
requires a finding for each. The check was broken five ways, the entry's
own approval restored among them, and each break failed the selftest.

## Consequences

The next lock that moves an approved package past its approval fails the
audit by name, before an install runs its script unapproved. An install
prints no warning on the desk or on the hosted runner.
