# 0063. Cut a public edition of a project by tier and by version

Status: Accepted
Date: 2026-11-10

## Context

The owner asked for a way to publish a project built from a style
without the style and what it records. The baseline already has every
tracked byte written for a public audience, so the whole repository can
go public as it stands, and nothing served the owner who wants the
product public and the workshop kept back. The shape was settled in
discussion. Tiers measure how much leaves, the repository in its
entirety is the baseline and has one version, a recommended tier reads
as if made by hand, the lowest holds code with no comment and no
docstring, and below the baseline a tier comes in two versions, one
saying it is a style's output and one saying nothing. Measured on
2026-11-09 over the four seats, the style and its trail are 140 to 180
of each seat's 210 to 360 tracked files and separate by path, and what
remains names the style in about twenty lines a seat.

Under treasury 0060 this is shared law, a document every seat mirrors
and a tool every seat carries, and every seat can carry it. The package
seat, the server seat, the host and the arrow carry one Python text, and
the client seat carries the same tool in its own stack.

## Decision

A project is published at one of four tiers, the whole repository, a
snapshot of it with its history cut, a hand-made tier that holds the
product as written and nothing of the workshop, and a bare tier with
comments and docstrings stripped. The hand-made and the bare tier are
each cut in an attributed version and a silent one. An edition tool in
every seat cuts a tier from the last commit into an empty folder outside
the repository, proves each strip against its source, refuses a silent
cut that still names the style, and never commits, pushes or deletes.
The edition of an inquiry is its arrows, each cut by its own tool.
Recorded in the package seat's 0126, mirrored into the arrow's inherited
folder, the server seat's 0131, the client seat's 0122 and the host
seat's 0122.

Two things changed beside the seats. The family audit holds the editions
document identical in every seat and the Python tool identical in the
three seats that carry it, with the arrow's copies carried from the
package seat's. The root workflow runs each tool's selftest, and its
tooling job exempts the host's copy of the tool from the one rule that
reads its suppressions as unused, since the artifact seats lint that
same text under their own configuration, whose security rules those
suppressions answer.

## What is refused, and what would reopen it

- Shedding the workshop by degrees. Refused, because records, rules and
  history cite one another and leave together, the snapshot being the
  one step that drops history alone. It reopens if a part of the
  workshop comes to stand without citing the rest.
- A lean tier between the hand-made and the bare. Refused by the owner,
  since it differs from the hand-made tier by a shorter README and a
  missing workflow. It reopens when a project needs code as tested with
  nothing to read.
- A tool that rewords a docstring or a document to make an edition
  silent. Refused, because those are what a product says of itself. It
  reopens only if the style's own carried bytes come to name it in a
  place the tool may not drop, which a silent cut would then refuse in
  every project.
- Strips for shell, YAML, a Dockerfile, a stylesheet and markup.
  Refused, because no parser at hand proves them, and such a kind is
  carried as written and named. It reopens for a kind when a parser the
  project already installs can prove its strip.
- One tool at the family's root that cuts any seat from outside.
  Refused, because a project built from a seat leaves this repository
  and must carry what cuts it.

## Consequences

An owner publishes a product and keeps the method, and a published
figure keeps its trace, since the owner tags the workshop commit an
edition was cut from. Every seat's gate now proves an edition tool, and
the family audit holds two more blocks and three more carried copies.
