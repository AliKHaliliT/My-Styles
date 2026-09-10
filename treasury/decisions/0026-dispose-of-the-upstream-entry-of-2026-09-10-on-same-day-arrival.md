# 0026. Dispose of the upstream entry of 2026-09-10 on same-day arrival

Status: Accepted
Date: 2026-09-10

## Context

An inquiry project aligned at `a98750217031` sent one defect entry in its
upstream file: the filename cap judged two claims committed hours before the
commit that brought the cap, because both moments were read as dates without
time and compared with a greater-or-equal, and the selftest then refused to
plant over the red tree and reported three rules not working. The maintainer
reproduced both in a scratch history, a long-named record committed on the
morning of the arrival day with the arrival replayed on top.

## Decision

Kept. Every history-reading check in every audit now compares commits by
ancestry: exempt when the record's commit is a proper ancestor of the rule's
arrival, judged when it is that commit or later. The queue-age check follows
the same rule. The selftest checks the tree first and stops with the audit's
own findings when it is red. Each style carries its own record.

## Consequences

A rule never reaches behind its own commit. The reporting project's renamed
claims stand as renamed; nothing else of its is asked to change.
