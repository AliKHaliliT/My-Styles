# 0123. Read an edition's destination as the system reads it

Status: Accepted
Date: 2026-11-17

## Context

The editions document has a cut written into a folder outside the
repository that holds nothing yet, and has the tool refuse a destination
under which a path would run past what the system is sure to write. Each
tool read the destination two ways and got one of them wrong. The client
seat's tool judged a destination by its spelling, while git names the
repository's root as the filesystem holds it, so a destination reached
through a link, or named by the short form of a folder's name, lay
inside the repository and was taken for outside. The one text the Python
seats carry judged a destination where the filesystem holds it and
measured it there too, though the system counts the spelling it is
handed, so a destination spelled longer than the folder it leads to
passed the measure and stopped partway. A project built from the client
seat met the first on a system whose temporary folder is reached through
a link, where the tool's own selftest failed at its refusal of a
destination inside the repository.

## Evidence

Run on 2026-11-17 at cf7a9c4, the commit the project's entry pins. The
entry's own system was not at hand, so its condition was made on Linux.
With the temporary folder reached through a symbolic link there, the
client seat's selftest failed one proof, that a destination inside the
repository was accepted, which is the failure the entry reports. On
Windows it failed the same proof with the folder reached through a
junction, and again with the folder named by its short form and no link
anywhere. A snapshot cut through a junction that leads into the
repository wrote all 235 files inside it. The Python text refused that
destination and passed its selftest under every one of those temporary
folders, yet a break of its judgment, the destination compared as
spelled, survived the selftest on a plain temporary folder, so nothing
proved what the text did right. Cut through a junction named 92
characters longer than the folder it leads to, the Python text accepted
a destination of 209 characters, stopped while it wrote and left 21 of
212 files, where the client seat's tool refused the same destination
before it wrote, naming a path of 317 characters. Through a short
junction to a folder with a long name, the Python text refused a
destination of 118 characters that the client seat's tool wrote whole.

## Options considered

- Compare the two folders by the identity the system gives each, in
  place of their names. Refused, because no gate here runs on a system
  where the names the filesystem returns disagree for one folder, so the
  comparison could not be watched failing. It reopens on an entry that
  shows one folder under two such names, a second mount of it or a
  spelling in another case on a volume that ignores case outside
  Windows.
- Write the cut under the folder as the filesystem holds it, so that one
  reading serves the judgment, the measure and the write. Refused,
  because a link is how an owner shortens a destination the system would
  not otherwise write, and the tool would then refuse a spelling the
  system accepts.
- Fail the selftest where the system makes no link. Refused, because a
  proof that cannot run on a system its tool serves is the defect this
  record answers, and the proof names itself as not run there.

## Decision

A destination is read as the system reads it. It is judged where the
filesystem holds it and measured as it is written. The client seat's
tool compares the destination's closest folder that exists, every link
on the way to it followed and the part not made yet under it, with the
repository's root read the same way. For a folder it takes the system's
own answer first, since that answer alone undoes a short name, reads
each link in turn where the system gives none, and leaves the path as
written where nothing can be read. The Python text measures a
destination by the spelling it writes under. Each tool keeps what it had
right, the client seat's measure and the Python text's judgment, and the
editions document stands as written, since it asked for both.

Each selftest proves both readings on a link of its own making, a
symbolic link, or a junction on Windows, where a symbolic link takes a
privilege. A destination behind a link into the repository is refused
with nothing written, and its length is counted as spelled. Where the
system makes no link the selftest says the proof did not run. Each proof
was watched failing before it was trusted. The proof of each reading
failed on the tool that had it wrong at the pin, and thirty-three breaks
of the client seat's tool and twenty-nine of the Python text, the
earlier ones among them, each failed a proof. Both selftests hold on
Linux and on Windows under a plain temporary folder and under one
reached through a link, and on Windows under one named by its short
form. The check withstands a destination given by mistake. A folder
replaced by a link between the check and the write is outside it, as the
entry says of its own correction.

## Consequences

A project whose temporary folder is reached through a link, or named by
a short form, passes the tool's selftest, and no other name for a folder
inside the repository takes an edition into it. A cut through a link is
refused when its spelling runs too long, however short the folder behind
it, and an owner who shortens a long destination with a link is let
through.
