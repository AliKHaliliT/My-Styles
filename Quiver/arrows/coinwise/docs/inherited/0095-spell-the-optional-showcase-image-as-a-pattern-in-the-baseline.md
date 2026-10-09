# 0095. Spell the optional showcase image as a pattern in the baseline

Status: Accepted
Date: 2026-10-09

## Context

The baseline's README composition permits a showcase image after the
badges and, in that optional clause, named its home as the literal
path `util_resources/readme/`. The docs audit judges every backticked
token that reads as a path whose first segment exists at the root, so
a project that keeps another tracked asset under `util_resources/` and
embeds no image failed on a folder the clause had called optional. A
maintainer of projects built from three of the family's styles
reported it on 2026-10-08 as an issue, having replaced the literal
with the path pattern and seen the finding go.

## Evidence

Measured on 2026-10-09. The audit's path test takes a backticked token
with a slash and no space, no angle bracket, star, brace or quote, and
a first segment the root holds, and fails it when the path does not
exist and git does not ignore it. The template's own tree holds no
`util_resources/`, so the token was never judged here, and on the
machine this template is kept on, git's ignore matching answered for
the absent folder, which masked the case in a worktree carrying another
asset. The pattern form carries an angle bracket and is read as prose.

## Options considered

- Creating the image folder in every tree. Refused, because a folder
  no file lives in is not a folder git can carry, and the clause is
  optional by design.
- Teaching the path check to skip paths an optional clause names.
  Refused, because no check can tell an optional clause from a claim,
  and the pattern form says in one token that the path is a shape.

## Decision

The baseline's optional clause names the image's home as the pattern
`util_resources/readme/<image>`, which the path check reads as prose.
The rule it states is unchanged. An embedded image lives in the image
folder under the resources folder, and nothing references one from
anywhere else.

## Consequences

A project with other tracked assets and no showcase image passes the
audit on the baseline it carries, and the day it embeds an image the
folder exists because the image does.
