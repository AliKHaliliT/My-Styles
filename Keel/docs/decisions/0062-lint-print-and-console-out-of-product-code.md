# 0062. Lint print and console out of product code

Status: Accepted
Date: 2026-09-16

## Context

Nothing in the family stopped a print statement or a console call from
reaching a tracked module. The baseline excluded debug output as files, the
scratch scripts and one-off harnesses that support a task, and said nothing
about debug output as lines, the print a worker adds while chasing a defect
and forgets. Treasury study 0005 found the countermeasure stated twice in
the published agent-skills ecosystem as a tag convention, prefix every
debug line with a unique token so one grep removes them all, and the family
disposition, treasury 0030, Take eight rules from the skills study and
refuse the rest, adopted the rule one rung higher, so the linter every seat
already runs refuses the statement itself and the tag is never needed.

## Evidence

The python linter's print rule was selected in no seat and the client
linter's console rule in none, checked on 2026-09-16 in every project file.
A dry run of the print rule found every finding but one family in the audit
and operational scripts, whose output is their purpose, and in the package
command module of the library seat, whose output is likewise its purpose.
The one family was a field-reordering utility in the server seat that
printed a trace behind a debug flag, nine lines of exactly the kind the
rule exists to catch. The client seat's one match for the word console was
prose in a page heading, not a call.

## Options considered

- The tag convention as the sources stated it. Refused under the ladder,
  because it depends on a worker remembering to tag, where the linter
  refuses the untagged and the tagged alike, and a grep for the tag becomes a
  check nobody needs.
- Refusing the rule in tests too. Refused for the client seat, whose suites
  are typed source under the same linter, and moot for the python seats,
  whose suites carry no print today; a test that prints has an assertion it
  is not making.
- Exempting the utility's debug trace as declared output. Refused, because
  a trace behind a flag is a diagnostic, and the server seat already routes
  diagnostics through the standard logger in its exception handlers; the
  utility now logs at debug level under the same flag.

## Decision

Every python seat selects the print rule, with the scripts exempt because a
script's output is its purpose and, in the library seat, the command module
exempt for the same reason, each exemption carrying its reason beside it in
the configuration. The client seat turns on the console rule for its typed
source and suites; its scripts lint under their own block and keep the
console. The server seat's field-reordering utility routes its debug trace
through the module logger. Every guide's Hard rules gain one bullet saying
that nothing prints from product code and where a diagnostic goes instead.
The rule lands as a check, the second rung, because no type can make a
print impossible and the linter decides the question on every run.

## Consequences

A worker who leaves a print behind fails the lint with the line named, and
answers it by deleting the line or by moving the diagnostic to the logger,
never by tagging it. The exemptions are three path patterns, each with its
reason, so a reader sees what was waived rather than a silent blanket. A
child re-aligning receives the rule with its configuration and the bullet
with its guide.
