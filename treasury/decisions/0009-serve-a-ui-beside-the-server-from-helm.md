# 0009. Serve a UI beside the server from Helm

Status: Accepted
Date: 2026-09-01

## Context

Before the styles existed, the owner's habit for a minimal dashboard beside
an ArchetypeCore server was a hand-written HTML, CSS, and JavaScript page
dropped into the server's static folder, one deploy and no integration. The
server template still carried the slots of that era in its form map, a
`static/` folder for assets and a `templates/` folder for Jinja2 rendering,
while the family had since built Helm, a full client style with its own law.
Two answers to one need sat side by side, and only one of them had a
rulebook.

## Decision

A user interface beside an ArchetypeCore server is a Helm instance. Helm
builds to static files, and the server serves them itself when one deploy
unit is wanted. The build output lands in `app/static/`, the server mounts
it under a prefix such as `/dashboard` with single-page fallback so client
routing survives a direct URL, and the API keeps `/api/v1`. Helm runs in
live mode against a relative API base, so the same build works co-hosted on
one origin, with no CORS and plain cookies, or standalone on any static
host. A multi-stage container image builds Helm in one stage and copies its
output into the server image in the next, which restores the one-push
convenience of the old habit.

The jurisdictions stay split. Helm's source lives under Helm's law in its
own tree, and the server consumes the built artifact only, never importing
or editing that source, on the same principle the research host applies to
its arrows. The `templates/` slot leaves the server's form, since
server-rendered pages would be a second frontend form with no rulebook, and
`static/` is re-annotated as the co-hosted dashboard's home. A hand-written
static page for a trivial status board remains legal content in that
folder, a file rather than a style.

## Options considered

- Keeping Jinja2 templates as the lightweight path was refused. The family
  would then carry two frontend forms, and the one without a rulebook is the
  one that drifts.
- Placing Helm's source inside the server tree was refused, because it would
  put one tree under two laws and let the server import what it should only
  serve.

## Consequences

A builder who wants a dashboard beside the server has one answer and knows
where the artifact lands. The server's map stops promising a rendering layer
it never carried. The choice between co-hosted and standalone becomes a
deployment decision made per project, with the build unchanged either way.
