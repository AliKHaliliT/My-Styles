# 0128. Leave the arrow's seams rule to its docs audit

Status: Accepted
Date: 2026-11-23

## Context

The host's workflow runs an arrow's gate in a job of its own, and that
job carried a step that grepped the arrow's suites for a patched module,
the step each artifact style carried in its own workflow. The artifact
styles now hold the rule in their docs audit, which the arrow's job runs
as its Docs step, so the step held nothing the job did not hold already.
A project built from the client style sent the case as an entry, from a
client kept inside a server, where the carried workflow runs nowhere.

## Options considered

- Keeping the step in the arrow's job beside the audit. Refused, because
  two holders of one claim drift apart.

## Decision

The step leaves the arrow's job, and the arrow's docs audit holds the
rule, as the arrow's own ledger now says. The host's audit is unchanged,
since it never reaches into an arrow.

## Consequences

An arrow's suites are held to the rule by the arrow's own gate wherever
that gate runs, inside the host or once the arrow is extracted.
