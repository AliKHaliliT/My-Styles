# 0098. Keep an entry's date with its title when it leaves the file

Status: Accepted
Date: 2026-10-09

## Context

An upstream entry carries its date in one place, the heading of the
form `### YYYY-MM-DD` followed by the title, with the kind and the pin
as lines beneath it. The guide describes the entry as it lives in a
project's upstream file and names no other channel, so when a
maintainer sent five entries as issues on the template's repository
on 2026-10-08, the heading became each issue's title and the date went
with it, while the kind and pin lines survived as body lines. The
channel's own stamp gave a date, but it is the day an entry was sent
and not the day it was written against its pin, and the two can lag.

## Evidence

Measured on 2026-10-09. Each of the five issues carried the kind, the
pin and the four parts the guide asks for, and none carried a date;
the records that disposed of them cite the channel's stamp. The entry
rule in the shared block of the four guides says where the date lives
and nothing about an entry that leaves the file.

## Options considered

- A check over issues. Refused, because the audit reads the tree and
  the tree does not hold an issue; a channel the law does not read is
  held by the sentence that describes it.
- A `Date:` line beside `Kind:` and `Pin:` in every entry. Refused,
  because the heading already carries the date in the file, and a
  second copy of one fact is a copy that drifts.

## Decision

An entry sent outside the file, as an issue on the template's
repository or in a message, keeps its heading whole as its first
line, the date and the title together, because the date is the day
the entry was written against its pin and the channel's own stamp is
the day it was sent. The entry rule in the shared upstream block of
the four guides says so, and the demo arrow carries the package
seat's guide.

## Consequences

An entry keeps its own date wherever it travels, and a record that
disposes of it cites the day it was written rather than the day it
arrived.
