# 0135. Hold every line of the state file to its schema

Status: Accepted
Date: 2026-11-24

## Context

The schema gives `STATE.md` exactly four sections and makes every entry
in them one line that ends with its last-verified date. A project built
from the host style kept thirteen paragraphs of finished work, with 29
links, above its `Now` section, and its audit passed, because no seat's
audit read a line outside the entries. The host's audit held the four
headings by their presence alone, and it told a section's empty line by
a word inside it, so an entry naming Nothing escaped the cap and the
date check alike. The other seats' audits passed an entry with no date,
since they read a date only where one stood. The host's selftest planted
none of its rules for the file, and the host's rulebook carried a
shorter form of the schema's bullets, without the sentence that a
narration of a landing never replaces a finished entry.

## Evidence

Run on 2026-11-24 at 777ea6f. Planted files were read by the host's
check and by the package seat's copy of the Python check the artifact
seats share, and the client seat's check reads the same way in its code.

- A paragraph above the sections and a paragraph inside one passed both
  checks.
- A fifth section passed the host's check and failed the shared one.
- An entry with no date passed the shared check and failed the host's,
  except where it named Nothing, which passed the host's as well.
- Six entries in `Now`, one of them naming Nothing, passed the host's
  check.
- The age check strips a date only where it closes the line. In a
  throwaway history an entry re-dated once was aged 327 days with its
  date closing the line and 4 days with a period after it.
- The family's adoption rehearsal and the host's queue-age plant each
  wrote an entry with a period after its date.

## Options considered

- Refusing only a paragraph above the sections. Refused, because a
  paragraph inside a section reads the same to no check.
- Telling a section's empty line by its opening word. Refused, because
  that test let an entry naming Nothing escape the cap and its date.
- Letting a period or more words follow an entry's date. Refused,
  because the age check finds an entry's text by stripping the date that
  closes it, so re-dating such an entry restarts its age.
- Capping an entry's length, so that one line cannot carry several
  tasks. Refused, as a length rule was refused before, because it cuts
  filler and never information. An entry that carries several tasks is
  review's to split.

## Decision

The schema now says the file holds its title and its four sections in
order and nothing else, and that every line in a section is an entry
closed by its date or the section's empty line standing alone, and its
table names each section's empty line. The check reads every line of the
file in every seat. A line above the sections beside the title fails.
Inside a section, a line that is not an entry, an entry whose date does
not close it, an empty line beside other lines and a section with no
line at all each fail, and the sections must be the four in order in the
host as in the other seats. The horizon reads the closing date, and
`Now` counts every line it holds. The host's rulebook carries the other
seats' bullets for the schema beside its own two.

Each point has a plant. The Python audits read sixteen files cut from a
legal one directly, three of them legal, at the cap's edge, at the
horizons' edges and with an older date inside an entry, and they keep,
or in the host gain, the three plants made through a whole run. The
client seat's proof runs three files cut the same way, each plant
raising a finding no other plant in its run can raise. The check was
then broken one point at a time, 31 breaks in each Python audit and 31
in the client seat, and every break failed a plant but one. The client
seat plants its horizons away from their edges, since its proof and its
audit read two clocks, so an entry on the last day of its horizon is
held there by review.

## Consequences

A state file holds nothing a rule does not read, so finished work cannot
collect above the sections or between the entries. A project re-aligning
to this commit finds every line outside the schema in red, and its first
task is the sweep the schema already asked for. An entry that carries
several tasks on one line still passes, and splitting it stays with
review.
