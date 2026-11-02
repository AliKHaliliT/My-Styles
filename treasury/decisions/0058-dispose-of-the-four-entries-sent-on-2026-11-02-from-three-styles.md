# 0058. Dispose of the four entries sent on 2026-11-02 from three styles

Status: Accepted
Date: 2026-11-02

## Context

One maintainer of projects built from three of the family's styles sent
four upstream entries as issues, the nineteenth to the twenty-second on
the repository, three dated 2026-11-02 and one 2026-10-26, pinned at the
family's d9176dc and edec8e4, which the family's history holds, all
filed as defects. Each was tested against the template's tree before
ruling, and each was real against the template's own law or its own
toolchain.

## Decision

- The asynchronous fixture loop scope left unset, from the server style.
  Kept, and widened to the package style, which carries the same
  configuration. A fresh install from the development requirements
  brings a plugin that warns at configuration while the scope is unset,
  and the suites turn warnings into errors; the scope is declared as
  function in both Python seats. Admitting the warning and pinning the
  plugin refused. The package seat's 0121 and the server seat's 0125.
- Lint dependencies retaining a vulnerable path matcher, from the client
  style. Kept. The lint stack moves to ESLint 10 with the plugins that
  declare it, the matcher is overridden to 11.0.1 or later while
  ESLint's own tree asks for the older major, and in-range dependencies
  take their patches, measured together with a clean audit, green lint,
  types, tests and build, and the quote rule still firing. A global
  override on ESLint 9 refused. The client seat's 0116.
- Push and pull-request events repeating one branch's checks, from the
  host. Kept, and widened to every workflow of the family, with fork
  coverage preserved. Every job runs on a pull request only when the
  request comes from a fork, by one condition on the job; dropping the
  pull-request event and a concurrency group refused. The package seat's
  0122, the server seat's 0126, the client seat's 0117 and the host
  seat's 0116.
- A fast-forward landing repeating the verified branch gate, from the
  host. Kept, and widened to every workflow of the family. A landing job
  carries the landed-branches step and asks the run history whether this
  workflow passed at this commit on a branch; every other job runs only
  without that evidence, and manual dispatch runs fresh. Skipping the
  run on main and trusting the fast-forward by its shape refused. The
  package seat's 0123, the server seat's 0127, the client seat's 0118
  and the host seat's 0117.

## Consequences

The projects delete the four entries at their next re-alignment and take
the templates' forms. The family has no dependency-audit step in any
gate; whether one joins every seat stays an open question for the owner,
raised and not decided here.
