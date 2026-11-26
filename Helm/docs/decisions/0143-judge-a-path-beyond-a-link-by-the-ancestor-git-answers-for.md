# 0143. Judge a path beyond a link by the ancestor git answers for

Status: Accepted
Date: 2026-11-26

## Context

A living document may name a path the ignore file covers, and the audit
reads such a path as prose, whatever the machine holds. To know, it asks
git whether the path is ignored, and git refuses to judge a path that
passes through a symbolic link, answering with an error where a verdict
was asked. The audit read every answer but ignored as not ignored, so a
generated file named in a document and kept behind an ignored link read
as a path the tree must hold, and the audit failed or passed with what
lay behind the link, though neither the index nor the ignore file had
changed. A project built from the package style met it at a documented
output behind such a link, and this style's audit asks git the same way.
The host style's audit was given the rule for this case earlier, for its
recorded artifacts, and this audit was not.

## Evidence

Run on 2026-11-26 with git 2.53.0 on Linux, in a repository of the
probe's own. With an ignore entry naming a link, git answered 0 for the
link and 128 for a path beneath it, saying the path is beyond a symbolic
link, whether or not the path existed behind the link, and with no link
there it answered 0 for the same path. With a directory pattern, a name
closed by a slash, it answered 1 for the link itself, since git reads a
link as a file.

## Options considered

- Following the link to see what it holds. Refused, because what a link
  points at on one machine says nothing about the tree, and the audit
  judges the tree.
- Running the generator before the audit, as the reporting project did.
  Refused, because a verdict that waits on a local artifact is the
  dependence the rule on ignored paths exists to remove.

## Decision

A path git refuses to judge is judged by the nearest ancestor git
answers for, because the ignore rule that covers a link covers
everything reached through it, and the link is never followed. The
selftest makes a link to a folder of its own, names a path beneath it in
a living document, and expects the path reported while the ignore file
leaves the link out and passed once it covers it, and it says so where
the machine cannot make a link. On Linux, three breaks, each one point,
each failed the proof.

## Consequences

A path behind an ignored link reads the same whatever the link leads to.
An ignore entry written as a directory pattern does not cover a link, so
a project that keeps storage behind one names the link itself.
