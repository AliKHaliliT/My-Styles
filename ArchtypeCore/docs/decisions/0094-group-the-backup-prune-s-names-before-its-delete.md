# 0094. Group the backup prune's names before its delete

Status: Accepted
Date: 2026-10-08

## Context

`scripts/backup.sh` prunes old backups with one `find` whose expression
reads the age test and then
`-name "*.db" -or -name "*.conf" -exec rm -f {} \;`.
`find` binds its implicit and more tightly than `-or`, so the
expression is two branches, the old database backups on the left and
the configuration backups on the right, and `-exec` belongs to the
right branch alone. Old database backups were matched and never
removed, and configuration backups were removed whatever their age. A
project built from a host style with an arrow of this seat reported it
on 2026-10-07, having dropped the configuration backup and read the
line its `-exec` was left bound to.

## Evidence

Measured on 2026-10-08. ShellCheck 0.11.0 over the family's two shell
scripts, this seat's entrypoint and its backup script, names exactly
this line, as SC2146, and nothing else.

## Options considered

- A ShellCheck step in the family's workflow. Declined under the rule
  that an addition covers every seat, because the server seat alone
  carries a shell script; it reopens when a second seat gains one.
- Backing up the database alone, as the project did. Refused for the
  template, because the demo's network configuration is part of what
  its backup promises to keep.

## Decision

The prune groups its two names before the delete, as
`\( -name "*.db" -o -name "*.conf" \)`, so the age test and the
delete apply to both kinds of backup.

## Consequences

Old backups of both kinds are removed after the retention period and
young ones of both kinds are kept, which is what the script's log line
has claimed all along.
