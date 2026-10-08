# 0074. Watch the paths of the style each arrow's manifest names

Status: Accepted
Date: 2026-10-08

## Context

Record 0009 narrowed the stale-pin scan to the paths inside an arrow
that can change what a run produces and enumerated them as `src`,
`tests` and `pyproject.toml`, the demo arrow's, which are a package's.
The scan applied that one list to every arrow, and the manifest's
Style line, which the rulebook requires, was never read by the audit.
An arrow built from the server style keeps its run under `app`, `db`,
`main.py` and `requirements.txt`, and one built from the client style
under `src`, `index.html` and its package and build files, so a claim
pinned to either would have stayed silent while its arrow's code moved.
A project built from this style reported it on 2026-10-08, having added
a server-style arrow beside its package arrow and read the scan while
writing the new manifest; no claim pinned the server arrow yet.

## Evidence

Measured on 2026-10-08. The audit held one tuple of three paths for
every arrow and no function of it read a manifest's Style line. The
server seat's tracked tree keeps its code in `app`, `db`, `engines` and
`main.py`, its suites in `tests`, and its dependencies and warning
behavior in `requirements.txt` and `pyproject.toml`; the client seat's
keeps its code in `src` and `index.html`, its suites in `tests`, and
its dependencies and build in `package.json`, `package-lock.json`,
`vite.config.ts` and its three `tsconfig` files. The movement plants of
record 0009 run over the demo arrow's history, which is the package
row's.

## Options considered

- Letting each manifest declare the paths it watches, as the project
  proposed first. Refused, because the paths are a fact of the style
  and not of the arrow, and a list every manifest copies is a list that
  drifts; the style's name is already on the manifest.
- Watching every path in an arrow except its documentation. Refused,
  because an arrow's `scripts/` folder holds the docs audit the template
  recopies at every landing beside scripts that produce evidence, so the
  negative list would advise on every landing or miss a producer.
- Falling back to the package row for a style the scan does not know.
  Refused, because a scan watching the wrong paths is silent where it
  should speak, and a check that cannot watch an arrow says so.

## Decision

The scan keeps one row of paths per style, the package seat's, the
server seat's and the client seat's as measured above, and reads the
style from the arrow manifest's Style line. The audit fails a manifest
whose Style line is absent or names a style the scan has no row for,
and the scan watches nothing in such an arrow, since the gate is
already red. The rulebook says the Style line fixes the paths the scan
watches, and the law's sentences on movement name the code, the suites
and the project files of the style the manifest names. The selftest
plants a manifest naming an unknown style and one naming none; the
movement plants keep proving the package row over the demo arrow's
history, and the other rows are data a person reads against the seat's
tree.

## Consequences

A claim pinned to an arrow of any family style is advised when that
arrow's code, suites or project files move. A style the family gains
adds a row here with its record, and an arrow of no family style cannot
carry a claim quietly.
